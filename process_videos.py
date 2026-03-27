#converts the videos to mp3
# import os
# import subprocess
# file=os.listdir("videoss")
# print(file)
# for files in file:
#   print(files)
# Converts the videos to mp3 
import os
import subprocess

files = os.listdir("videoss")

for file in files:
    if "#" in file:
        tutorial_number = file.split("#")[1].split(".")[0]
    else:
        tutorial_number = "unknown"

    file_name = file.split(".mp4")[0]

    print(tutorial_number, file_name)

    subprocess.run([
        "ffmpeg",
        "-i", f"videoss/{file}",
        f"audios/{tutorial_number}_{file_name}.mp3"
    ])