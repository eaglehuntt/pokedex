import time
from upload_video import upload_video

print('ENSURE POKEMON IS IN THE DATABASE. IF NOT, RUN MYSQL SCRIPTS TO ADD IT')
dex_num = int(input("Enter Pokedex number: "))
name = str(input("Enter Name: ")).upper()

video_data = {
    "file": "vid.mp4",
    "title": f"It's #Pokemon {dex_num}, #{name}!",
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
