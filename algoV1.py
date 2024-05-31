import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Téléchargement des données historiques pour une action
ticker = "AAPL"  # Action Apple
data = yf.download(ticker, start="2019-05-20", end="2024-05-28")

# Calcul des moyennes mobiles
data["SMA50"] = data["Close"].rolling(window=50).mean()
data["SMA200"] = data["Close"].rolling(window=200).mean()

# Génération des signaux
data["Signal_SMA"] = 0
data["Signal_SMA"][50:] = np.where((data["SMA50"][50:] > data["SMA200"][50:]) & (data["SMA50"][50:].shift(1) <= data["SMA200"][50:].shift(1)), 1, 0)  # Signal d'achat lorsque la SMA50 croise au-dessus de la SMA200
data["Signal_SMA"][50:] = np.where((data["SMA50"][50:] < data["SMA200"][50:]) & (data["SMA50"][50:].shift(1) >= data["SMA200"][50:].shift(1)), -1, data["Signal_SMA"][50:])  # Signal de vente lorsque la SMA50 croise en-dessous de la SMA200

# Filtrage des données pour s'assurer que les SMAs sont bien calculées
data = data.dropna()



# Calcul du montant du portefeuille
initial_cash = 1000  # Capital initial en $
shares = initial_cash / data["Close"].iloc[0]
data["Portfolio"] = shares * data["Close"]

# Utilisation de Plotly pour créer le graphique des signaux
fig_signals = go.Figure()
fig_signals.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name='Prix de Clôture', line=dict(color='black', width=1)))
fig_signals.add_trace(go.Scatter(x=data.index, y=data["SMA50"], mode='lines', name='SMA 50 jours', line=dict(color='blue', width=1.5)))
fig_signals.add_trace(go.Scatter(x=data.index, y=data["SMA200"], mode='lines', name='SMA 200 jours', line=dict(color='red', width=1.5)))
fig_signals.add_trace(go.Scatter(x=data[data["Signal_SMA"] == 1].index, y=data["Close"][data["Signal_SMA"] == 1],
                                 mode='markers', name='Signal d\'achat', marker=dict(symbol='triangle-up', color='green', size=8)))
fig_signals.add_trace(go.Scatter(x=data[data["Signal_SMA"] == -1].index, y=data["Close"][data["Signal_SMA"] == -1],
                                 mode='markers', name='Signal de vente', marker=dict(symbol='triangle-down', color='red', size=8)))
fig_signals.update_layout(title=f"Signaux de Trading pour {ticker}",
                          xaxis_title='Date',
                          yaxis_title='Prix',
                          legend=dict(font=dict(size=12)),
                          xaxis_rangeslider_visible=False)
fig_signals.show()

# Utilisation de Plotly pour créer le graphique de l'évolution du portefeuille
fig_portfolio = go.Figure()
fig_portfolio.add_trace(go.Scatter(x=data.index, y=data["Portfolio"], mode='lines', name='Portefeuille', line=dict(color='purple', width=2)))
fig_portfolio.update_layout(title="Evolution du Portefeuille",
                            xaxis_title='Date',
                            yaxis_title='Montant ($)',
                            xaxis_rangeslider_visible=False)
fig_portfolio.show()
