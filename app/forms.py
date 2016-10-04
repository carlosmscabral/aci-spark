from wtforms import Form, StringField, PasswordField, validators, SelectField



class tokenForm(Form):
    token = StringField('user_token', [validators.Length(min=64,max=64)])


class apicForm(Form):
    apicIP = StringField('apic_ip', [validators.IPAddress()])
    apicAdmin = StringField('apic_admin', [validators.DataRequired()])
    apicPassword = PasswordField('apic_password', [validators.DataRequired()])


class subscribe_option(Form):
    obj_type = SelectField('obj_subj')


