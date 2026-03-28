import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import base64

# Config
st.set_page_config(page_title="Tool Spese Sovraindebitamento", layout="wide")
st.title("🔍 Tool di controllo spese - Sovraindebitamento")

# Dati ISTAT 2024 Italia media (da adattare per regione)
istat_data = {
    'Voce': [
        '01. Prodotti alimentari e bevande analcoliche',
        '02. Bevande alcoliche e tabacchi',
        '03. Abbigliamento e calzature',
        '04. Abitazione, acqua, elettricità, gas',
        '05. Mobili, articoli per la casa',
        '06. Salute',
        '07. Trasporti',
        '08. Comunicazione',
        '09. Ricreazione, sport, cultura',
        '10. Istruzione',
        '11. Ristorazione e alloggio',
        '12. Assicurazioni e finanza',
        '13. Cura persona e altri'
    ],
    'Media_IT_2024': [531, 28, 155, 984, 122, 97, 316, 85, 204, 38, 191, 126, 78]
}

df_istat = pd.DataFrame(istat_data)

# Scala Carbonaro
carbonaro = {1: 0.6, 2: 1.0, 3: 1.33, 4: 1.63, 5: 1.9, 6: 2.16, 7: 2.4}

# Sidebar anagrafica
with st.sidebar:
    st.header("📋 Anagrafica")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    regione = st.selectbox("Regione", ["Italia", "Nord-Est (Veneto)", "Nord-Ovest", "Centro", "Sud", "Isole"])
    n_fam = st.number_input("Componenti familiari", 1, 10, 2)
    note = st.text_area("Note speciali")
    
    # Fattore Carbonaro
    fattore = carbonaro.get(min(n_fam, 7), 2.4)
    st.info(f"**Fattore Carbonaro**: {fattore:.2f}")

# Adatta ISTAT per regione e famiglia (semplificato)
if regione == "Nord-Est (Veneto)":
    df_istat['Media_adattata'] = df_istat['Media_IT_2024'] * 1.1 * fattore
else:
    df_istat['Media_adattata'] = df_istat['Media_IT_2024'] * fattore

# Main form
st.header("💰 Inserisci le tue spese mensili (€)")
col1, col2, col3 = st.columns(3)

spese = {}
for i, voce in enumerate(df_istat['Voce']):
    with col1 if i%3==0 else col2 if i%3==1 else col3:
        spese[voce] = st.number_input(voce[:30] + "...", 0.0, 5000.0, 0.0)

# Spese aggiuntive
st.header("➕ Spese aggiuntive")
extra_desc = st.text_area("Descrizione")
extra_imp = st.number_input("Importo mensile (€)", 0.0)
extra_motivo = st.text_area("Motivazione")

# Calcola
if st.button("🔢 Calcola confronto"):
    # Aggiungi spese a df
    df_confronto = df_istat.copy()
    df_confronto['Tua_spesa'] = [spese.get(v, 0) for v in df_istat['Voce']]
    df_confronto['Differenza_%'] = ((df_confronto['Tua_spesa'] - df_confronto['Media_adattata']) / df_confronto['Media_adattata'] * 100).round(1)
    
    # Colori
    def get_color(pct):
        if pct <= 0:
            return "🟢"
        elif pct <= 10:
            return "🟡"
        else:
            return "🔴"
    
    df_confronto['Semaforo'] = [get_color(p) for p in df_confronto['Differenza_%']]
    
    # Tabella
    st.subheader("📊 Confronto dettagliato")
    st.subheader("📊 Confronto dettagliato")
st.dataframe(df_confronto)
    
    # Totali
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Totale ISTAT adattato", f"{df_confronto['Media_adattata'].sum():.0f}€")
    with col2:
        st.metric("Tue spese standard", f"{df_confronto['Tua_spesa'].sum():.0f}€")
    with col3:
        pct_tot = ((df_confronto['Tua_spesa'].sum() - df_confronto['Media_adattata'].sum()) / df_confronto['Media_adattata'].sum() * 100)
        st.metric("Scostamento totale", f"{pct_tot:.1f}%", delta=f"{pct_tot:.1f}%")
    with col4:
        if extra_imp > 0:
            st.metric("Spese extra", f"{extra_imp:.0f}€")
    
    # Grafico
    fig = px.bar(df_confronto, x='Voce', y=['Media_adattata', 'Tua_spesa'], barmode='group', title="Confronto grafico")
    st.plotly_chart(fig, use_container_width=True)
    
    # PDF
    if st.button("📄 Scarica report PDF"):
        # Logica PDF semplificata
        st.success("Report pronto! (Implementazione completa nel codice finale)")
    
    # Spese extra
    if extra_imp > 0:
        st.subheader("📝 Spese aggiuntive dichiarate")
        st.write(f"**{extra_desc}**: {extra_imp}€ - {extra_motivo}")

# Footer
st.markdown("---")
st.markdown("Tool per procedure sovraindebitamento basato su dati ISTAT 2024 [web:1][page:0]")
