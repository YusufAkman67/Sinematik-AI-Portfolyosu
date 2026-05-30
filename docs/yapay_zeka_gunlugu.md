# Yapay Zeka Geliştirme Günlüğü (AI Log)

Bu günlük, **Sinematik AI Prompt Portfolyosu ve AI Günlüğü** projesinin geliştirilme sürecinde, kullanıcının (öğrencinin) yapay zeka asistanını (AI Agent) nasıl yönlendirdiğini, modern standartları nasıl dikte ettiğini ve mimari disiplini nasıl sağladığını gösteren teknik bir seyir defteridir.

---

## 👨‍💻 Kullanıcı Müdahaleleri ve Kritik Oturumlar

Aşağıda, kullanıcının projeyi şekillendiren ve AI asistanının eski/yanlış kod yazma alışkanlıklarını kırarak modern standartları zorunlu kıldığı kritik oturumlar listelenmiştir:

### 📅 Oturum 1 — 26 Mayıs 2026 — 14:00 - 15:30

- **Hedef:** Projenin temel veritabanı mimarisini kurmak ve AI ajanı ile çalışma prensiplerimi (vibe coding kısıtlarını) belirlemek.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Gemini 3 Pro | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "Veritabanı modellerini (PromptEntry, User, Tag) oluştur. Eski Flask-SQLAlchemy sorguları (Model.query) kullanmak KESİNLİKLE YASAKTIR. Modern SQLAlchemy 2.x standardını (db.session.execute, select) kullan."
- **Ajanın Önerdiği Plan:** Ajan, veritabanı tablolarını oluşturmak için bir plan sundu ancak ilk denemesinde alışkanlık olarak eski `.query` yapısını kullanmaya meyilliydi.  
  `[Ekran görüntüsü eklenecek: docs/img/oturum-1-plan.png]`
