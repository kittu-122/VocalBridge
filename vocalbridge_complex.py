import os
import numpy as np
import gradio as gr
import assemblyai as aai
from translate import Translator
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pathlib import Path
from pydantic import BaseModel

# Supported languages with full names
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'ur': 'Urdu',
    'ta': 'Tamil',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'ko': 'Korean',
    'es': 'Spanish',
    'tr': 'Turkish',
    'sv': 'Swedish',
    'ru': 'Russian',
    'de': 'German',
    'ja': 'Japanese'
}

class ModelConfig:
    protected_namespaces = ()  # Fix Pydantic warning

class SpeechHistoryItemResponse(BaseModel):
    model_id: str

    class Config(ModelConfig):
        populate_by_name = True

class Model(BaseModel):
    model_id: str

    class Config(ModelConfig):
        populate_by_name = True

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
        markdown_messages = {}
        for code, translation in translations.items():
            try:
                audio_paths[code] = text_to_speech(translation, SUPPORTED_LANGUAGES[code])
                markdown_messages[code] = f"{SUPPORTED_LANGUAGES[code]} translation was successful. Audio file saved."
            except gr.Error as e:
                audio_paths[code] = "Error"
                markdown_messages[code] = f"Error generating speech for {SUPPORTED_LANGUAGES[code]}: {str(e)}"
        
        # Fill in missing languages with "Error"
        for code in SUPPORTED_LANGUAGES.keys():
            if code not in audio_paths:
                audio_paths[code] = "Error"
                markdown_messages[code] = f"No audio for {SUPPORTED_LANGUAGES[code]}"
        
        # Return both the audio paths and markdown messages for each language
        outputs = []
        for code in SUPPORTED_LANGUAGES.keys():
            outputs.append(audio_paths[code])
            outputs.append(markdown_messages[code])
        
        return tuple(outputs)

    except gr.Error as e:
        print(f"Gradio error: {str(e)}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise gr.Error("An unexpected error occurred during processing.")

# Function to handle audio transcription using AssemblyAI
def audio_transcription(audio_file):
    try:
        aai.settings.api_key = "your_assemblyai_api_key"  # Replace with your AssemblyAI API key
        transcriber = aai.Transcriber()
        transcription = transcriber.transcribe(audio_file)
        return transcription
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        raise gr.Error("Failed to transcribe audio.")

# Function to handle text translation
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
        client = ElevenLabs(api_key="your_elevenlabs_api_key")  # Replace with your ElevenLabs API key

        response = client.text_to_speech.convert(
            voice_id="your_voice_id",  # Replace with the appropriate voice ID
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

# Define the Gradio interface with 3 translations per row
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🌍 VocalBridge</h1>")
    gr.Markdown("<h3 style='text-align: center;'>Record or Upload your voice and receive voice translations in multiple languages.</h3>")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                show_download_button=True,
                label="🎙️ Record or Upload Voice",
                waveform_options=gr.WaveformOptions(
                    waveform_color="#01C6FF",
                    waveform_progress_color="#0066B4",
                    skip_length=2,
                    show_controls=False,
                )
            )
            input_lang_code = gr.Dropdown(
                choices=[(code, f"{lang} ({code})") for code, lang in SUPPORTED_LANGUAGES.items()],
                label="Select Input Language",
                value="en"
            )

            # Place Translate and Clear buttons below the audio input
            with gr.Row(equal_height=True):
                submit = gr.Button("Translate 🎧", variant="primary")
                clear_btn = gr.ClearButton(audio_input, "Clear")

    # Display outputs in a grid of 3 languages per row
    output_components = []
    languages = list(SUPPORTED_LANGUAGES.items())
    for i in range(0, len(languages), 3):
        with gr.Row():  # Create a row for every 3 languages
            for code, lang in languages[i:i+3]:  # Iterate over 3 languages at a time
                with gr.Column():
                    output_components.append(gr.Audio(label=f"{lang} Output", interactive=False, waveform_options=gr.WaveformOptions(
                        waveform_color="#01C6FF",
                        waveform_progress_color="#0066B4",
                        skip_length=2,
                        show_controls=False,
                    )))
                    output_components.append(gr.Markdown())

    # Connect the submit button to the voice_to_voice function
    submit.click(fn=voice_to_voice, inputs=[audio_input, input_lang_code], outputs=output_components, show_progress=True)

# Run the Gradio app
if __name__ == "__main__":
    demo.launch()
