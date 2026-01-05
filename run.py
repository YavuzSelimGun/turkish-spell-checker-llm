#!/usr/bin/env python3
"""
Türkçe Yazım Denetimi Web Uygulaması
BERTurk + Zemberek ile güçlendirilmiş
"""

import os
import sys
from app import app

def check_requirements():
    """Gerekli dosya ve klasörlerin varlığını kontrol et"""
    required_items = [
        'spell_checker/bert_checker.py',
        'spell_checker/zemberek-full.jar',
        'spell_checker/ZemberekSpellChecker.class',
        'models/bert-turkish',
        'templates/index.html'
    ]
    
    missing_items = []
    for item in required_items:
        if not os.path.exists(item):
            missing_items.append(item)
    
    if missing_items:
        print("❌ Eksik dosya/klasörler:")
        for item in missing_items:
            print(f"   - {item}")
        print("\nLütfen eksik dosyaları kontrol edin.")
        return False
    
    print("✅ Tüm gerekli dosyalar mevcut.")
    return True

def main():
    """Ana fonksiyon"""
    print("🇹🇷 Türkçe Yazım Denetimi Uygulaması")
    print("=" * 50)
    
    # Gereksinimler kontrolü
    if not check_requirements():
        sys.exit(1)
    
    print("🚀 Web sunucusu başlatılıyor...")
    print("📍 Uygulama adresi: http://localhost:5000")
    print("🔄 Geliştirme modu aktif (debug=True)")
    print("⏹️  Durdurmak için Ctrl+C")
    print("=" * 50)
    
    try:
        # Flask uygulamasını başlat
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Uygulama kapatılıyor...")
    except Exception as e:
        print(f"❌ Hata: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()