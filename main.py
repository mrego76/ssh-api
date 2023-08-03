import logging
from fastapi import FastAPI, Header, HTTPException, Depends, BackgroundTasks
from fastapi.responses import PlainTextResponse
import paramiko
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

HOST = os.getenv("SSH_HOST")
PORT = os.getenv("SSH_PORT")
USERNAME = os.getenv("SSH_USERNAME")
PASSWORD = os.getenv("SSH_PASSWORD")
FAST_API_KEY = os.getenv("FAST_API_KEY")


class RequestParams(BaseModel):
    message: str


app = FastAPI()


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != FAST_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key


def run_command(command="ls"):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(HOST, PORT, USERNAME, PASSWORD)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    result = stdout.read().decode()
    ssh_client.close()
    logger.info(f"{command}: \n{result}")  # 결과를 로그에 기록
    return result


@app.get("/hello")
def hello(
    background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)
):
    background_tasks.add_task(run_command)
    return {"result": "Hello World"}


@app.post("/hello")
def hello(
    request: RequestParams,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
):
    background_tasks.add_task(run_command, request.message)
    return {"result": "Hello World"}


@app.get("/robots.txt")
def read_robots_txt():
    content = """User-agent: *
Disallow: /"""
    return PlainTextResponse(content)
