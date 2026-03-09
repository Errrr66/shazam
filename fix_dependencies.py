import subprocess
import sys

def install(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    try:
        install("shazamio-core==1.1.2")
        print("Successfully installed shazamio-core==1.1.2")

        # Verify installation
        import shazamio_core
        print(f"shazamio_core version: {getattr(shazamio_core, '__version__', 'unknown')}")
        try:
             from shazamio_core import SearchParams
             print("SearchParams is available.")
        except ImportError:
             print("SearchParams is STILL NOT available.")

    except Exception as e:
        print(f"Failed to install: {e}")

