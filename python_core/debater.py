from abc import ABC, abstractmethod
from enum import Enum
from typing import *
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
import time

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


class OpenAILLM(LLM):
    def __init__(self, get_file_content: Callable[[], str]):
        from llama_index.core import Settings
        from llama_index.llms.openai import OpenAI
        from llama_index.embeddings.openai import OpenAIEmbedding

        super().__init__()
        self.get_file_content = get_file_content
        self.is_index_updated = False
        self.query_engine = None
        self.llm = OpenAI(model="gpt-3.5-turbo")

        Settings.llm = self.llm
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

    def get_engine(self) -> RouterQueryEngine:
        """
        Build query engine.
        If input file change, build new query engine.
        Otherwise, just return existing one.

        :return:
        """
        if self.is_index_updated:
            print("index is updated")
            return self.query_engine

        print(f"input text: {self.get_file_content()}")

        time_start = time.time()

        documents = [Document(text=t) for t in self.get_file_content()]
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(documents)
        summary_index = SummaryIndex(nodes)
        vector_index = VectorStoreIndex(nodes)

        print(f"Finish building nodes and indices in {time.time() - time_start} seconds.")

        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize",
            use_async=True,
        )
        vector_query_engine = vector_index.as_query_engine()

        print(f"Finish building query engines in {time.time() - time_start} seconds.")

        summary_tool = QueryEngineTool.from_defaults(
            query_engine=summary_query_engine,
            description=(
                "Useful for summarization questions"
            ),
        )

        vector_tool = QueryEngineTool.from_defaults(
            query_engine=vector_query_engine,
            description=(
                "Useful for retrieving specific context"
            ),
        )

        self.query_engine = RouterQueryEngine(
            selector=LLMSingleSelector.from_defaults(),
            query_engine_tools=[
                summary_tool,
                vector_tool,
            ],
            verbose=True
        )

        print(f"Finish building router query engine in {time.time() - time_start} seconds.")

        self.is_index_updated = True

        return self.query_engine

    def send(self, message: str) -> str:
        """
        Send a message to the llm.
        If files are provided, query will be sent to query engine that indexed the file first.
        :param message:
        :return: response from llm
        """
        if len(self.get_file_content()) == 0:
            return self.llm.complete(message).text

        return self.get_engine().query(message).response


class StubLLM(LLM):
    STUB_RESPONSE = "Stub response"

    def send(self, message: str) -> str:
        return StubLLM.STUB_RESPONSE


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
            self.llm = OpenAILLM(lambda: self.input_files)

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
