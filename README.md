# Sinematik AI Prompt Portfolyosu ve AI Günlüğü
### İnternet Programcılığı Dersi Proje Raporu ve Kullanım Kılavuzu

Bu proje, yapay zeka tabanlı görsel üretim araçları (Midjourney, Stable Diffusion, DALL-E vb.) kullanan tasarımcılar ve yönetmenler için geliştirilmiş; sinematografik prompt kayıtlarını, lens/ışıklandırma etiketlerini ve görsel üretim günlüklerini yönetmeyi sağlayan **premium bir web uygulamasıdır**.

Uygulama, modern yazılım mimarisi standartlarına uygun olarak **Flask 3.x** framework'ü ile **Application Factory Pattern** ve **Blueprint** mimarisi kullanılarak geliştirilmiştir.

---

## Proje Klasör Yapısı

Proje, modülerliği ve sürdürülebilirliği artırmak amacıyla aşağıdaki şekilde katmanlara ayrılmıştır:

```text
sinematikaiportfolyosu/
│
├── app/                       # Ana uygulama klasörü
│   ├── __init__.py            # Application factory (Uygulama başlatıcı ve eklenti bağlayıcı)
│   ├── models.py              # SQLAlchemy 2.x Veritabanı Modelleri
│   │
│   ├── auth/                  # Oturum yönetimi (Giriş/Kayıt/Çıkış) Blueprint'i
│   │   ├── __init__.py
│   │   ├── forms.py           # WTForms Kayıt ve Giriş Formları
│   │   └── routes.py          # Oturum yönlendirmeleri ve mantığı
│   │
│   ├── main/                  # Prompt ve Günlük İşlemleri Blueprint'i
│   │   ├── __init__.py
│   │   ├── forms.py           # Prompt ve Günlük veri giriş formları
│   │   └── routes.py          # CRUD, Arama, Filtreleme ve detay rotaları
│   │
│   ├── static/                # Statik dosyalar
│   │   └── css/
│   │       └── style.css      # Premium Vanilla CSS Stil Şablonu
│   │
│   └── templates/             # Jinja2 HTML Şablonları
│       ├── base.html          # Ortak iskelet layout (Navbar, Footer, Flash bildirimleri)
│       ├── index.html         # Ana sayfa (Prompt kartları, Arama, Yan menü Tag bulutu)
│       ├── prompt.html        # Prompt detayları, kopyalama butonları ve ilişkili günlükler
│       ├── prompt_form.html   # Prompt ekleme ve düzenleme formu
│       ├── diary.html         # AI Günlük timeline listesi
│       ├── diary_form.html    # Günlük ekleme ve düzenleme arayüzü
│       └── auth/
│           ├── login.html     # Giriş Yap sayfası
│           └── register.html  # Kayıt Ol sayfası
│
├── instance/                  # SQLite veritabanı dosyası konumu
├── migrations/                # Alembic veritabanı migrasyon geçmişi
├── tests/                     # Unittest senaryoları
├── config.py                  # Geliştirme, Test ve Production konfigürasyonları
├── requirements.txt           # Bağımlılık paketleri
├── .env                       # Çevre değişkenleri (Gizli anahtarlar, veritabanı bağlantıları)
└── README.md                  # Proje Raporu (Bu dosya)
```

---

## Veritabanı Mimarisi (Entity-Relationship)

Uygulama, **SQLAlchemy 2.x Mapped/mapped_column** API'si ile tasarlanmış modern bir ilişkisel veritabanı şeması kullanmaktadır. Şema 4 temel tablodan oluşur:

### 1. Tablolar ve Kolonları

| Tablo Adı | Kolonlar | Açıklama |
| :--- | :--- | :--- |
| **`user`** | `id` (PK), `username`, `email`, `password_hash`, `created_at` | Kullanıcı kimlik ve oturum bilgileri. |
| **`prompt_entry`** | `id` (PK), `title`, `original_prompt`, `negative_prompt`, `created_at`, `user_id` (FK) | Sinematografik prompt kayıtları. |
| **`tag`** | `id` (PK), `name` (Unique, Index) | Işıklandırma, lens, çözünürlük gibi meta etiketleri. |
| **`ai_diary_entry`** | `id` (PK), `title`, `content`, `created_at`, `user_id` (FK), `prompt_entry_id` (FK, Nullable) | Görsel üretim süreçlerine dair tutulan kişisel günlük notları. |
| **`prompt_tag`** | `prompt_entry_id` (FK), `tag_id` (FK) | Prompt ve Tag arasındaki Çoka-Çok ilişkiyi kuran ara tablo. |

### 2. İlişki Yapıları (Relationships)
- **Kullanıcı ↔ Prompt (One-to-Many)**: Bir kullanıcı birden fazla prompt ekleyebilir; bir prompt sadece bir yazara aittir (`user.prompts` ↔ `prompt_entry.author`).
- **Kullanıcı ↔ Günlük (One-to-Many)**: Bir kullanıcı birden fazla günlük girdisi yazabilir (`user.diary_entries` ↔ `ai_diary_entry.author`).
- **Prompt ↔ Etiket (Many-to-Many)**: Bir promptun birden fazla etiketi olabilir; bir etiket birden fazla promptta kullanılabilir (`prompt_entry.tags` ↔ `tag.prompts`).
- **Prompt ↔ Günlük (One-to-Many, Opsiyonel)**: Bir günlük girdisi opsiyonel olarak bir prompt kaydı ile ilişkilendirilebilir. Bu sayede üretim sonuçları prompt bazında takip edilebilir (`prompt_entry.diary_entries` ↔ `ai_diary_entry.prompt_entry`).

