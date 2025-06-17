import streamlit as st
import pandas as pd
import pydeck as pdk
import json
from streamlit_lottie import st_lottie
from streamlit_card import card

st.set_page_config(page_title="Mapa de Presença", layout="wide")

st.title('Mapa de Presença das Minhas Corridas')
st.markdown("""
   
Explore uma visualização geográfica interativa de aproximadamente 10 meses de corridas registradas pelo GPS Garmin. Este projeto reúne dados de localização para mapear trajetos com precisão e oferecer uma experiência imersiva.

## Sobre o Projeto

Utilizando todos os arquivos .FIT disponíveis do Garmin, que contêm registros de latitude e longitude, criei um pipeline em Python para processar e consolidar os dados em um único arquivo CSV. A partir disso, desenvolvi uma visualização interativa com **Streamlit** e **PyDeck**, destacando os percursos das corridas em um mapa dinâmico.

## Como Funciona

1. **Coleta de Dados**: Extração de coordenadas (latitude e longitude) dos arquivos .FIT do Garmin.
2. **Processamento**: Script em Python para unificar os dados em um arquivo CSV otimizado.
3. **Visualização**: Geração de um mapa interativo com Streamlit e PyDeck, permitindo explorar os trajetos de forma fluida.



**Divirta-se explorando os caminhos percorridos!**

---
""")

with st.sidebar:
    card(
        title="Pedro Potz", text="Visite meu site", image="https://taote.vercel.app/meandmiau.jpeg",
        url="https://pedrop.vercel.app"
    )
st.sidebar.title("An app by Pedro Potz.")
st.sidebar.success("Geo Vizualization App")



# Carregar CSV
df = pd.read_csv('CSV/todas_corridas.csv')

# cores adicionada posteriormente

color_range = [
    [1, 152, 189],
    [73, 227, 206],
    [216, 254, 181],
    [254, 237, 177],
    [254, 173, 84],
    [209, 55, 78]
]
color_range2 = [
    [10, 50, 150],   # Azul profundo, quase cobalto
    [50, 100, 200],  # Azul celeste vibrante
    [100, 200, 255], # Ciano luminoso
    [150, 255, 200], # Verde-água etéreo
    [255, 150, 100], # Laranja quente
    [200, 50, 50]    # Vermelho intenso
]
color_range3 = [
    [30, 30, 50],    # Cinza-azulado escuro, quase apagado
    [70, 50, 100],   # Roxo profundo, misterioso
    [150, 50, 150],  # Magenta vibrante
    [255, 100, 50],  # Laranja flamejante
    [255, 200, 50],  # Amarelo brilhante
    [255, 50, 50]    # Vermelho ardente
]
material = {
    "ambient": 0.5,
    "diffuse": 0.9,
    "shininess": 32,
    "specularColor": [60, 64, 70]
}
with st.sidebar:
    paleta = st.selectbox(
        'Escolha opções de cores',
        ["Aurora Cósmica", "Chama no Escuro", "Cores Atuais"]
    )
if paleta == "Aurora Cósmica":
    color_range = [
        [1, 152, 189],
        [73, 227, 206],
        [216, 254, 181],
        [254, 237, 177],
        [254, 173, 84],
        [209, 55, 78]
    ]

elif paleta == "Chama no Escuro":
    color_range = [
        [255, 237, 160],
        [254, 217, 118],
        [254, 178, 76],
        [253, 141, 60],
        [252, 78, 42],
        [227, 26, 28]
    ]

elif paleta == "Cores Atuais":
    color_range = [
        [102, 194, 165],
        [252, 141, 98],
        [141, 160, 203],
        [231, 138, 195],
        [166, 216, 84],
        [255, 217, 47]
    ]
# Mapa
layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position='[lon, lat]',
    auto_highlight=True,
    radius=50, #acrescentei
    elevation_scale=30,
    pickable=True,
    elevation_range=[0, 500],
    extruded=True,
    coverage=1,
    opacity=0.4,
    color_range=color_range,
    material=material,

)


layer2 = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=30,
    get_fill_color='[180, 0, 200, 140]',
    get_line_color=[0, 0, 0],
    pickable=True,
    opacity=0.1,
    stroked=True,
    filled=True,
    radius_scale=3,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
)

view_state = pdk.ViewState(
    latitude=df['lat'].mean(),
    longitude=df['lon'].mean(),
    zoom=11,
    pitch=40,
    bearing=2,
)



r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="dark"
)
# Funtime



st.pydeck_chart(r)
