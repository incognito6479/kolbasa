from datetime import datetime

import pyrebase

from outlay.models import Outlay


def checking_for_geolocation():
    outlay_model = Outlay.objects.select_related('building', 'building__supplier').get(pk=outlay_id)
    config = {
        "apiKey": "AIzaSyBa6FMte1g2_363ugaIo_eFNBhTIdyyTWQ",
        "authDomain": "kolbasa-4f744.firebaseapp.com",
        "databaseURL": "https://kolbasa-4f744-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "kolbasa-4f744",
        "storageBucket": "kolbasa-4f744.appspot.com",
        "messagingSenderId": "356758906555",
        "appId": "1:356758906555:web:eee62c6621b87cd187ab9e",
        "measurementId": "G-XEQ3WR82YW"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    db.child("users").stream(checking_for_geolocation_handler)


def checking_for_geolocation_handler(massage):
    data = massage['data']
