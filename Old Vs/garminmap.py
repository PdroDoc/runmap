from operator import truediv

import streamlit as st
import pandas as pd
import pydeck as pdk
from webview.platforms.cocoa import get_position

import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('Garmin Pedro Map')
st.write(
    """Esse App plota suas corridas no mapa, usando dados GPS extraídos do Garmin."""
)

# Carregar dados
Garmin_df = pd.read_csv('CSV/fillefull.csv')

# Verificar dados
st.dataframe(Garmin_df.head())

# Configurar camada de mapa
layer = pdk.Layer(
    'HexagonLayer',
    data=Garmin_df,
    get_position='[positionLong, positionLat]',  # Atenção: longitude primeiro
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
)

# Definir o ponto central do mapa (use a média dos seus dados)
view_state = pdk.ViewState(
    longitude=Garmin_df['positionLong'].mean(),
    latitude=Garmin_df['positionLat'].mean(),
    zoom=13,
    pitch=50,
)

# Renderizar o mapa no Streamlit
st.pydeck_chart(pdk.Deck(
    map_style="light",  # Pode ser "light", "dark", "road"
    initial_view_state=view_state,
    layers=[layer],
))