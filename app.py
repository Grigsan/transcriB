import os
import whisper
from flask import Flask, render_template, request, jsonify
import re
# Массив самых частых слов-паразитов и междометий
PARASITE_WORDS = [
    "ээ", "э", "ну", "мм", "м", "аа", "а",
    "типа", "как бы", "это самое", "значит", "вот"
]
def clean_text(text):
    # Remove parasite words, case-insensitive, as separate words
    for w in PARASITE_WORDS:
        text = re.sub(fr'\b{w}\b', '', text, flags=re.IGNORECASE)
    # Remove extra spaces
    text = re.sub(r' +', ' ', text)
    # Удалить слова длиной 1-2 символа (за исключением аббревиатур в верхнем регистре)
    text = ' '.join([word for word in text.split() if len(word.strip()) > 2 or word.isupper()])
    return text.strip()

app = Flask(__name__)

# Конфигурация
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Загружаем модель Whisper
# Доступные модели: "tiny", "base", "small", "medium", "large"
print("Загрузка модели Whisper... Пожалуйста, подождите.")
model = whisper.load_model("small")
print("Модель загружена!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не найден'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        try:
            # fp16=False обеспечивает работу на CPU без ошибок
            result = model.transcribe(filepath, fp16=False)
            text = result['text']
            text = clean_text(text)
            # Удаляем файл после обработки
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'text': text})
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
