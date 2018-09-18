from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class CreatePostForm(FlaskForm):
    
    # Title Field
    title = StringField(
        'Post Title', 
        validators=[
            DataRequired()
        ]
    )
    
    # Content Field
    content = TextAreaField(
        'Post Content', 
        validators=[
            DataRequired()
        ]
    )
    
    # Submit Field
    submit = SubmitField(
        'Add Post'
    )