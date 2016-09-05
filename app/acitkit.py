from  acitoolkit.acitoolkit import *

def APIC_login_CLI(apic_ip, apic_admin, apic_password):
    # Getting credentials from the command line.
    description = 'VoD application'

    url='https://' + str(apic_ip)

    # Login to APIC
    session = Session(url, str(apic_admin), str(apic_password))
    session.login()

    return session