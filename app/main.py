from fastapi import FastAPI
import uvicorn

from app.api.students_api import students
from app.api.group_api import groups

app = FastAPI()
app.include_router(students)
app.include_router(groups)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)