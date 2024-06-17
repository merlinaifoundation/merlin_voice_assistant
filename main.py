# NEW LIBS
from wizard.wizard import Wizard

try:

    wizard = Wizard()
    wizard.StartThread()


except Exception as error:
    print("\nExiting...", error)
