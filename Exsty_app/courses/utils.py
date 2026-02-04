import os
import secrets
from PIL import Image
from flask import current_app


def save_Course_pic(form_picture):
    os.makedirs("static/Courses", exist_ok=True)

    # random filename
    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.root_path, "static/Courses", picture_fn)

    # resize (optional but recommended)
    output_size = (740, 740)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_fn
