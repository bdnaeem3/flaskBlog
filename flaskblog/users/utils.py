from flask import url_for
from flaskblog import app, mail
from PIL import Image
from flask_mail import Message
import secrets
import os



def save_image(image):
    random_hex = secrets.token_hex(8)
    _, image_ext = os.path.splitext(image.filename)
    image_name = random_hex + image_ext
    saving_path = os.path.join(app.root_path, 'static/profile_image', image_name)

    output = (125,125)
    i = Image.open(image)
    i.thumbnail(output)

    i.save(saving_path)

    return image_name



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='bdnaeem3@gmail.com', recipients=[user.email])
    msg.body = f'''
        To reset your password, visit the following link:
        {url_for('users.reset_password', token=token, _external=True)}

        If you didn't request this reset. Then just skip this email. Everything will be as before.

        Regards
        Naeem Ahmed
        Someone in Pluto InfoTech
    '''
    mail.send(msg)