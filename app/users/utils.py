import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail, app


def save_picture(form_picture):
    '''
    Function to create a random file name for the image then
    save it in the apps picture dir and return the new file name
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # underscore is for the unused variable (file name) that is returned
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    # resize picture on upload to prevent unnessacary large files
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) # save the picture to the file system
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='charliebickerton@gmail.com', 
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
    '''
    mail.send(msg)