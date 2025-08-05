# data.py
import pandas as pd

def get_dataframe():
    file_path = 'data/poblacion.xlsx'
    df = pd.read_excel(file_path, sheet_name=1)
    return df

