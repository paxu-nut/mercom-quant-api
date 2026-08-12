import numpy as np
import matplotlib.pyplot as plt

# 1. Generation d'un historique de prix simule (marche aleatoire)
np.random.seed(42)
nb_jours = 250
prix = 100 + np.cumsum(np.random.randn(nb_jours) * 1.5)

# 2. Calcul des moyennes mobiles
f_courte = 10
f_longue = 30

sma_courte = np.convolve(prix, np.ones(f_courte)/f_courte, mode='valid')
sma_longue = np.convolve(prix, np.ones(f_longue)/f_longue, mode='valid')

# Alignement des tableaux de donnees
decalage = f_longue - 1
prix_aligne = prix[decalage:]
sma_courte_alignee = sma_courte[f_longue - f_courte:]

# 3. Generation des signaux : 1 (Achat) si courte > longue, sinon -1 (Vente)
signaux = np.where(sma_courte_alignee > sma_longue, 1, -1)

# 4. Calcul de la performance du capital
rendements_journaliers = np.diff(prix_aligne) / prix_aligne[:-1]
rendements_strategie = rendements_journaliers * signaux[:-1]

capital_initial = 10000
capital_mercom = capital_initial * np.cumprod(1 + rendements_strategie)
capital_buy_hold = capital_initial * (prix_aligne[1:] / prix_aligne[0])

# 5. Rendement final
perf_mercom = ((capital_mercom[-1] - capital_initial) / capital_initial) * 100
perf_bh = ((capital_buy_hold[-1] - capital_initial) / capital_initial) * 100

print(f"=== MERCOM BACKTEST RESULTS ===")
print(f"Capital Initial     : {capital_initial} €")
print(f"Performance Mercom  : {perf_mercom:.2f}% (Final: {capital_mercom[-1]:.2f} €)")
print(f"Buy & Hold          : {perf_bh:.2f}% (Final: {capital_buy_hold[-1]:.2f} €)")

# 6. Affichage des courbes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

ax1.plot(prix_aligne, label="Prix actif", color="gray", alpha=0.5)
ax1.plot(sma_courte_alignee, label=f"SMA {f_courte}j", color="blue")
ax1.plot(sma_longue, label=f"SMA {f_longue}j", color="orange")
ax1.set_title("Mercom Backtest Engine — Strategie SMA Crossover")
ax1.set_ylabel("Prix (€)")
ax1.legend()
ax1.grid(True)

ax2.plot(capital_mercom, label="Capital Strategie Mercom", color="green", linewidth=2)
ax2.plot(capital_buy_hold, label="Buy & Hold", color="red", linestyle="--")
ax2.set_ylabel("Capital (€)")
ax2.set_xlabel("Jours")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()