import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Robô FII", layout="wide")

st.title("📊 Robô Analisador de FIIs")
st.write("Faça upload do seu arquivo CSV para análise automática.")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

if uploaded_file is not None:
    
    # Ler arquivo
    df = pd.read_csv(uploaded_file)

    # Limpar nomes das colunas (remove espaços invisíveis)
    df.columns = df.columns.str.strip()

    st.subheader("📋 Dados carregados")
    st.write(df.head())

    # Garantir que colunas numéricas sejam numéricas
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # Criar Score se não existir
    if "Score" not in df.columns:
        st.info("Coluna 'Score' não encontrada. Criando Score automático.")

        colunas_numericas = df.select_dtypes(include=np.number).columns

        if len(colunas_numericas) > 0:
            # Normalização simples para evitar distorção
            df_normalizado = df[colunas_numericas].apply(
                lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0
            )
            
            df["Score"] = df_normalizado.sum(axis=1)
        else:
            st.error("Nenhuma coluna numérica encontrada para gerar Score.")
            st.stop()

    # Ordenar pelo Score
    df = df.sort_values(by="Score", ascending=False)

    st.subheader("🏆 Ranking por Score")
    st.dataframe(df, use_container_width=True)

    # Mostrar Top 10
    st.subheader("🔥 Top 10 FIIs")
    st.dataframe(df.head(10), use_container_width=True)

else:
    st.warning("Envie um arquivo CSV para começar.")
