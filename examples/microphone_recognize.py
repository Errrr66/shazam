# To run this script, ensure you have pyaudio installed:
# pip install pyaudio

import asyncio
import logging
import pyaudio
import wave
import io
from shazamio import Shazam, Serialize

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize Shazam
    shazam = Shazam()

    # Audio recording parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10

    p = pyaudio.PyAudio()

    print(f"Recording for {RECORD_SECONDS} seconds...")

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Finished recording")

        stream.stop_stream()
        stream.close()
        sample_size = p.get_sample_size(FORMAT)

    except Exception as e:
        logger.error(f"Error during recording: {e}")
        p.terminate()
        return

    p.terminate()

    # Create a WAV file in memory
    try:
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(sample_size)
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        audio_bytes = buffer.getvalue()

        print("Recognizing song...")
        # Recognize the song
        out = await shazam.recognize(audio_bytes)

        # Print the result
        print(Serialize.full_track(out))

        # Also print a simplified summary
        if 'track' in out:
            track = out['track']
            title = track.get('title', 'Unknown Title')
            subtitle = track.get('subtitle', 'Unknown Artist')
            print(f"\nFound match: {title} by {subtitle}")
        else:
            print("\nNo match found.")

    except Exception as e:
        logger.error(f"Error during recognition: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())

