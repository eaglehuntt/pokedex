from get_info import *
import random

# This file is to make a video without updating database and uploading to YouTube.

pokemon = Pokemon_info(random.randint(1, 900)).dex_to_video()
