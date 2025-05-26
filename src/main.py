from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title = "inventary",
    description = "API REST for managin inventory",
    version = "0.1.0",
)


@app.get ("/")
async def root():
    return {"message": "Welcome to the inventory"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host= "127.0.1.0", port=port)