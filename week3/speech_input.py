"""
week3/speech_input.py — Smart Farm Speech Input Module (Week 3)
===============================================================
Provides speech-to-text capability for the Smart Farm chatbot
so that farmers can speak their problem instead of typing.

Uses the SpeechRecognition library with Google's Web Speech API
as the primary engine, with a fallback to offline Sphinx recognition.

Course: BIT4133 Natural Language Processing — Week 3
Project: Smart Farm AI Assistant
"""

import sys
import os


def get_speech_input(timeout: int = 5, phrase_limit: int = 10,
                     language: str = "en-US") -> str:
    """
    Listen to the microphone and transcribe speech to text.

    Args:
        timeout      : Seconds to wait for speech to start
        phrase_limit : Maximum seconds of speech to listen for
        language     : BCP-47 language code (default: en-US)

    Returns:
        Transcribed text string, or empty string on failure.
    """
    try:
        import speech_recognition as sr
    except ImportError:
        print("  ⚠  SpeechRecognition not installed.")
        print("     Run: pip install SpeechRecognition pyaudio")
        return ""

    recognizer = sr.Recognizer()

    # Adjust for ambient noise
    print("  🎤 Adjusting for ambient noise — please wait...")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"  🎤 Listening... (speak within {timeout}s)")
            audio = recognizer.listen(source,
                                      timeout=timeout,
                                      phrase_time_limit=phrase_limit)
    except OSError:
        print("  ⚠  No microphone detected or PyAudio not available.")
        print("     Please type your question instead.")
        return ""
    except Exception as e:
        print(f"  ⚠  Microphone error: {e}")
        return ""

    # Try Google Web Speech API first
    print("  🔄 Transcribing...")
    try:
        text = recognizer.recognize_google(audio, language=language)
        print(f"  ✅ Recognised: \"{text}\"")
        return text
    except sr.UnknownValueError:
        print("  ⚠  Could not understand speech. Please try again or type instead.")
    except sr.RequestError as e:
        print(f"  ⚠  Google API unavailable ({e}). Trying offline Sphinx...")

    # Fallback to CMU Sphinx (offline)
    try:
        import pocketsphinx  # noqa: F401
        text = recognizer.recognize_sphinx(audio)
        print(f"  ✅ Recognised (Sphinx): \"{text}\"")
        return text
    except sr.UnknownValueError:
        print("  ⚠  Sphinx could not understand speech.")
    except (sr.RequestError, ImportError):
        print("  ⚠  Sphinx not available. Please type your question.")

    return ""


def check_speech_dependencies() -> bool:
    """
    Check whether SpeechRecognition and PyAudio are available.

    Returns:
        True if both are available, False otherwise.
    """
    sr_ok      = False
    pyaudio_ok = False

    try:
        import speech_recognition  # noqa: F401
        sr_ok = True
    except ImportError:
        pass

    try:
        import pyaudio  # noqa: F401
        pyaudio_ok = True
    except ImportError:
        pass

    return sr_ok and pyaudio_ok


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("   SMART FARM — Speech Input Module Test")
    print("=" * 60)
    print()

    if check_speech_dependencies():
        print("✅ SpeechRecognition and PyAudio are installed.")
        print()
        print("Testing microphone input...")
        print("Please speak a farming problem when prompted.")
        print()
        result = get_speech_input(timeout=6, phrase_limit=12)
        if result:
            print(f"\n📝 Captured text: \"{result}\"")
            print("   This text will be passed to the NLP chatbot pipeline.")
        else:
            print("No speech captured. The chatbot will fall back to text input.")
    else:
        print("⚠  Speech dependencies not fully installed.")
        print("   Install with: pip install SpeechRecognition pyaudio")
        print()
        print("   Note: PyAudio on Windows may require a wheel:")
        print("   pip install pipwin && pipwin install pyaudio")
