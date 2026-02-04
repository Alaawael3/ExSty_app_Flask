import os
import secrets
from PIL import Image
from Exsty_app import mail
from flask_mail import Message
from flask import current_app
from flask import url_for


def save_picture(form_picture):
    os.makedirs("static/profile_pics", exist_ok=True)

    # random filename
    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )

    # resize (optional but recommended)
    output_size = (740, 740)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "ExStdy app passward reset request",
        sender="lolowaelmo456@gmail.com",
        recipients=[user.email],
        body=f"""to reset the passward, visit this link:
        {url_for("users.reset_passward", token=token, _external=True)}""",
    )
    mail.send(msg)
