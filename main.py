from fastapi import FastAPI

app = FastAPI(
    title="Mercom Quant API",
    description="API de calculs quantitatifs et analyse B2B",
    version="1.0.0"
)

# Route d'accueil pour supprimer l'erreur Not Found
@app.get("/")
def home():
    return {
        "status": "online",
        "project": "Mercom Quant API",
        "docs": "/docs"
    }

# Route de vérification d'état
@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.post("/api/v1/backtest")
def executer_backtest(data: BacktestData):
    prices = np.array(data.prix)
    if len(prices) <= data.fenetre_longue:
        return {"error": "Historique de prix trop court pour la fenêtre longue choisie."}
    
    # Calcul des moyennes mobiles
    sma_short = np.convolve(prices, np.ones(data.fenetre_courte)/data.fenetre_courte, mode='valid')
    sma_long = np.convolve(prices, np.ones(data.fenetre_longue)/data.fenetre_longue, mode='valid')
    
    # Alignement des tableaux
    offset = data.fenetre_longue - data.fenetre_courte
    sma_short_aligned = sma_short[offset:]
    
    # Signal (1 si moyenne courte > moyenne longue, 0 sinon)
    positions = np.where(sma_short_aligned > sma_long, 1, 0)
    
    # Rendements quotidiens
    prices_aligned = prices[data.fenetre_longue - 1:]
    returns = np.diff(prices_aligned) / prices_aligned[:-1]
    
    # Performance de la stratégie
    strat_returns = positions[:-1] * returns
    perf_strat = float(np.prod(1 + strat_returns) - 1)
    perf_buy_hold = float((prices_aligned[-1] - prices_aligned[0]) / prices_aligned[0])
    
    return {
        "parametres": {
            "fenetre_courte": data.fenetre_courte,
            "fenetre_longue": data.fenetre_longue,
            "nb_points_analyses": len(prices)
        },
        "performance": {
            "strategie_mercom_pct": round(perf_strat * 100, 2),
            "buy_and_hold_pct": round(perf_buy_hold * 100, 2),
            "surperformance_pct": round((perf_strat - perf_buy_hold) * 100, 2)
        }
    }
