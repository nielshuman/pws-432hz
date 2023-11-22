import yt_dlp
import pydub
import os

def download_audio(url, output_path):
    # Set options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': output_path,
        'quiet': True,
    }

    # Create yt-dlp instance
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # Download the video
    ydl.download([url])

def trim_and_fade_audio(input_path, output_path, start_time, end_time, fade_duration):
    # Convert start and end times from minutes:seconds string to milliseconds
    start_minutes, start_seconds = map(int, start_time.split(':'))
    end_minutes, end_seconds = map(int, end_time.split(':'))
    start_time_ms = (start_minutes * 60 + start_seconds) * 1000
    end_time_ms = (end_minutes * 60 + end_seconds) * 1000

    # Load the audio file
    audio = pydub.AudioSegment.from_wav(input_path)

    # Trim the audio between start and end times
    trimmed_audio = audio[start_time_ms:end_time_ms]

    # Fade in and out the trimmed audio
    faded_audio = trimmed_audio.fade_in(fade_duration).fade_out(fade_duration)

    # Save the trimmed and faded audio
    faded_audio.export(output_path, format="wav")

def get_video_title(url):
    # Create yt-dlp instance
    ydl = yt_dlp.YoutubeDL({'quiet': True})

    # Extract video info
    info = ydl.extract_info(url, download=False)

    # Get video title
    title = info.get('title')

    # Remove trailing or leading whitespace
    title = title.strip()

    # Remove any illegal characters from the title
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        title = title.replace(char, '')

    # replace ' - ' with '-'
    title = title.replace(' - ', '-')

    # replace spaces with underscores
    title = title.replace(' ', '_')

    # constrain title to 15 characters
    title = title[:20]
    return title

def downloadtrim(output_path, url, start_time="0:00", end_time=None, fade_duration=1000):
    # Download the audio
    download_audio(url, '_temp')

    # If end time is not specified, set end time to start time + 15 seconds
    if end_time is None:
        start_minutes, start_seconds = map(int, start_time.split(':'))
        end_minutes = start_minutes
        end_seconds = start_seconds + 15
        end_time = f"{end_minutes}:{end_seconds}"
    
    # Trim and fade the audio
    trim_and_fade_audio('_temp.wav', output_path, start_time, end_time, fade_duration)
    # Delete the temporary audio file
    os.remove('_temp.wav')

videos = [
    ["https://www.youtube.com/watch?v=NlprozGcs80", "2:06"],
    ['https://www.youtube.com/watch?v=l-dYNttdgl0', '0:01'],
]

# read videos from csv
import csv
with open('videos.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        videos.append(row)

for video in videos:
    # Download and trim the video

    title = get_video_title(video[0])
    # print Downloading video title with progress
    print(f'[{videos.index(video)+1}/{len(videos)}] Downloading {title}...')

    downloadtrim(f"downloads/{title}.wav", *video)