- **Plan'da Sorguladıklarım:** Eski Flask-SQLAlchemy kullanımına karşı çıktım çünkü dersin rubriğinde modern standartlar ve sürdürülebilir kod mimarisi isteniyordu. Ajanın planını reddedip 2.x standardında ısrar ettim.
- **Üretilen Kodda Düzelttiklerim:** Sadece [models.py](file:///c:/Users/user/OneDrive/Masaüstü/sinematikaiportfolyosu/app/models.py) üretilirken araya girip, ajan kodu tam yazmadan 2.x kısıtlamasını tekrar hatırlattım.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Eski dökümanlardan kaynaklı `User.query.filter_by` kullanımı gelmesi.
  - **Çözüm:** Promptlara "Strictly SQLAlchemy 2.x" kuralını ekleyerek ajanı doğru yola soktum.
- **Bu Oturumdan Öğrendiğim:** Yapay zeka ajanlarının varsayılan olarak eski (StackOverflow gibi eski tarihli) verilerle eğitildiği için eski kod kalıplarını yazmaya meyilli olduğunu, kaliteli bir mimari için ajana baştan katı kurallar (sistem promptları/kısıtlar) koymam gerektiğini öğrendim.
- **Sonraki Oturum İçin Notlar:** Formlar ve Rotalar ([routes.py](file:///c:/Users/user/OneDrive/Masaüstü/sinematikaiportfolyosu/app/main/routes.py)) yazılırken işleri küçük parçalara (commitlere) bölerek ilerlemeliyim.

---

### 📅 Oturum 2 — 27 Mayıs 2026 — 11:30 - 13:00

- **Hedef:** Oluşturulan promptları düzenleme ve silme işlevlerini eklemek, daha da önemlisi başkalarının promptlarını silmeyi engelleyecek güvenlik (yetki) kontrollerini kurmak.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Claude Sonnet 4.6 | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "Kullanıcıların promptları düzenlemesi ve silmesi için /edit ve /delete rotalarını yaz. KRİTİK: Her iki rotada da prompt.user_id ile current_user.id eşleşmiyorsa abort(403) ile yetkisiz erişim hatası döndür."
- **Ajanın Önerdiği Plan:** Ajan rotaları oluşturdu ve yetki denetimini plana başarıyla dahil etti. Eski rotaların kırılmaması için geri dönük uyumluluk önerdi.  
  `[Ekran görüntüsü eklenecek: docs/img/oturum-2-yetki-plani.png]`
- **Plan'da Sorguladıklarım:** Ajanın planını dikkatle inceledim çünkü güvenlik açığı projenin kalitesini doğrudan etkiler. Planın içinde `abort(403)` adımını net olarak gördüğüm için ekstra bir müdahaleye gerek duymadan onayladım.
- **Üretilen Kodda Düzelttiklerim:** [create_prompt.html](file:///c:/Users/user/OneDrive/Masaüstü/sinematikaiportfolyosu/app/templates/main/create_prompt.html) dosyasında düzenleme moduna geçildiğinde sayfa başlığının dinamik (`{% if is_edit %}`) değişmesi kodunu başarılı bulup aynen bıraktım.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Çoka-çok (Many-to-Many) etiket kaydederken eski etiketlerin temizlenmemesi riski.
  - **Çözüm:** Ajana formdan gelen etiketleri `strip()` ile temizleyip veritabanında var olup olmadığını kontrol ettirerek ilişki kurdurdum.
- **Bu Oturumdan Öğrendiğim:** Güvenlik adımlarının (Authentication ve Authorization) ajana bırakılamayacak kadar kritik olduğunu, prompt yazarken "sadece sil" demek yerine "yetkisi varsa sil" mantığını doğrudan benim dikte etmem gerektiğini tecrübe ettim.
- **Sonraki Oturum İçin Notlar:** Sayfalama (Pagination) eklenecek, UI tarafında kart tasarımı iyileştirilecek.

---

### 📅 Oturum 3 — 28 Mayıs 2026 — 14:00 - 15:30

- **Hedef:** Anasayfaya +3 bonus puanlık "Arama" (Search) özelliğini eklemek ve veritabanı performansını optimize etmek için etiketleri (Tag) filtrelemek.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Gemini 3 Pro | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "Sayfalama (Pagination) ekle. Arama ve etiket filtreleme yapıldığında URL parametrelerinin (q ve tag) 2. sayfaya geçerken kaybolmaması için koruma ekle."
  > 
  > "Etiket filtrelemesi yaparken iki ayrı sorgu atma, SQLAlchemy .any() fonksiyonunu kullanarak tek sorguda (EXISTS) işi bitir."
- **Ajanın Önerdiği Plan:** Ajan, hem büyük/küçük harf duyarsız arama için `ilike` kullandı hem de etiket filtresi için `.any()` optimizasyonunu plana dahil etti. URL'deki `q` parametresini sayfalama linklerinde korudu.  
  `[Ekran görüntüsü eklenecek: docs/img/oturum-3-arama-pagination.png]`
- **Plan'da Sorguladıklarım:** Sayfalar arası geçişte arama kelimesinin sıfırlanması çok yaygın bir hatadır. Ajanın HTML tarafında `url_for('main.index', page=..., q=q, tag=tag_name)` yazarak bu parametreleri koruyup korumadığını özellikle kontrol ettim.
- **Üretilen Kodda Düzelttiklerim:** Jinja2 şablonundaki değişken çakışmalarını önlemek için etiket parametresini `tag_name` olarak izole ettik.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Yok. Ajan `.any()` yapısını kusursuz kurdu.
  - **Çözüm:** -
- **Bu Oturumdan Öğrendiğim:** Yapay zeka ile kod yazarken sadece özelliğin "çalışması" değil, "nasıl çalıştığı" da önemlidir. Ajanın veritabanını yoracak N+1 veya çift sorgu mantığı yerine, `.any()` gibi optimize edilmiş ORM standartlarına yönlendirilmesinin performansa ciddi katkı sağladığını öğrendim.

---

### 📅 Oturum 4 — 29 Mayıs 2026 — 12:00 - 13:30

- **Hedef:** Kullanıcı deneyimini (UX) artırmak için özel 404/500 hata sayfaları eklemek ve kullanıcılara kendi promptlarını sergileyebilecekleri herkese açık bir Profil (Portfolyo) sayfası oluşturmak.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Claude Sonnet 4.6 | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "404 ve 500 hatalarını yakalamak için errors adında yeni bir blueprint oluştur ve sinematik tasarımlı hata sayfaları (html) ekle."
  > 
  > "Kullanıcıların promptlarını sergileyecekleri /profile/<username> rotasını ekle ve anasayfadaki kartlarda yazan kullanıcı isimlerini bu profile giden tıklanabilir linklere dönüştür."
- **Ajanın Önerdiği Plan:** Ajan, hata yönetimini ana koddan ayırıp merkezi bir errors blueprint'i kurmayı önerdi. Profil sayfası için de anasayfadaki kart tasarımının birebir aynısını kullanarak görsel bütünlüğü sağladı.
- **Plan'da Sorguladıklarım:** Başlangıçta profil rotası kurulmuştu ancak anasayfadan bu profillere yönlendirme yoktu. UX (Kullanıcı Deneyimi) açısından bu eksikliği fark ettim ve ajanın planına müdahale ederek anasayfadaki yazar isimlerini `href` ile tıklanabilir hale getirmesini talep ettim.
- **Üretilen Kodda Düzelttiklerim:** [index.html](file:///c:/Users/user/OneDrive/Masaüstü/sinematikaiportfolyosu/app/templates/main/index.html) içinde, yazar adının (`prompt.author.username`) düz metin olmaktan çıkarılıp `url_for('main.profile', username=prompt.author.username)` ile sarılmasını sağladım.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Kullanıcıların profillerini manuel olarak URL'ye yazarak bulmak zorunda kalması (Kötü UX).
  - **Çözüm:** Anasayfadaki yazar isimlerinin altı çizgisiz (`text-decoration-none`) şık linklere dönüştürülerek kullanıcılar arası navigasyonun sağlanması.
- **Bu Oturumdan Öğrendiğim:** İyi bir yazılımın sadece arka planda tıkır tıkır çalışan kodlardan ibaret olmadığını; arayüzdeki ufak bir tıklanabilir linkin (UX dokunuşunun) uygulamanın "amatör bir ödev" ile "profesyonel bir ürün" arasındaki farkı belirlediğini tecrübe ettim. Ayrıca hata sayfalarının ayrı bir Blueprint ile yönetilmesinin kod okunabilirliğine büyük katkısı olduğunu gördüm.
- **Sonraki Oturum İçin Notlar:** PROJE TAMAMLANDI. Tüm dokümantasyon (README, Rapor ve AI Günlüğü) güncellenerek son commit atıldı ve GitHub'a push'landı.

---

### 📅 Oturum 5 — 30 Mayıs 2026 — 12:00 - 12:10

- **Hedef:** Kullanıcı deneyimini (UX) artırmak için prompt metinlerini tek tıkla kopyalayabilen bir buton eklemek.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Gemini 3.5 Flash | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "app/templates/main/index.html ve (varsa) profile.html içindeki prompt kartlarının sağ alt köşesine küçük, şık bir "Kopyala" butonu (veya kopyalama ikonu) ekle. Butona tıklandığında Vanilla JavaScript kullanarak prompt.original_prompt metnini kullanıcının panosuna kopyala. Kopyalama başarılı olduğunda butonun metni 2 saniyeliğine 'Kopyalandı!' olarak değişsin, sonra eski haline dönsün."
- **Ajanın Önerdiği Plan:** Ajan, kopyalama işlemini global olarak yönetmek için [base.html](file:///c:/Users/user/OneDrive/Masaüstü/sinematikaiportfolyosu/app/templates/base.html) içine tek bir JavaScript fonksiyonu eklemeyi, kartların içine ise görünmez `.prompt-text-source` konteynerları yerleştirmeyi önerdi.
- **Plan'da Sorguladıklarım:** Kopyalanan promptların kısaltılmış (`truncate(160)`) versiyonu yerine orijinal uzun halinin kopyalanmasını garanti altına almak için `prompt.original_prompt` verisini sayfada güvenli bir hidden div'de saklama yaklaşımını özellikle kontrol ettim ve onayladım.
- **Üretilen Kodda Düzelttiklerim:** Başarılı kopyalama sonrasında butona eklenen `.copied` sınıfının Vanilla CSS ile yeşil renk ve hafif bir parlama efektiyle modern bir glassmorphism animasyonuna sahip olmasını sağladım.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Çift tırnak içeren promptların HTML data niteliklerine yazıldığında HTML etiket yapısını kırması riski.
  - **Çözüm:** Prompt metnini veri öznitelikleri (`data-prompt`) yerine, kart içerisinde `style="display: none;"` olan görünmez bir div içinde tutarak HTML parsing hatalarını tamamen engelledim.
- **Bu Oturumdan Öğrendiğim:** Kullanıcıların sıkça yapacağı "kopyala-yapıştır" işlemini kolaylaştırmanın ürünü çok daha profesyonel hissettirdiğini gördüm. Ayrıca, kod tekrarlarını önlemek amacıyla bu tür global etkileşimlerin ortak bir base şablonda tekilleştirilmesinin mimari sürdürülebilirliğe katkısını pekiştirdim.

---

### 📅 Oturum 6 — 30 Mayıs 2026 — 12:10 - 12:20

- **Hedef:** Kullanıcının profil sayfasının üst kısmına, üretkenliğini gösteren ufak bir istatistik paneli (dashboard) eklemek.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Gemini 3.5 Flash | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "app/main/routes.py içindeki profile rotasında, bu kullanıcının toplam kaç prompt ürettiğini SQLAlchemy 2.x standardı ile say (db.session.scalar(select(func.count()).select_from(PromptEntry).where(...))). app/templates/main/profile.html sayfasında, kullanıcının adının hemen altına şık Bootstrap 5 Badge'leri veya ufak kartlar kullanarak bu istatistiği yaz (Örn: "Toplam Üretim: 12 Prompt")."
- **Ajanın Önerdiği Plan:** Ajan, `sqlalchemy` modülünden `func` yapısını kullanarak modern bir count sorgusu oluşturmayı ve elde edilen değeri şablona aktarmayı önerdi. Arayüz tarafında ise harici Bootstrap bağımlılığı olmadan, uygulamanın kendi Vanilla CSS tasarım sistemine entegre edilmiş şık ve glassmorphic bir rozet tasarladı.
- **Plan'da Sorguladıklarım:** Profil sayfasının responsive yapısının ve genel görünümünün bozulmaması için rozetin konumlandırılacağı yeri ve yerel CSS değişkenlerinin (`--accent-primary`, `--success` vb.) uyumluluğunu kontrol ettim.
- **Üretilen Kodda Düzelttiklerim:** Eklenen istatistik rozetinin sol tarafına SVG tabanlı bir döküman ikonu yerleştirerek görsel zenginliği artırdım. Ayrıca test suite içerisine bu istatistiğin doğru şekilde sorgulanıp gösterildiğini doğrulayan yeni bir assertion eklettim.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Projede genel olarak Bootstrap CSS kütüphanesinin (hata sayfaları hariç) yüklü olmaması sebebiyle saf Bootstrap badge sınıflarının profil sayfasında stilize edilmeden ham görünmesi riski.
  - **Çözüm:** `style.css` dosyasına `.stats-badge` adında özel bir glassmorphic stil kuralı ekleyerek Bootstrap stil kısıtını tamamen aştım ve görsel bütünlüğü korudum.
- **Bu Oturumdan Öğrendiğim:** Basit okuma (SELECT) operasyonlarının bile SQLAlchemy 2.x standartlarına göre titizlikle yazılması gerektiğini, projedeki kütüphane kısıtlarına göre (harici kütüphane/Bootstrap bağımlılığı olmadan) Vanilla CSS ile esnek çözümler üretmenin önemini tecrübe ettim.

---

### 📅 Oturum 7 — 30 Mayıs 2026 — 12:20 - 12:30

- **Hedef:** Dış sistemlerin verilerimizi okuyabilmesi için son eklenen 10 promptu JSON formatında döndüren bir REST API endpoint'i eklemek.
- **Kullandığım Mod ve Model:** Mod: Plan | Model: Gemini 3.5 Flash | Görünüm: Manager View
- **Verdiğim Promptlar:**
  > "app/main/routes.py içine /api/v1/prompts rotasını (sadece GET metodu) ekle. Veritabanındaki en yeni 10 PromptEntry kaydını çek (SQLAlchemy 2.x ile). Bu kayıtların id, title, original_prompt, author ve tags alanlarını bir Python sözlüğüne dönüştür. Bu veriyi jsonify() kullanarak JSON formatında döndür."
- **Ajanın Önerdiği Plan:** Ajan, `flask` modülünden `jsonify` kullanarak yeni bir rota tanımlamayı, bu rotada SQLAlchemy 2.x standardı ile en yeni 10 promptu sorgulamayı ve bunları uygun JSON yapısıyla dışa aktarmayı önerdi.
- **Plan'da Sorguladıklarım:** API rotasının güvenli olması, sadece GET isteklerine cevap vermesi ve JSON çıktısında yazar adının (`username`) ve ilişkili etiketlerin doğru biçimde serileştirildiğinden emin olmak için planı denetledim.
- **Üretilen Kodda Düzelttiklerim:** Rota için sıfırdan `tests/test_api.py` adında bir test modülü yazdırarak, API yanıtının durum kodunu (200 OK), içerik türünü (`application/json`) ve veri uzunluğunu/formatını test kapsamına eklettim.
- **Karşılaştığım Hatalar ve Çözümler:**
  - **Hata:** Yok. Rota ve serileştirme mantığı SQLAlchemy 2.x ile sorunsuz çalıştı.
  - **Çözüm:** -
- **Bu Oturumdan Öğrendiğim:** Uygulamanın sadece bir web arayüzünden ibaret kalmayıp dış dünyaya bir servis (REST API) olarak açılmasının modern yazılım mimarisindeki önemini kavradım. API yapılarının kararlılığını korumak için entegrasyon testlerinin ne kadar kritik bir yer tuttuğunu pekiştirdim.

---

## 📈 Geliştirme Adımları ve Teknik Kararlar (Özet)

*   **Adım 1: Proje İskeleti (Factory Pattern):** Flask 3.x ve Blueprint mimarisiyle sürdürülebilir altyapı kuruldu.
*   **Adım 2: Veritabanı Şeması:** Flask-Migrate ile SQLite şema göçleri yönetildi.
*   **Adım 3: HTML5 & Premium Vanilla CSS:** Slate-900 glassmorphism tasarımı, kopyalama fonksiyonu ve responsive navigasyon vanilla CSS ([style.css](file:///c:/Users/user/OneDrive/Masaüstü/sinematikaiportfolyosu/app/static/css/style.css)) ile geliştirildi.
*   **Adım 4: Birim ve Entegrasyon Testleri:** Flask test client kullanılarak yetkilendirme, arama, sayfalama, hata yönetimi, profil ve REST API süreçleri 39 birim testiyle %100 doğrulandı.
