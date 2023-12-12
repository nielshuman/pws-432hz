import subprocess, soundfile
audio = []
import os
import yaml, random
def pitch_shift(input_file, output_file, factor):
    try:
        subprocess.call(
            ['ffmpeg', 
             '-i', input_file, 
             '-af', 'aresample=44100, asetrate={},aresample=44100'.format(factor*44100), 
             output_file])

        print(f"Successfully pitch shifted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error pitch shifting {input_file} to {output_file}: {str(e)}")

os.makedirs('www/audio/432', exist_ok=True)
os.makedirs('www/audio/440', exist_ok=True)
os.makedirs('www/audio/448', exist_ok=True)

def shift_and_add(files, original, target):
    for file in files:
        if not file.endswith('.wav'):
            continue

        cat = f'{original}-{target}'
        title = file[:-4]
        if file.startswith('J'):
            cat2 = 'Jazz'
            title = title[1:]
        else:
            cat2 = 'Classical'
        filename_a = f'audio/{original}/{title}.mp3'
        filename_b = f'audio/{target}/{title}.mp3'
        if not os.path.exists(f'www/{filename_a}'):
            pitch_shift(f'downloads/{file}', f'www/{filename_a}', 1)
        pitch_shift(f'downloads/{file}', f'www/{filename_b}', (target/original)**2)
        a = {'filename': filename_a, 'cat': f'{original}'}
        b = {'filename': filename_b, 'cat': f'{target}'}
            # 50% chance to swap a and b
        if random.random() < 0.5:
            a, b = b, a
        audio.append({
            'title': title,
            'cat': cat,
            'cat2': cat2,
            'a': a,
            'b': b
        })

        # print(audio)
        with open('www/audio.yml', 'w') as outfile:
            yaml.dump(audio, outfile, default_flow_style=False)

    
shift_and_add(os.listdir('downloads'), 440, 448)
shift_and_add(os.listdir('downloads'), 440, 432)

# pitch_shift('example2.mp3', 'example2_pitchshifted.mp3', 432/440)