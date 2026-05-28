# Sinematik AI Prompt Portfolyosu ve AI Günlüğü - Proje Raporu

## 1. Proje Özeti ve Amacı
Bu proje, yapay zeka tabanlı görsel üretim araçları (Midjourney, Stable Diffusion, DALL-E vb.) için optimize edilmiş prompt girişlerini ve bunlara bağlı gözlemleri saklamak amacıyla geliştirilmiş ilişkisel bir portfolyo ve günlük uygulamasıdır. Projenin temel amacı, kullanıcıların başarılı görsel girdilerini ve bu girdilere bağlı model davranışlarını sistemli bir şekilde kayıt altında tutmasını sağlamaktır.

## 2. Mimarî Yapı (Application Factory & Blueprints)
Uygulama, Flask topluluğu tarafından önerilen modern **Application Factory Pattern** ve **Blueprint** mimarisi ile kurulmuştur:
- **`app/`**: Tüm uygulama dosyalarını barındıran çekirdek klasör.
- **`auth` Blueprint**: Kullanıcı kayıt, giriş ve çıkış işlemlerinin mantıksal katmanı.
- **`main` Blueprint**: Rotaların (Prompt ve Günlük işlemleri) CRUD mantığı, arama ve etiket bazlı filtreleme süreçleri.
- **`models.py`**: SQLite veritabanı şeması ve SQLAlchemy ORM tanımları.

## 3. Veritabanı Modelleri ve İlişki Yapıları
Veritabanı ilişkileri modern SQLAlchemy 2.x API (Mapped, mapped_column) stiliyle kodlanmıştır:

- **`User` Modeli**: Kullanıcı kimlik verilerini saklar. `prompts` ve `diary_entries` alanlarıyla ilişkili verileri dinamik olarak yükler. Şifreler `werkzeug.security` aracılığıyla hashlenerek saklanır.
- **`PromptEntry` Modeli**: Başlık, asıl prompt ve negatif prompt alanlarını tutar. Yazar (`User`) ve çoka-çok ilişkiyle etiket (`Tag`) modellerine bağlıdır.
- **`Tag` Modeli**: Promptlara eklenen sinematografik meta etiketlerini (örn: `35mm lens`, `cinematic lighting`) temsil eder. Prompt tablosuyla çoka-çok ilişkiye sahiptir.
- **`AIDiaryEntry` Modeli**: Görsel üretim deneyimlerini saklar. Bir kullanıcıya aittir ve isteğe bağlı olarak tek bir `PromptEntry` ile ilişkilendirilebilir.

## 4. Kullanıcı Deneyimi ve Arayüz Tasarımı
- **Tasarım Dili**: Slate-900 / dark arka plan üzerine kurulu glassmorphism paneller (yarı saydam border ve arka plan blur) kullanılmıştır.
- **Responsive Arayüz**: Mobil cihazlar, tabletler ve bilgisayarlarla tam uyumlu esnek CSS Grid ve Flexbox yapısı kullanılmıştır.
- **Pano Kopyalama**: Prompt detay sayfasında yer alan "Kopyala" butonları ile metinler tek tıkla panoya kopyalanabilir.
- **Sayfalama (Pagination)**: Anasayfada promptların listelendiği alanın altına sayfa numaralarını ve ileri/geri navigasyon butonlarını içeren yarı saydam, glassmorphic sayfalama çubuğu eklenmiştir. Arama ve etiket filtreleri sayfa geçişlerinde korunmaktadır.

## 5. Test ve Doğrulama Süreçleri
Uygulamada yer alan tüm yetkilendirme sınırları, CRUD operasyonları, arama/filtreleme mantığı ve sayfalama süreçleri yazılan **34 birim test** ile otomatik olarak test edilmektedir.
 Test komutu:
```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests
```
Bütün test senaryoları `OK` durumundadır.
