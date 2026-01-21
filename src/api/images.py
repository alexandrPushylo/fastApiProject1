import shutil

from fastapi import APIRouter, UploadFile
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post('')
def upload_image(image: UploadFile):
    img_path = f"src/static/images/{image.filename}"
    with open(img_path, "wb+") as image_file:
        shutil.copyfileobj(image.file, image_file)
    resize_image.delay(img_path)