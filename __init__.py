# -*- coding: utf-8 -*-
# Version: 2.5
# See github page to report issues or to contribute:
# https://github.com/hssm/anki-addons

from anki.hooks import wrap
from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.webview import WebContent
from . import gui
from .config import getConfig, getKeyForContext, switch

addon_package = mw.addonManager.addonFromModule(__name__)


def myLoadNote(editor, focuseTo=None) -> None:
    count = getConfig(editor, getKeyForContext(editor), defaultValue=1)
    editor.web.eval(f"setColumnCount({count});")
    editor.ccSpin.blockSignals(True)
    editor.ccSpin.setValue(count)
    editor.ccSpin.blockSignals(False)
    editor.web.eval(f"resetSingleLine();")
    for fld_name, val in editor.note.items():
        key = getKeyForContext(editor, field=fld_name)
        if getConfig(editor, key, False):
            editor.web.eval(f"setSingleLine('{fld_name}');")


Editor.loadNote = wrap(Editor.loadNote, myLoadNote, "before")


mw.addonManager.setWebExports(__name__, r".*(css|js)")


def on_webview_will_set_content(web_content: WebContent, context):
    if not isinstance(context, Editor):
        return
    web_content.js.append(f"/_addons/{addon_package}/editor.js")
    web_content.css.append(f"/_addons/{addon_package}/editor.css")


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)

def onBridge(handled, message, editor):
    """Extends the js<->py bridge with our pycmd handler"""
    if not isinstance(editor, Editor):
        return handled
    if not message.startswith("MCEW"):
        return handled
    if not editor.note:
        return handled
    fld = message[len("MCEW:"):]
    switch(editor, fld)
    editor.loadNoteKeepingFocus()
    return (True, None)
gui_hooks.webview_did_receive_js_message.append(onBridge)
