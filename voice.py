import subprocess
import shlex


def speak(text):

    # Sanitize quotes for PowerShell invocation
    safe_text = str(text).replace('"', "'")

    command = (
        'Add-Type -AssemblyName System.Speech; '
        "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$speak.SelectVoice('Microsoft Zira Desktop'); "
        f"$speak.Speak(\"{safe_text}\");"
    )

    try:
        subprocess.run(["powershell", "-Command", command], check=True)
    except subprocess.CalledProcessError as e:
        # Fallback: print text if speech failed
        print("(speak failed)", text)