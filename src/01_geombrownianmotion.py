import numpy as np
import matplotlib.pyplot as plt

S_initial = 329.0
mu=0.45
sigma=0.35
T=1
N=252
M=10000
dt = T/N
Z=np.random.standard_normal((N,M))

S = np.zeros((N+1, M))
S[0] = S_initial    

for t in range(1,N+1):
    S[t] = S[t-1] * np.exp(((mu)-(0.5) * (sigma**2))*dt + (sigma * np.sqrt(dt) * Z[t-1]))

plt.figure(figsize=(10,6))
plt.plot(S)
plt.title("Monte Carlo Simulation with Derived Data from THYAO")
plt.xlabel("Time (Days)")
plt.ylabel("Price (TRY)")
plt.grid(True)
plt.show()

print(((S[-1] > 500).sum()/M) * 100)