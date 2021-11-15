import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from fsvid2vid import inference, output_path

app = FastAPI()


@app.post("/talking_head")
def talking_head(files: List[UploadFile] = File(...)):
    # Check number of files uploaded
    if len(files) != 2:
        raise HTTPException(400, detail="Invalid number of files: expected 2 files")

    # Sort files by filename extension
    files = sorted(files, key=lambda f: Path(f.filename).suffix)
    if files[0].content_type != "image/jpeg" or files[1].content_type != "video/mp4":
        raise HTTPException(400, detail="Invalid files types: expected 1 jpg and 1 mp4")

    # Write files to temporary directory
    tmp_filenames = []
    for file in files:
        try:
            suffix = Path(file.filename).suffix
            with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_filenames.append(tmp.name)
        finally:
            file.file.close()

    # Model inference
    inference(*tmp_filenames)

    # https://stackoverflow.com/questions/59760739/how-do-i-return-a-dict-an-image-from-a-fastapi-endpoint
    return {"input_files": [file.filename for file in files]}, FileResponse(
        os.path.join(output_path, "00000.jpg"),
        media_type="video/mp4",
        filename="output.mp4",
    )
