from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from typing import Optional
import aiosqlite
from time import time

app = FastAPI()


# Open the sqlite database
@app.on_event("startup")
async def startup():
    # Initialize the SQLite connection
    app.state.db = \
        await aiosqlite.connect("/data/db.sqlite")

    query = "CREATE TABLE IF NOT EXISTS healthcheck(" + \
        "id INTEGER PRIMARY KEY AUTOINCREMENT, " + \
        "name TEXT UNIQUE, " + \
        "expires LONG," + \
        "status INTEGER" + \
        ")"

    await app.state.db.execute(query)


# Disconnect/clean-up on shutdown
@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.get("/")
async def root():
    return {"ready": "yes"}


@app.get("/ping/{name}")
async def ping(name: str,
               ttl: int | None = Header(default=3600)
               ):
    expires = int(time() + ttl)
    query = 'INSERT INTO healthcheck(name, expires, status) ' + \
        f'VALUES(\'{name}\', {expires}, 1) ' + \
        f'ON CONFLICT(name) DO UPDATE SET expires={expires}'

    await app.state.db.execute(query)
    await app.state.db.commit()

    return {"expires": expires, "now": int(time())}


@app.delete("/ping/{name}")
async def removeCheck(name: str):
    query = f'DELETE FROM healthcheck where name="{name}";'

    await app.state.db.execute(query)
    await app.state.db.commit()

    return {"status": "ok"}


@app.get("/status")
@app.get("/status/")
@app.get("/status/{name}")
async def status(name: Optional[str] = '%'):
    now = int(time())
    return_code = 200
    statustQuery = f"select name, expires from healthcheck " \
        f"where name like '{name}'"
    cursor = await app.state.db.execute(statustQuery)
    records = await cursor.fetchall()
    checks = {}
    for (key, val) in records:
        checks[key] = val - now
        if val < now:
            return_code = 503

    return JSONResponse(status_code=return_code, content=checks)
