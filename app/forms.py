from wtforms import Form, StringField, validators



class tokenForm(Form):
    token = StringField('user_token', [validators.Length(min=64,max=64)])
