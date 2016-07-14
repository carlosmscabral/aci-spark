import sys
from  acitoolkit.acitoolkit import *
import os


###################################################################################################
#
#  GLOBAL VARIABLES
#
###################################################################################################

spark_messages = "https://api.ciscospark.com/v1/messages"
access_token = "YmI3MTE1YjItOWVmZS00MDI4LWE2OWEtM2NmNDlmOTI5NjUzMWViNzBkZmItZTcx"
room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vOGFjNmZmNTAtNDliZS0xMWU2LTgyNDgtY2Y4ZDI4MDg3Mzkx"


###################################################################################################
#
#  UTILITY FUNCTIONS
#
###################################################################################################

def write_spark_message(msg_data='test', token=access_token, room=room_id):
    output=os.system('curl ' + str(spark_messages) + ' -X POST -H "Authorization:Bearer ' + str(token) + '" --data "roomId=' + str(room) + '" --data "text=' + msg_data + '"')


def list_ACI_interfaces(session):
    data = []

    interfaces = Interface.get(session)

    for interface in interfaces:
            data.append((interface.attributes['if_name'],
                         interface.attributes['porttype'],
                         interface.attributes['adminstatus'],
                         interface.attributes['operSt'],
                         interface.attributes['speed'],
                         interface.attributes['mtu'],
                         interface.attributes['usage']))

    formated_data = ""
    msg_n=0

    template = "{0:17} {1:6} {2:^6} {3:^6} {4:7} {5:6} {6:9} "
    write_spark_message(template.format("INTERFACE", "TYPE", "ADMIN", "OPER", "SPEED", "MTU", "USAGE"))
    write_spark_message(template.format("---------", "----", "------", "------", "-----", "___", "---------"))

    for rec in data:
        formated_data+=(template.format(*rec))
        formated_data+=("\n")
        msg_n+=1
        if msg_n == 20:
            write_spark_message(formated_data)
            msg_n=0

def APIC_login_CLI():
    # Getting credentials from the command line.
    description = 'VoD application'
    creds = Credentials('apic', description)
    creds.add_argument('--delete', action='store_true',
                   help='Delete the configuration from the APIC')

    args = creds.get()

    # Delete the configuration if desired
    if args.delete:
                tenant.mark_as_deleted()

    # Login to APIC
    session = Session(args.url, args.login, args.password)
    session.login()

    return session





###################################################################################################
#
#  MAIN SECTION
#
###################################################################################################


# Login to the APIC with CLI input
aci_session=APIC_login_CLI()

# List ACI interfaces and send to Spark Room
list_ACI_interfaces(aci_session)









