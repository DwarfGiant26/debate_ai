from abc import ABC, abstractmethod
from enum import Enum
from typing import *

from langchain.memory import ConversationTokenBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI


class LLM(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def send(self, message: str) -> str:
        """
        Sends a message to the LLM and get the response
        :param message: prompt message
        :return: response from the llm in string
        """
        pass

    @abstractmethod
    def get_memory(self) -> str:
        """
        Get history of the conversation that the LLM remember.
        :return: history from the llm in string
        """
        pass


class OpenAILLM(LLM):
    def __init__(self):
        super().__init__()
        self.model = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo")
        self.memory = ConversationTokenBufferMemory(llm=self.model, max_token_limit=500)

        self.conversation = ConversationChain(
            llm=self.model,
            memory=self.memory,
            verbose=True
        )

    def send(self, message: str) -> str:
        """
        Send a message to the llm, and update the memory on the new input and the new llm response/
        If files are provided, query will be sent to query engine that indexed the file first.
        :param message:
        :return: response from llm
        """

        output = self.conversation.predict(input=message)
        return output

    def get_memory(self) -> str:
        return self.memory.buffer


class StubLLM(LLM):
    STUB_RESPONSE = "Stub response"

    def send(self, message: str) -> str:
        return StubLLM.STUB_RESPONSE

    def get_memory(self) -> str:
        # TODO
        return ""


class LLMType(Enum):
    STUB = 1
    OPENAI = 2


class Debater:
    def __init__(self, name: str, llm: LLM = StubLLM) -> None:
        self.name = name
        self.llm = llm
        self.input_files = []
        self.role: str = None

    def set_llm(self, llm_type: LLMType):
        if llm_type == LLMType.STUB:
            self.llm = StubLLM()
        elif llm_type == LLMType.OPENAI:
            self.llm = OpenAILLM()

    def set_role(self, role: str):
        self.role = role
        self.specify_role_to_llm()

    def specify_role_to_llm(self):
        if self.role is None or self.role == "":
            return

        to_send: str = f"""
         Hey I want you to act as a really good debater. 
         You need to fully believe what you say.
         Don't back down on any point. Keep fighting on it.
         Your role this time is {self.role}. Really act like a {self.role}.   
         Think of what kind of word choices will {self.role} use.
        """
        response = self.send(to_send)
        print(f"{to_send}, response:{response}")

    def get_name(self) -> str:
        return self.name

    def send(self, message: str) -> str:
        return self.llm.send(message)

    def set_file_contents(self, input_files: str):
        self.input_files = input_files
        self.llm.is_index_updated = False
