import os
import typing
from tempfile import NamedTemporaryFile

# import cloudinary
import pydantic
import requests
from cloudinary.uploader import upload as cloudinary_upload
from fastapi import FastAPI, HTTPException

from fsvid2vid import inference, output_dir

app = FastAPI()


class TalkingHeadRequest(pydantic.BaseModel):
    driving_video_url: str
    reference_image_url: str


@app.post("/talking_head", response_model=typing.Dict[str, str])
async def talking_head(request: TalkingHeadRequest):
    # Check the content type of the URL before downloading the content
    h = requests.head(request.reference_image_url, allow_redirects=True)
    if "image/jpeg" not in h.headers["Content-Type"]:
        raise HTTPException(400, detail="Invalid file type: expected jpg/jpeg")

    h = requests.head(request.driving_video_url, allow_redirects=True)
    if "video/mp4" not in h.headers["Content-Type"]:
        raise HTTPException(400, detail="Invalid file type: expected mp4")

    # Download and write files to temporary directory
    resp = requests.get(request.reference_image_url)
    with NamedTemporaryFile(delete=False, suffix=".jpg") as image_tmp:
        image_tmp.write(resp.content)

    resp = requests.get(request.driving_video_url)
    with NamedTemporaryFile(delete=False, suffix=".mp4") as video_tmp:
        video_tmp.write(resp.content)

    # Model inference
    inference(image_tmp.name, video_tmp.name)

    # Upload model output
    upload_resp = cloudinary_upload(
        os.path.join(output_dir, "001.mp4"),
        folder="fewshot-vid2vid-outputs",
        resource_type="video",
    )

    return {"output_url": upload_resp["url"]}
