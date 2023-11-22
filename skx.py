import subprocess

def speak(text: str):
    try:
        subprocess.run(["espeak", text], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Example usage
text_to_speak = "person indentified"
speak(text_to_speak)

# rasp123