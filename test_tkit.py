from app.acitkit import *

session=APIC_login_CLI("10.97.39.125","admin","1234Qwer")

print session

resp = session.login()

print resp