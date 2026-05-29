# Sinematik AI Prompt Portfolyosu ve AI Günlüğü

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

Bu proje, **Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı** dersi dönem projesi kapsamında geliştirilen bir web uygulamasıdır. Yapay zeka tabanlı görsel üretim araçları (Midjourney, Stable Diffusion vb.) kullanan tasarımcılar ve yönetmenler için sinematografik prompt kayıtlarını, lens/ışıklandırma etiketlerini ve görsel üretim günlüklerini yönetmeyi sağlayan premium bir yönetim panelidir.

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
  errors/
    __init__.py        # Hata Yönetimi Blueprint tanımlaması
    handlers.py        # 404 ve 500 merkezi hata yakalayıcılar
  models.py            # Veritabanı modelleri (SQLAlchemy 2.x - Mapped)
  templates/           # Jinja2 HTML şablonları
    errors/            # 404 ve 500 hata sayfaları (Bootstrap 5)
  static/              # CSS, JS ve görsel dosyaları
docs/
  yapay_zeka_gunlugu.md # Yapay Zeka Günlüğü (AI Log)
  proje_raporu.md       # Proje Raporu (Project Report)
migrations/            # Flask-Migrate veritabanı şema göç dosyaları
tests/                 # Birim ve entegrasyon testleri (36 test)
config.py              # Uygulama yapılandırma parametreleri
requirements.txt       # Gerekli Python kütüphaneleri listesi
.env.example           # Örnek çevre değişkenleri şablonu
.env                   # Yerel çevre değişkenleri (Veritabanı URI, Gizli Anahtar vb.)
run.py                 # Uygulamayı başlatan ana giriş noktası
```

---

## 🛠️ Kullanılan Teknolojiler

Projede sadece aşağıda belirtilen temel kütüphaneler kullanılmıştır:
- **Flask 3.x**: Web uygulama çatısı
- **Flask-SQLAlchemy**: Veritabanı işlemleri ve modern ORM (SQLAlchemy 2.x) yönetimi
- **Flask-Migrate**: Veritabanı şeması göç işlemleri
- **Flask-Login**: Kullanıcı giriş/çıkış ve oturum yönetimi
- **Flask-WTF**: Güvenli form işlemleri ve CSRF koruması
- **python-dotenv**: `.env` dosyasındaki çevre değişkenlerinin yönetimi
- **SQLite**: Hafif ve taşınabilir yerel ilişkisel veritabanı
- **Bootstrap 5**: Hata sayfalarının (404/500) responsive ve şık tasarımı için

---

## ⚙️ Kurulum ve Yerelde Çalıştırma

Projeyi yerel bilgisayarınızda ayağa kaldırmak için aşağıdaki adımları sırasıyla uygulayın:

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/YusufAkman67/sinematik-ai-portfolyosu.git
cd sinematik-ai-portfolyosu
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin
```powershell
# Windows için (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux için:
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Çevre Değişkenlerini Ayarlayın
`.env.example` dosyasının bir kopyasını oluşturup adını `.env` olarak değiştirin ve içeriğini düzenleyin:
```env
SECRET_KEY=dev-secret-key-12345
DATABASE_URL=sqlite:///app_dev.db
FLASK_APP=run.py
FLASK_DEBUG=1
```

### 5. Veritabanını Yapılandırın ve Göçleri Uygulayın
Veritabanı şemasını oluşturmak veya en güncel sürüme yükseltmek için:
```bash
flask db upgrade
```

### 6. Uygulamayı Başlatın
```bash
flask run
```
Uygulama varsayılan olarak **`http://127.0.0.1:5000`** adresinde çalışmaya başlayacaktır. Tarayıcınızda bu adresi açarak uygulamayı kullanabilirsiniz.

---

## 🧪 Testlerin Koşturulması

Uygulamada yer alan tüm birim ve entegrasyon testlerini (toplam 36 adet) koşturmak için terminalde şu komutu çalıştırınız:
```bash
venv\Scripts\python.exe -m unittest discover tests
```
Tüm testler hatasız bir şekilde (`OK`) tamamlanmaktadır.
