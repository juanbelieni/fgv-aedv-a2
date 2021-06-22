import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="A2 de AEDV", )


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

# Justificativa dos elementos gráficos

st.header("Justificativa dos elementos gráficos")

st.write(
    "O primeiro gráfico apresentado se propõe a estudar a idade dos "
    "pacientes que tiveram e dos que não tiveram derrame, bem como analisar "
    "o impacto de hipertensão e doenças cardiovasculares nestes dados. Se "
    "espera encontrar grupos de risco para derrame, hipertensão e doenças "
    "cardiovasculares"
)

st.write(
    "O gráfico escolhido para isto havia inicialmente sido o _boxplot_, porém "
    "decidimos por utilizar o _violin plot_ que é uma versão melhorada do _boxplot_,"
    " mostrando com mais clareza a distribuição dos dados. Este tipo de gráfico é útil "
    "para entender como grupos demográficos estão distribuídos e é muito utilizado "
    "com o fim de ver a idade de um grupo. No eixo y do gráfico foi colocada a "
    "idade de maneira fixa, e no eixo x o gráfico recebeu dois parâmetros: \"sim\" ou "
    "\"não\" para uma determinada condição de saúde. Esta condição pode ser escolhida "
    "dinamicamente através do _Streamlit_ e as opções são se o paciente tem hipertensão "
    "ou se ele tem doenças cardiovasculares. Também foi segmentado em se o paciente "
    "teve ou não derrame, e para isto foi utilizada a variável cor com a posição: os "
    "pacientes que não tiveram derrame estão em verde à esquerda e os pacientes que "
    "tiveram derrame estão em vermelho à direita."
)

st.write(
    "A paleta de cores foi encontrada na internet através da plataforma "
    "[_Color Combos_](https://www.colorcombos.com/). Foi escolhida por possuir tons agradáveis "
    "de verde e vermelho, que são cores facilmente compreendidas como \"bom\" e \"ruim\" e "
    "pode ser encontrada [aqui](https://www.colorcombos.com/color-schemes/375/ColorCombo375.html)."
)

st.write(
    "No segundo gráfico foram estudadas variáveis relacionadas "
    "ao estado físico do paciente, desconsiderando-se as doenças "
    "observadas no gráfico 1. As variáveis utilizadas foram o Índice "
    "de Massa Corporal e o nível de glucose médio, ambos muito "
    "relacionados com o estilo de vida e alimentação do paciente. "
    "Posteriormente também mostramos que há uma correlação um pouco "
    "forte entre estas duas variáveis e a idade do paciente."
)

st.write(
    "O objetivo desta análise não é encontrar a relação do derrame com "
    "a idade, pois esta não pode ser prevenida, mas sim do derrame com "
    "as duas outras variáveis, pois, estas sim, podem ser alteradas através "
    "de um estilo de vida e alimentação mais saudáveis."
)

st.write(
    "Para fazer esta análise os pacientes também serão divididos entre "
    "os que tiveram derrame e os que não tiveram, e então deveria ser feito "
    "um gráfico de densidade para cada variável, como no gráfico 1, mas como "
    "também é interessante analisarmos a correlação entre o nível de glucose "
    "e o IMC, por serem duas variáveis relacionadas à saúde, decidimos por fazer "
    "um gráfico de dispersão facetado."
)


st.write(
    "Neste gráfico, cada variável fica em um eixo e é possível analisar se "
    "elas são correlatas ou não. Caso sejam, os pontos tendem a ficar em torno "
    "da linha $y=x$ (salvas proporções) ou $y=-x$. Caso não sejam correlatos é "
    "difícil achar alguma reta ou curva que possa descrever o lugar geométrico "
    "dos pontos com pouco erro."
)

st.write(
    "Sobre a paleta de cores, foi utilizada uma paleta do próprio _Plotly_, a "
    "\"burg\", que possuí um gradiente de cores bem intuitivo para a variável "
    "em que ela foi empregada, a idade."
)

# Gráfico 1

st.header("Gráfico 1")

st.write(
    "Nesse gráfico, tivemos o objetivo de comparar como a idade afeta "
    "a ocorrência de derrame em populações que possuíam e não um "
    "determinado tipo de doença. Abaixo, é possível filtrar os dados "
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
    "Neste gráfico houve uma dúvida sobre como foi realizada a coleta destes dados, "
    "se foi feita com uma amostragem enviesada ou não. Como não temos como confirmar "
    "isso, assumimos que os dados foram coletados de pacientes sem saber se eles já haviam "
    "enfermidades ou coisas do gênero."
)

