from  acitoolkit.acitoolkit import *

from spark import *

import time

def APIC_login_CLI(apic_ip, apic_admin, apic_password):

    # Login to APIC
    session = Session('https://' + str(apic_ip), str(apic_admin), str(apic_password))

    return session



def getAllTenants(session):
    tenants = Tenant.get(session)
    tenant_list = []
    for tenant in tenants:
        tenant_list.append((tenant.name,tenant.name))

    return tenant_list


def APIC_tenant_subscribe(session, token, room_id, tenant_name):


    Tenant.subscribe(session)
    AppProfile.subscribe(session)
    EPG.subscribe(session)
    Endpoint.subscribe(session)

    lastEPG = None

    while True:

        if Tenant.has_events(session):
            event = Tenant.get_event(session)

            if event.name == tenant_name:
                if event.is_deleted():
                    writeMessage(token, room_id, "### Tenant Deleted ###")
                else:
                    writeMessage(token, room_id, "### Tenant Created ###" )

                writeMessage(token, room_id, 'Tn:*' + event.name + '*\n' )


        if AppProfile.has_events(session):
            event = AppProfile.get_event(session)
            tenant = event.get_parent()

            if tenant.name == tenant_name:
                if event.is_deleted():
                    writeMessage(token, room_id, "### App Profile Deleted ###")
                else:
                    writeMessage(token, room_id, "### App Profile Created ###")

                writeMessage(token, room_id, 'Tn:' + tenant.name + '\n =>' + 'AppProfile:*' + event.name + '*\n')

        if EPG.has_events(session):

            event = EPG.get_event(session)
            appProf = event.get_parent()
            tenant = appProf.get_parent()



            if tenant.name == tenant_name:
                if event.is_deleted():
                    writeMessage(token, room_id, "### EPG Removed ###")
                else:
                    if lastEPG != event.name:
                        writeMessage(token, room_id, "### EPG Added ###")
                        writeMessage(token, room_id, 'Tn:' + tenant.name + '\n =>' + 'AppProfile:' + appProf.name + '\n ==>' + 'EPG:*' + event.name + '*\n')
                        lastEPG = event.name
                    else:
                        lastEPG = None


        if Endpoint.has_events(session):
            event = Endpoint.get_event(session)
            epg = event.get_parent()
            appProf = epg.get_parent()
            tenant = appProf.get_parent()

            if tenant.name == tenant_name:
                if event.is_deleted():
                    writeMessage(token, room_id, "### EP Removed ###")
                else:
                    writeMessage(token, room_id, "### EP Attached ###")

                    writeMessage(token, room_id, 'Tn:' + tenant.name + '\n =>' + 'AppProfile:' + appProf.name + '\n ==>' + 'EPG:' + epg.name + '\n ===>' + 'EP:*' + event.name + '*\n')

        time.sleep(0.1)