# -*- coding: utf-8 -*-
# Version: 2.5
# See github page to report issues or to contribute:
# https://github.com/hssm/anki-addons

from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.webview import WebContent

from .config import getConfig, getKeyForContext
from .gui import ffFix

addon_package = mw.addonManager.addonFromModule(__name__)


def myOnBridgeCmd(handled, cmd, editor):
    """
    Called from JavaScript to inject some values before it needs
    them.
    """
    if not isinstance(editor, Editor):
        return handled
    if cmd != "mceTrigger":
        return handled
    count = getConfig(editor, getKeyForContext(editor), defaultValue=1)
    editor.web.eval(f"setColumnCount({count});")
    editor.ccSpin.blockSignals(True)
    editor.ccSpin.setValue(count)
    editor.ccSpin.blockSignals(False)
    for fld, val in editor.note.items():
        key = getKeyForContext(editor, field=fld)
        if getConfig(editor, key, False):
            editor.web.eval(f"setSingleLine('{fld}');")
    if ffFix:
        editor.web.eval("setFFFix(true)")
    editor.web.eval("makeColumns2()")
    return (True, None)


gui_hooks.webview_did_receive_js_message.append(myOnBridgeCmd)


mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")


def on_webview_will_set_content(web_content: WebContent, context):
    if not isinstance(context, Editor):
        return
    web_content.js.append(f"/_addons/{addon_package}/web/editor.js")
    web_content.js.append(f"/_addons/{addon_package}/web/editor.css")
    web_content.body += "<script>$('#fields').bind('DOMNodeInserted', makeColumns);</script>"


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
