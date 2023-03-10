import mysql.connector
from get_info import *
from upload_video import upload_video
import time
# Connect to local database.

DBHOST = input("Server: ")
DBUSER = input("User: ")
DBPSSWD = input("Password: ")
DB = input("Database: ")


db = mysql.connector.connect(
    host=DBHOST,
    user=DBUSER,
    passwd=DBPSSWD,
    database=DB
)

# Initialize a cursor
cursor = db.cursor()

while True:

    pokemon = valid_dex_to_video(db, cursor)

    video_data = {
        "file": "vid.mp4",
        "title": f"{pokemon}",
        "description": "#shorts\nThis video series turns your subscriptions box into a pokedex! Check back daily for informative videos on all your favorite Pokemon. Subscribe for more! ",
        "keywords": "Pokemon,Pokedex,daily,nintendo,gamefreak,gaming,anime,scarlet,violet",
        "privacyStatus": "public"
    }

    print(video_data["title"])
    print("Posting Video in 1 minute...")
    time.sleep(15)
    print("45 seconds...")
    time.sleep(15)
    print("30 seconds...")
    time.sleep(15)
    print("15 seconds...")
    time.sleep(15)
    upload_video(video_data)
    current_time = date_entered = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Uploaded at {current_time}\n")
    print("Making a new video in 24 hours...")

    time.sleep(60 * 60 * 24 - 1)

db.close()
