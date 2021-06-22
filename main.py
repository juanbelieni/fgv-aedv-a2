import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="A2 de AEDV")


@st.cache
def get_data():
    import pandas as pd
    df = pd.read_csv("data/healthcare-dataset-stroke-data.csv")

    df.hypertension = df.hypertension.map(lambda v: "Sim" if v == 1 else "Não")
    df.heart_disease = df.heart_disease.map(lambda v: "Sim" if v == 1 else "Não")
    df.stroke = df.stroke.map(lambda v: "Sim" if v == 1 else "Não")

    return df


st.title("A2 de AEDV")

st.write(
    "A base de dados escolhida foi a "
    "[Stroke Prediction Dataset | Kaggle](https://www.kaggle.com/fedesoriano/stroke-prediction-dataset), "
    "por possuir dados de tipos diversos e que permitem uma boa "
    "análise exploratória com potenciais insights sobre a correlação entre os casos e os dados."
)

# Gráfico 1

st.header("Gráfico 1")

st.write(
    "Nesse gráfico, tivemos o objetivo de comparar como a idade afeta "
    "a ocorrência de derrame em populações que possuíam e não possuíam"
    "um determinado tipo de doença. Abaixo, é possível filtrar os dados "
    "dinamicamente."
)

data = get_data()

disease_options = {
    "hypertension": "Hipertensão",
    "heart_disease": "Doença cardíaca"
}

disease_option = st.selectbox(
    label="Doença",
    options=list(disease_options.keys()),
    format_func=lambda k: disease_options[k]
)

fig = go.Figure()

fig.add_trace(go.Violin(
    x=data[disease_option][data["stroke"] == "Não"],
    y=data["age"][data["stroke"] == "Não"],
    name='Não teve derrame',
    side="negative",
    line_color="#A9CF54",
    hoverinfo="skip"
))

fig.add_trace(go.Violin(
    x=data[disease_option][data["stroke"] == "Sim"],
    y=data["age"][data["stroke"] == "Sim"],
    name='Teve derrame',
    side="positive",
    line_color="#F1433F",
    hoverinfo="skip"
))

fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_traces(meanline_visible=True)
fig.update_layout(
    xaxis_title=disease_options[disease_option],
    yaxis_title="Idade",
    hovermode="y",
    violinmode="overlay"
)

st.plotly_chart(fig)

st.write(
    "Para ambas as doenças, a incidência daqueles que tiveram algumas delas e/ou derrame "
    "se dá muito mais na população mais velha. Como não sabemos o método de coleta desses "
    "dados, só é possível concluir que ..."
)

# Gráfico 2

st.header("Gráfico 2")

st.write(
    "Para essa análise, buscamos uma que permitisse "
    "visualizar a dispersão da ocorrência de derrame ou não de acordo "
    "com o nível de glucose médio e o IMC dos pacientes."
)

st.write(
    "Além disso, foi adicionada uma barra horizontal com a valor numérico da "
    "média geral do nível de glucose para cada caso."
)

fig = px.scatter(
    data.query("bmi < 50"),
    x="bmi",
    y="avg_glucose_level",
    facet_col="stroke",
    color="age",
    color_continuous_scale="burg",
    labels={
        "bmi": "IMC",
        "avg_glucose_level": "Nível de glucose médio",
        "hypertension": "Hipertensão",
        "heart_disease": "Doença cardíaca",
        "age": "Idade",
        "stroke": "Teve derrame"
    }
)

stroke_mean_glucose_level = int(data.query("stroke == 'Sim'").avg_glucose_level.mean())
not_stroke_mean_glucose_level = int(data.query("stroke == 'Não'").avg_glucose_level.mean())

fig.add_hline(
    y=stroke_mean_glucose_level,
    col=1,
    line_color="black",
    annotation_text=stroke_mean_glucose_level,
    annotation_font_size=12,
    annotation_font_color="black",
    annotation_position="top left"
)
fig.add_hline(
    y=not_stroke_mean_glucose_level,
    col=2,
    line_color="black",
    annotation_text=not_stroke_mean_glucose_level,
    annotation_font_size=12,
    annotation_font_color="black",
    annotation_position="top left"
)
fig.update_traces(marker=dict(opacity=0.5))

st.plotly_chart(fig)
