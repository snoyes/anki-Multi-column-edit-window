# -*- coding: utf-8 -*-
# Version: 2.5
# See github page to report issues or to contribute:
# https://github.com/hssm/anki-addons

from anki.hooks import wrap
from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.webview import WebContent

from .config import getConfig, getKeyForContext
from .gui import ffFix

addon_package = mw.addonManager.addonFromModule(__name__)


def myLoadNote(editor, focuseTo=None) -> None:
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

Editor.loadNote = wrap(Editor.loadNote, myLoadNote, "before")


mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")


def on_webview_will_set_content(web_content: WebContent, context):
    if not isinstance(context, Editor):
        return
    web_content.js.append(f"/_addons/{addon_package}/web/editor.js")
    web_content.css.append(f"/_addons/{addon_package}/web/editor.css")


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
