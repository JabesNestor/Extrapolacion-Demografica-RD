import pandas as pd
import os
import math 
from datetime import datetime
file_path = 'data/poblacion.xlsx'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"El archivo '{file_path}' no existe. Verifica la ruta.")

try:
    df = pd.read_excel(file_path, sheet_name=1)
except ValueError as e:
    raise ValueError(f"Error al leer la hoja de cálculo: {e}")

#print(df.head(2))

class Incremento:
    POBLACION_2010 = 9445281
    POBLACION_2020 = 10760028
    DIAS_TRANSCURRIDOS = 28 + (8 * 365) + 317
    
    def __init__(self, df):
        self.df = df
        self.años_equivalentes = self.DIAS_TRANSCURRIDOS / 365
    
    def calcular_incremento_aritmetico(self):
        incremento_anual_lineal = ((self.POBLACION_2020 / self.POBLACION_2010) - 1) / self.años_equivalentes
        return incremento_anual_lineal
    
    def calcular_incremento_geometrico(self):
        r_geometrico = math.log(self.POBLACION_2020 / self.POBLACION_2010) / self.años_equivalentes
        return r_geometrico
    
    def calcular_incremento_logritmico(self):
       r_log = math.exp(math.log(self.POBLACION_2020 / self.POBLACION_2010) / self.años_equivalentes) - 1
       return r_log 
   
class Extrapolacion:
    FECHA_CENSO = datetime(2022,12, 11)
    
    def __init__(self,df,name,nn, nz):
        self.name = df[df['municipio'].str.lower() == name.lower()]
        if self.name.empty:
            raise ValueError(f"No se encontró el municipio '{name}' en el DataFrame.")
        self.nn = 2022  # Año actual 
        self.nz = nz # Años a extrapolar
        if nn < 2022:
            raise ValueError("El año de extrapolación debe ser mayor o igual a 2022.")
        self.df = df
        self.poblacion_inicial = self.name['Total'].iloc[0]  # Población en el año inicial
        self.periodo = nn - nz
        self.incremento_calc = Incremento(df)
        
    def extrapolar_aritmetico(self):
        """ 
        Extraplacion aritmetico formula: nz = nn +(nn x (rxn))
        """
        r_aritmetico = self.incremento_calc.calcular_incremento_aritmetico()  
        poblacion_extrapolada_ar = self.poblacion_inicial + (self.poblacion_inicial * r_aritmetico * self.periodo)
        return poblacion_extrapolada_ar
        
    def extrapolar_aritmetica_dias(self, fecha_objetivo):
        fecha_censo = datetime(2022, 11, 12)  # Fecha del censo
        fecha_target = datetime.strptime(fecha_objetivo, '%Y-%m-%d')
        
        dias_transcurridos = (fecha_target - fecha_censo).days
        años_transcurridos = dias_transcurridos / 365.25
        
        r_aritmetico = self.incremento_calc.calcular_incremento_aritmetico()  
        poblacion_extrapolada = self.poblacion_inicial + (self.poblacion_inicial * r_aritmetico * años_transcurridos)
        return print(f"Poblacion extrapolada usando el metodo aritmetico: {round(poblacion_extrapolada,1)} Dias transcurridos {dias_transcurridos}   Años transcurrido {round(años_transcurridos,2)}")
    
    def extrapolar_geometrico(self):
        """ 
        Formula: N= Nz x (1+r)
        """ 
        r_geometrico = self.incremento_calc.calcular_incremento_geometrico()  
        poblacion_extrapolada_ge = self.poblacion_inicial * math.exp(r_geometrico * self.periodo)  
        return poblacion_extrapolada_ge
    
    def extrapolar_geometrico_dias(self, fecha_objetivo):
        fecha_censo = datetime(2022, 11, 12)  
        fecha_target = datetime.strptime(fecha_objetivo, '%Y-%m-%d')
        
        dias_transcurridos = (fecha_target - fecha_censo).days
        años_transcurridos = dias_transcurridos / 365.25 
        
        r_geometrico = self.incremento_calc.calcular_incremento_geometrico()  
        poblacion_extrapolada_ge = self.poblacion_inicial * math.exp(r_geometrico * años_transcurridos)  
        return poblacion_extrapolada_ge
    
    def extrapolar_logaritmico(self):
        """
        Formula: N = N0 * e^(r * t) 
        """ 
        r_logaritmico = self.incremento_calc.calcular_incremento_logritmico()
        poblacion_extrapolada_log = self.poblacion_inicial * math.exp(r_logaritmico * self.periodo)
        return poblacion_extrapolada_log
    
    
    def extrapolar_logaritmica_dias(self, fecha_objetivo):
        fecha_censo = datetime(2022, 11, 12)
        fecha_target = datetime.strptime(fecha_objetivo, '%Y-%m-%d')
    
        dias_transcurridos = (fecha_target - fecha_censo).days
        años_transcurridos = dias_transcurridos / 365.25
    
        r_logaritmico = self.incremento_calc.calcular_incremento_logritmico()
        poblacion_extrapolada_log = self.poblacion_inicial * math.exp(r_logaritmico * años_transcurridos)
        return poblacion_extrapolada_log, dias_transcurridos, años_transcurridos
  
def test_todos_los_metodos():
    print("=== TEST TODOS LOS MÉTODOS ===")
    municipio_test = df['municipio'].iloc[0]
    print(f"Probando: {municipio_test}")
    
""" 
# Test básico de carga
#print("=== TEST 1: Carga de datos ===")
#print(f"Municipios disponibles: {len(df)}")
#print(f"Primeros municipios: {df['municipio'].head(3).tolist()}")
#print()
"""
