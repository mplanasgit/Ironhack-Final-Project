import plotly.express as px

# ------------------------------------------------------------------------------------------------------------
# Function to plot seasonality index
def plot_seasonality_index(df):
    df = df.sort_values(by=['Seasonality index'])
    df['Seasonality index'] = round(df['Seasonality index'], 2)
    fig = px.scatter(df, y="Seasonality index", x="City",
                    title="<b>Seasonality index of European capitals</b>", 
                    color="Seasonality index",
                    color_continuous_scale='Redor')
    fig.update_traces(marker=dict(size=12))
    fig.update_layout(
        yaxis_range=[0,80],
        title={'y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'})

    for city, value in zip(df['City'], df['Seasonality index']):
        fig.add_shape(type='line',
                    x0=city,
                    y0=0,
                    x1=city,
                    y1=value-1.5,
                    line=dict(color='black',dash="dot", width=1))
    return fig

# ------------------------------------------------------------------------------------------------------------
# Function to plot timeseries
def plot_timeseries(df):
    # Define figure
    fig = px.line(data_frame=df, x='Datetime', y="Concentration")
    fig.update_traces(line_color='black', line_width=1)
    # Modify axes labels
    fig.update_xaxes( 
            title_text = "Year",
            title_font = {"size": 15},
            title_standoff = 10)
    fig.update_yaxes( 
            title_text = "Concentration [µg/m3]",
            title_font = {"size": 15},
            title_standoff = 10)
    # Add air quality thresholds
    air_quality = {0: 'Good', 20:'Fair', 50:'Poor', 100:'Very Poor', 150:'Extremelly Poor'}
    for key, value in air_quality.items():
        fig.add_hline(
            y=key, 
            line_dash="dot",
            line_color='black',
            annotation_text=f'<b>{value}</b>', 
            annotation_position="top right",
            annotation=dict(font_size=12, font_color='black'),
            opacity=0.5)
    # Add seasons
    for i in range(2013,2022):
            fig.add_vrect(x0=f'{i}-03-20', x1=f'{i}-06-20', fillcolor='green', opacity=0.15, line_width=1)
            fig.add_vrect(x0=f'{i}-06-21', x1=f'{i}-09-22', fillcolor='orange', opacity=0.15, line_width=1)
            fig.add_vrect(x0=f'{i}-09-23', x1=f'{i}-12-20', fillcolor='brown', opacity=0.15, line_width=1)
            fig.add_vrect(x0=f'{i}-12-21', x1=f'{i}-12-31', fillcolor='blue', opacity=0.15, line_width=1)
            fig.add_vrect(x0=f'{i}-01-01', x1=f'{i}-03-19', fillcolor='blue', opacity=0.15, line_width=1)
    # Show plot
    return fig

# ------------------------------------------------------------------------------------------------------------
# Function to plot timeseries given date
def plot_timeseries_period(df):
    fig = px.line(data_frame=df, x='Datetime', y="Concentration")
    fig.update_traces(line_color='black', line_width=1)
    fig.update_xaxes( 
    title_text = "Period of time",
    title_font = {"size": 15},
    title_standoff = 10)
    fig.update_yaxes( 
            title_text = "Concentration [µg/m3]",
            title_font = {"size": 15},
            title_standoff = 10)
    air_quality = {0: 'Good', 20:'Fair', 40:'Moderate', 50:'Poor', 100:'Very Poor', 150:'Extremelly Poor'}
    for key, value in air_quality.items():
            fig.add_hline(
            y=key, 
            line_dash="dot",
            line_color='black',
            annotation_text=f'<b>{value}</b>', 
            annotation_position="top right",
            annotation=dict(font_size=12, font_color='black'),
            opacity=0.5)
    return fig