# -*- coding: utf-8 -*-
# Version: 2.5
# See github page to report issues or to contribute:
# https://github.com/hssm/anki-addons

from anki.hooks import wrap
from aqt import *
from aqt.editor import Editor
import aqt.editor
from . import config


# Flag to enable hack to make Frozen Fields look normal
ffFix = False

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
js_file = os.path.join(__location__,"js.js")
user_files = os.path.join(__location__,"user_files")
css_file = os.path.join(user_files,"css.css")
with open(js_file,"r") as f:
    js= f.read()
with open(css_file,"r") as f:
    css= f.read()

aqt.editor._html += f"""<style>{css}</style><script>{js}</script>"""

def getKeyForContext(self,field=None):
    """Get a key that takes into account the parent window type and
    the note type.
    
    This allows us to have a different key for different contexts,
    since we may want different column counts in the browser vs
    note adder, or for different note types.
    """
    #We use mid and not model name because we want the configuration
    #to remain if the model is renamed.
    key = str(self.note.mid)
    if not config.getConfig("same config for each window",True):
        key=f"{self.parentWindow.__class__.__name__}-{key}"
    if field is not None:
        key=f"{key}{field}"
    return key

def setConfig(self,key,value):
    config.setConfig(key,value)
    self.loadNote()

def onColumnCountChanged(self, count):
    "Save column count to settings and re-draw with new count."
    setConfig(self,getKeyForContext(self),count)

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
    self.ccSpin.setMaximum(config.getConfig("MAX_COLUMNS", 18))
    self.ccSpin.valueChanged.connect(lambda value: onColumnCountChanged(self, value))

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


def myOnBridgeCmd(self, cmd):
    """
    Called from JavaScript to inject some values before it needs
    them.
    """
    if cmd == "mceTrigger":
        count = config.getConfig(getKeyForContext(self), 1)
        self.web.eval(f"setColumnCount({count});")
        self.ccSpin.blockSignals(True)
        self.ccSpin.setValue(count)
        self.ccSpin.blockSignals(False)
        for fld, val in self.note.items():
            key=getKeyForContext(self,field=fld)
            if config.getConfig(key, False):
                self.web.eval(f"setSingleLine('{fld}');")
        if ffFix:
            self.web.eval("setFFFix(true)")
        self.web.eval("makeColumns2()")


def onConfigClick(self):
    m = QMenu(self.mw)
    def addCheckableAction(menu, key, text):
        a = menu.addAction(text)
        a.setCheckable(True)
        a.setChecked(config.getConfig(key, False))
        a.toggled.connect(lambda b, k=key: onCheck(self, k))

    # Descriptive title thing
    a = QAction(u"―Single Row―", m)
    a.setEnabled(False)
    m.addAction(a)
    
    for fld, val in self.note.items():
        key = getKeyForContext(self,field=fld)
        addCheckableAction(m, key, fld)

    m.exec_(QCursor.pos())


def onCheck(self, key):
    setConfig(self,key,not config.getConfig(key))


Editor.__init__ = wrap(Editor.__init__, myEditorInit)
Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, myOnBridgeCmd, 'before')

