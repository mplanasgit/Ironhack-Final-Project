import tools.cleaning as clean
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

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
    plt.xticks(rotation=45)

    # Add horizontal lines for air quality
    plt.axhline(y = 20, color = 'black', linestyle = 'dotted', alpha = 0.2, label = "Good")
    plt.axhline(y = 50, color = 'black', linestyle = 'dotted', alpha = 0.3, label = "Fair")
    plt.axhline(y = 100, color = 'black', linestyle = 'dotted', alpha = 0.4, label = "Poor")
    plt.axhline(y = 150, color = 'black', linestyle = 'dotted', alpha = 0.5, label = "Very Poor")

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

    return plt.show()