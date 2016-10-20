from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class RestaurantForm(Form):
    name = StringField('Name:',validators=[Required()])
    submit = SubmitField('Submit')

class RestaurantMenuForm(Form):
    name = StringField('Name:', validators=[Required()])
    description = TextAreaField('Description:')
    price = StringField('Price:',validators=[Required()])
    course = StringField('Course:',validators=[Required()])
    submit = SubmitField('Submit')