st.write(
    "Para ambas as doenças, a incidência daqueles que tiveram algumas delas e/ou derrame "
    "se dá muito mais na população mais velha e, portanto, reconhecemos as pessoas mais idosas "
    "como grupo de risco."
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

st.write(
    "Tanto o nível de glucose médio quanto o IMC estão bem dispersos no gráfico. "
    "Por mais que a dispersão dos pontos pareça se dividir ao redor de dois núcleos principais, "
    "a variável ainda pode estar bem distribuída. Para analisar isto com mais precisão "
    "lançamos mão do coeficiente de correlação de Pearson. Ele equivale à covariância entre "
    "as variáveis dividida pela raiz do produto de suas variâncias individuais, e varia de 1 a -1."
    " Para calcular a correlação, foram utilizadas as seguintes linhas de código:"
)

st.code(
    "stroke_glucose_corr = df[\"stroke\"].corr(df[\"avg_glucose_level\"])\n"
    "stroke_bmi_corr = df[\"stroke\"].corr(df[\"bmi\"])",
    language="python"
)

mapped_data = data.copy()
mapped_data["stroke"] = mapped_data["stroke"].map(lambda s: 1 if s == "Sim" else 0)

stroke_glucose_corr = mapped_data["stroke"].corr(mapped_data["avg_glucose_level"])
stroke_bmi_corr = mapped_data["stroke"].corr(mapped_data["bmi"])

st.write(
    "Antes de mostrar as correlações, nossas previsões são de que ambas as "
    "variáveis possuirão correlações pequenas com o índice de derrame, mas "
    "não podemos afirmar o quão pequenas são essas correlações, sendo encontrar "
    "este valor o objetivo do cálculo delas."
)

st.write(
    f"A correlação entre derrame e o nível de glucose médio é de "
    f"**{stroke_glucose_corr:.4f}**, e a correlação entre derrame e o IMC "
    f"da pessoa é de **{stroke_bmi_corr:.4f}**, ambos pequenos, confirmando nossa "
    f"hipótese inicial. Este valor pequeno mostra que não importa "
    f"muito se a pessoa possuí um nível de glucose ou IMC menores, "
    f"que a chance de ter um derrame não é afetada por estes fatores. "
)

st.write("Esta pequena correlação existente talvez possa ser explicada por uma correlação residual da idade:")

age_stroke_corr = mapped_data["age"].corr(mapped_data["stroke"])
age_glucose_corr = mapped_data["age"].corr(mapped_data["avg_glucose_level"])
age_bmi_corr = mapped_data["age"].corr(mapped_data["bmi"])


st.write(f"Correlação da idade ☓ derrame: **{age_stroke_corr:.4f}**")
st.write(f"Correlação da idade ☓ glucose: **{age_glucose_corr:.4f}**")
st.write(f"Correlação da idade ☓ IMC: **{age_bmi_corr:.4f}**")

st.write(
    "Percebe-se que a correlação entre derrame e idade é bem maior que "
    "entre derrame e glucose ou IMC, e existe uma correlação grande entre "
    "idade e glucose ou IMC. Isto deve ser um ponto de atenção, pois, especialmente "
    "a correlação entre IMC e derrame, que ficou baixíssima, pode ser majoritariamente "
    "explicada por correlações indiretas."
)


st.header("Conclusão")

st.subheader("Insights")

st.write(
    "Com os gráficos e valores de dispersão analisados, chega-se à conclusão de que o "
    "maior fator de impacto é a idade, sendo relevante para os casos de derrame, hipertensão e "
    "doenças cardiovasculares. Portanto, deve-se ter uma atenção elevada para os pacientes idosos "
    "que correm risco de derrame ou algum dos outros quadros acima por outras questões como "
    "histórico na família."
)

st.write(
    "As variáveis “nível de glucose médio” e “IMC” possuem uma correlação bem pequena com os casos "
    "de derrame, porém estamos falando de um fator que pode ajudar a prever um problema grande de "
    "saúde altamente tratável se interceptado na fase inicial. Assim sendo, estas variáveis devem sim "
    "ser levadas em consideração. Também deve ser lembrado que ao contrário da idade, é possível "
    "trabalhar nestas variáveis, através de alimentação mais saudável e exercícios físicos, diminuindo "
    "a chance do derrame, mesmo que por pouco."
)

st.subheader("Escolha dos pacotes")

st.write(
    "Para o trabalho, decidimos utilizar o _Python_. Foi decidido isso como um desafio, "
    "para nos forçar a aplicar os conhecimentos de análise exploratória fora do _ggplot2_. "
    "Por isso, nos deparamos com a biblioteca [_Streamlit_](https://streamlit.io/), que permite "
    "fazer uma visualização interativa, porém agnóstica quanto a biblioteca de gráficos que é "
    "utilizada. Por isso, o [_Plotly_](https://plotly.com/) nos forneceu uma boa API para fazer os "
    "gráficos que desejávamos."
)

st.subheader("Dinâmica de trabalho")

st.write(
    "Inicialmente, dividimos para cada um os gráficos que gostaríamos que fossem feitos. Após isso, "
    "eu (Juan) me dediquei a descobrir as funcionalidades do _Streamlit_, enquanto o Vinícius se preocupou "
    "em fazer as análises. No fim, cada um revisou o trabalho um do outro, com o fim de validar o que foi feito. "
    "Além disso, foi utilizado o _GitHub_ para centralizar o código, e o _Heroku_ para fazer o deploy e a "
    "visualização conjunta."
)

st.header("Aprendizados")

st.subheader("Vinícius")

st.write(
    "> ‟Acredito que houveram vários pontos de aprendizado neste trabalho, incluindo sobre análise "
    "estatística, segmentação do dataframe, divisão de trabalho… mas sinto que meu maior aprendizado "
    "foi o ferramental utilizado. Ter a oportunidade de transpor os conhecimentos de R para Python foi "
    "muito bom, especialmente tendo acesso a grandes bibliotecas que provavelmente farão parte do dia "
    "a dia da minha carreira.”"
)

st.subheader("Juan")

st.write(
    "> ‟Eu sinto que meu maior aprendizado foi em como portar conhecimentos, antes contidos em apenas uma "
    "ferramenta, para outra com a sintaxe muito diferente. Por isso, foi necessário consultar bastante a "
    "documentação e olhar vários exemplos. Por essas coisas, tive a oportunidade de mexer com o _Pandas_ "
    " e o _Plotly_, importantes bibliotecas no mundo de visualização de dados.”"
)