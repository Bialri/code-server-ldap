from operator import truediv
from typing import Annotated
import subprocess
import ldap
from fastapi import FastAPI, Response, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, PlainTextResponse
from fastapi import status
from pydantic import BaseModel
import asyncio
import time
import requests


class ShutdownRequest(BaseModel):
    code_server_hash: str


def get_username_from_hash(hash):
    hashes_file = open("hashes.txt", "r")
    hashes = {x.split(':')[0]: x.split(':')[1] for x in hashes_file.read().split("\n")}
    if hash in hashes.values():
        for username, hash_candidate in hashes.items():
            if hash == hash_candidate:
                return username
    return None


async def start_container(username):
    container_name = username.lower().split(".")[1] + username.lower().split(".")[0]
    # subprocess.run(['docker-compose', 'up', '-d', f'{container_name}'])
    started = time.time()
    while True:
        if time.time() - started > 10:
            return False
        try:
            response = requests.get(f"http://{container_name}:8080/healthz")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        await asyncio.sleep(0.1)

app = FastAPI()

@app.get("{rest_of_path:path}/login")
async def get_login(request:Request):
    server_hash = request.cookies.get("code-server-session")
    print(server_hash)
    if server_hash:
        username = get_username_from_hash(server_hash)
        print(username)
        if username:
            short_username = username.lower().split(".")[0][0] + username.lower().split(".")[1]

            started = await start_container(username)
            print(started)


            print(short_username)
            return RedirectResponse(f"/{short_username}/", status_code=status.HTTP_303_SEE_OTHER)


    login_file = open("login.html", "r")
    login_page = login_file.read()
    login_file.close()
    return HTMLResponse(content=login_page, status_code=status.HTTP_200_OK)

@app.get("/global.css")
async def get_global_css():
    login_file = open("global.css", "r")
    login_page = login_file.read()
    login_file.close()
    return PlainTextResponse(content=login_page, status_code=status.HTTP_200_OK)

@app.get("/login.css")
async def get_global_css():
    login_file = open("login.css", "r")
    login_page = login_file.read()
    login_file.close()
    return PlainTextResponse(content=login_page, status_code=status.HTTP_200_OK)

@app.post("{rest_of_path:path}/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    try:
        conn = ldap.initialize('ldap://openldap:389')
        base_dn = "dc=localhost"
        user_dn = "cn={},{}".format(username, base_dn)
        # Perform a synchronous bind
        conn.simple_bind_s(user_dn, password)
        short_username = username.lower().split(".")[0][0] + username.lower().split(".")[1]
        response = RedirectResponse(f"/{short_username}/", status_code=status.HTTP_303_SEE_OTHER)
        hashes_file = open("hashes.txt", "r")
        hashes = { x.split(':')[0]:x.split(':')[1] for x in hashes_file.read().split("\n")}
        if username in hashes.keys():

            started = await start_container(username)
            print(started)

            response.set_cookie(key="code-server-session", value=hashes[username], path="/", samesite='lax')
        else:
            return Response(content="No hash found for user", status_code=status.HTTP_401_UNAUTHORIZED)
        return response
    except ldap.INVALID_CREDENTIALS:
        response = RedirectResponse(f"/login?error=1&username={username}", status_code=status.HTTP_303_SEE_OTHER)
        return response


@app.get("/")
async def home(request:Request):
    server_hash = request.cookies.get("code-server-session")
    if not server_hash:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    if get_username_from_hash(server_hash):
        username = get_username_from_hash(server_hash)
        short_username = username.lower().split(".")[0][0] + username.lower().split(".")[1]

        started = await start_container(username)
        print(started)

        return RedirectResponse(f"/{short_username}/", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/shutContainer")
def shut_container(request: ShutdownRequest):
    print(request.code_server_hash)
