from pynput import keyboard
from keyCodes import universal_key

def on_key_press(key, keys, listener):
    try:
        keys.append(key.char)
        print("{} key is pressed".format(key.char))
    except AttributeError:
        if str(key) == "Key.{}".format(universal_key.lower()):
            listener.stop()
            return
        keys.append('$' + str(key))
        print("{} special key is pressed".format(key))

def record_macro():
    keys = []
    with keyboard.Listener(on_press=lambda key: on_key_press(key, keys, listener)) as listener:
        listener.join()
        return keys
