import requests as rq
import random
import pyttsx3
import re
from moviepy.editor import *
import time

# Main Pokemon class. This contains all relevant information and functions to construct a video


class Pokemon_info:

    def __init__(self, dex_num):
        self.pokemon = self.get_pokemon(dex_num)
        self.species = self.get_species(self.pokemon)
        self.dex_num = dex_num
        self.name = self.get_name(self.pokemon)
        self.type = self.get_type(self.pokemon)
        self.LegMythBby = self.get_LegMythBby(self.species)
        self.native_region = self.get_native_region(self.dex_num)
        self.native_region_tts = self.get_native_region_tts(self.native_region)
        self.pre_flavor_text = self.get_flavor_text(self.species)
        self.flavor_text_version = self.get_flavor_text_version(
            self.species, self.pre_flavor_text)
        self.flavor_text = self.clean_flavor_text(
            self.pre_flavor_text)
        self.sprite = self.pokemon["sprites"]["front_default"]
        self.base_stats = self.get_base_stats(self.pokemon)
        self.highest_stat = self.get_highest_stat(self.base_stats)
        self.total_base_stats = self.get_total_base_stats(self.base_stats)
        self.capture_rate = self.get_capture_rate(self.species)
        self.egg_group = self.get_egg_group(self.species)
        self.evolves_from = self.get_evolves_from(self.species)
        self.evolution_status = self.get_evolution_status(self.evolves_from)
        # Average Pokemon base stats, depending on their evolution status
        # Data from https://pokemon.fandom.com/wiki/Statistics
        self.global_avg_stage1_stats = {
            "hp": 68,
            "attack": 75,
            "defense": 73,
            "special-attack": 69,
            "special-defense": 69,
            "speed": 66,
            "total": 420
        }
        self.global_avg_evolved_stats = {
            "hp": 80,
            "attack": 90,
            "defense": 83,
            "special-attack": 83,
            "special-defense": 83,
            "speed": 78,
            "total": 497
        }
        self.script = self.info_to_script()
        self.flavor_text_display = self.get_flavor_text_display()
        self.base_stats_vs_average = self.get_base_stats_vs_average()
        self.video_title = f"It's #Pokemon {self.dex_num}, #{self.name}!"

    def __repr__(self):
        return (self.script)

    def get_pokemon(self, dex_num):
        pokemon = rq.get(f"https://pokeapi.co/api/v2/pokemon/{dex_num}").json()
        return pokemon

    def get_species(self, pokemon):
        species = rq.get(pokemon["species"]["url"]).json()
        return species

    def get_name(self, pokemon):
        return pokemon["name"].upper()

    def get_base_stats(self, pokemon):
        # Logic to get base stat data and return it as a dictionary
        stats_info_array = pokemon["stats"]
        pokemon_base_stats = {}

        for stat_ht in stats_info_array:
            pokemon_base_stats[stat_ht["stat"]["name"]] = stat_ht["base_stat"]

        return pokemon_base_stats

    def get_total_base_stats(self, base_stats):
        totaler = []

        for stat in base_stats.values():
            totaler.append(stat)

        return sum(totaler)

    def get_native_region(self, dex_num):

        if dex_num <= 151:
            native_region = "Kanto"
        elif dex_num <= 251:
            native_region = "Johto"
        elif dex_num <= 386:
            native_region = "Hoenn"
        elif dex_num <= 493:
            native_region = "Sinnoh"
        elif dex_num <= 649:
            native_region = "Unova"
        elif dex_num <= 721:
            native_region = "Kalos"
        elif dex_num <= 807:
            native_region = "Alola"
        elif dex_num == 808:
            native_region = "Go"
        elif dex_num == 809:
            native_region = "Go"
        elif dex_num <= 905:
            native_region = "Galar"
        else:
            "unknown"
        return native_region

    def get_native_region_tts(self, native_region):
        tts = {
            "Kanto": "KANTO",
            "Johto": "JOHTO",
            "Hoenn": "HO-AN",
            "Sinnoh": "SINNOH",
            "Unova": "YUNAVA",
            "Kalos": "KA-LOS",
            "Alola": "ALOLA",
            "Galar": "GAHLOR",
            "Hisui": "HISUEE",
            "unknown": "PALDAYA"
        }

        return tts[native_region]

    def get_LegMythBby(self, species):
        # Determine if Pokemon is legendary, mythical, or baby
        if species["is_legendary"] == True:
            pokemon_LegMythBby = "legendary"

        elif species["is_baby"] == True:
            pokemon_LegMythBby = "baby"

        elif species["is_mythical"] == True:
            pokemon_LegMythBby = "mythical"
        else:
            pokemon_LegMythBby = ""

        return pokemon_LegMythBby

    def get_type(self, pokemon):
        # Logic to check if pokemon is single or dual type
        if len(pokemon["types"]) > 1:
            type1 = pokemon["types"][0]["type"]["name"]
            type2 = pokemon["types"][1]["type"]["name"]
            pokemon_type = [type1, type2]
        else:
            pokemon_type = [pokemon["types"][0]["type"]["name"]]

        return pokemon_type

    def get_flavor_text(self, species):
        # Logic that determines if flavor text language is English, then randomly selects an entry
        check = 0
        flavor_text = species["flavor_text_entries"]
        possible_entries = []

        for entry in flavor_text:
            if flavor_text[check]["language"]["name"] == "en":
                possible_entries.append(flavor_text[check]["flavor_text"])
                check += 1
            else:
                check += 1

        text = random.choice(possible_entries)
        return text

    def clean_flavor_text(self, text):

        # Clearing out characters that will mess up text to speech
        pokemon_flavor_text = text.replace('é', 'e')
        pokemon_flavor_text = pokemon_flavor_text.replace('.', '. ')
        pokemon_flavor_text = pokemon_flavor_text.replace('\xad', ' ')
        pokemon_flavor_text = pokemon_flavor_text.replace('\n', ' ')
        pokemon_flavor_text = pokemon_flavor_text.replace('\x0c', ' ')
        pokemon_flavor_text = pokemon_flavor_text.replace("'", '')
        return pokemon_flavor_text

    def get_flavor_text_version(self, species, text):

        flavor_text = species["flavor_text_entries"]
        version_checker = 0
        for entry in flavor_text:
            if flavor_text[version_checker]["flavor_text"] == text:
                flavor_text_version = flavor_text[version_checker]["version"]["name"].upper(
                )
            else:
                version_checker += 1

        return flavor_text_version

    def get_capture_rate(self, species):
        return species['capture_rate']

    def get_egg_group(self, species):
        # Logic to interpret egg group info
        pokemon_egg_group = []

        all_groups = species['egg_groups']
        if all_groups[0]['name'] == 'no-eggs':
            pokemon_egg_group.append('')
        else:
            for egg_group in all_groups:
                pokemon_egg_group.append(egg_group['name'])

        return pokemon_egg_group

    def get_evolves_from(self, species):

        # Determine if pokemon evolves:
        if species['evolves_from_species'] is not None:
            pokemon_evolves_from = species['evolves_from_species']['name'].upper(
            )
        else:
            pokemon_evolves_from = None

        return pokemon_evolves_from

    def get_evolution_status(self, pokemon_evolves_from):
        # Logic to determine if pokemon has an evolution line
        if pokemon_evolves_from is not None:
            pokemon_evolution_status = "evolved"
        else:
            pokemon_evolution_status = "stage1"
        return pokemon_evolution_status

    def get_highest_stat(self, base_stats):

        # Set an array to hold an stat of 0
        highest_stat = [0]

        # Iterate over pokemon's base stat values and if the value is greater than the stat in array,
        # clear the array and append the new greatest stat
        for stat in (sorted(self.base_stats.values())):
            if stat > highest_stat[0]:
                highest_stat.clear()
                highest_stat.append(stat)
            elif stat == highest_stat[0]:
                highest_stat.append(stat)

        # If the pokemon only has 1 highest stat, return the stat in a hashtable
        if len(highest_stat) == 1:
            highest_stat = list(base_stats.keys())[list(
                base_stats.values()).index(highest_stat[0])]
            return {base_stats[highest_stat]: [highest_stat]}

        else:
            # Else that means that the pokemon's shares multiple highest stats.
            # Create a hashtable and append all the stats that share a value

            stat_ht = {}
            for stat, value in base_stats.items():
                stat_ht.setdefault(value, []).append(stat)

            # Return a new hashtable, this time as {highest stat value : shared stat names}
            highest_stat = highest_stat[0]
            return {highest_stat: stat_ht[highest_stat]}

    def info_to_script(self):

        # Import the API data and dynamically generate an intro script suitable for all pokemon

        # {}, the {{} and} {} type pokemon
        # intro = f"{name}, the "
        intro = f"Number {self.dex_num}, {self.name}. This "

        if len(self.type) == 1:
            type = f" {self.type[0]} type pokemon"
        else:
            type = (
                f" {self.type[0]} and {self.type[1]} type pokemon")

        # was first seen in {} region.
        if self.native_region == "unkown":
            native_region = f" has just been discovered recently!"
        elif self.native_region == "Go":
            native_region = f" was first documented by real world trainers in Pokemon Go."
        else:
            native_region = f" was first seen in the {self.native_region_tts} region."

        # if evolved:
            # {} evolves from {}
        if self.evolves_from is not None:
            evolution = f" {self.name} evolves from {self.evolves_from}."
        else:
            evolution = ""

        # {}'s pokedex states {}
        flavor_text_version = (
            f" {self.flavor_text_version} version's pokedex states: ")

        flavor_text = (f"{self.flavor_text}")

        # Analyze the top 2 stats

        # {}'s catch rate is {}, and
        catch_rate = f" {self.name}'s catch rate is {self.capture_rate}, and"

        # Determine script for the egg group.
        if self.egg_group == ["ditto"]:
            egg_group = f" has the niche ability to breed with every egg group. Pokemon trainers that are serious about competitive battling often use {self.name} to pass down desired traits."
        elif self.LegMythBby == 'baby':
            egg_group = f" is a baby pokemon. Its egg group is unknown until it's older."
        elif len(self.egg_group) == 1 and self.egg_group != ['']:
            egg_group = f" belongs to the {self.egg_group[0]} egg group."
        elif len(self.egg_group) > 1:
            egg_group = f" belongs to the {self.egg_group[0]} and {self.egg_group[1]} egg groups."
        else:
            egg_group = f" has no known egg group."

        # Get name and value of highest stat(s)
        for keys, value in self.highest_stat.items():
            highest_stat_name = value
        for keys, value in self.highest_stat.items():
            highest_stat_value = keys

        # {}'s base stat total is {}
        intro_to_stats = f" {self.name}'s base stat total is {self.total_base_stats},"

        if len(highest_stat_name) == 1:
            highest_stat_names = highest_stat_name[0]
            display_stats = f" with its highest stat in {highest_stat_name[0]} at {highest_stat_value}."

        elif len(highest_stat_name) == 2:
            highest_stat_names = " and ".join(highest_stat_name)
            display_stats = f" with its highest stats {highest_stat_names} tied at {highest_stat_value}."

        elif len(highest_stat_name) == 6:
            highest_stat_names = "base stats all tied at"
            display_stats = f" with all its base stats tied at {highest_stat_value}."

        else:
            highest_stat_names = ", ".join(highest_stat_name)
            display_stats = f" with its highest stats {highest_stat_names} all tied at {highest_stat_value}."

        if self.evolution_status == "evolved" or self.evolution_status != "evolved" and self.LegMythBby == 'legendary' or self.evolution_status != "evolved" and self.LegMythBby == 'mythical':

            # Determine evolution status and display analysis accordingly.
            old = self.global_avg_evolved_stats['total']
            new = self.total_base_stats

            # if base stat total is greater than the average, calculate the percentage increase
            if new >= old:
                change = self.find_increase(old, new)
                more_or_less = "more"
            # Else if base stat total is less than the average, calculate the percentage decrease
            elif new < old:
                change = self.find_decrease(old, new)
                more_or_less = "less"

            old = self.global_avg_evolved_stats[highest_stat_name[0]]
            new = highest_stat_value

            if new >= old:
                highest_stat_change = self.find_increase(old, new)
                highest_stat_more_or_less = "more"

            elif new < old:
                highest_stat_change = self.find_decrease(old, new)
                highest_stat_more_or_less = "less"
        # 's
            intro_analysis = f" This puts {self.name}'s base stat total approximately  {change}% {more_or_less} than the average fully evolved Pokemon, and its {highest_stat_names} approximately  {highest_stat_change}% {highest_stat_more_or_less} than the average fully evolved Pokemon."

        else:

            old = self.global_avg_stage1_stats['total']
            new = self.total_base_stats

            if new >= old:
                change = self.find_increase(old, new)
                more_or_less = "more"

            elif new < old:
                change = self.find_decrease(old, new)
                more_or_less = "less"

            old = self.global_avg_stage1_stats[highest_stat_name[0]]
            new = highest_stat_value

            if new >= old:
                highest_stat_change = self.find_increase(old, new)
                highest_stat_more_or_less = "more"

            elif new < old:
                highest_stat_change = self.find_decrease(old, new)
                highest_stat_more_or_less = "less"

            # 's
            intro_analysis = f" This puts {self.name}'s base stat total approximately  {change}% {more_or_less} than the average basic Pokemon, and its {highest_stat_names} approximately {highest_stat_change}% {highest_stat_more_or_less} than the average stage 1 Pokemon."

        return "".join(intro + self.LegMythBby + type + native_region + evolution +
                       flavor_text_version + flavor_text + catch_rate +
                       egg_group + intro_to_stats + display_stats + intro_analysis)

        # .join could be slower

    def find_increase(self, old, new):
        return round(((new-old)/old) * 100)

    def find_decrease(self, old, new):
        return round(((old-new)/old) * 100)

    def txt_to_speech(self):
        engine = pyttsx3.init()
        # rate = engine.getProperty('rate')
        engine.setProperty('rate', 210)
        engine.save_to_file(self.script, 'script.mp3')
        engine.runAndWait()

    def get_flavor_text_display(self):
        n = 60
        return '- \n'.join(re.findall('.{1,%i}' % n, self.flavor_text))

    def get_base_stats_vs_average(self):
        if self.evolution_status == "evolved":
            if self.total_base_stats >= self.global_avg_evolved_stats['total']:
                return "above"
            else:
                return "below"
        else:
            if self.total_base_stats >= self.global_avg_stage1_stats['total']:
                return "above"
            else:
                return "below"

    def dex_to_video(self):

        # Call text to speech function. This saves it as an mp3 file
        self.txt_to_speech()

        # Import the mp3
        script = AudioFileClip('script.mp3')
        script_len = script.duration + 0.7

        # Before making video, print dex number and name
        print(self.dex_num, self.name)

        # Place relevent information onto the video in correct locations
        # ------------------------------------------------------------------------
        dex_num = TextClip(f"#{str(self.dex_num)}.", color='black', font='Bauhaus-93',
                           fontsize=32, ).set_position((550, 295))

        name = TextClip(self.name, color='black', font='Bauhaus-93',
                        fontsize=32, ).set_position((640, 295))

        # Display native region
        native_region = TextClip(self.native_region.upper(), color='white', font='Bauhaus-93',
                                 fontsize=32, ).set_position((550, 353))

        # Display stats
        if self.base_stats_vs_average == "above":
            base_stats_vs_avg = ImageClip('above.png')
            base_stats_vs_avg = base_stats_vs_avg.set_position(
                (840, 580)).resize((20, 40))
        else:
            base_stats_vs_avg = ImageClip('below.png')
            base_stats_vs_avg = base_stats_vs_avg.set_position(
                (840, 580)).resize((35, 40))

        hp = TextClip(f"{str(self.base_stats['hp'])}", color='black', font='Bauhaus-93',
                      fontsize=32, ).set_position((880, 400))

        attack = TextClip(f"{str(self.base_stats['attack'])}", color='black', font='Bauhaus-93',
                          fontsize=32, ).set_position((880, 430))

        defense = TextClip(f"{str(self.base_stats['defense'])}", color='black', font='Bauhaus-93',
                           fontsize=32, ).set_position((880, 460))

        special_attack = TextClip(f"{str(self.base_stats['special-attack'])}", color='black', font='Bauhaus-93',
                                  fontsize=32, ).set_position((880, 490))

        special_defense = TextClip(f"{str(self.base_stats['special-defense'])}", color='black', font='Bauhaus-93',
                                   fontsize=32, ).set_position((880, 520))

        speed = TextClip(f"{str(self.base_stats['speed'])}", color='black', font='Bauhaus-93',
                         fontsize=32, ).set_position((880, 550))

        base_stat_total = TextClip(f"{str(self.total_base_stats)}", color='black', font='Bauhaus-93',
                                   fontsize=32, ).set_position((880, 580))

        sprite = ImageClip(self.sprite).set_position(
            (100, 400)).resize((400, 400))

        if self.egg_group == ['']:
            egg = "UNKOWN"
        else:
            egg = " / ".join(self.egg_group)

        egg_group = TextClip(f"{str(egg)}", color='black', font='Bauhaus-93',
                             fontsize=32, ).set_position((580, 735))

        catch_rate = TextClip(f"{str(self.capture_rate)}", color='black', font='Bauhaus-93',
                              fontsize=32, ).set_position((580, 650))

        typing = " / ".join(self.type)
        typing = TextClip(f"{str(typing)}", color='black', font='Bauhaus-93',
                          fontsize=32, ).set_position((580, 870))

        flavor_text = TextClip(f"{str(self.flavor_text_display)}", color='white', font='Bauhaus-93',
                               fontsize=32, ).set_position((100, 1000))
        # ------------------------------------------------------------------------
        # Import the background video
        bg_video = VideoFileClip("bg_dex_entry.mp4")

        dex_entry = CompositeVideoClip(
            [bg_video, sprite, dex_num, name, native_region, hp, attack, defense, special_attack, special_defense, speed, base_stat_total, catch_rate, typing, egg_group, flavor_text, base_stats_vs_avg]).set_duration(script_len).set_audio(script)

        intro = VideoFileClip("intro.mp4")
        outro = VideoFileClip("outro.mp4")
        # Combine intro with dex entry
        final_clip = concatenate_videoclips([intro, dex_entry, outro])

        # Render the final video
        final_clip.write_videofile("vid.mp4")


# Functions to validate if video has already been created

def initialize_pokemon(dex_num):
    return Pokemon_info(dex_num)


def initialize_dex():
    return random.randint(1, 900)


def validate_res(dex_num, cursor):

    cursor.execute(
        "SELECT * FROM videos WHERE EXISTS (SELECT * FROM videos WHERE dex_num=%s)", (dex_num,))

    rows = cursor.fetchall()

    for row in rows:
        if dex_num == row[1]:
            print(f"{dex_num} is already in database. Retrying...")
            return False

    return True


def valid_dex_to_video(db, cursor):
    dex_num = initialize_dex()
    valid = validate_res(dex_num, cursor)

    # Continue to initialize new Pokemon until entry is valid
    while valid == False:
        dex_num = initialize_dex()
        valid = validate_res(dex_num, cursor)

    pokemon = initialize_pokemon(dex_num)

    pokemon.dex_to_video()

    print("\nvideo created!")

    date_entered = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO videos (name, dex_num, date_entered) VALUES (%s, %s, %s)", (
            pokemon.name, pokemon.dex_num, date_entered))

    db.commit()

    print(f"{pokemon.name} added to database.")

    return pokemon.video_title
