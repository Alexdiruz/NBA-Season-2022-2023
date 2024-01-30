#Librerías.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Base de datos.
team_stats = pd.read_csv('team_stats.csv')

def matriz_correlacion(dataframe, columnas):

    # Se extraen las columnas indicadas del dataframe indicado.
    sub_dataframe = dataframe[columnas]

    # Se calcula la matriz de correlación entre las columnas seleccionadas.
    matriz_correlacion = sub_dataframe.corr()

    # Se ajuste el tamaño de la gráfica para obtener resultados visualmente atractivos.
    plt.figure(figsize=(len(columnas), len(columnas)))

    # Se grafica la matriz mostrando las correlaciones con dos cifras decimales. Se utilizó una paleta de
    #colores secuencial para facilitar la visualización.
    sns.heatmap(matriz_correlacion, annot=True, cmap='seismic', fmt=".2f", linewidths=0.4, vmin=-1, vmax=1)
    plt.title('Matriz de Correlación')
    plt.show()

#Selección de columnas y activación de función.
# Para esta matriz de correlación se utilizan únicamente variables numéricas.
cols = ['MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB',
        'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']

matriz_correlacion(team_stats, cols)

#Resultados:
#Nota: Los valores de correlación se encuentran estrictamente entre -1 y 1. Se considera que un valor mayor a 0.5 y menor 
#a 0.75 es una correlación moderada y mayor a 0.75 es una correlación fuerte.

#Correlaciones moderadas: 'FG%' vs 'AST': 0.53, 'PTS' vs '3P%': 0.54, 'FG%' vs '3P%': 0.54, 'PTS' vs 'AST': 0.55, 'FGA' vs 'OREB': 0.59, 'FGM' vs 'AST': 0.60,
#'OREB' vs 'REB': 0.61, 'PTS' vs 'FG%': 0.70, '3PM' vs '3PA': 0.70.

#Correlaciones fuertes: 'FGM' vs 'FG%': 0.76, '3PM' vs '3P%': 0.76, 'DREB' vs 'REB': 0.81, 'PTS' vs 'FGM': 0.84, 'FTM' vs 'FTA': 0.92.

