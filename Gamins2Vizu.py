import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit import sidebar
from streamlit_card import card
from streamlit_lottie import st_lottie
import json


st.set_page_config(page_title="Mapa de Presença", layout="wide")

st.title('Mapa de Presença das Minhas Corridas')
with open("catrun.json") as f:
    lottie_json = json.load(f)
    st_lottie(lottie_json, height=300, key="runcat")

st.markdown("""

Explore uma visualização geográfica interativa de aproximadamente **10 meses** de corridas registradas pelo GPS Garmin. Este projeto reúne dados de localização para mapear trajetos com precisão e oferecer uma experiência imersiva.

## Sobre o Projeto

Utilizando todos os arquivos .FIT disponíveis do Garmin, que contêm registros de latitude e longitude, criei um pipeline em Python para processar e consolidar os dados em um único arquivo CSV. A partir disso, desenvolvi uma visualização interativa com **Streamlit** e **PyDeck**, destacando os percursos das corridas em um mapa dinâmico.

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
with sidebar:
    st.info(
        "[🇺🇸English Version:]()")
st.sidebar.title("An app by Pedro Potz.")
st.sidebar.success("Geo Visualization App")
with sidebar:
    st.info(
        "[💤Acesse também o App de Análise do Sono](https://sleepdataview.streamlit.app/)")
st.sidebar.title("An app by Pedro Potz.")
st.sidebar.success("Geo Visualization App")


# Carregar CSV
df = pd.read_csv('CSV/todas_corridas.csv')

# Sidebar - Paletas de cor
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


material = {
    "ambient": 0.5,
    "diffuse": 0.9,
    "shininess": 32,
    "specularColor": [60, 64, 70]
}

# Sidebar - Tipo de visualização
with st.sidebar:
    viz = st.selectbox(
        'Tipo de Visualização',
        ["Mapa de Presença", "Percursos Compilados"]
    )


### ------------------------- Layer Hexagon ------------------------

hex_layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position='[lon, lat]',
    auto_highlight=True,
    radius=50,
    elevation_scale=40,
    pickable=True,
    elevation_range=[0, 500],
    extruded=True,
    coverage=0.8,
    opacity=0.5,
    color_range=color_range,
    material=material,
)


### ------------------------- Layer Path ------------------------

# Agrupar por arquivo para gerar as linhas de percurso
trajetos = []

for file_name, grupo in df.groupby('file'):
    coords = grupo[['lon', 'lat']].values.tolist()
    trajetos.append({'file': file_name, 'coordinates': coords})

df_paths = pd.DataFrame(trajetos)

path_layer = pdk.Layer(
    "PathLayer",
    data=df_paths,
    get_path="coordinates",
    get_color=[253, 128, 93],
    width_scale=20,
    get_with=5,
    width_min_pixels=2,
    opacity=1
)


### ------------------------- View ------------------------

view_state = pdk.ViewState(
    latitude=df['lat'].mean(),
    longitude=df['lon'].mean(),
    zoom=11,
    pitch=40,
    bearing=2,
)

### ------------------------- Render ------------------------

if viz == "Mapa de Presença":
    r = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        map_style="dark"
    )

elif viz == "Percursos Compilados":
    r = pdk.Deck(
        layers=[path_layer],
        initial_view_state=view_state,
        map_style="dark"  )

st.pydeck_chart(r)