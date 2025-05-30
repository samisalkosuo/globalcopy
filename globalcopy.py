import yaml
import os
from pynput import keyboard
import clipman
clipman.init()

class ExitException(Exception): pass

def load_hotkeys(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"File '{file_path}' not found.\n\n"
            "Expected YAML file format:\n"
            "hot_keys:\n"
            "  - key: \"<alt_gr>+i\"\n"
            "    text: \"Text to be copied\"\n"
            "    desc: \"Description of this\"\n"
            "  - key: \"<alt_gr>+j\"\n"
            "    text: \"Another Text to be copied\"\n"
            "    desc: \"Description of this one\"\n"
            "  - key: \"<alt_gr>+x\"\n"
            "    text: \"exit\"\n"
            "    desc: \"Exit program. text must be 'exit'.\"\n"
        )

    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    result = {
        entry['key']: {
            'text': entry['text'],
            'desc': entry['desc']
        }
        for entry in data.get('hot_keys', [])
    }

    return result

def generate_hotkey_functions(config):
    #global globalHotkeys
    globalHotkeys = {}
    for key_combo, info in config.items():
        # Create a function using a closure to capture key_combo and info
        def make_function(text, desc):
            if text == "exit":
                def action():
                    raise ExitException()
                return action
            else:
                def action():
                    clipman.copy(text)
                    print(desc)
                return action

        globalHotkeys[key_combo] = make_function(info['text'], info['desc'])
    return globalHotkeys

def main():
    print("Global copy started.")
    globalHotkeyConfig = load_hotkeys('globalcopy.yaml')
    globalHotkeys = generate_hotkey_functions(globalHotkeyConfig)
    #global hotkeys
    #see: https://github.com/moses-palmer/pynput/blob/master/docs/keyboard-usage.rst
    with keyboard.GlobalHotKeys(globalHotkeys) as h:
        try:
            h.join()
        except ExitException:
            print("Exiting GlobalCopy...")

if __name__ == "__main__":
    main()
