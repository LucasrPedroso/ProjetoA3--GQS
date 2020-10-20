import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDneRY8_Zpez6H_izJ2p8oz6fyStECNz2c",
    "authDomain": "gamerdl.firebaseapp.com",
    "projectId": "gamerdl",
    "storageBucket": "gamerdl.firebasestorage.app",
    "messagingSenderId": "237635781428",
    "appId": "1:237635781428:web:ec6526558f92860e775b61",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
