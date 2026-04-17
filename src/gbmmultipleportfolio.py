import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt 

tickers = ["THYAO.IS" , "BIMAS.IS", "TUPRS.IS"]
print(f"{tickers[0]}, {tickers[1]} and {tickers[2]} data is being collected")
end_time = dt.datetime.now()
start_time = end_time - dt.timedelta(days = 365)

raw_data = yf.download(tickers, start=start_time , end = end_time)
data = raw_data['Close'].dropna()

returns = np.log(data/data.shift(1)).dropna()

mu = returns.mean() * 252
sigma = returns.std() * np.sqrt(252)

corr_matrix = returns.corr()
L = np.linalg.cholesky(corr_matrix) # bunu hala tam öğrenmedim ama baya sağlam bir şey

print("-" * 40)
print(f"3x3 Correlation Matrix :\n{corr_matrix}")
print("-" * 40)

S_initial = data.iloc[-1].to_numpy()
T=1
N=252
M=50000
dt = T/N

S=np.zeros((N+1,len(tickers),M))
for i in range(len(tickers)):
    S[0,i,:] = S_initial[i]

for t in range(1, N+1):
    Z_ind = np.random.standard_normal((len(tickers),M))

    Z_corr = np.dot(L,Z_ind)

    for i in range(len(tickers)):
        S[t,i,:] = S[t-1,i,:] * np.exp((mu[i]-0.5*sigma[i]**2)*dt+sigma[i]*np.sqrt(dt)*Z_corr[i,:])

starting_money = 300000
inv_per_stock = starting_money / len(tickers)

stock_held= inv_per_stock / S_initial

portfolio_end_value = (S[-1,0,:] * stock_held[0]) + \
                      (S[-1,1,:] * stock_held[1]) + \
                      (S[-1,2,:] * stock_held[2])

fig, ax = plt.subplots(1,2, figsize=(16,6))

ax[0].plot((S[:, 0, 10] / S_initial[0] - 1)*100, label='THYAO', color='red')
ax[0].plot((S[:, 1, 10] / S_initial[1] - 1)*100, label='BIMAS', color='green')
ax[0].plot((S[:, 2, 10] / S_initial[2] - 1)*100, label='TUPRS', color='blue')
ax[0].set_title("Örnek Bir Senaryoda 3 Hissenin Getiri (%) Eğrileri")
ax[0].set_xlabel("Gün")
ax[0].set_ylabel("Getiri (%)")
ax[0].legend()
ax[0].grid(True)

# Sağ Grafik: Portföyün Toplam Değer Dağılımı (Diversification Effect)
ax[1].hist(portfolio_end_value, bins=100, color='gold', edgecolor='black', alpha=0.7)
ax[1].set_title("300.000 TL'lik Portföyün 1 Yıl Sonraki Olası Değeri")
ax[1].set_xlabel("Toplam Portföy Büyüklüğü (TRY)")
ax[1].set_ylabel("Frekans")

medyan_portfoy = np.median(portfolio_end_value)
ax[1].axvline(starting_money, color='red', linestyle='--', linewidth=2, label=f'Ana Para: {starting_money:,} TL')
ax[1].axvline(medyan_portfoy, color='green', linestyle='-', linewidth=2, label=f'Medyan: {medyan_portfoy:,.0f} TL')
ax[1].legend()
ax[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ANALİZ ÇIKTILARI
olasilik_zarar = (portfolio_end_value < starting_money).sum() / M * 100
olasilik_kar_yuzde50 = (portfolio_end_value > starting_money * 1.5).sum() / M * 100

print(f"\nPORTFÖY RİSK ANALİZİ ({M} Senaryo):")
print(f"Ana Parayı (300.000 TL) Kaybetme İhtimali: %{olasilik_zarar:.2f}")
print(f"Portföyü %50 Büyütme (450.000 TL Üstü) İhtimali: %{olasilik_kar_yuzde50:.2f}")