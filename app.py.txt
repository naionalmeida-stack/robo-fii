import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.title("📊 Robô FIIs - Renda Mensal")

fiis = ["HGLG11.SA","KNRI11.SA","MXRF11.SA","VISC11.SA"]

if st.button("Atualizar Análise"):

    resultado = []

    for fii in fiis:
        try:
            dados = yf.download(fii, period="1y", progress=False)

            dados['mm200'] = dados['Close'].rolling(200).mean()
            dados['rsi'] = ta.momentum.RSIIndicator(dados['Close'], window=14).rsi()

            preco = dados['Close'].iloc[-1]
            mm200 = dados['mm200'].iloc[-1]
            rsi = dados['rsi'].iloc[-1]

            score = 0

            if preco < mm200:
                score += 1

            if rsi < 40:
                score += 1

            resultado.append({
                "FII": fii,
                "Preço": round(preco,2),
                "RSI": round(rsi,2),
                "Score": score
            })

        except:
            continue

    df = pd.DataFrame(resultado)
    df = df.sort_values(by="Score", ascending=False)

    st.dataframe(df)
