#Librerías
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Base de datos
team_stats = pd.read_csv('team_stats.csv')

#Función matriz_correlación
def matriz_correlacion(dataframe, columnas):

    # Se extraen las columnas indicadas del dataframe indicado.
    sub_dataframe = dataframe[columnas]

    # Se calcula la matriz de correlación entre las columnas seleccionadas.
    matriz_correlacion = sub_dataframe.corr()

    # Se ajuste el tamaño de la gráfica para obtener resultados visualmente atractivos.
    plt.figure(figsize=(len(columnas), len(columnas)))

    # Se grafica la matriz mostrando las correlaciones con dos cifras decimales. Se utilizó una paleta de
    #colores secuencial para facilitar la lectura.
    sns.heatmap(matriz_correlacion, annot=True, cmap='seismic', fmt=".2f", linewidths=0.4, vmin=-1, vmax=1)

    # Se le asigna un título al gráfico y se muestra.
    plt.title('Matriz de Correlación')
    plt.show()

#Selección de columnas y llamada de función
# Para esta matriz de correlación, se utilizan únicamente las variables númericas
cols = ['MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB',
        'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']

matriz_correlacion(team_stats, cols)
