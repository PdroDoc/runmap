import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit import sidebar
from streamlit_card import card
from streamlit_lottie import st_lottie
import json


st.set_page_config(page_title="Presence Map", layout="wide")

st.title('Presence Map of My Runs')
with open("catrun.json") as f:
    lottie_json = json.load(f)
    st_lottie(lottie_json, height=300, key="runcat")

st.markdown("""

Explore an interactive geographical visualization of approximately **10 months** of runs recorded by Garmin GPS. This project compiles location data to map routes with precision, offering an immersive experience.

## About the Project

Using all available .FIT files from Garmin, which contain latitude and longitude records, I created a Python pipeline to process and consolidate the data into a single CSV file. From there, I developed an interactive visualization with **Streamlit** and **PyDeck**, highlighting the running routes on a dynamic map.

## How It Works

1. **Data Collection**: Extraction of coordinates (latitude and longitude) from Garmin .FIT files.
2. **Processing**: Python script to unify the data into an optimized CSV file.
3. **Visualization**: Generation of an interactive map with Streamlit and PyDeck, allowing seamless exploration of the routes.

**Enjoy exploring the paths traveled!**

---
""")

with st.sidebar:
    card(
        title="Pedro Potz", text="Visit my website", image="https://taote.vercel.app/meandmiau.jpeg",
        url="https://pedrop.vercel.app"
    )
with sidebar:
    st.info(
        "[🇵🇹Versão em Português:]()")
st.sidebar.title("An app by Pedro Potz.")
st.sidebar.success("Geo Visualization App")
with sidebar:
    st.info(
        "[💤Access the Sleep Analysis App](https://sleepdataview.streamlit.app/)")
st.sidebar.title("An app by Pedro Potz.")
st.sidebar.success("Geo Visualization App")


# Carregar CSV
df = pd.read_csv('CSV/todas_corridas.csv')

# Sidebar - Paletas de cor
with st.sidebar:
    paleta = st.selectbox(
        'Choose color options',
        ["Cosmic Aurora", "Flame in the Dark", "Current Colors"]
    )

if paleta == "Cosmic Aurora":
    color_range = [
        [1, 152, 189],
        [73, 227, 206],
        [216, 254, 181],
        [254, 237, 177],
        [254, 173, 84],
        [209, 55, 78]
    ]

elif paleta == "Flame in the Dark":
    color_range = [
        [255, 237, 160],
        [254, 217, 118],
        [254, 178, 76],
        [253, 141, 60],
        [252, 78, 42],
        [227, 26, 28]
    ]

elif paleta == "Current Colors":
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
        'Visualization Type',
        ["Presence Map", "Compiled Routes"]
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

if viz == "Presence Map":
    r = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        map_style="dark"
    )

elif viz == "Compiled Routes":
    r = pdk.Deck(
        layers=[path_layer],
        initial_view_state=view_state,
        map_style="dark"  )

st.pydeck_chart(r)