# 🎤 VocalBridge : A Voice Translator App

This Streamlit app allows users to record speech, perform language detection, translate the text into Kannada, analyze the sentiment, identify named entities, and play the translated speech as audio.

## 🙏 Acknowledgements

- **Streamlit**: For providing a simple and fast framework to build data apps. 🌟
- **Google Trans API**: For offering translation capabilities. 🌍
- **spaCy**: For its powerful NLP functionalities. 🤖
- **SpeechRecognition**: For its robust speech-to-text conversion. 🗣️
- **gTTS**: For text-to-speech generation. 🔊
- **pygame**: For audio playback capabilities. 🎵

## 📚 Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Acknowledgements](#acknowledgements)

## Steps taken to complete the project
- Step 1: Recognize Speech
- Step 2: Detect Language
- Step 3: Translate Text
- Step 4: Sentiment Analysis
- Step 5: Named Entity Recognition
- Step 6: Text-to-Speech
- Step 7: Audio Playback
- Step 8: Display Results
- Step 9: Error Handling
- Step 10: Streamlit App
- Step 11: Run

## 🚀 Features

- **Speech Recognition**: Record speech through a microphone and transcribe it to text. 🎙️
- **Language Detection**: Automatically detect the language of the transcribed speech. 🌐
- **Translation**: Translate the detected text to Kannada. 🔄
- **Named Entity Recognition**: Extract entities (such as names, dates, locations) from the text using spaCy. 🏷️
- **Sentiment Analysis**: Analyze the polarity (positive/negative) and subjectivity of the text using TextBlob. 📊
- **Text-to-Speech**: Convert the translated text to speech in Kannada and play it back. 📢
- **Audio Playback**: Plays the audio of the translated text. 🎶

## 🛠️ Technologies Used

This project leverages the following libraries and tools:

- **[Streamlit](https://streamlit.io/)**: To create the user interface for the web app. 🌐
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)**: To capture and recognize speech from the microphone. 🎤
- **[googletrans](https://pypi.org/project/googletrans/)**: For language translation. 🌍
- **[gTTS](https://pypi.org/project/gTTS/)**: To convert text into speech. 🔈
- **[spaCy](https://spacy.io/)**: For Named Entity Recognition (NER). 🧠
- **[langdetect](https://pypi.org/project/langdetect/)**: For detecting the language of the text. 🌐
- **[TextBlob](https://textblob.readthedocs.io/)**: For sentiment analysis. 📝
- **[pygame](https://pypi.org/project/pygame/)**: For audio playback of the translated speech. 🎵

## 🏗️ Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.7+** 🐍
- **pip**: Python package manager. 📦

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/kittu-122/VocalBridge.git
   cd speech-translation-app
   ```

2. Install the required dependencies using `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

3. Download the spaCy language model:

    ```bash
    python -m spacy download en_core_web_sm
    ```

4. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## 🧑‍💻 Usage

- **Recording Speech**: Click the "Record" button to start capturing your speech using the microphone. 🎤
- **Language Detection**: After recording, the app will automatically detect the language of the transcribed text. 🌍
- **Translation**: If the detected language is not Kannada, the app will translate the text to Kannada. 🔄
- **Text-to-Speech**: The translated text is converted to Kannada speech and played back through the app. 🔊
- **Named Entity Recognition**: The app extracts key entities such as names, locations, and dates from the text. 🏷️
- **Sentiment Analysis**: The app provides insights into the emotional tone and subjectivity of the text. 📊

### Additional Dependencies

If you encounter issues during installation, particularly with `pygame`, ensure that the appropriate system libraries are installed. For example, on WINDOWS, you may need to install the following:

```bash
pip install pygame
```

## 📦 Dependencies
- `streamlit`
- `numpy`
- `soundfile`
- `speechrecognition`
- `googletrans==4.0.0-rc1`
- `gtts`
- `langdetect`
- `textblob`
- `spacy`
- `pyaudio`
- `pydub`
- `ffmpeg-python` (optional)

### Key Sections:
- **Features**: Lists the key functionalities of the app.
- **Technologies Used**: Mentions the libraries used.
- **Installation**: Provides step-by-step instructions on how to set up the project.
- **Usage**: Explains how to use the app with a brief walkthrough.
- **Project Structure**: Gives an overview of the app’s file organization.
- **Acknowledgements**: Credits the libraries and tools used.

## Contributing
- We're are open to enhancements & bug-fixes.
- Feel free to add issues and submit patches.

**Thank you for choosing this project. Hoping that this project proves useful and delivers a seamless experience for your needs!**
