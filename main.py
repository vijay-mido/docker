from fastapi import FastAPI
from .routs import route
app= FastAPI(title="new Test")

app.include_router(route)