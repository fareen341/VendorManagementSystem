# VendorManagementSystem

# Using Git
Git clone the repository: https://github.com/fareen341/VendorManagementSystem.git
<b>Create virtual env and install requirements:</b>
<pre>python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
</pre>

# Using Docker
if you have docker just pull and run using below command:
<pre>
docker pull fareen341/vendor-management
docker run -d -p 8000:8000 fareen341/vendor-management
  
application will start running at: "http://0.0.0.0:8000/"
</pre>

<b>UI to login credentials:</b>
username = admin
pswd = admin

<b>After login create a token for admin user.</b>
In postman authenticate using API Key: 
key: Authorization
Value: Token <generated_token>
