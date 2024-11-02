import json

from pipeline import *
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from fastapi import FastAPI

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

# debater_a: Debater = Debater("Person A", StubLLM())
# debater_b: Debater = Debater("Person B", StubLLM())
with open("secrets.json", "r") as secrets_file:
    secrets = json.load(secrets_file)
    for secret_key in secrets:
        os.environ[secret_key] = secrets[secret_key]

debater_a: Debater = Debater("Person A")
debater_a.set_llm(LLMType.OPENAI)
debater_b: Debater = Debater("Person B")
debater_b.set_llm(LLMType.OPENAI)
pipeline: DebatePipeline = DebatePipeline(0.001, debater_a, debater_b, 3)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class DebateTopic(BaseModel):
    topic: str


@app.post("/start-debate")
async def start_debate(debate_topic: DebateTopic):
    pipeline.run(debate_topic.topic)
    return {"message": pipeline.transcript.data}


class InputFilesInfo(BaseModel):
    file_contents: str
    is_debater_a: bool


@app.post("/input-files/")
async def input_files(input_files_info: InputFilesInfo):
    if input_files_info.is_debater_a:
        debater_a.set_file_contents(input_files_info.file_contents)
    else:
        debater_b.set_file_contents(input_files_info.file_contents)


class RoleInfo(BaseModel):
    role: str
    is_debater_a: bool


@app.post("/submit-role/")
async def submit_role(role_info: RoleInfo):
    if role_info.is_debater_a:
        debater_b.set_role(role_info.role)
    else:
        debater_b.set_role(role_info.role)
    return


@app.get("/resume-debate")
async def resume_debate():
    pipeline.resume_debate()
    return {"message": pipeline.transcript.data}