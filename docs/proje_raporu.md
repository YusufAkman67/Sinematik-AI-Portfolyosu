# Sinematik AI Prompt Portfolyosu ve AI Günlüğü - Proje Raporu

## 1. Proje Özeti ve Amacı
Bu proje, yapay zeka tabanlı görsel üretim araçları (Midjourney, Stable Diffusion, DALL-E vb.) için optimize edilmiş prompt girişlerini ve bunlara bağlı gözlemleri saklamak amacıyla geliştirilmiş ilişkisel bir portfolyo ve günlük uygulamasıdır. Kullanıcıların başarılı görsel girdilerini ve bu girdilere bağlı model davranışlarını sistemli bir şekilde kayıt altında tutmasını sağlar.

## 2. Mimarî Yapı (Application Factory & Blueprints)
Uygulama, Flask topluluğu tarafından önerilen modern ve modüler **Application Factory Pattern** ve **Blueprint** mimarisi ile kurulmuştur:
- **`app/`**: Tüm uygulama dosyalarını barındıran çekirdek klasör.
- **`auth` Blueprint**: Kullanıcı kayıt, giriş ve çıkış işlemlerinin mantıksal katmanı.
- **`main` Blueprint**: Rotaların (Prompt ve Günlük işlemleri) CRUD mantığı, arama, etiket bazlı filtreleme, sayfalama, kullanıcı profili (`/profile/<username>`) ve dış sistemler için `/api/v1/prompts` REST API endpoint süreçleri.
- **`errors` Blueprint**: Uygulama genelinde oluşan 404 (Sayfa Bulunamadı) ve 500 (Sunucu Hatası) hatalarını yakalayan merkezi hata yönetimi katmanı.

## 3. Veritabanı Modelleri ve İlişki Yapıları
Veritabanı ilişkileri modern SQLAlchemy 2.x API (Mapped, mapped_column) stiliyle kodlanmıştır:
- **`User` Modeli**: Kullanıcı kimlik verilerini saklar. `prompts` ve `diary_entries` alanlarıyla ilişkili verileri dinamik olarak yükler. Şifreler `werkzeug.security` aracılığıyla hashlenerek saklanır.
- **`PromptEntry` Modeli**: Başlık, asıl prompt, negatif prompt ve oluşturulma tarihi alanlarını tutar. Yazar (`User`) ve çoka-çok ilişkiyle etiket (`Tag`) modellerine bağlıdır.
- **`Tag` Modeli**: Promptlara eklenen sinematografik meta etiketlerini (örn: `35mm lens`, `cinematic lighting`) temsil eder. Prompt tablosuyla çoka-çok ilişkiye sahiptir. Sorgularda veritabanı optimizasyonu için ilişkili sorgularda `.any()` yapısı kullanılmıştır.
- **`AIDiaryEntry` Modeli**: Görsel üretim deneyimlerini saklar. Bir kullanıcıya aittir ve isteğe bağlı olarak tek bir `PromptEntry` ile ilişkilendirilebilir.
- **Otomatik Etiket Temizliği ve Veritabanı Bakımı**: Siteden bir prompt silindiğinde, ilişkili etiketlerden kimsesiz/sahipsiz (başka hiçbir promptta kullanılmayan) kalanlar SQLAlchemy 2.x sorgulamalarıyla tespit edilerek otomatik ve gerçek zamanlı olarak silinir. Ayrıca veritabanındaki eski veya geçersiz etiketleri (`##night`, `#night` vb.) toplu temizlemek için bağımsız bir `cleanup.py` bakım betiği projeye entegre edilmiştir.

## 4. Tasarım Dili ve Kullanıcı Deneyimi (UI/UX)
- **Tasarım Dili (Slate-900 Glassmorphism):** Arayüzde `Slate-900` (`#090d16` - `#111827`) tonlarında karanlık ve sinematik bir arka plan kullanılmıştır. Kartlar, form alanları ve menüler yarı saydam (`rgba`), ince beyaz sınırlı (`border-color: rgba(255, 255, 255, 0.05)`) ve arka plan bluru (`backdrop-filter: blur(16px)`) içeren **glassmorphism** stiliyle tasarlanmıştır. Indigo ve violet degradeleri ile canlandırılmıştır.
- **Bootstrap 5 & Responsive Yapı:** Hata sayfaları (404 & 500) ve profil sayfası bağımsız ve güvenli şablonlar olarak tasarlanmış olup Bootstrap 5 grid sistemi ve responsive sınıflarından yararlanılmıştır. Tüm portfolyo ekranları mobil, tablet ve masaüstü çözünürlükleriyle tam uyumludur.
- **Tıklanabilir Yazar Profil Bağlantıları:** Anasayfa (`index.html`) ve profil sayfasındaki (`profile.html`) prompt kartlarında yer alan yazar kullanıcı adları, kartın görsel yapısını bozmayacak şekilde tıklanabilir linklere dönüştürülmüş ve yazarın kişisel portfolyosuna yönlendirme sağlanmıştır.
- **Sayfalama (Pagination):** Anasayfada promptların listelendiği alanın altına sayfa numaralarını ve ileri/geri navigasyon butonlarını içeren yarı saydam, glassmorphic sayfalama çubuğu eklenmiştir. Arama ve etiket filtreleri sayfa geçişlerinde URL parametreleri olarak korunmaktadır.
- **Kopyalama Fonksiyonu:** Anasayfa, profil ve detay sayfalarındaki prompt kartlarına eklenen "Kopyala" butonu sayesinde, kullanıcılar orijinal prompt içeriğini tek tıkla panoya kopyalayabilir (başarılı kopyalamada buton yeşile dönüp "Kopyalandı!" uyarısı verir).
- **Profil İstatistikleri (Dashboard):** Kullanıcı profil sayfalarına eklenen özel tasarım istatistik rozeti ile kullanıcının toplamda ürettiği prompt sayısı modern ve görsel bir biçimde listelenir.

## 5. Güvenlik ve Hata Yönetimi
- **Erişim Kontrolleri:** Prompt düzenleme ve silme işlemlerinde, işlem yapan kullanıcının prompt sahibi olup olmadığı kontrol edilerek yetkisiz durumlarda `abort(403)` tetiklenmektedir.
- **İşlem Güvenliği:** 500 sunucu hatası oluştuğunda, yarım kalan veritabanı işlemlerinin veri tutarsızlığına yol açmaması için `db.session.rollback()` çalıştırılarak oturum güvenli bir şekilde sıfırlanmaktadır.

## 6. Test ve Doğrulama Süreçleri
Uygulamada yer alan tüm yetkilendirme sınırları, CRUD operasyonları, arama/filtreleme mantığı, sayfalama süreçleri, profil sayfaları, hata yakalama senaryoları ve REST API süreçleri yazılan **39 adet birim ve entegrasyon testi** (unittest) ile otomatik olarak test edilmektedir.
Testlerin koşturulma komutu:
```powershell
venv\Scripts\python.exe -m unittest discover tests
```
Tüm test senaryoları başarıyla geçmiştir (`OK`).
