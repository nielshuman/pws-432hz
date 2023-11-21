import subprocess, soundfile

def convert_mp3_to_wav(mp3_file, wav_file):
    try:
        subprocess.run(['ffmpeg', '-i', mp3_file, wav_file])
        print(f"Successfully converted {mp3_file} to {wav_file}")
    except Exception as e:
        print(f"Error converting {mp3_file} to {wav_file}: {str(e)}")

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

# # Load the audio data
# audio, sr = soundfile.read('temp_output.wav')
# soundfile.write('example2_pitchshifted.wav', audio, int(sr*(400/440)))

pitch_shift('example2.mp3', 'example2_pitchshifted.mp3', 426/440)