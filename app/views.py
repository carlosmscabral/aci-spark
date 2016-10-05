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
        print "yay2"
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


