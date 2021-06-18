import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


@st.cache
def get_data():
    import pandas as pd
    df = pd.read_csv("data/healthcare-dataset-stroke-data.csv")

    df.hypertension = df.hypertension.map(lambda v: "Sim" if v == 1 else "Não")
    df.heart_disease = df.heart_disease.map(lambda v: "Sim" if v == 1 else "Não")
    df.stroke = df.stroke.map(lambda v: "Sim" if v == 1 else "Não")

    return df


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
    side="negative",
    line_color="blue",
    hoverinfo="skip"
))

fig.add_trace(go.Violin(
    x=data[disease_option][data["stroke"] == "Sim"],
    y=data["age"][data["stroke"] == "Sim"],
    side="positive",
    line_color="red",
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

fig = px.scatter(
    data.query("bmi < 50"),
    x="bmi",
    y="avg_glucose_level",
    facet_col="stroke",
    color="age",
    labels={
        "bmi": "IMC",
        "avg_glucose_level": "Nível de glucose médio",
        "hypertension": "Hipertensão",
        "heart_disease": "Doença cardíaca"
    }
)

fig.add_hline(y=data.query("stroke == 'Sim'").avg_glucose_level.mean(), col=1, line_color="red")
fig.add_hline(y=data.query("stroke == 'Não'").avg_glucose_level.mean(), col=2, line_color="red")
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_traces(marker=dict(opacity=0.5))


st.plotly_chart(fig)

fig = px.box(data.query("age > 20"), x="ever_married", y="bmi")

st.plotly_chart(fig)
