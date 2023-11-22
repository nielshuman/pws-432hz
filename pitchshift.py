import subprocess, soundfile
audio = []
import os
import yaml

def pitch_shift(input_file, output_file, factor):
    try:
        subprocess.run(
            ['ffmpeg', 
             '-i', input_file, 
             '-af', 'aresample=44100, asetrate={},aresample=44100'.format(factor*44100), 
             output_file])
        print(f"Successfully pitch shifted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error pitch shifting {input_file} to {output_file}: {str(e)}")

for file in os.listdir('downloads'):
    if not file.endswith('.wav'):
        continue
    cat = '440-432'
    title = file[:-4]
    filename_440 = f'audio/440/{file}'
    filename_432 = f'audio/432/{file}'
    pitch_shift(f'downloads/{file}', f'www/{filename_440}', 1)
    pitch_shift(f'downloads/{file}', f'www/{filename_432}', 432/440)
    audio.append({
        'title': title,
        'cat': cat,
        'filename_440': filename_440,
        'filename_432': filename_432
    })
    with open('www/audio.yml', 'w') as outfile:
        yaml.dump(audio, outfile, default_flow_style=False)
    

# pitch_shift('example2.mp3', 'example2_pitchshifted.mp3', 432/440)