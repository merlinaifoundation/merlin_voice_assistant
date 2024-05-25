from threading import Thread
from time import sleep
import textwrap


class TextDisplay(Thread):
    def __init__(self):
        super().__init__()
        self.chat = None

        self._stop = False

    def Tell(self, chat):
        self.chat = chat
        self.start()

    def run(self):

        try:

            wrapper = textwrap.TextWrapper(width=70)
            if self.chat != None:
                paragraphs = self.chat.split("\n")
                wrapped_chat = "\n".join([wrapper.fill(p) for p in paragraphs])
                for word in wrapped_chat:
                    sleep(0.055)
                    print(word, end="", flush=True)
                print()

        except Exception as error:
            print("Error:", error)

        self._stop = True
        self.chat = None

