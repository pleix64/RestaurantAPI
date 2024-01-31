# Instruction for a few API endpoints:

* /admin/
Admin interface. Only users with staff status can login. 

* /token/login/
Login interface for Token Authentication. 

* /api-auth/login/
Login interface for Session Authentication. To work with it, uncomment the line of 'rest_framework.authentication.SessionAuthentication' within REST_FRAMEWORK in settings.py.
Once logged in with Session Authentication, you may test all API endpoints with DRF Browsable API View on browser. 


* /api/groups/manager/users
* /api/groups/delivery-crew/users
POST
For a manager to add any user to Manager or Delivery Crew group, provide json data as below:
{
    "username": "your_user_name"
}
The user to be added as Manager or Delivery Crew has to be registered before. 


* To place order, first add menu items to cart using:
/api/cart/menu-items

* Once cart items are added, place order at:
/api/orders
with an empty json { }, and with the same user token. 


* Usage of other API endpoints are straighforward. 



# usernames and passwords:

admin
lemon@789!

adrian
ad@lemon789

mario
ma@lemon789

mikasa
mi@lemon123

eren 
you@refr33

jsmith
js@lemon789

jdoe
jd@lemon789

frieren
himmel-yousha

himmel
warrior2023
