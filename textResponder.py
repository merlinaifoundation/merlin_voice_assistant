from threading import Thread
from time import sleep
import textwrap


class TextDisplay(Thread):
    def __init__(self):
        super().__init__()
        self.chat = None

        self._stop = True

    def run(self):

        try:

            wrapper = textwrap.TextWrapper(width=70)
            if self.chat != None:
                paragraphs = self.chat.split("\n")
                wrapped_chat = "\n".join([wrapper.fill(p) for p in paragraphs])
                for word in wrapped_chat:
                    sleep(0.055)
                    print(word, end="", flush=True)
                print('\n')
                

        except Exception as error:
            print("Error:", error)

        self._stop = True
        
        

    def Tell(self, chat):
        if (self._stop) and (chat is not None):
            self._stop = False
            self.chat = chat
            self.start()

    def Finished(self):
        return (self._stop) and (self.chat is not None)
