import openai
from threading import Thread
from decouple import config
from openai import OpenAI


class ChatGPT(Thread):

    def __init__(self):
        super().__init__()

        OPENAI_API_KEY = config("OPENAI_API_KEY")
        self.CHAT_LOG = config("CHAT_LOG")

        self.defaultModel = 0
        self.GPT_MODELS = [
            config("GPT_MODEL0"),
            config("GPT_MODEL1"),
            config("GPT_MODEL2"),
        ]

        print("Using OPENAI KEY", OPENAI_API_KEY)
        print("Using Chat Log", self.CHAT_LOG)

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
            {"role": "system", "content": self.CHAT_LOG},
        ]
        self.cummulative = []

    def getModel(self):
        model = str(self.GPT_MODELS[self.defaultModel])
        print("Using GPT_MODEL", model)
        return model

    def makeQueryObj(self, query):
        # create a query object
        user_query = [
            {"role": "user", "content": query},
        ]
        # create the query to be sent
        send_query = self.chat_log + self.cummulative + user_query
        return send_query

    def sendQueryObj(self, model, send_query):
        # make a OpenAI connection client
        # construct a response object for the query message
        response = self.client.chat.completions.create(model=model, messages=send_query)
        # get OpenAI answer!
        answer = response.choices[0].message.content
        # return the answer trimmed
        return str.strip(str(answer))

    def ClearCummulativeAnswers(self):
        self.cummulative = []
        print("Clearing Cumm Answers", self.cummulative)

    def AppendAnswer(self, answer):
        self.cummulative.append({"role": "assistant", "content": answer})

    # to be tested
    def SwitchModel(self):
        self.defaultModel = self.defaultModel + 1
        if self.defaultModel >= len(self.GPT_MODELS):
            self.defaultModel = 0
        model = str(self.GPT_MODELS[self.defaultModel])
        print("Using Default Model", model, "from length", len(self.GPT_MODELS))

    def Query(self, query):
        
        response = None
        hastranscriptLen = len(query)

        if hastranscriptLen == 0:
            return response
            
        try:
            model = self.getModel()
            queryToSend = self.makeQueryObj(query)
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
