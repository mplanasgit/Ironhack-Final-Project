import tools.cleaning as clean
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import plotly.express as px

# Seasons:
# Primavera: inicia el 20 de marzo al 21 de junio.
# Verano: inicia el 21 de junio y finaliza el 23 de septiembre.
# Otoño: inicia el 23 de septiembre y finaliza el 21 de diciembre.
# Invierno: inicia el 21 de diciembre y finaliza el 20 de marzo.

# ------------------------------------------------------------------------------------------------------------
def plot_lineplot_timeseries(name,year_min,year_max):
    # Load df and transform datetime
    df = pd.read_csv(f'../data/EEA/All/Date_extracted/{name}_pm10_extracted.csv')
    clean.transform_datetime(df,'Datetime')
    
    # Build fig environment
    fig, ax = plt.subplots()
    
    # Actual plot
    sns.lineplot(x="Datetime", y="Concentration", 
    data=df[(df['Year'] >= year_min) & (df['Year'] < year_max)], 
    ax=ax, color='black', linewidth = 0.5)
    plt.ylim(bottom = 0)

    # Color seasons
    for i in range(year_min,year_max):
        ax.axvspan(f'{i}-03-20',f'{i}-06-20', color="green", alpha=0.1) # spring
        ax.axvspan(f'{i}-06-21',f'{i}-09-22', color="orange", alpha=0.1) # summer
        ax.axvspan(f'{i}-09-23',f'{i}-12-20', color="brown", alpha=0.1) # fall
        ax.axvspan(f'{i}-12-21',f'{i}-12-31', facecolor="blue", alpha=0.1) # winter
        ax.axvspan(f'{i}-01-01',f'{i}-03-19', facecolor="blue", alpha=0.1) # winter
    # plt.xticks(rotation=45)
    plt.title(f"PM10 concentration evolution in {name}", y = 1.02, fontweight="bold", fontsize = 15)
    plt.ylabel("Concentration of PM10 [µg/m$^3$]")
    plt.xlabel("Year")

    # Add horizontal lines for air quality
    plt.axhline(y = 20, color = 'black', linestyle = 'dotted', alpha = 0.2, label = "Good")
    plt.axhline(y = 50, color = 'black', linestyle = 'dotted', alpha = 0.4, label = "Fair")
    plt.axhline(y = 100, color = 'black', linestyle = 'dotted', alpha = 0.6, label = "Poor")
    plt.axhline(y = 150, color = 'black', linestyle = 'dotted', alpha = 0.8, label = "Very Poor")

    # Add custom legend for seasons (Patch) and air quality (Line2D)
    legend_elements = [Patch(color='blue', alpha = 0.2, label='Winter'), 
                        Patch(color='green', alpha = 0.2, label='Spring'),
                        Patch(color='orange', alpha = 0.2, label='Summer'), 
                        Patch(color='brown', alpha = 0.2, label='Fall'),
                    Line2D([0], [0], lw=0, label = ''),
                        Line2D([0], [0], color='black', lw=1, label = 'Very Poor',linestyle = 'dotted', alpha = 1),
                        Line2D([0], [0], color='black', lw=1, label = 'Poor',linestyle = 'dotted', alpha = 0.8),
                        Line2D([0], [0], color='black', lw=1, label = 'Fair',linestyle = 'dotted', alpha = 0.6),
                        Line2D([0], [0], color='black', lw=1, label = 'Good',linestyle = 'dotted', alpha = 0.4)
    ]
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1))
    fig.savefig(f"./output/time_series/{name}.jpg", dpi=1000, bbox_inches='tight')
    return plt.show()

# ------------------------------------------------------------------------------------------------------------
def plot_map(df, geo_json, match_location, value_plotted, animation, palette, range):
    fig = px.choropleth_mapbox(data_frame=df,
                            geojson=geo_json,
                            locations=df[match_location],
                            featureidkey = 'properties.name',
                            color=value_plotted,
                            center={'lat':58, 'lon':10},
                            mapbox_style='open-street-map',
                            zoom=2,
                            color_continuous_scale=palette,
                            range_color=(range[0], range[1]),
                            animation_frame=animation,
                            width=850,
                            height=650)
    return fig

# ------------------------------------------------------------------------------------------------------------
def plot_lineplot(df, location_subset, x, y, order_legend, title):
    # Subset
    location = location_subset
    dataset = df[df['Location'].isin(location)]
    # plot
    fig = sns.lineplot(x=x, y=y, data=dataset, hue='Location', marker='o', palette='Set1');
    plt.title(title, y = 1.02, fontweight="bold", fontsize = 15);
    # reordering the labels
    handles, labels = plt.gca().get_legend_handles_labels()
    # pass handle & labels lists along with order as below
    plt.legend([handles[i] for i in order_legend], [labels[i] for i in order_legend])
    return fig