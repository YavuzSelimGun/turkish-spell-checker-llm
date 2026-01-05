from flask import Flask, render_template, request, jsonify
import os
import sys
from spell_checker.bert_checker import duzelt_cumle

app = Flask(__name__)

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/check_spelling', methods=['POST'])
def check_spelling():
    """Yazım denetimi API endpoint'i"""
    try:
        # JSON verisini al
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Metin verisi bulunamadı'
            }), 400
        
        input_text = data['text'].strip()
        
        if not input_text:
            return jsonify({
                'success': False,
                'error': 'Boş metin gönderildi'
            }), 400
        
        # Yazım denetimi yap
        corrected_text = duzelt_cumle(input_text)
        
        # Sonucu döndür
        return jsonify({
            'success': True,
            'original_text': input_text,
            'corrected_text': corrected_text,
            'has_corrections': input_text != corrected_text
        })
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'İşlem sırasında hata oluştu: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Sistem durumu kontrolü"""
    try:
        # Gerekli dosyaların varlığını kontrol et
        required_files = [
            'spell_checker/bert_checker.py',
            'spell_checker/zemberek-full.jar',
            'spell_checker/ZemberekSpellChecker.class',
            'models/bert-turkish'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            return jsonify({
                'status': 'unhealthy',
                'missing_files': missing_files
            }), 500
        
        return jsonify({
            'status': 'healthy',
            'message': 'Tüm bileşenler hazır'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Geliştirme modunda çalıştır
    app.run(debug=True, host='0.0.0.0', port=5000)