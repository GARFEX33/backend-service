import os
from uuid import uuid4
from fastapi import UploadFile

def save_uploaded_file(file: UploadFile, categoria: str) -> str:
    ext = file.filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    directory = f"media/{categoria}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/media/{categoria}/{filename}", filename
