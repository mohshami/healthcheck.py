from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
import aiosqlite
from time import time


class Settings(BaseSettings):
    app_name: str = "healthcheck.py"
    db_path: str = "/data/db.sqlite"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
app = FastAPI()


# Open the sqlite database
@app.on_event("startup")
async def startup():
    # Initialize the SQLite connection
    app.state.db = await aiosqlite.connect(settings.db_path)

    query = (
        "CREATE TABLE IF NOT EXISTS healthcheck("
        + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        + "name TEXT UNIQUE, "
        + "lastupdate DATETIME DEFAULT CURRENT_TIMESTAMP,"
        + "grace LONG,"
        + "output TEXT,"
        + "exitcode INTEGER"
        + ")"
    )

    await app.state.db.execute(query)


# Disconnect/clean-up on shutdown
@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.get("/")
async def root():
    return {"ready": "yes"}


@app.get("/update/{name}")
async def update(
    name: str,
    grace: int | None = Header(default=3600),
    output: str | None = Header(default=""),
    exitcode: int | None = Header(default=0),
):
    query = (
        "INSERT INTO healthcheck(name, grace, output, exitcode) "
        + f"VALUES('{name}', {grace}, '{output}', {exitcode}) "
        + f"ON CONFLICT(name) DO UPDATE SET lastupdate=CURRENT_TIMESTAMP, grace={grace}, output='{output}', exitcode={exitcode}"
    )

    try:
        await app.state.db.execute(query)
        await app.state.db.commit()
    except Exception:
        return JSONResponse(status_code=500, content={"status": "Error"})

    return {"status": "Success"}


@app.get("/status")
async def statusall():
    query = (
        "select count(id) from healthcheck where "
        + "unixepoch(lastupdate)+grace < unixepoch(CURRENT_TIMESTAMP) "
        + " or exitcode != 0"
    )

    try:
        cursor = await app.state.db.execute(query)
        record = await cursor.fetchone()
    except Exception:
        return JSONResponse(status_code=500, content={"status": "Error"})

    if int(record[0]) == 0:
        return {"status": "OK"}

    return {"status": "Error", "Message": "At least one check failed or expired"}


@app.get("/status/{name}")
async def status(name: str):
    query = f"select unixepoch(lastupdate), grace, output, exitcode from healthcheck where name='{name}'"

    try:
        cursor = await app.state.db.execute(query)
        record = await cursor.fetchone()
    except Exception:
        return JSONResponse(status_code=500, content={"status": "Error"})

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Check not found",
        )

    return {
        "lastupdate": record[0],
        "grace": record[1],
        "output": "" if record[2] is None else record[2],
        "status": record[3],
        "expired": (record[0] + record[1]) < time(),
    }


@app.get("/delete/{name}")
async def removeCheck(name: str):
    query = f'DELETE FROM healthcheck where name="{name}";'

    try:
        await app.state.db.execute(query)
        await app.state.db.commit()
    except Exception:
        return JSONResponse(status_code=500, content={"status": "Error"})

    return {"status": "ok"}
