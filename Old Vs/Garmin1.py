import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('Mapa das Corridas - Garmin')

# Carregar os dados
df = pd.read_csv('CSV/fillefull.csv')

# Visualizar o dataframe
st.dataframe(df.head())
st.write(df.isna().sum())
# Configurar o layer (Heart Rate como cor)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[positionLong, positionLat]',
    get_color='[heartRate, 100, 140, 200]',  # Variando com HR
    get_radius=10,
    pickable=True,
    opacity=0.8
)

# Viewport automático
view_state = pdk.ViewState(
    longitude=df['positionLong'].mean(),
    latitude=df['positionLat'].mean(),
    zoom=14,
    pitch=40,
)

# Renderizar
st.pydeck_chart(pdk.Deck(
    map_style="light",
    initial_view_state=view_state,
    layers=[scatter_layer],
    tooltip={"text": "HR: {heartRate}"}  # Hover mostrando HR
))