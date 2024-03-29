#Librerías.
import numpy as np
import pandas as pd

#Base de datos.
team_stats = pd.read_csv('team_stats.csv')

# Se elimina el primer caracter de la columna 'TEAM' porque en la base de datos original hay un
# espacio antes del nombre del equipo.
team_stats['TEAM'] = team_stats['TEAM'].str[1:]

#Función conteo_record.
# Función que crea tres columnas: número de partidos ganados ('GW'), partidos perdidos ('GL')
# y una variable que indica si el equipo tiene un record negativo (0), record neutral (1) o record
# positivo (1) después de ese partido.
def conteo_record(equipos):
    equipos['GW'] = equipos['W/L'].eq('W').groupby(equipos['TEAM']).cumsum()
    equipos['GL'] = equipos['W/L'].eq('L').groupby(equipos['TEAM']).cumsum()
    equipos['REC'] = np.where(equipos['GW'] > equipos['GL'], 2, np.where(equipos['GW'] == equipos['GL'], 1, 0))

conteo_record(team_stats)

# El siguiente código descarga la nueva base de datos como csv:
team_stats.to_csv('team_stats_record.csv', index=False)
