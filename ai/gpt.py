import time
import openai
from threading import Thread
from decouple import config
from openai import OpenAI
from difflib import SequenceMatcher


class ChatGPT(Thread):

    def __init__(self):
        super().__init__()

        OPENAI_API_KEY = config("OPENAI_API_KEY")
        CHAT_LOG = config("CHAT_LOG")
        self.CHAT_LOG_LAST = str(config("CHAT_LOG_LAST"))

        self.frequencyPenalty = float(config("CHATGPT_FREQUENCY_PENALTY"))
        self.temperature = float(config("CHATGPT_TEMPERATURE"))

        self.defaultModel = 0
        self.GPT_MODELS = [
            config("GPT_MODEL0"),
            config("GPT_MODEL1"),
            config("GPT_MODEL2"),
        ]
        self._stop = False
        # print("Using OPENAI KEY", OPENAI_API_KEY)
        print("Using Merlin Default Prompt: ")
        print(CHAT_LOG)

        self.prompt = [
            "How may I assist you?",
            "How may I help?",
            "What can I do for you?",
            "Ask me anything.",
            "Yes?",
            "I'm here.",
            "I'm listening.",
            "What would you like me to do?",
        ]

        self.client = OpenAI(api_key=str(OPENAI_API_KEY))
        self.count = 0
        self.chat_log = [
            {"role": "system", "content": CHAT_LOG},
        ]
        self._cancelled = False
        self._cummulativeResponse = []
        self._hasRecordedStuff = None
        self.lastAiResponse = None

        self._cummulativeChat = []
        self._isIdle = True

    def getModel(self):
        model = str(self.GPT_MODELS[self.defaultModel])
        print("Using GPT_MODEL", model)
        return model

    def makeQueryObj(self, query, role):
        # create a query object
        user_query = [
            {"role": role, "content": query},
        ]
        # create the query to be sent
        send_query = self.chat_log + self._cummulativeChat + user_query
        return send_query

    def sendQueryObj(self, model, send_query):
        # make a OpenAI connection client
        # construct a response object for the query message
        response = self.client.chat.completions.create(
            model=model,
            messages=send_query,
            temperature=self.temperature,
            frequency_penalty=self.frequencyPenalty,
        )
        # get OpenAI answer!
        answer = response.choices[0].message.content
        # return the answer trimmed
        return str.strip(str(answer))

    def clearCummulativeList(self):
        self._cummulativeChat = []

    def clearCummulativeResponse(self):
        self._cummulativeResponse = []

    def appendToConversation(self, questionOrAnswer, role, maximum):
        QAs = len(self._cummulativeChat)
        if QAs > maximum:
            print("Clearing Cumm List", QAs)
            self.clearCummulativeList()
        if questionOrAnswer is not None:
            self._cummulativeChat.append({"role": role, "content": questionOrAnswer})

    def getBrieferCommand(self):
        return self.CHAT_LOG_LAST

    def speechToText(self, file, response_format):

        transcription = None
        try:

            if file:
                audio_file = open(file, "rb")
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format=response_format
                )
                if transcription:
                    transcription = str(transcription)

        except Exception as e:
            print("\nError", e)

        return transcription

    def query(self, query, role):

        response = None
        if query is None or not query:
            return response
        if len(query) == 0:
            return response

        try:

            model = self.getModel()
            queryToSend = self.makeQueryObj(query, role)
            response = self.sendQueryObj(model, queryToSend)
        except openai.error.APIError as e:
            response = "\nThere was an API error.  Please try again in a few minutes."
            print(e)
        except openai.error.Timeout as e:
            response = "\nYour request timed out.  Please try again in a few minutes."
            print(e)
        except openai.error.RateLimitError as e:
            response = "\nYou have hit your assigned rate limit."
            print(e)
        except openai.error.APIConnectionError as e:
            response = "\nI am having trouble connecting to the API.  Please check your network connection and then try again."
            print(e)
        except openai.error.AuthenticationError as e:
            response = "\nYour OpenAI API key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program."
            print(e)
        except openai.error.ServiceUnavailableError as e:
            response = (
                "\nThere is an issue with OpenAI's servers.  Please try again later."
            )
            print(e)
        return response

    def isRedundancy(self, userTranscript):
        if userTranscript and self.lastAiResponse:
            matcher = SequenceMatcher(
                isjunk=None, a=userTranscript, b=self.lastAiResponse, autojunk=True
            )
            ratio = matcher.ratio()
            self.lastAiResponse = None
            print("Typical Identical Ratio:", ratio)
            if ratio > 0.75:
                print(
                    "ABORT! Too similar to last response",
                )
                return True
        return False

    def run(self):

        while not self._stop:

            time.sleep(0.001)

            # if self._isIdle:

            # self._isIdle = False

            if self._hasRecordedStuff:
                if not self._cancelled:
                    userTranscript = self.speechToText(self._hasRecordedStuff, "text")
                    self._hasRecordedStuff = None
                    print("\nTranscript:", userTranscript)
                    abortResearch = self.isRedundancy(userTranscript)
                    if userTranscript and not abortResearch:
                        role = "user"
                        self.lastAiResponse = self.query(userTranscript, role)
                        if self.lastAiResponse:
                            self._cummulativeResponse.append(self.lastAiResponse)
                            if not self._cancelled:
                                self.appendToConversation(
                                    self.lastAiResponse, "assistant", 20
                                )
                                if userTranscript:
                                    self.appendToConversation(userTranscript, role, 20)
                self.printCummulative()

            else:
                if self._cancelled:
                    userTranscript = self.getBrieferCommand()
                    role = "system"
                    self.lastAiResponse = self.query(userTranscript, role)
                    if self.lastAiResponse:
                        self.clearCummulativeList()
                        self.clearCummulativeResponse()
                        aiResponse = "Our last conversation was about: " + str(
                            self.lastAiResponse
                        )
                        self.appendToConversation(
                            aiResponse,
                            role,
                            20,
                        )
                        self.lastAiResponse = aiResponse
                    self.printCummulative()

                # self._isIdle = True

        # sys.exit(None)

    def printCummulative(self):
        print(
            "\nCurrent Cumm Responses: ",
            len(self._cummulativeResponse),
        )
        print(
            "Current Cumm Chat: ",
            len(self._cummulativeChat),
        )

    def SetQuery(self, recordedStuff):
        self._hasRecordedStuff = recordedStuff

    def SetCancelled(self, cancelled):
        self._cancelled = cancelled

    def TakeResponse(self):
        if len(self._cummulativeResponse) > 0:
            return self._cummulativeResponse.pop(0)
        return None

    # to be tested
    def SwitchModel(self):
        self.defaultModel = self.defaultModel + 1
        if self.defaultModel >= len(self.GPT_MODELS):
            self.defaultModel = 0
        model = str(self.GPT_MODELS[self.defaultModel])
        print("Using Default Model", model, "from length", len(self.GPT_MODELS))

    def StartThread(self):
        self.start()

    def StopThread(self):
        self._stop = True
