from flask import render_template, flash, redirect, session, url_for, request

#from flask.ext.login import login_user, logout_user, current_user, \
#    login_required

from app import application #, db, lm, oid
from forms import tokenForm, apicForm, subscribe_option
from acitkit import *

from spark import *

application.secret_key = 'huhuhuahuhuehuaheuaehuaheuha'

@application.route('/', methods=['GET','POST'])
@application.route('/index', methods=['GET','POST'])
def index():
    form=tokenForm(request.form)
    if request.method == 'POST' and form.validate():
        user=get_me_name(form.token.data)
        session['usr_displayName'] = user
        session['usr_token'] = form.token.data
        flash('Thanks for your token, lets begin!')
        return redirect(url_for('begin'))
    return render_template('index.html',
                           title='Home',
                           form=form)

@application.route('/begin',methods=['GET','POST'])
def begin():
    apicform = apicForm(request.form)
    if request.method == 'POST' and apicform.validate():
        apicIP=apicform.apicIP.data
        apicAdmin=apicform.apicAdmin.data
        apicPassword=apicform.apicPassword.data

        aci_session = APIC_login_CLI(apicIP,apicAdmin,apicPassword)

        resp = aci_session.login()

        aci_session.close()

        if not resp.ok:
            flash('Something wrong with your login. Are the IP/credentials correct?')
            return redirect(url_for('begin'))


        session['apicIP'] = apicIP
        session['apicAdmin'] = apicAdmin
        session['apicPassword'] = apicPassword

        room_id = createRoom(session['usr_token'])

        session['roomId'] = room_id

        return redirect(url_for('run'))


    return render_template('begin.html',
                           user=session.get('usr_displayName', None),
                           form = apicform)


@application.route('/run', methods=['GET','POST'])
def run():
    aci_session = APIC_login_CLI(session['apicIP'], session['apicAdmin'], session['apicPassword'])
    aci_session.login()

    tenant_list = getAllTenants(aci_session)

    subscribe_form = edit_list(request.form, tenant_list)

    aci_session.close()

    if request.method == 'POST':
        aci_session = APIC_login_CLI(session['apicIP'],session['apicAdmin'],session['apicPassword'])
        aci_session.login()
        APIC_tenant_subscribe(aci_session, session['usr_token'], session['roomId'], subscribe_form.obj_type.data)

    return render_template('run.html',
                            form=subscribe_form)


def edit_list(request, tenant_list):
    form = subscribe_option(request, obj=tenant_list)
    form.obj_type.choices = tenant_list
    return form



#from .forms import LoginForm
# from .models import User


# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))
#
#
# @app.before_request
# def before_request():
#     g.user = current_user
#
#
# @app.route('/')
# @app.route('/index')
# @login_required
# def index():
#     user = g.user
#     posts = [
#         {
#             'author': {'nickname': 'John'},
#             'body': 'Beautiful day in Portland!'
#         },
#         {
#             'author': {'nickname': 'Susan'},
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('index.html',
#                            title='Home',
#                            user=user,
#                            posts=posts)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None and g.user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])
#
#
# @oid.after_login
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email=resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(nickname=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember=remember_me)
#     return redirect(request.args.get('next') or url_for('index'))
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
