# -*- coding: utf-8 -*-
# Version: 2.5
# See github page to report issues or to contribute:
# https://github.com/hssm/anki-addons

from anki.hooks import wrap
from aqt import (QAction, QCursor, QHBoxLayout, QLabel, QMenu, QPushButton,
                 QSpinBox, gui_hooks, mw)
from aqt.editor import Editor
from aqt.webview import WebContent

from .config import getConfig, getKeyForContext, setConfig

addon_package = mw.addonManager.addonFromModule(__name__)


# Flag to enable hack to make Frozen Fields look normal
ffFix = False


def onColumnCountChanged(self, count):
    "Save column count to settings and re-draw with new count."
    setConfig(self, getKeyForContext(self), count)


def myEditorInit(self, mw, widget, parentWindow, addMode=False):
    self.ccSpin = QSpinBox(self.widget)
    b = QPushButton(u"▾")
    b.clicked.connect(lambda: onConfigClick(self))
    b.setFixedHeight(self.tags.height())
    b.setFixedWidth(25)
    b.setAutoDefault(False)
    hbox = QHBoxLayout()
    hbox.setSpacing(0)
    label = QLabel("Columns:", self.widget)
    hbox.addWidget(label)
    hbox.addWidget(self.ccSpin)
    hbox.addWidget(b)

    self.ccSpin.setMinimum(1)
    self.ccSpin.setMaximum(getConfig(self, "MAX_COLUMNS"))
    self.ccSpin.valueChanged.connect(
        lambda value: onColumnCountChanged(self, value))

    # We will place the column count editor next to the tags widget.
    pLayout = self.tags.parentWidget().layout()
    # Get the indices of the tags widget
    (rIdx, cIdx, r, c) = pLayout.getItemPosition(pLayout.indexOf(self.tags))
    # Place ours on the same row, to its right.
    pLayout.addLayout(hbox, rIdx, cIdx+1)

    # If the user has the Frozen Fields add-on installed, tweak the
    # layout a bit to make it look right.
    global ffFix
    try:
        __import__("Frozen Fields")
        ffFix = True
    except:
        pass


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


def onConfigClick(self):
    m = QMenu(self.mw)

    def addCheckableAction(menu, key, text):
        a = menu.addAction(text)
        a.setCheckable(True)
        a.setChecked(getConfig(self, key, False))
        a.toggled.connect(lambda b, k=key: onCheck(self, k))

    # Descriptive title thing
    a = QAction(u"―Single Row―", m)
    a.setEnabled(False)
    m.addAction(a)

    for fld, val in self.note.items():
        key = getKeyForContext(self, field=fld)
        addCheckableAction(m, key, fld)

    m.exec_(QCursor.pos())


def onCheck(self, key):
    setConfig(self, key, not getConfig(self, key))


Editor.__init__ = wrap(Editor.__init__, myEditorInit)
mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")


def on_webview_will_set_content(web_content: WebContent, context):
    if not isinstance(context, Editor):
        return
    web_content.js.append(f"/_addons/{addon_package}/web/editor.js")
    web_content.js.append(f"/_addons/{addon_package}/web/editor.css")
    web_content.body += "<script>$('#fields').bind('DOMNodeInserted', makeColumns);</script>"


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
