import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🔍 Tool Spese Sovraindebitamento")

st.header("Dati anagrafici")
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome")
with col2:
    n_fam = st.number_input("Familiari", 1, 10, 2)

st.header("Spese mensili (€)")
spese = {}
voci = ['Alimentari', 'Abitazione', 'Trasporti', 'Salute', 'Altro']

data = {'Voce': voci, 'ISTAT': [531, 984, 316, 97, 924]}
df = pd.DataFrame(data)

for voce in voci:
    spese[voce] = st.number_input(voce, 0.0, 5000.0)

if st.button("Calcola"):
    df['Tua'] = [spese[v] for v in voci]
    df['%'] = ((df['Tua'] - df['ISTAT']) / df['ISTAT'] * 100).round(1)
    
    # Colori
    def color(val):
        if val <= 0: return '🟢'
        elif val <= 10: return '🟡'
        else: return '🔴'
    df['Allerta'] = [color(p) for p in df['%']]
    
    st.subheader("Risultati")
    st.dataframe(df)
    
    totale_istat = df['ISTAT'].sum()
    totale_tua = df['Tua'].sum()
    pct_tot = ((totale_tua - totale_istat) / totale_istat * 100).round(1)
    st.metric("Scostamento totale", f"{pct_tot}%", delta=f"{pct_tot:.1f}%")

st.info("Basato su ISTAT 2024 [web:1]")
