What is it?
 
ACI-Spark is a web-application that can be used by ACI admins to monitor every change in their ACI environment (or for the object they chose to monitor) and get the updates directly in Spark (Web, Mobile...). It leverages Python, Flask (Welcome | Flask (A Python Microframework) ), WTForms (WTForms Documentation ), ACI toolkit (GitHub - datacenter/acitoolkit: A basic toolkit for accessing the Cisco APIC ), Spark APIs (Spark for Developers ) and more.
 
It is available in GitHub (GitHub - carlosmscabral/aci-spark ) and packaged in a container form factor (https://hub.docker.com/r/carlosmscabral/acispark/ ). I am using the auto-build function of DockerHub so To run it, just execute, on a Docker-enabled host:
 
docker pull carlosmscabral/acispark
docker run -itd -p 5000:5000 carlosmscabral/acispark
 
 
Reason for running on a container form-factor is not because this is a "cloud-native", "distributed" application. It is more for packaging/installation convenience, since I had some trouble making sure all libraries/binaries had versions that were all compatible (SSL, ACI Toolkit, virtualenv, Python...).
 
Application is composed of several Python files (for rendering WTForms, Flask views, speaking with Spark, speaking with APIC leveraging the ACI Toolkit) and HTML/CSS files - that is, a traditional Flask setup.
 
This is not intended to be a complete, production grade application but rather a show case of integration and openness of ACI, Spark, their APIs and SDKs, alongside common development tools such as Python, Flask and its components.  It was more of a learning project for me on development, API learning, SDK learning, Container learning and so on.
 
 
 
How does it work?
 
After the application is started, get to your web browser at localhost:5000 (this is the default port for Flask). 
The index page rendered by the Flask view will first ask for your Spark Developer token - which can be retrieved at Spark for Developers . The page is smart enough to validate the input, check the authentication, etc. At this moment, the application will interact with the People Spark API (Spark for Developers People ) to get the user information - aka, "me".
The next screen will ask for APIC information - IP address, admin/password. There is form validation here, as well as APIC credentials validation (leveraging the ACI toolkit Session class). After validation, a Spark Room will be created, named ACI-Spark + a timestamp. Of course, the Room Spark API (Spark for Developers Rooms ) is used, with information retrieved from the user as well.
Assuming everything is fine, ACI-Spark will now get a list of all the current tenants leveraging the ACI Toolkit and display on a drop-list for the use to pick and choose. Basically, this will be the monitored Tenant and its sub-objects on the ACI MIT.
After that, the application enters its main loop - it will subscribe to ACI Object events under the chosen Tenant (using, of course, the APIC subscription features). Every time the application sees an event, it will figure out what is the event class, if it is a creation/deletion, what is the tree structure it belongs and send a message with that info leveraging the Messages Spark API (Spark for Developers Messages ).
 
 
Possible future work?
 
Subscribe to more objects in the Fabric.
Face-lift (maybe using Bootstrap - https://pythonhosted.org/Flask-Bootstrap/ )
Leverage bots / Webhooks (needs NAT config) for actually configuring the ACI Fabric from Spark
Get more granular using the Cobra SDK instead of acitoolkit.
