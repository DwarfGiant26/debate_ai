from abc import ABC, abstractmethod
from enum import Enum
from typing import *
from llama_index.core import Document


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


from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector


class OpenAILLM(LLM):
    def __init__(self, get_input_files: Callable[[], list[str]], is_input_files_change: Callable[[], bool],
                 set_is_index_updated: Callable[[], None]):
        from llama_index.core import Settings
        from llama_index.llms.openai import OpenAI
        from llama_index.embeddings.openai import OpenAIEmbedding

        super().__init__()
        self.query_engine = self.get_engine()
        self.get_input_files = get_input_files
        self.is_input_files_change = is_input_files_change
        self.set_is_index_updated = set_is_index_updated

        Settings.llm = OpenAI(model="gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

    def get_engine(self) -> RouterQueryEngine:
        """
        Build query engine.
        If input file change, build new query engine.
        Otherwise, just return existing one.

        :return:
        """
        if not self.is_input_files_change():
            return self.query_engine

        documents = [Document(text=t) for t in self.get_input_files()]
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(documents)
        summary_index = SummaryIndex(nodes)
        vector_index = VectorStoreIndex(nodes)

        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize",
            use_async=True,
        )
        vector_query_engine = vector_index.as_query_engine()

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

        self.set_is_index_updated()

        return self.query_engine

    def send(self, message: str) -> str:
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
        self.last_input_files = set()
        self.is_index_updated = True

    def set_llm(self, llm_type: LLMType):
        if llm_type == LLMType.STUB:
            self.llm = StubLLM()
        elif llm_type == LLMType.OPENAI:
            self.llm = OpenAILLM(lambda: self.input_files, lambda: self.is_index_updated, self.set_is_index_updated)

    def get_name(self) -> str:
        return self.name

    def send(self, message: str) -> str:
        return self.llm.send(message)

    def set_input_files(self, input_files: list[str]):
        self.input_files = input_files

    def set_is_index_updated(self):
        self.is_index_updated = True

    def is_input_files_change(self) -> bool:
        """
        Checks if the input filenames are changing. Doesn't check if the file content is different.
        :return: Whether the input filenames are changing
        """
        if len(self.input_files) != len(self.last_input_files):
            return False

        for input_file in self.input_files:
            if input_file not in self.last_input_files:
                return False

        return True
