from aqt import mw
userOption = None
from .debug import debugFun

def getUserOption():
    global userOption
    if userOption is None:
        userOption = mw.addonManager.getConfig(__name__)
    return userOption

@debugFun
def getConfig(key, default = None):
    return getUserOption().get(key,default)

def setConfig(key, value):
    getUserOption()[key] = value
    mw.addonManager.writeConfig(__name__,userOption)


def update(_):
    global userOption
    userOption = None

mw.addonManager.setConfigUpdatedAction(__name__,update)
