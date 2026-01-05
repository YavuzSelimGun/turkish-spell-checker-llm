import os
import subprocess
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

# Modeli yerel dizinden yükle
model_dir = "./models/bert-turkish"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForMaskedLM.from_pretrained(model_dir)
model.eval()

def run_zemberek(cumle):
    """Zemberek ile yazım denetimi yap"""
    # spell_checker klasörünün yolu
    cwd = os.path.join(os.getcwd(), "spell_checker")
    
    # Windows ve Unix için classpath ayarı
    classpath = ".;zemberek-full.jar" if os.name == "nt" else ".:zemberek-full.jar"
    
    # Java komutu
    cmd = ["java", "-cp", classpath, "ZemberekSpellChecker"]
    
    try:
        # Java programını çalıştır
        process = subprocess.run(
            cmd, 
            input=cumle.encode("utf-8"), 
            cwd=cwd, 
            check=True,
            capture_output=True,
            timeout=30  # 30 saniye timeout
        )
        return True
    except subprocess.TimeoutExpired:
        print("Zemberek işlemi zaman aşımına uğradı")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Zemberek hatası: {e}")
        return False
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        return False

def parse_oneriler(filename="spell_checker/oneriler.txt"):
    """Öneri dosyasını parse et"""
    kelime_onerileri = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    hatali, oneriler = line.split(":", 1)
                    kelime_onerileri[hatali] = [o.strip() for o in oneriler.split(",") if o.strip()]
    except FileNotFoundError:
        print(f"Öneri dosyası bulunamadı: {filename}")
    except Exception as e:
        print(f"Öneri dosyası okuma hatası: {e}")
    
    return kelime_onerileri

def bert_mask_predict(masked_sentence, candidates):
    """BERT ile maskelenmiş kelime tahmini"""
    try:
        # Cümleyi tokenize et
        inputs = tokenizer(masked_sentence, return_tensors="pt", max_length=512, truncation=True)
        
        # Mask token pozisyonunu bul
        mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]
        
        if len(mask_token_index) == 0:
            print("Mask token bulunamadı")
            return candidates[0] if candidates else ""
        
        # Model çıkarımı
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
        
        # Mask pozisyonundaki logitleri al
        mask_token_logits = logits[0, mask_token_index[0], :].squeeze()
        
        # Her aday için skor hesapla
        scores = {}
        for candidate in candidates:
            try:
                # Kelimeyi tokenize et
                tokens = tokenizer.tokenize(candidate)
                if tokens:  # Boş token listesi kontrolü
                    token_id = tokenizer.convert_tokens_to_ids(tokens[0])
                    scores[candidate] = mask_token_logits[token_id].item()
                else:
                    scores[candidate] = float('-inf')
            except Exception as e:
                print(f"Token dönüştürme hatası {candidate}: {e}")
                scores[candidate] = float('-inf')
        
        # En yüksek skorlu öneriyi döndür
        if scores:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            return sorted_scores[0][0]
        else:
            return candidates[0] if candidates else ""
            
    except Exception as e:
        print(f"BERT tahmin hatası: {e}")
        return candidates[0] if candidates else ""

def duzelt_cumle(cumle):
    """Ana yazım denetimi fonksiyonu"""
    try:
        # Öneriler dosyasını temizle
        oneriler_dosyasi = "spell_checker/oneriler.txt"
        if os.path.exists(oneriler_dosyasi):
            os.remove(oneriler_dosyasi)
        
        # Java ile önerileri al
        if not run_zemberek(cumle):
            print("Zemberek çalıştırılamadı")
            return cumle
        
        # Hatalı kelime ve önerileri oku
        oneriler = parse_oneriler()
        
        if not oneriler:
            # Hiç öneri yoksa orijinal cümleyi döndür
            return cumle
        
        kelimeler = cumle.split()
        
        # Her kelime için kontrol et
        for i, kelime in enumerate(kelimeler):
            # Noktalama işaretlerini temizle
            temiz_kelime = kelime.strip('.,!?;:"()[]{}')
            
            if temiz_kelime in oneriler and oneriler[temiz_kelime]:
                candidates = oneriler[temiz_kelime]
                
                # Maskelenmiş cümle oluştur
                masked_tokens = kelimeler.copy()
                masked_tokens[i] = tokenizer.mask_token
                masked_sentence = " ".join(masked_tokens)
                
                # BERT ile en iyi öneriyi seç
                best_token = bert_mask_predict(masked_sentence, candidates)
                
                # Orijinal noktalama işaretlerini koru
                if best_token:
                    noktalama = kelime[len(temiz_kelime):]
                    kelimeler[i] = best_token + noktalama
        
        return " ".join(kelimeler)
        
    except Exception as e:
        print(f"Cümle düzeltme hatası: {e}")
        return cumle

# Test için
if __name__ == "__main__":
    girdi = input("Cümle giriniz: ")
    sonuc = duzelt_cumle(girdi)
    print("Düzeltilmiş:", sonuc)