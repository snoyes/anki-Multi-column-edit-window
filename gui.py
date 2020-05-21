from anki.hooks import wrap
from aqt import (QAction, QCursor, QHBoxLayout, QLabel, QMenu, QPushButton,
                 QSpinBox)
from aqt.editor import Editor
from aqt import gui_hooks

from .config import getConfig, getKeyForContext, setConfig, switch

def onColumnCountChanged(self, count):
    "Save column count to settings and re-draw with new count."
    setConfig(self, getKeyForContext(self), count)


def myEditorInit(self):
    self.ccSpin = QSpinBox(self.widget)
    hbox = QHBoxLayout()
    hbox.setSpacing(0)
    label = QLabel("Columns:", self.widget)
    hbox.addWidget(label)
    hbox.addWidget(self.ccSpin)

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


gui_hooks.editor_did_init.append(myEditorInit)
