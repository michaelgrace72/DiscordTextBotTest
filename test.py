import subprocess

def check_ffmpeg_audio():
    try:
        # Define the command to play a short audio file
        command = [
            'ffmpeg',
            '-i', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            '-f', 'null', '-'  # Output to null to avoid creating an actual file
        ]
        
        # Run the command
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        # If the command runs successfully, FFmpeg can play audio
        print("FFmpeg can play audio.")
        return True
    except subprocess.CalledProcessError as e:
        # If an error occurs, print the error message
        print("Error occurred while trying to play audio with FFmpeg:", e.stderr.decode('utf-8'))
        return False

# Check if FFmpeg can play audio
check_ffmpeg_audio()
