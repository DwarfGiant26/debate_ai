from pipeline import *
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI, File

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

debater_a: Debater = Debater("Person A", StubLLM())
debater_b: Debater = Debater("Person B", StubLLM())
# debater_a: Debater = Debater("Person A")
# debater_a.set_llm(LLMType.OPENAI)
# debater_b: Debater = Debater("Person B")
# debater_b.set_llm(LLMType.OPENAI)
pipeline: DebatePipeline = DebatePipeline(0.001, debater_a, debater_b, 10, "Starting question")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/start-debate")
async def start_debate():
    pipeline.start()
    return {"message": pipeline.transcript.data}


class InputFilesInfo(BaseModel):
    file_contents: str
    is_debater_a: bool


@app.post("/input-files/")
async def input_files(input_files_info: InputFilesInfo):
    files: list[str] = [str(file) for file in input_files_info.file_contents]
    if input_files_info.is_debater_a:
        debater_a.set_input_files(files)
    else:
        debater_b.set_input_files(files)
