import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyB07JiaeBfXONn4Sz4TvdJ4xWQqE3X21D8",
    "authDomain": "budget-software.firebaseapp.com",
    "databaseURL": "",
    "projectId": "budget-software",
    "storageBucket": "budget-software.appspot.com",
    "messagingSenderId": "124067844106",
    "appId": "1:124067844106:web:ccc1224030c1958a3a8ff3",
    "measurementId": "G-8MHJ83WY4T"
}

firebase = pyrebase.initialize_app(firebaseConfig)

# db = firebase.database()
# auth = firebase.auth()
storage = firebase.storage()

# Authentication
# Login
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
#     except:
#         print("Email already exists")

# Storage
# fileName = input("Enter file name for upload: ")
# cloudFileName = input("Enter cloud file name: ")
# storage.child(cloudFileName).put(fileName)

cloudFileName = input("Enter file to download: ")
storage.child(cloudFileName).download("", "dCars.txt")
print("Success")