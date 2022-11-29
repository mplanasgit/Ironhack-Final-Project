import streamlit as st
import plotly.express as px
import src.tools.sql_query as sql
import streamlit.components.v1 as components
import codecs
from PIL import Image

# Explanation
image=Image.open('./images/seasonality_index_calculation.jpg')
col1, col2 = st.columns(2)
with col1:
    st.title('PM10 Seasonality')
    st.markdown('#### Seasonality index')
    st.markdown('- Grouped by Year and Month')
    st.markdown('- Difference between max and min concentration values')
    st.markdown('- The greater the difference, the greater the seasonality')
with col2:
    st.image(image, width=350)

# Plot: Seasonality index by city
seasonality = sql.get_country('seasonality_index')
seasonality = seasonality.sort_values(by=['Seasonality index'])
seasonality['Seasonality index'] = round(seasonality['Seasonality index'], 2)
fig = px.scatter(seasonality, y="Seasonality index", x="City",
                 title="Seasonality index of European capitals", 
                 color="Seasonality index",
                 color_continuous_scale='Redor')
fig.update_traces(marker=dict(size=12))
fig.update_layout(
    yaxis_range=[0,80],
    title={'y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'})

for city, value in zip(seasonality['City'], seasonality['Seasonality index']):
    fig.add_shape(type='line',
                x0=city,
                y0=0,
                x1=city,
                y1=value-1.5,
                line=dict(color='black',dash="dot", width=1))
st.plotly_chart(fig)

# -----------------------------------------------------------------------------------------------------------------
st.markdown('#### The cities with the highest seasonality index are geographically related')

# Map: Seasonality index by city
f=codecs.open("./src/output/global/seasonality_index_map.html", 'r')
seasonality_map = f.read()
components.html(seasonality_map,height=600,scrolling=False)


st.markdown('')
image0=Image.open('./images/Balkan_Peninsula.png')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(' ')
with col2:
    st.image(image0)
with col3:
    st.write(' ')

st.write(' ')
image1 = Image.open('./images/balkans_pollution_news.jpg')
st.image(image1)