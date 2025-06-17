import streamlit as st
import pandas as pd
import pydeck as pdk


def semicircle_to_degree(semicircle):
    return semicircle * (180 / 2**31)

st.set_page_config(page_title="Garmin Map", layout="wide")

st.title('Garmin Map Visualization')

# 🗂️ Carregar o CSV bruto
df = pd.read_csv('CSV/fillefull.csv')



# Cria bins (grids) espaciais

# 🔧 Corrigir latitude e longitude
df['lat'] = df['positionLat'].apply(semicircle_to_degree)
df['lon'] = df['positionLong'].apply(semicircle_to_degree)
# 🔧 Renomear colunas secundárias (se desejar)
df = df.rename(columns={
    'heartRate': 'hr',
    'power': 'power'
})


df['lat_bin'] = (df['lat'] *200).round(0) / 1
df['lon_bin'] = (df['lon'] * 200).round(0) / 1

# Agrupa por região e pega temperatura máxima
agg = df.groupby(['lat_bin', 'lon_bin']).agg({
    'temperature': 'max',
    'lat': 'mean',
    'lon': 'mean'
}).reset_index()

# Plota
layer = pdk.Layer(
    "ScatterplotLayer",
    data=agg,
    get_position='[lon, lat]',
    get_color='[temperature * 5, 100, 150, 200]',  # Cor proporcional à temperatura
    get_radius=40,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=agg['lat'].mean(),
    longitude=agg['lon'].mean(),
    zoom=13,
    pitch=40
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="light"
)

st.pydeck_chart(r)