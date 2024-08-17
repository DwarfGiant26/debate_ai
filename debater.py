from abc import ABC, abstractmethod


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


class StubLLM(LLM):
    STUB_RESPONSE = "Stub response"

    def send(self, message: str) -> str:
        return StubLLM.STUB_RESPONSE


class Debater:
    def __init__(self, name: str, llm: LLM) -> None:
        self.name = name
        self.llm = llm

    def get_name(self) -> str:
        return self.name

    def send(self, message: str) -> str:
        return self.llm.send(message)
