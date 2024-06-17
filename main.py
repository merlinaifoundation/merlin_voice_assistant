# NEW LIBS
from wizard.base import Wizard

try:

    wizard = Wizard()
    wizard.StartThread()


except Exception as error:
    print("\nExiting...", error)
