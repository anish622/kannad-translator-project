from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    english_text = data.get('text', '').strip().lower()  # Normalize input

    # Custom translations for only "good morning" and "good night"
    if english_text == "good morning":
        kannada_text = "ಶುಭೋದಯ"  # Shubhodaya in Kannada
    elif english_text == "good night":
        kannada_text = "ಶುಭ ರಾತ್ರಿ"  # Shubha Ratri in Kannada
    else:
        # Use Google Translator for all other input
        try:
            translated = translator.translate(english_text, src='en', dest='kn')
            kannada_text = translated.text
        except Exception as e:
            return jsonify({'error': 'Translation failed. Please try again.', 'details': str(e)}), 500

    # Generate audio for the Kannada text
    try:
        tts = gTTS(kannada_text, lang='kn')
        audio_file = "output.mp3"
        tts.save(os.path.join('static', audio_file))
    except Exception as e:
        return jsonify({'error': 'Audio generation failed. Please try again.', 'details': str(e)}), 500

    return jsonify({'translatedText': kannada_text, 'audioFile': audio_file})

if __name__ == '__main__':
    app.run(debug=True)
