import numpy as np 
import matplotlib.pyplot as plt
import yfinance as yf
import datetime

ticker = "THYAO.IS"
print(f"{ticker} data is being collected...")
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=365)

stock = yf.Ticker(ticker)
data = stock.history(start=start_time, end=end_time)

prices = data['Close']
S_initial = float(prices.dropna().iloc[-1])

daily_profit = np.log(prices / prices.shift(1)).dropna()

sigma = float(daily_profit.std() * np.sqrt(252))

mu = float(daily_profit.mean() * 252)

print("-" * 30)
print(f"Automatically Calculated initial S:     {S_initial:.2f}TL")
print(f"Automatically Calculated initial mu:     %{mu*100:.2f}")
print(f"Automatically Calculated initial sigma:     %{sigma*100:.2f}")

T = 1
N = 252 
M = 1000000
dt = T/N

Z = np.random.standard_normal((N,M))

S = np.zeros((N+1,M))
S[0] = S_initial

for t in range(1, N+1):
    S[t] = S[t-1] * np.exp((mu - 0.5 * sigma**2)*dt + sigma * np.sqrt(dt) * Z[t-1])

fig, ax= plt.subplots(1, 2, figsize=(14,6))

ax[0].plot(S[:, :100], alpha=0.7)
ax[0].set_title("THYAO Next Year (First 100 Scenario)")
ax[0].set_xlabel("Zaman (Gün)")
ax[0].set_ylabel("Fiyat (TRY)")
ax[0].grid(True)

ax[1].hist(S[-1], bins=100, color='skyblue', edgecolor='black', alpha=0.8)
ax[1].set_title("1 Yıl Sonraki Olası Kapanış Fiyatları Dağılımı")
ax[1].set_xlabel("Fiyat (TRY)")
ax[1].set_ylabel("Frekans")

medyan = np.median(S[-1])
ax[1].axvline(S_initial, color='red', linestyle='--', linewidth=2, label=f'Şu Anki Fiyat: {S_initial:.0f} TL')
ax[1].axvline(medyan, color='green', linestyle='-', linewidth=2, label=f'Medyan (Orta Nokta): {medyan:.0f} TL')
ax[1].legend()
ax[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

hedef_fiyat = S_initial * 1.50 
olasilik_hedef = (S[-1] > hedef_fiyat).sum() / M * 100
olasilik_zarar = (S[-1] < S_initial).sum() / M * 100

print(f"Analiz: 1 Yıl sonunda yatırımcının zarar etme ihtimali: %{olasilik_zarar:.2f}")
print(f"Analiz: 1 Yıl sonunda hissenin %50'den fazla prim yapma ihtimali: %{olasilik_hedef:.2f}")