import logging
from fastapi import FastAPI, Header, HTTPException, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
import paramiko
import os
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

HOST = os.getenv("SSH_HOST")
PORT = os.getenv("SSH_PORT")
USERNAME = os.getenv("SSH_USERNAME")
PASSWORD = os.getenv("SSH_PASSWORD")
FAST_API_KEY = os.getenv("FAST_API_KEY")

app = FastAPI()

app.mount("/", StaticFiles(directory="static"), name="static")


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


@app.get("/list-directory")
def list_directory(
    background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)
):
    background_tasks.add_task(run_command)
    return {"result": "Command is running in the background"}
