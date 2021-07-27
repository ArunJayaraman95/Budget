import pyrebase
import urllib

firebaseConfig = {
    "apiKey": "AIzaSyB07JiaeBfXONn4Sz4TvdJ4xWQqE3X21D8",
    "authDomain": "budget-software.firebaseapp.com",
    "databaseURL": "https://budget-software-default-rtdb.firebaseio.com/",
    "projectId": "budget-software",
    "storageBucket": "budget-software.appspot.com",
    "messagingSenderId": "124067844106",
    "appId": "1:124067844106:web:ccc1224030c1958a3a8ff3",
    "measurementId": "G-8MHJ83WY4T"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

#Authentication
#Login
# email = input("Enter email: ")
# password = input ("Enter password: ")
# try:
#     auth.sign_in_with_email_and_password(email, password)
#     print("Successfully signed in!")
# except:
#     print("Invalid credentials. Try again.")

# Signup
# email = input("Enter email: ")
# password = input("Enter password: ")
# confirmPassword = input("Re-enter password: ")
# if password == confirmPassword:
#     try:
#         auth.create_user_with_email_and_password(email, password)
#         print("Account made")
#     except:
#         print("Email already exists")
# else:
#   print("Passwords don't match try again")


# Storage
# fileName = input("Enter file name for upload: ")
# cloudFileName = input("Enter cloud file name: ")
# storage.child(cloudFileName).put(fileName)

# Downloading file
# cloudFileName = input("Enter file to download: ")
# storage.child(cloudFileName).download("", "dCars.txt")
# print("Success")
'''
# Reading file
cloudFileName = input("File to download")
url = storage.child(cloudFileName).get_url(None)
f = urllib.request.urlopen(url).read()
print(f)'''

# Database

# Create
#data={'age': 30, 'address':"Detrroit", 'employed': False, 'name': "AJ"}
#db.child("people").child("Arun").set(data)
# use .push instead of .set for unique id cpu generated

# Update
# db.child("people").child("Neal").update({'name': 'Stupid'})

# people = db.child("people").get()
# for person in people.each():
#   # print(person.val())
#   # print(person.key())
#   if person.val()['name'] == 'codol guy':
#     db.child("people").child(person.key()).update({'name': 'dumb guy'})

#Delete
#db.child("people").child("Arun").child('employed').add()

# Read
#people = db.child("people").child("f").get()
# if people: get stuff from people
#print(people.val()['address'])
people = db.child("people").order_by_child("address").equal_to("LAX").get()
for person in people:
  print(person.val())