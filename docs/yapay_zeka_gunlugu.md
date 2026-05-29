# Yapay Zeka Geliştirme Günlüğü (AI Log)

Bu günlük, **Sinematik AI Prompt Portfolyosu ve AI Günlüğü** projesinin geliştirilme sürecinde, kullanıcının (öğrencinin) yapay zeka asistanını (AI Agent) nasıl yönlendirdiğini, modern standartları nasıl dikte ettiğini ve mimari disiplini nasıl sağladığını gösteren teknik bir seyir defteridir.

---

## 👨‍💻 Kullanıcı Müdahaleleri ve Kritik Oturumlar

Aşağıda, kullanıcının projeyi şekillendiren ve AI asistanının eski/yanlış kod yazma alışkanlıklarını kırarak modern standartları zorunlu kıldığı kritik oturumlar listelenmiştir:

### 📅 Oturum 1-2: SQLAlchemy 2.x Standartlarının Zorlanması ve Model Tasarımı
*   **Kullanıcı Yönlendirmesi & Uyarı:** AI asistanının Flask-SQLAlchemy projelerinde yaygın olarak kullanılan eski `.query.all()` veya `.query.filter_by()` gibi legacy (SQLAlchemy 1.x) kalıplarını kullanma eğilimi fark edilmiş ve asistan katı bir dille uyarılmıştır.
*   **Teknik Müdahale:** Veritabanı sorgularının tamamında modern SQLAlchemy 2.0 standartları olan `select`, `scalars` ve `db.session.execute()` yapılarının kullanılması sağlanmıştır. Model tanımlamalarında modern `Mapped` ve `mapped_column` zorunlu kılınmıştır.

### 📅 Oturum 3: Mimari Temizlik (forms.py & routes.py Ayrımı) ve Commit Disiplini
*   **Kullanıcı Yönlendirmesi & Uyarı:** Uygulama modüllerinin kod karmaşasını önlemek adına forms yapılarının doğrudan routes veya şablonlar içinde tanımlanmaması, kesin bir "Separation of Concerns" (Sorumlulukların Ayrılması) prensibiyle çalışılması uyarısı yapılmıştır.
*   **Teknik Müdahale:** Form tanımları `forms.py` dosyasına taşınmış; rotalar ve iş mantığı `routes.py` içinde bırakılmıştır. İşler küçük parçalara bölünerek sık ve açıklayıcı Git commit'leri (commit odaklı geliştirme) ile ilerlenmiştir.

### 📅 Oturum 4: Güvenlik Kontrolleri ve Yetkilendirme (abort(403))
*   **Kullanıcı Yönlendirmesi & Uyarı:** Kullanıcıların diğer yazarların oluşturduğu promptları düzenlemesini veya silmesini önlemek adına rotalarda güvenlik açıklarının bırakılmaması gerektiği talimatı verilmiştir.
*   **Teknik Müdahale:** `prompt_edit` ve `prompt_delete` rotalarında, işlem yapan kullanıcının prompt sahibi olup olmadığı (`prompt.user_id != current_user.id`) kontrol edilmiş, yetkisiz erişimlerde Flask'ın `abort(403)` fonksiyonu tetiklenerek güvenli bir erişim kontrolü kurulmuştur.

### 📅 Oturum 5: Arama/Filtreleme Optimizasyonu ve Sayfalama Parametrelerinin Korunması
*   **Kullanıcı Yönlendirmesi & Uyarı:** Çoklu filtreleme (arama sorgusu `q` ve etiket filtresi `tag`) yapıldığında, sonraki sayfalara geçildiğinde filtrelerin kaybolması sorunu kullanıcı tarafından fark edilmiş ve parametrelerin korunması talimatı verilmiştir. Ayrıca etiket ilişkilerindeki performans kaybını engellemek için veritabanı sorgularının optimize edilmesi istenmiştir.
*   **Teknik Müdahale:** Jinja2 şablonlarındaki sayfalama linklerine `q` ve `tag` parametreleri entegre edilmiştir. Etiket filtrelemesinde ilişkili tablo üzerinden `any()` filtresi kullanılarak tek adımlı, performanslı bir veritabanı sorgusu oluşturulmuştur.

### 📅 Oturum 6: Sinematik Hata Yönetimi ve Test Kapsamı
*   **Kullanıcı Yönlendirmesi & Uyarı:** Uygulamanın tamamlanmasının ardından, profesyonel bir dokunuş için 404 (Sayfa Bulunamadı) ve 500 (Sunucu Hatası) durumlarının yakalanıp sinematik temaya uygun özelleştirilmiş hata şablonlarıyla gösterilmesi uyarısı yapılmıştır.
*   **Teknik Müdahale:** `app/errors` adında yeni bir blueprint oluşturulmuştur. 500 hatası durumunda veritabanında oluşabilecek tutarsızlıkları önlemek için `db.session.rollback()` çağrısı eklenmiş, Bootstrap 5 tabanlı, premium dark temalı `404.html` ve `500.html` sayfaları oluşturulmuştur. 404 sayfasında *"Aradığınız sahne mevcut değil"*, 500 sayfasında ise *"Beklenmedik bir kurgu hatası oluştu"* gibi yaratıcı metinler ve CSS animasyonları kullanılmıştır.

---

## 📈 Geliştirme Adımları ve Teknik Kararlar (Özet)

*   **Adım 1: Proje İskeleti (Factory Pattern):** Flask 3.x ve Blueprint mimarisiyle sürdürülebilir altyapı kuruldu.
*   **Adım 2: Veritabanı Şeması:** Flask-Migrate ile SQLite şema göçleri yönetildi.
*   **Adım 3: HTML5 & Premium Vanilla CSS:** Slate-900 glassmorphism tasarımı, kopyalama fonksiyonu ve responsive navigasyon vanilla CSS (`style.css`) ile geliştirildi.
*   **Adım 4: Birim ve Entegrasyon Testleri:** Flask test client kullanılarak yetkilendirme, arama, sayfalama ve hata yönetimi süreçleri 36 birim testiyle %100 doğrulandı.
