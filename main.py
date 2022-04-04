import pyautogui
import time
import keyboard
import func

from os import system
from keyCodes import universal_key
from keyCodes import macro_key_codes

system("title Macro Mate")

print(" Welcome to macro mate! ".center(70, "="))
print("1. Record a macro (very very unstable avoid using this)")
print("2. Run an existing macro")
print("3. To get a list of keynames to use in *.mc file (Marco file)")
print("Note: we will recommend creating a macro file manually instead of recording".center(70, " "))
print("\n")

choice = input("Enter your choice (default is 2): ")
if len(choice) == 0:
    choice = '2'
if choice == '3':
    for key in macro_key_codes:
        print(r"'{}'".format(key))
elif choice == '1':
    print("recording...")
    macro_keys = func.record_macro()
    print(macro_keys)
    print(" Macro Options ".center(70, "="))
    print("1. Run the macro")
    print("2. Save the macro")

    choice2 = input("\nEnter your choice: ")
    if choice2 == '1':
        print("Press '{}' to play the macro ('q' to quit)".format(universal_key))
        while not keyboard.is_pressed('q'):
            if keyboard.is_pressed('{}'.format(universal_key.lower())):
                print("running the macro")
                for key in macro_keys:
                    try:
                        pyautogui.press(key.replace("$Key.", '$'))
                    except:
                        print("Error while trying to simulate key: {}".format(str(key.replace("Key.", ""))))
    if choice2 == '2':
        with open("macro.mc", 'w') as file:
            for key in macro_keys:
                file.write(str(key.replace('$Key.', '')) + "\n")
elif choice == '2':
    print("Type the path of Macro File", end=": ")
    file_path = input()
    try:
        with open(file_path, "r") as file:
            print("\nPress '{}' to play the macro ('q' to quit)".format(universal_key))

            file_contents = file.read().split("\n")
            pressed = False
            while not keyboard.is_pressed('q'):
                if keyboard.is_pressed('{}'.format(universal_key.lower())) and not pressed:
                    pressed = True
                    print("\nrunning the macro")
                    for index, key in enumerate(file_contents):
                        try:
                            if key.startswith('$DELAY'):
                                args = key.split()
                                if len(args) == 2:
                                    time.sleep(float(args[1]))
                                else:
                                    print("Syntax error on line '{}'".format(index+1))
                                    exit(1)
                                continue
                            elif key.startswith('$'):
                                pyautogui.press(key.replace('$', ''))
                                # print('Pressing "{}"'.format(key.replace('$', '')))
                            elif key.startswith('!'):
                                args = key.replace('!', '').split()
                                hotKeyArgsLength = len(args)
                                # print('[DEBUG] Args: "{}"'.format(hotKeyArgsLength))
                                if hotKeyArgsLength == 2:
                                    with pyautogui.hold(args[0]):
                                        pyautogui.press(args[1])
                                    # print('Pressing hotkey "{}"'.format(key.replace('!', '')))
                            else:
                                pyautogui.typewrite(key.replace('$', ''))
                                # win32api.keybd_event(VK_CODE[str(button)], 0,0,0)
                                # time.sleep(0.005)
                                # win32api.keybd_event(VK_CODE[str(button)],0 ,win32con.KEYEVENTF_KEYUP ,0)
                        except Exception as e:
                            print('[DEBUG] actual error: "{}"'.format(str(e)))
                            print("Error while trying to simulate key: {}".format(str(key.replace("Key.", ""))))
                    print("If you wanna run the macro then press '{}' again else press 'q'".format(universal_key))
                    pressed = False
    except Exception as e:
        print("[DEBUG] actual error: \"{}\"".format(str(e)))
        print("File not found or program crashed...")
else:
    print("\nInvalid option")

print("Program Exited")
system("pause>nul")
