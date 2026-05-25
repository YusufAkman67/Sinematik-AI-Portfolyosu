# Sinematik AI Prompt Portfolyosu

Bu proje, **Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı** dersi dönem projesi kapsamında geliştirilen bir web uygulamasıdır. Sistem; yapay zeka tabanlı görsel üretim araçları (Midjourney, Stable Diffusion vb.) kullanan tasarımcılar için sinematografik prompt kayıtlarını, lens/ışıklandırma etiketlerini ve görsel üretim günlüklerini yönetmeyi sağlayan bir yönetim panelini oluşturur.

---

## 🚀 Proje Mimarisi: Application Factory Pattern & Blueprints

Proje, Flask topluluğu tarafından önerilen modern ve sürdürülebilir **Application Factory Pattern** (Uygulama Fabrikası Şablonu) ve **Blueprint** (Modüler Yapı) yaklaşımı kullanılarak sıfırdan tasarlanmıştır. Bu yapı projenin ölçeklenebilirliğini artırır ve modüller arasında döngüsel bağımlılıkların oluşmasını engeller.

### Dizin Yapısı
```text
app/
  __init__.py          # Flask Uygulama Fabrikası (create_app) ve eklentilerin başlangıcı
  main/
    __init__.py        # Main Blueprint tanımlaması
    forms.py           # Prompt ve Günlük WTForms sınıfları
    routes.py          # Ana sayfa, prompt/günlük CRUD ve genel rotalar
  auth/
    __init__.py        # Auth Blueprint tanımlaması
    forms.py           # Oturum yönetimi formları
    routes.py          # Giriş/çıkış ve kimlik doğrulama rotaları
  models.py            # Veritabanı modelleri (SQLAlchemy 2.x)
  templates/           # Jinja2 HTML şablonları
  static/              # CSS, JS ve görsel dosyaları
docs/
  yapay_zeka_gunlugu.md # Yapay Zeka Günlüğü (AI Log)
  proje_raporu.md       # Proje Raporu (Project Report)
migrations/            # Flask-Migrate veritabanı şema göç dosyaları
tests/                 # Birim ve entegrasyon testleri
config.py              # Uygulama yapılandırma parametreleri
requirements.txt       # Gerekli Python kütüphaneleri listesi
.env.example           # Örnek çevre değişkenleri şablonu
.env                   # Yerel çevre değişkenleri (Veritabanı URI, Gizli Anahtar vb.)
.gitignore             # Git'e eklenmeyecek dosyalar listesi
run.py                 # Uygulamayı başlatan ana giriş noktası
```

---

## 🛠️ Kullanılan Teknolojiler

Projede sadece aşağıda belirtilen temel kütüphaneler kullanılmıştır:
- **Flask 3.x**: Web uygulama çatısı
- **Flask-SQLAlchemy**: Veritabanı işlemleri ve ORM yönetimi
- **Flask-Migrate**: Veritabanı şeması göç işlemleri
- **Flask-Login**: Kullanıcı giriş/çıkış ve oturum yönetimi
- **Flask-WTF**: Güvenli form işlemleri ve CSRF koruması
- **python-dotenv**: `.env` dosyasındaki çevre değişkenlerinin yönetimi
- **SQLite**: Hafif ve taşınabilir yerel ilişkisel veritabanı

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Projeyi Klonlayın
```powershell
git clone https://github.com/YusufAkman67/sinematik-ai-portfolyosu.git
cd sinematik-ai-portfolyosu
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin
```powershell
# Windows için:
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux için:
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```powershell
pip install -r requirements.txt
```

### 4. Çevre Değişkenlerini Ayarlayın
`.env.example` dosyasının adını `.env` olarak değiştirin veya kopyalayın, ardından içeriğini projenize göre düzenleyin:
```env
SECRET_KEY=dev-secret-key-12345
DATABASE_URL=sqlite:///app_dev.db
FLASK_APP=run.py
FLASK_DEBUG=1
```

### 5. Veritabanı Göçlerini Uygulayın
```powershell
flask db upgrade
```

### 6. Uygulamayı Çalıştırın
```powershell
python run.py
```
Uygulama varsayılan olarak **`http://127.0.0.1:5000`** adresinde çalışmaya başlayacaktır.

---

## 🧪 Testlerin Koşturulması

Uygulamada yer alan tüm testleri çalıştırmak için terminalde şu komutu uygulayınız:
```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests
```
