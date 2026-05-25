# Yapay Zeka Geliştirme Günlüğü (AI Log)

Bu günlük, **Sinematik AI Prompt Portfolyosu ve AI Günlüğü** projesinin yapay zeka asistanı yardımıyla sıfırdan geliştirilme sürecindeki tüm adımları, teknik kararları ve test aşamalarını özetlemektedir.

---

## 📅 Adım 1: Proje İskeletinin Kurulması
- Flask 3.x sürümü esas alınarak **Application Factory Pattern** yapısında klasör ve modül hiyerarşisi oluşturuldu.
- Gerekli kütüphaneler (`flask`, `flask-sqlalchemy`, `flask-migrate`, `flask-login`, `flask-wtf`, `python-dotenv`) `requirements.txt` dosyasına eklendi ve sanal ortam kurularak yüklemeler tamamlandı.
- Çevre değişkenlerini yönetmek üzere `.env` ve örnek şablon `.env.example` dosyaları hazırlandı.

## 📅 Adım 2: Veritabanı Modellerinin Tasarımı
- Modern SQLAlchemy 2.0 standartları (Mapped ve mapped_column) kullanılarak modeller kodlandı:
  - **`User`**: `UserMixin` entegreli oturum ve şifre hashleme yetenekleri.
  - **`PromptEntry`**: Asıl prompt ve negatif prompt alanları.
  - **`Tag`**: Çoka-çok (Many-to-Many) ilişki ile promptlara bağlanabilen etiketler.
  - **`AIDiaryEntry`**: Kullanıcının denemelerini tutabileceği ve promptlar ile opsiyonel ilişkilendirebileceği günlük nesnesi.
- Flask-Migrate altyapısı `flask db init` ile kuruldu, `flask db migrate` ile ilk migrasyon dosyası oluşturuldu ve `flask db upgrade` ile SQLite veritabanı şeması başarıyla yaratıldı.

## 📅 Adım 3: Yetkilendirme ve Main Blueprint İşlemleri
- Giriş, kayıt ve çıkış rotaları `app/auth/routes.py` içerisinde güvenli yönlendirme mantığı ile kodlandı.
- Portfolyo arama/filtreleme rotaları, prompt CRUD ve günlük CRUD fonksiyonları `app/main/routes.py` dosyasına yazıldı.
- Prompt formunda virgülle girilen etiketleri tek tek ayıklayarak etiket tablosuyla eşleştiren veritabanı mantığı kuruldu.

## 📅 Adım 4: HTML Şablonları ve Premium Vanilla CSS Geliştirmesi
- `base.html` şablonu ile modern navigasyon, flash bildirim alanları ve responsive mobil hamburger menü entegre edildi.
- Görsel kalitesi yüksek, `Slate-900` arka plana sahip yarı saydam glassmorphism paneller ve neon butonlar vanilla CSS (`style.css`) ile tasarlandı.
- Prompt detay sayfasında prompt metinlerinin tek tıkla kopyalanmasını sağlayan JavaScript kod bloğu yazıldı.

## 📅 Adım 5: Doğrulama, Hata Giderme ve Git Entegrasyonu
- Uygulama sınırlarını ve veri tutarlılığını test eden 31 adet unittest yazıldı (`test_auth.py` ve `test_routes.py`).
- **Sorun Giderme**: WTForms email doğrulaması için gereken ağır `email_validator` bağımlılığı yerine, `forms.py` dosyasına özel ve hafif bir Regex doğrulayıcı eklenerek paket bağımlılıkları temizlendi.
- Yapılan unittest çalıştırmasında 31 testin tamamının başarıyla geçtiği doğrulandı (`OK`).
- Git deposu başlatılarak tüm kodlar ilk commit ile yerel depoya alındı, GitHub uzak sunucusu eklenerek kodlar başarıyla push edildi.
