import psutil
import shutil
import os

def get_resource_usage1(label="Snapshot"):
    """Records and prints current RAM and disk usage."""
    # RAM Usage
    process = psutil.Process(os.getpid())
    ram_mb = process.memory_info().rss / (1024 * 1024)  # RSS memory in MB

    # Disk Usage for /content directory
    total, used, free = shutil.disk_usage('/content')
    disk_used_gb = used / (1024**3)  # Convert bytes to GB

    print(f"-- {label} --")
    print(f"RAM Used: {ram_mb:.2f} MB")
    print(f"Disk Used (/content): {disk_used_gb:.2f} GB")
    print("------------------")
    return ram_mb, disk_used_gb


# Initial resource usage measurement
ram1, disk1 = get_resource_usage1("Initial State")

from pydub import AudioSegment
from IPython.display import Audio
import random, os

def load_songs3(folder_name):
    """
    taking songs from the folder and putting them into a dictionary so that they can be easily called
    """
    folder = f"/content/{folder_name}/"

    songs_list = {}

    original_list = list(range(0, 179))
    random_numbers = random.sample(original_list, 100)

    for i, file in enumerate(os.listdir(folder), 1):
        if i in random_numbers:
            if file.endswith(".mp3"):
                songs_list[f"song{i}"] = AudioSegment.from_mp3(os.path.join(folder, file))

    print(f"songs going for mixing have count {len(songs_list)}")
    return songs_list


def mix_songs4(played_chunks, songs, chunk_size=0, folder_name="songs"):
    """
    more randomised mixing, where chunk_size is also randomly chosen between 15,30 seconds
    played_chunks = how many clip/chunk you want connected in the final song
    chunk_size = how many seconds you want per clip/chunk (default is 0, which leads to randomness)
    """
    chunks = []

    for song_id, song in songs.items():
        if chunk_size == 0 or chunk_size >= 4:
            chunk_size = random.randint(15, 30)

        chunks += [(song_id, song[i:i+chunk_size*1000])
                   for i in range(0, len(song), chunk_size*1000)]

    selected = random.sample(chunks, played_chunks)
    result = sum([chunk for song_id, chunk in selected], AudioSegment.empty())
    result.export("random_mix.mp3", format="mp3")
    return Audio("random_mix.mp3")

# first load songs once (reusable), then keep mixing again and again
if 'songs_loaded' not in globals():
    songs_loaded = load_songs3("songs")
    import time

start = time.time()
final_song = mix_songs4(200, songs=songs_loaded)

end=time.time()
print(f"time taken is {round(end-start)} seconds")

final_song

# Measure resource usage after downloading and mixing
ram2, disk2 = get_resource_usage1("After Song Download and Mixing")

