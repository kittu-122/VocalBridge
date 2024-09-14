import gradio as gr
import assemblyai as aai
from translate import Translator
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
from pathlib import Path
from pydantic import BaseModel

# Updated list of supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'ur': 'Urdu',
    'ta': 'Tamil',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'pa': 'Punjabi'
}

# Define Gradio audio input component (without 'source' argument)
audio_input = gr.Audio(
    type="filepath",  # Filepath type will store the audio temporarily
    label="Record your voice"
)

# Define Gradio dropdown for selecting input language
input_language_dropdown = gr.Dropdown(
    choices=list(SUPPORTED_LANGUAGES.keys()),  # List of language codes
    label="Select Input Language",
    value=list(SUPPORTED_LANGUAGES.keys())[0]  # Set a valid default
)

class ModelConfig:
    protected_namespaces = ()

class SpeechHistoryItemResponse(BaseModel):
    model_id: str

    class Config(ModelConfig):
        pass

class Model(BaseModel):
    model_id: str

    class Config(ModelConfig):
        pass

def voice_to_voice(audio_file, input_lang_code):
    try:
        # Transcribe the audio file to text
        transcription_response = audio_transcription(audio_file)
        if transcription_response.status == aai.TranscriptStatus.error:
            raise gr.Error(transcription_response.error)
        
        # Extract the transcribed text
        text = transcription_response.text
        
        # Determine target languages based on input language
        target_languages = {code: lang for code, lang in SUPPORTED_LANGUAGES.items() if code != input_lang_code}
        
        # Perform text translation to all target languages
        translations = {code: text_translation(text, input_lang_code, code) for code in target_languages}
        
        # Convert the translated text to speech for each language
        audio_paths = {}
        for code, translation in translations.items():
            try:
                audio_paths[code] = text_to_speech(translation, SUPPORTED_LANGUAGES[code])
            except gr.Error as e:
                audio_paths[code] = f"Error generating speech for {SUPPORTED_LANGUAGES[code]}: {str(e)}"

        # Return the audio paths as a tuple
        return tuple(audio_paths.get(code, "Error") for code in SUPPORTED_LANGUAGES.keys())

    except gr.Error as e:
        print(f"Gradio error: {str(e)}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise gr.Error("An unexpected error occurred during processing.")

# Function to handle audio transcription using AssemblyAI
def audio_transcription(audio_file):
    try:
        aai.settings.api_key = "33454009539c418997079206265147e7"  # Replace with your AssemblyAI API key
        transcriber = aai.Transcriber()
        transcription = transcriber.transcribe(audio_file)
        return transcription
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        raise gr.Error("Failed to transcribe audio.")

# Function to handle text translation using different languages
def text_translation(text, from_lang_code, to_lang_code):
    try:
        translator = Translator(from_lang=from_lang_code, to_lang=to_lang_code)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        raise gr.Error(f"Failed to translate text from {from_lang_code} to {to_lang_code}.")

# Function to handle text-to-speech conversion using ElevenLabs
def text_to_speech(text, language_label):
    try:
        client = ElevenLabs(api_key="sk_1b243082e39c4e2d35b514a91a5dbea0a7147a38797e7755")  # Replace with your ElevenLabs API key

        response = client.text_to_speech.convert(
            voice_id="M91M4GIcfXKgGCdbXQFv",  # Replace with the appropriate voice ID
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",  # Use the multilingual model for other languages
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.8,
                style=0.5,
                use_speaker_boost=True,
            ),
        )

        # Generate a unique file name for the output MP3 file
        save_file_path = f"{language_label}_{uuid.uuid4()}.mp3"

        # Write the audio to a file
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"{save_file_path}: A new audio file was saved successfully!")
        return save_file_path

    except Exception as e:
        error_message = str(e)
        print(f"Text-to-speech error for {language_label}: {error_message}")

        if "quota_exceeded" in error_message.lower():
            return f"Quota exceeded for {language_label}. Please try again later."
        else:
            return f"Failed to convert text to speech for {language_label}."

# Define the Gradio interface
demo = gr.Interface(
    fn=voice_to_voice,
    inputs=[audio_input, input_language_dropdown],
    outputs=[gr.Audio(label=SUPPORTED_LANGUAGES[code] + " Output") for code in SUPPORTED_LANGUAGES.keys()],
    title="Multilingual Voice Translator",
    description="Record your voice in any supported language and translate it into multiple languages."
)

# Run the Gradio app
if __name__ == "__main__":
    demo.launch()
