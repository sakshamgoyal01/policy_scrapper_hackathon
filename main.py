from fastapi import FastAPI
from routes.api import router
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
app = FastAPI(title="Policy Query Retrieval")
app.include_router(router, prefix="/api/v1")