---

## Öne Çıkan Özellikler

### 🔐 Gelişmiş Kimlik Doğrulama (`auth`)
- **Güvenli Şifreleme**: Şifreler veritabanına asla düz metin olarak kaydedilmez; kayıt anında `werkzeug.security` aracılığıyla hashlenir.
- **E-posta & Kullanıcı Adı ile Giriş**: Formlarda regex tabanlı format doğrulamaları bulunur ve benzersiz kayıt kontrolleri yapılır.
- **Oturum Koruması**: `@login_required` dekoratörü ile yetkisiz kullanıcıların günlük oluşturma veya prompt düzenleme sayfalarına girmesi engellenir.

### 🎬 Prompt Portfolyosu & Akıllı Arama
- **Vaka Duyarsız Arama (Case-Insensitive Search)**: Başlıkta, prompt içeriğinde veya negatif promptta kelime bazlı arama yapabilirsiniz.
- **Etiket Filtreleme**: Ana sayfadaki tag bulutuna veya kartlardaki etiket badge'lerine tıklayarak filtreleme uygulayabilirsiniz.
- **Pano Kopyalama**: Prompt detay sayfasındaki "Kopyala" butonlarına tıklandığında, prompt metni tek tıkla arka planda kopyalanır ve kullanıcıya "Kopyalandı!" animasyonlu bildirimi gösterilir.

### 📝 AI Günlüğü (Gözlem Defteri)
- Kullanıcılar, üretim sırasındaki tohum (seed) değerlerini, render sürelerini, model kıyaslamalarını (örn: Midjourney v5 vs v6) günlük notu olarak yazabilirler.
- Günlük eklenirken, o günlüğün hangi prompt çalışmasına ait olduğu seçim kutusundan (sadece kendi promptları listelenir) ilişkilendirilebilir.
- Başka bir kullanıcının prompt ID'sinin form üzerinden hileyle ilişkilendirilmeye çalışılması backend kontrolü ile engellenir.

### 💎 Premium Arayüz ve CSS Tasarımı
- **Görsel Dil**: Karanlık mod (Dark mode) odaklı, `Slate-900` ve `Slate-800` renk şemaları.
- **Glassmorphism**: Arayüz elementlerinde `backdrop-filter: blur()`, ince saydam sınır çizgileri ve yumuşak neon gölgeler kullanılarak üst segment bir derinlik hissi verilmiştir.
- **Responsive Fluid Grid**: CSS Grid ve esnek Flexbox yapıları sayesinde akıllı telefonlar, tabletler ve bilgisayar ekranlarıyla %100 uyumludur.

---

## Kurulum ve Çalıştırma Adımları

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayınız:

### 1. Gereksinimler
- Bilgisayarınızda **Python 3.12** veya üzeri bir sürümün kurulu olması gerekmektedir.

### 2. Sanal Ortam Oluşturma ve Paketlerin Kurulumu
Proje klasörünün içerisine girip bir terminal açtıktan sonra şu komutları sırasıyla çalıştırın:

```powershell
# 1. Sanal ortamı oluşturun
python -m venv venv

# 2. Sanal ortamı aktif edin (Windows PowerShell için)
.\venv\Scripts\Activate.ps1

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Çevre Değişkenleri (`.env`)
Proje dizininde yer alan `.env` dosyasını kendi ayarlarınıza göre güncelleyin. Örnek şablon `.env.example` dosyasında yer almaktadır:
```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=hard-to-guess-dev-key-12345
DATABASE_URL=sqlite:///app_dev.db
```

### 4. Veritabanı Kurulumu ve Güncelleme
Veritabanı şemasını SQLite üzerine yansıtmak için terminalde şu komutu çalıştırın:
```powershell
flask db upgrade
```
Bu komut, `instance/app_dev.db` veritabanı dosyasını oluşturacak ve şemayı kuracaktır.

### 5. Uygulamayı Çalıştırma
Uygulama sunucusunu ayağa kaldırmak için:
```powershell
flask run
```
Sunucu çalıştıktan sonra tarayıcınızdan **`http://127.0.0.1:5000`** adresine giderek uygulamayı kullanmaya başlayabilirsiniz.

---

## Testlerin Koşturulması

Uygulamada yer alan tüm yetkilendirme, CRUD, arama, filtreleme ve veritabanı ilişki bütünlük kurallarını doğrulamak için yazılmış 31 adet unittest senaryosu bulunmaktadır. Testleri çalıştırmak için terminalde şu komutu uygulayınız:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests
```

**Başarılı Test Çıktısı örneği:**
```text
Ran 31 tests in 12.021s

OK
```

---

## Lisans ve Haklar
Bu proje İnternet Programcılığı Dersi kapsamında bir dönem projesi olarak geliştirilmiştir. Kodların tamamı temiz kod (clean code) prensiplerine ve Flask 3.x standartlarına uygundur.
