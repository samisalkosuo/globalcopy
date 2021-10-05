from os.path import exists
import configparser
from pynput import keyboard
import pyperclip

HOTKEYS = []
EXIT_NOW=False

def exit():
    print('Exiting...')
    global EXIT_NOW
    EXIT_NOW=True


def configureShortcuts():
    config = configparser.ConfigParser(strict=False)
    customIniFile="globalcopy_custom.ini"
    if  exists(customIniFile):
        #read config from custom ini file
        config.read(customIniFile)
    else:
        #read config from sample ini file
        config.read('globalcopy.ini')
    #group sections
    global HOTKEYS
    HOTKEYS = []
    groupSections = config.sections()
    shortcut_index=0
    for shortcut in groupSections:
        print("Shortcut: %s" % shortcut)
        shortcutCfg=config[shortcut]
        textToCopy=shortcutCfg["text"]
        textToPrint=shortcutCfg["description"]
        if textToCopy == "EXIT_COMMAND":
            exec("HOTKEYS.append(keyboard.HotKey(keyboard.HotKey.parse('%s'), exit))" % shortcut)
        else:
            #create function to copy text to clipboard
            exec("""
def on_hotkey_%d():
    pyperclip.copy('%s')
    print('%s')
""" % (shortcut_index, textToCopy, textToPrint))
            #add hotkey
            exec("HOTKEYS.append(keyboard.HotKey(keyboard.HotKey.parse('%s'), on_hotkey_%d))" % (shortcut, shortcut_index))
            shortcut_index = shortcut_index + 1

def on_press(listener, key):
    for hotkey in HOTKEYS:
        hotkey.press(listener.canonical(key))

def on_release(listener, key):
    for hotkey in HOTKEYS:
        hotkey.release(listener.canonical(key))
    if EXIT_NOW==True:
        return False



def main():
    configureShortcuts()
    with keyboard.Listener(
            on_press=lambda *a: on_press(listener, *a),
            on_release=lambda *a: on_release(listener, *a)) as listener:
        listener.join()

if __name__ == "__main__":
    main()
