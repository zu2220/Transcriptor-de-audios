from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
from transcribe import transcribe_file


app = FastAPI(title="Transcriptor con Diarización")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.post('/transcribir')
async def transcribir(file: UploadFile = File(...)):
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    result = transcribe_file(tmp_path)
# limpiar si se desea
    return {"transcripcion": result}