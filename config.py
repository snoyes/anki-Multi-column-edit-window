from aqt import mw

config = mw.addonManager.getConfig(__name__)
if config is None:
    config = dict()


def getConfig(self, key, defaultValue=None):
    return config.get(key, defaultValue)


def getKeyForContext(self, field=None):
    """Get a key that takes into account the parent window type and
    the note type.

    This allows us to have a different key for different contexts,
    since we may want different column counts in the browser vs
    note adder, or for different note types.
    """
    key = str(self.note.mid)
    if getConfig(self, "same config for each window", False):
        key = f"{self.parentWindow.__class__.__name__}-{key}"
    if field is not None:
        key = f"{key}{field}"
    return key


def shortcut():
    return config.get("shortcut", "alt+f")

def setConfig(self, key, value):
    config[key] = value
    mw.addonManager.writeConfig(__name__, config)
    self.loadNote()

def update(_):
    global config
    config = None

mw.addonManager.setConfigUpdatedAction(__name__, update)
