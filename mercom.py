import numpy as np

def analyser_portefeuille(rendements):
    r_array = np.array(rendements)
    rendement_moyen = np.mean(r_array)
    volatilite = np.std(r_array)
    rf = 0.02 
    sharpe_ratio = (rendement_moyen - rf) / volatilite if volatilite != 0 else 0
    
    return {
        "Rendement moyen": f"{rendement_moyen * 100:.2f}%",
        "Volatilité": f"{volatilite * 100:.2f}%",
        "Ratio de Sharpe": round(sharpe_ratio, 2)
    }

historique = [0.012, -0.005, 0.008, 0.015, -0.002, 0.021, -0.010]

metrics = analyser_portefeuille(historique)
print("=== MERCOM QUANT ENGINE ===")
for k, v in metrics.items():
    print(f"{k} : {v}")