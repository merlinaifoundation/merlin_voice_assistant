# NEW LIBS
import sys
from wizard.wizard import Wizard
#from pynput.keyboard import Key, Listener

wizard = Wizard()

def on_press(key):
    pass
    #print(f"{key} pressed")

def on_release(key):
    #print(f"{key} released")
    #if key == Key.esc:
        wizard.StopThread()
        #listener.stop()
        sys.exit(None)

#listener = Listener(on_press=on_press, on_release=on_release)

try:
    
    wizard.StartThread()

    #listener.start()

    #listener.join()


except Exception as error:
    print("\nExiting...", error)
