from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def read_root(request: Request):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {"docs": str(docs_url)}
