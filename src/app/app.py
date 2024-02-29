import argparse
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run
import pathlib
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.search.engine import SearchEngine

script_dir = pathlib.Path(__file__).resolve().parent
templates_path = script_dir / "templates"
static_path = script_dir / "static"


app = FastAPI()
engine = SearchEngine()
templates = Jinja2Templates(directory=str(templates_path))
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with specific origins
    allow_credentials=True,
    # Add other HTTP methods as needed
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],  # You can replace "*" with specific headers
)


@app.get("/", response_class=HTMLResponse)
async def search(request: Request, query: str = Query("")):  # Use Query param instead of Path
    posts = engine.posts
    if query:
        results, resp_time = engine.handle_search(query, n=10)
    else:
        results = {}
        resp_time = 0.0
    return templates.TemplateResponse(
        "search.html", {"request": request, "posts": posts,
                        "results": results, "query": query, "time": resp_time}
    )


class SearchRequest(BaseModel):
    search_query: str


@app.post("/api")
# Use Query param instead of Path
async def get_search(request: Request, data: SearchRequest):

    query = data.model_dump()['search_query']

    if query:
        results = engine.handle_search(query, n=10)
    else:
        results = {}
    return results



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(app, host="127.0.0.1", port=8000)
