# BIST-100 Monte Carlo Portfolio Simulator

Bu proje, Borsa İstanbul (BIST) verilerini kullanarak çoklu varlık portföylerinin gelecekteki olası değerlerini **Geometrik Brownian Hareketi (GBM)** ve **Cholesky Ayrışımı** yöntemleriyle modelleyen bir finansal simülasyon aracıdır.

Elektrik-Elektronik mühendisliği perspektifiyle stokastik süreçlerin ekonomi alanına uygulanması üzerine bir çalışma niteliğindedir.

## 🚀 Proje Hakkında
Bu simülatör, tekil hisse senedi tahminlerinin ötesine geçerek, varlıklar arasındaki **korelasyonu** hesaba katan bir risk analiz motoru sunar. 

### Temel Özellikler:
* **Canlı Veri Entegrasyonu:** `yfinance` API aracılığıyla BIST verilerinin anlık çekilmesi.
* **GBM Modellemesi:** Hisse senedi fiyatlarının log-normal dağılım sergilediği varsayımıyla rastgele yürüyüş (random walk) üretimi.
* **Korelasyon Yönetimi:** Cholesky Ayrışımı kullanılarak, bağımsız rastgele şokların piyasa gerçeklerine uygun şekilde birbirine bağlanması.
* **Portföy Analizi:** On binlerce senaryo ile portföyün 1 yıl sonraki değer dağılımının ve risk metriklerinin hesaplanması.

## 🧬 Matematiksel Çerçeve

Simülasyonun kalbinde, fiyat değişimlerini bir diferansiyel denklem olarak ele alan Geometrik Brownian Hareketi yatar. Beklenen getiri ($\mu$) ve volatilite ($\sigma$) kullanılarak fiyat yolları şu şekilde türetilir:

$$dS_t=\mu S_t dt+\sigma S_t dW_t$$

Çoklu varlık modellemesinde ise, bağımsız rastgele değişkenleri ($X$) korele piyasa şoklarına ($Z$) dönüştürmek için Cholesky matris ayrışımı uygulanmıştır. $R$ korelasyon matrisini temsil etmek üzere sistemin alt üçgensel matrisi ($L$) şu şekilde kurulur:

$$L \cdot L^T=R$$

Matris çarpımı ile filtrelenmiş korele şoklar elde edilir:

$$Z=L \cdot X$$

## 📊 Görselleştirme ve Analiz
Kod çalıştırıldığında iki temel çıktı üretir:
1. **Senaryo Yolları:** Hisselerin izleyebileceği örnek fiyat patikalarının zaman serisi analizi.
2. **Olasılık Yoğunluk Fonksiyonu:** Portföyün nihai değerinin dağılımı (Histogram).

*(Not: Görsel çıktı örneği)*
`![Portföy Dağılımı](assets/3port.png)`

## 🛠 Kurulum ve Kullanım

1. Projeyi klonlayın:
```bash
git clone https://github.com/KULLANICI_ADIN/monte-carlo-portfolio-sim.git
```
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```
3. Simülasyonu başlatın:
```bash
python src/portfolio_sim.py
```

## ⚠️ Yasal Uyarı
Bu proje tamamen eğitim ve mühendislik analizi amaçlıdır. Kesinlikle **yatırım tavsiyesi içermez**. Simülasyon sonuçları geçmiş verilere dayanmaktadır ve gelecekteki piyasa hareketlerini garanti etmez.