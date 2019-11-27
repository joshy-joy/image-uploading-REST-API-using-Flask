from wtforms import Form, TextAreaField, StringField, PasswordField, validators

class RegisterForm(Form):
    fullname = StringField('Full Name', [validators.Length(min = 1, max = 190)])
    email = StringField('Email', [validators.Length(min = 6, max = 90)])
    username = StringField('User Name', [validators.Length(min = 1, max = 90)])
    password = PasswordField('Password', [
        validators.required(), validators.EqualTo('confirm', message = 'Password Missmatch')
    ])

    confirm = PasswordField('Confirm Password')