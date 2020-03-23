from anki.hooks import wrap
from aqt import (QAction, QCursor, QHBoxLayout, QLabel, QMenu, QPushButton,
                 QSpinBox)
from aqt.editor import Editor

from .config import getConfig, getKeyForContext, setConfig

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


Editor.__init__ = wrap(Editor.__init__, myEditorInit)


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
