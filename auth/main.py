from typing import Annotated

import ldap
from fastapi import FastAPI, Response, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, PlainTextResponse
from fastapi import status
import os

def get_username_from_hash(hash):
    hashes_file = open("hashes.txt", "r")
    hashes = {x.split(':')[0]: x.split(':')[1] for x in hashes_file.read().split("\n")}
    if hash in hashes.values():
        for username, hash_candidate in hashes.items():
            if hash == hash_candidate:
                return username
    return None


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
            response.set_cookie(key="code-server-session", value=hashes[username], path="/", samesite='lax')
        else:
            return Response(content="No hash found for user", status_code=status.HTTP_401_UNAUTHORIZED)
        return response
    except ldap.INVALID_CREDENTIALS:
        response = RedirectResponse(f"/login?error=1&username={username}", status_code=status.HTTP_303_SEE_OTHER)
        return response


@app.get("/")
def home(request:Request):
    server_hash = request.cookies.get("code-server-session")
    if not server_hash:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    if get_username_from_hash(server_hash):
        username = get_username_from_hash(server_hash)
        short_username = username.lower().split(".")[0][0] + username.lower().split(".")[1]
        return RedirectResponse(f"/{short_username}/", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

