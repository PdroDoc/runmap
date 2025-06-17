import streamlit as st
import pandas as pd
import pydeck as pdk


def semicircle_to_degree(semicircle):
    return semicircle * (180 / 2**31)

st.set_page_config(page_title="Garmin Map", layout="wide")

st.title('Garmin Map Visualization')

# 🗂️ Carregar o CSV bruto
df = pd.read_csv('CSV/todas_corridas.csv')

# 🔧 Corrigir latitude e longitude
df['lat'] = df['positionLat'].apply(semicircle_to_degree)
df['lon'] = df['positionLong'].apply(semicircle_to_degree)

# 🔧 Renomear colunas secundárias (se desejar)
df = df.rename(columns={
    'heartRate': 'hr',
    'power': 'power'
})

# 🚩 Checagem simples
st.subheader('Check Dados')
st.write(df[['lat', 'lon', 'hr', 'power']].head())

# 🚀 Mapa simples Streamlit
st.subheader('Mapa simples')
st.map(df[['lat', 'lon']])

## Após conversões, analisar os dados.

temp= df['temperature']



# 🔥 Layer Pydeck
layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position='[lon, lat]',
    auto_highlight=True,
    radius=40,
    #elevation_scale='temperature',
    pickable=True,
    elevation_range=[0, 40],
    extruded=True,
)

# 🎯 View
view_state = pdk.ViewState(
    latitude=df['lat'].mean(),
    longitude=df['lon'].mean(),
    zoom=14,
    pitch=40,
)

# 🗺️ Deck
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Lat: {lat}\nLon: {lon}\nHR: {hr}\nPower: {power}"}
)

st.subheader('Mapa Avançado com Pydeck')
st.pydeck_chart(r)