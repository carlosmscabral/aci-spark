import sys
from  acitoolkit.acitoolkit import *


#Tenant Creation
tenant = Tenant('Matrix')

#My VRF creation, under the Tenant Matrix created above
context= Context('Matrix-Router', tenant)

#My BridgeDomain, under the Context/Tenant created above
bd = BridgeDomain('BD1', tenant)
bd.add_context(context)

#Creation of the AppProfile - Will you take the Red or the Blue pill?
app = AppProfile('RedOrBlueANP', tenant)

#Create the EPG RED and attach it to the BD1
red = EPG('RED', app )
red.add_bd(bd)

#Create the EPG BLUE and attach it to the BD1
blue = EPG('BLUE', app )
blue.add_bd(bd)     


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

# Now we'll actually push what we created.
resp = tenant.push_to_apic(session)
if resp.ok:
    print 'Success'

# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()















