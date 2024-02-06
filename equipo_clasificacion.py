# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 00:50:30 2024

@author: alexd
"""

import pandas as pd

team_stats = pd.read_csv('team_stats_conteo.csv')

teams = team_stats['TEAM'].unique()
p_g = []

for i in range(81, 2460, 82):
    p_g.append(team_stats["GW"][i])
del i

data = {"Equipo": teams, "Partidos Ganados": p_g}
partidos_ganados = pd.DataFrame(data)

partidos_ganados = partidos_ganados.sort_values(by='Partidos Ganados', ascending=False)

print(partidos_ganados)

equipos = partidos_ganados['Equipo'].tolist()

equipos_top = equipos[:10]
equipos_mid = equipos[10:20]
equipos_bottom = equipos[20:30]


#%% Medias por clasificación

def obtener_medias_por_clasificacion(team_stats, equipos, clasificaciones):
    estadisticas_dict = {}

    for clasificacion in clasificaciones:
        estadisticas_clasificacion = {}
        
        for equipo in equipos:
            eq_vs_clasi = team_stats[(team_stats['TEAM'] == equipo) & (team_stats['VS'].isin(clasificacion))]
            columns_numericas = eq_vs_clasi.select_dtypes(include='number').columns
            media_stats = eq_vs_clasi[columns_numericas].mean()
            
            estadisticas_clasificacion[equipo] = media_stats
        
        estadisticas_dict[tuple(clasificacion)] = estadisticas_clasificacion
    
    return estadisticas_dict

clasificaciones = [equipos_top, equipos_mid, equipos_bottom]
medias_dict = obtener_medias_por_clasificacion(team_stats, teams, clasificaciones)


medias_vs_top = pd.DataFrame(medias_dict[tuple(equipos_top)])
medias_vs_mid = pd.DataFrame(medias_dict[tuple(equipos_mid)])
medias_vs_bottom = pd.DataFrame(medias_dict[tuple(equipos_bottom)])


#%% Varianzas por clasificación

def obtener_varianzas_por_clasificacion(team_stats, equipos, clasificaciones):
    estadisticas_dict = {}

    for clasificacion in clasificaciones:
        estadisticas_clasificacion = {}
        
        for equipo in equipos:
            eq_vs_clasi = team_stats[(team_stats['TEAM'] == equipo) & (team_stats['VS'].isin(clasificacion))]
            columns_numericas = eq_vs_clasi.select_dtypes(include='number').columns
            varianza_stats = eq_vs_clasi[columns_numericas].var()    
            estadisticas_clasificacion[equipo] = varianza_stats
            
        estadisticas_dict[tuple(clasificacion)] = estadisticas_clasificacion
    
    return estadisticas_dict


varianzas_dict = obtener_varianzas_por_clasificacion(team_stats, teams, clasificaciones)

varianzas_vs_top = pd.DataFrame(varianzas_dict[tuple(equipos_top)])
varianzas_vs_mid = pd.DataFrame(varianzas_dict[tuple(equipos_mid)])
varianzas_vs_bottom = pd.DataFrame(varianzas_dict[tuple(equipos_bottom)])

#%% Desviaciones estándar por clasificación

def obtener_desviaciones_estandar_por_clasificacion(team_stats, equipos, clasificaciones):
    estadisticas_dict = {}

    for clasificacion in clasificaciones:
        estadisticas_clasificacion = {}
        
        for equipo in equipos:
            eq_vs_clasi = team_stats[(team_stats['TEAM'] == equipo) & (team_stats['VS'].isin(clasificacion))]
            columns_numericas = eq_vs_clasi.select_dtypes(include='number').columns
            desviacion_stats = eq_vs_clasi[columns_numericas].std()  # Cambiando var() por std()
            
            estadisticas_clasificacion[equipo] = desviacion_stats

        estadisticas_dict[tuple(clasificacion)] = estadisticas_clasificacion
    
    return estadisticas_dict

desviaciones_dict = obtener_desviaciones_estandar_por_clasificacion(team_stats, teams, clasificaciones)

desviaciones_vs_top = pd.DataFrame(desviaciones_dict[tuple(equipos_top)])
desviaciones_vs_mid = pd.DataFrame(desviaciones_dict[tuple(equipos_mid)])
desviaciones_vs_bottom = pd.DataFrame(desviaciones_dict[tuple(equipos_bottom)])


#%% Visualización


import matplotlib.pyplot as plt
import numpy as np

# Función para visualizar medias y desviaciones estándar de todos los equipos de mayor a menor
def visualizar_datos(variable, clasificacion):
    medias = medias_vs_top.loc[variable]
    desviaciones = desviaciones_vs_top.loc[variable]
    sorted_indices = np.argsort(medias.values)[::-1]
    variables = medias.index[sorted_indices]
    sorted_medias = medias.iloc[sorted_indices]
    sorted_desviaciones = desviaciones.iloc[sorted_indices]

    plt.figure(figsize=(10, 6))
    plt.bar(variables, sorted_medias, yerr=sorted_desviaciones, capsize=5, color='red', alpha=0.7)

    plt.title(f'Medias y Desviaciones Estándar vs {clasificacion}')
    plt.xlabel(variable)
    plt.ylabel('Valor')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

visualizar_datos('FGM','equipos top')

#%%Función comparativa

# Función que crea un conjunto de gráficas de barras para comparar las medias y desviaciones estádar de las estadísiticas de un
#equipo en diferentes variables, clasificadas por equipos de nivel superior (Top Teams), equipos de nivel medio (Mid Teams) y
#equipos de nivel inferior (Bottom Teams).

def comparar_medias_con_desviacion_estandar(equipo, var_teams):
    num_vars = len(var_teams)
    num_rows = num_vars // 4
    num_cols = min(4, num_vars)
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(15, num_rows*2))
    fig.suptitle(f'Comparación de medias con desviación estándar {equipo} vs Clasificación', fontsize=16)
    color = 'red'

    for i, var in enumerate(var_teams[:num_rows * num_cols]):
        medias = [
            medias_vs_top.loc[var, equipo],
            medias_vs_mid.loc[var, equipo],
            medias_vs_bottom.loc[var, equipo]
        ]
        desviaciones = [
            desviaciones_vs_top.loc[var, equipo],
            desviaciones_vs_mid.loc[var, equipo],
            desviaciones_vs_bottom.loc[var, equipo]
        ]

        row, col = divmod(i, num_cols)
        ax = axes[row, col]

        if not all(m == 0 for m in medias):
            ax.bar(['Top Teams', 'Mid Teams', 'Bottom Teams'], medias, yerr=desviaciones, capsize=5, color=color, alpha=0.7)
            ax.set_title(f'{var}')

            if col == 0:
                ax.set_ylabel('Media', fontsize=10)
                
            if row == num_rows - 1:
                ax.set_xlabel('Categorías', fontsize=10)

            if col != 0:
                ax.set_yticklabels([])

            if row != num_rows - 1:
                ax.set_xticklabels([])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

var_teams = medias_vs_top.index.tolist()
comparar_medias_con_desviacion_estandar('MIL', var_teams)


    

