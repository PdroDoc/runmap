import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit import sidebar
from streamlit_card import card
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Mapa de Presença", layout="wide")

st.title('Geo-Visualização: Heatmap de 10 meses de gps de minhas corridas!')
with open("catrun.json") as f:
    lottie_json = json.load(f)
    st_lottie(lottie_json, height=300, key="runcat")

st.markdown("""


##   62.940 LINHAS DE GPS reunidas em um gráfico: Como a Magia Acontece

Eu mergulhei fundo em exatamente **62.940 linhas de dados GPS** brutos, extraídos diretamente dos meus arquivos .FIT do Garmin. Esse não é apenas um mapa qualquer; é um **heatmap 3D dinâmico**, construído com a poderosa combinação de **Streamlit** e **PyDeck**. Pense nisso como uma paisagem urbana de suas corridas:

* **Torres de Atividade**: Cada local por onde você mais correu se eleva em uma "torre" mais alta, revelando os seus pontos de treino favoritos e as áreas de maior intensidade.
* **Hexagon Layer**: Utilizando a técnica de Hexagon Layer, os dados são agrupados de forma inteligente, criando uma visualização limpa e poderosa que destaca padrões de movimento que você nunca percebeu.

## Sobre o Projeto

Utilizando todos os arquivos .FIT disponíveis do Garmin, que contêm registros de latitude e longitude, criei um pipeline em Python para processar e consolidar os dados em um único arquivo CSV. A partir disso, desenvolvi uma visualização interativa com **Streamlit** e **PyDeck**, destacando os percursos das corridas em um mapa dinâmico.

## Como Funciona
1.  **Coleta de Dados Brutos**: Todos os seus registros de latitude e longitude foram coletados com precisão dos arquivos .FIT do Garmin.
2.  **Transformação Pythonica**: Um pipeline robusto em Python processa e consolida esses dados massivos em um arquivo CSV otimizado, preparando-os para a visualização.
3.  **Visualização Dinâmica com Streamlit & PyDeck**: A mágica acontece! Seus dados são projetados em um mapa interativo, onde você pode explorar seus trajetos com fluidez e descobrir a história por trás de cada corrida


---
""")

with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/205710427?v=4", caption="Advogado que programa é unicórnio!",
             use_container_width=True)  # Sua imagem com uma frase de poder
    st.markdown("---")
    st.header("Pedro Potz")
    st.markdown("Advogado Programador")
    st.link_button("Conheça meu novo site", "https://pedrop.vercel.app/")


st.markdown("---")
st.sidebar.success("Geo Visualization App")

# Carregar CSV
df = pd.read_csv('CSV/todas_corridas.csv')

# Sidebar - Paletas de cor
with st.sidebar:
    paleta = st.selectbox(
        'Escolha opções de cores',
        ["Aurora Cósmica", "Chama no Escuro", "Cores Quentes"]
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

elif paleta == "Cores Quentes":
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
        map_style="dark")

st.pydeck_chart(r)

with st.expander("Veja os dados brutos"):
    st.dataframe(df)
st.markdown("---")


st.markdown("### Não perca meus tutoriais e outras ferrramentas gratuitas! ")
st.link_button("Conheça mais!", "https://pedrop.vercel.app/", help="Aprenda a programar do zero ao avançado!")

st.markdown("---")
st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px;'>
        App desenvolvido por Pedro Potz<br>
        Advogado especializado em soluções jurídico-tecnológicas<br>
        🦄 <em>Advogado que programa é unicórnio!</em>
        </div>
        """, unsafe_allow_html=True)

with sidebar:
    st.markdown("---")
    st.info(
        "[💤Análise de dados de Sono](https://sleepdataview.streamlit.app/)")
    st.info(
        "[Calculadoras Jurídicas Avançadas:](https://pedrocalc.streamlit.app/)")
    st.info("[Esqueça o Excel - O Futuro é aqui:](https://pedroduck.streamlit.app)")
    st.markdown("---")
    st.markdown(">Be aware- Dont Slip - Pelo Miau")