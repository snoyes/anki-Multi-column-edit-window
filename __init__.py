# -*- coding: utf-8 -*-
# Version: 2.5
# See github page to report issues or to contribute:
# https://github.com/hssm/anki-addons

from anki.hooks import wrap
from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.webview import WebContent
from . import gui
from .config import getConfig, getKeyForContext, shortcut

addon_package = mw.addonManager.addonFromModule(__name__)


def myLoadNote(editor, focuseTo=None) -> None:
    model = editor.note.model()
    count = model.get("nb column")
    need_saving = False
    if count is None:
        # configuration may be saved in configuration file. Eventually delete this part of the code
        count = getConfig(editor, getKeyForContext(editor), defaultValue=1)
        model["nb column"] = count
        need_saving = True
    editor.web.eval(f"setColumnCount({count});")
    editor.ccSpin.blockSignals(True)
    editor.ccSpin.setValue(count)
    editor.ccSpin.blockSignals(False)
    editor.web.eval(f"resetSingleLine();")
    editor.web.eval(f"""var shortcut_full_line = "{shortcut()}";""")

    for field in model["flds"]:
        single_line = field.get("single line")
        fld_name = field["name"]
        if single_line is None:
            # configuration may be saved in configuration file. Eventually delete this part of the code
            key = getKeyForContext(editor, field=fld_name)
            single_line = getConfig(editor, key, False)
            field["single line"] = single_line
            need_saving = True
        if single_line:
            editor.web.eval(f"setSingleLine('{fld_name}');")
    if need_saving:
        editor.mw.col.models.save(model, updateReqs=False)

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
    fld_ord = int(message[len("MCEW:"):])
    model = editor.note.model()
    field = model["flds"][fld_ord]
    field["single line"] = not (field.get("single line", False))
    editor.mw.col.models.save(model, updateReqs=False)
    editor.loadNoteKeepingFocus()
    return (True, None)
gui_hooks.webview_did_receive_js_message.append(onBridge)


def onSetupShortcuts(cuts, editor):
    def onMultipleLine():
        editor.web.eval(f"onMultipleLine({editor.currentField})")
    pair = (shortcut(), onMultipleLine)
    cuts.append(pair)
gui_hooks.editor_did_init_shortcuts.append(onSetupShortcuts)
