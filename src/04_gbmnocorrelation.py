import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt 

tickers = ["THYAO.IS" , "BIMAS.IS"]
print(f"{tickers[0]} and {tickers[1]} data is being collected")
end_time = dt.datetime.now()
start_time = end_time - dt.timedelta(days = 365)

raw_data = yf.download(tickers, start=start_time , end = end_time)
data = raw_data['Close'].dropna()

returns = np.log(data/data.shift(1)).dropna()

mu = returns.mean() * 252
sigma = returns.std() * np.sqrt(252)

corr_matrix = returns.corr()
L = np.linalg.cholesky(corr_matrix) # bunu hala tam öğrenmedim ama baya sağlam bir şey

print("-" * 30)
print(f"Correlation between stocks :\n{corr_matrix}")
print("-" * 30)

S_initial = data.iloc[-1].values
T=1
N=252
M=10000
dt = T/N

S=np.zeros((N+1,len(tickers),M))
for i in range(len(tickers)):
    S[0,i,:] = S_initial[i]

for t in range(1, N+1):
    Z_ind = np.random.standard_normal((len(tickers),M))

    Z_corr = np.dot(L,Z_ind)

    for i in range(len(tickers)):
        S[t,i,:] = S[t-1,i,:] * np.exp((mu[i]-0.5*sigma[i]**2)*dt+sigma[i]*np.sqrt(dt)*Z_corr[i,:])

fig, ax = plt.subplots(1,2, figsize=(15,6))

ax[0].plot(S[:, 0, 0], label='THYAO', color='red')
ax[0].plot(S[:, 1, 0], label='BIMAS', color='blue')
ax[0].set_title("Örnek Bir Senaryoda Birlikte Hareket (Correlation)")
ax[0].set_xlabel("Gün")
ax[0].set_ylabel("Fiyat (TRY)")
ax[0].legend()
ax[0].grid(True)

# İki hissenin yıl sonu getirilerini kıyaslayan Scatter Plot
ax[1].scatter(S[-1, 0, :], S[-1, 1, :], alpha=0.3, s=10)
ax[1].set_title("1 Yıl Sonraki Olası Fiyat İlişkisi")
ax[1].set_xlabel("THYAO Yıl Sonu Fiyatı")
ax[1].set_ylabel("BIMAS Yıl Sonu Fiyatı")
ax[1].grid(True)

plt.tight_layout()
plt.show()