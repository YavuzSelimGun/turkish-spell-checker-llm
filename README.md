# Büyük Dil Modelleri ile Türkçe Yazım Düzeltme Aracı

Bu proje, Türkçe diline özgü morfolojik yapı ve bağlamsal özellikler dikkate
alınarak geliştirilen, **hibrit bir yazım düzeltme sistemi**dir.
Çalışma, bir bitirme projesi kapsamında akademik amaçlarla gerçekleştirilmiştir.

Projenin temel motivasyonu, mevcut yazım düzeltme araçlarının Türkçe gibi
morfolojik açıdan zengin dillerde bağlamı yeterince dikkate alamamasıdır.

---

## Problem Tanımı

Türkçe;
- eklemeli (agglutinative) bir dil olması,
- kelime kökü + ek kombinasyonlarının fazlalığı,
- serbest cümle dizilimi

nedeniyle yazım denetimi açısından zorlu bir dildir.

Mevcut araçlar genellikle:
- yalnızca **edit-distance** tabanlı çalışmakta,
- ya da bağlamı dikkate alsa bile Türkçe için yeterli performans gösterememektedir.

---

## Yaklaşım

Bu projede **hibrit bir yazım düzeltme yaklaşımı** benimsenmiştir:

### 1. Zemberek (Kural Tabanlı Katman)
- Türkçe’ye özgü kelime yapısı kullanılarak yazım hataları tespit edilir
- Hatalı kelime için aday düzeltmeler üretilir
- Kelime düzeyinde yüksek doğruluk sağlar ancak bağlamı dikkate almaz

### 2. BERTurk (Bağlamsal Katman)
- Hatalı kelime cümle içinde maskelenir
- Zemberek tarafından önerilen adaylar tek tek denenir
- Maskeli dil modeli üzerinden **bağlamsal olasılık skorları** hesaplanır
- En yüksek skora sahip aday seçilir

Bu iki katman birlikte kullanılarak hem kelime düzeyinde hem bağlamsal olarak
daha tutarlı sonuçlar elde edilmiştir.

---

## Kullanılan Modeller ve Araçlar

### Tokenizasyon Karşılaştırması
- **Zemberek**: Türkçe için en başarılı tokenizasyon
- **BERT / RoBERTa**: İngilizce odaklı, Türkçe için yetersiz
- **BERTurk**: Türkçe verilerle eğitilmiş, ancak tek başına yeterli değil
- **T5**: Seq2Seq yapısı nedeniyle yazım düzeltmede sınırlı

### Yazım Düzeltme Araçları (Benchmark)
| Model | Final Accuracy | Final Error Rate |
|------|----------------|-----------------|
| SymSpell | 0.9719 | 0.0281 |
| JamSpell | 0.6462 | 0.3538 |
| Contextual Spell Check | 0.9598 | 0.0402 |
| Gramformer | 0.9679 | 0.0321 |

SymSpell yüksek doğruluk sağlasa da bağlamı değerlendiremez.
Transformer tabanlı çözümler ise Türkçe için yeterli performans gösterememiştir.

---

## Hibrit Sistem Sonuçları

Hibrit yaklaşım, tekil modellerin zayıf yönlerini dengeleyerek
daha tutarlı sonuçlar üretmiştir.

### Örnek Düzeltmeler
- “Silam güzel ahlaktır” → “İslam güzel ahlaktır”
- “Silam, bugün nasılsın?” → “Selam, bugün nasılsın?”
- “Neden bane inanmıyorsun?” → “Neden bana inanmıyorsun?”
- “buraya geleyor.” → “O buraya geliyor”

---

## Uygulama Yapısı

Bu repository’de:
- NLP pipeline’ı,
- hibrit karar mekanizması,
- deneysel karşılaştırmalar

yer almaktadır.

Önceden eğitilmiş modeller (BERTurk), Zemberek kaynakları ve çalışma ortamı
(virtual environment) **bilinçli olarak repository’ye dahil edilmemiştir**.
Bu proje bir ürün değil, **akademik bir araştırma prototipi** olarak
tasarlanmıştır.

---

## Sonuç ve Gelecek Çalışmalar

Çalışma, Türkçe yazım düzeltme problemlerinde
kural tabanlı ve bağlamsal modellerin birlikte kullanımının
önemli avantajlar sunduğunu göstermektedir.

Gelecek çalışmalarda:
- dilbilgisi (grammar) düzeltimi,
- daha kapsamlı bağlamsal analiz,
- cümle düzeyinde tutarlılık kontrolü

gibi konular ele alınabilir.

