from flask import Flask, request, jsonify, Response
import json
from modulos.data import get_dataframe
from extrapolacion import *

df = get_dataframe()

app = Flask(__name__)

@app.route("/censo", methods=['GET'])
def obtener_datos_censo_2022():
     json_data = json.dumps(df.to_dict(orient="records"), ensure_ascii=False)
     return Response(json_data, content_type='application/json; charset=utf-8')

@app.route("/censo/municipio", methods=['GET'])
def bucar_municipo():
     municipio =  df['municipio'].tolist()
     json_data = json.dumps(municipio, ensure_ascii=False)
     return Response(json_data, content_type='application/json; charset=utf-8')


@app.route("/censo/modelos", methods=['POST'])
def extrapolacion_basica():  
    try:
        # Obtener datos del POST
        data = request.json
        municipio = data['municipio']
        año = data['año']  # El año objetivo
        

        extrapolador = Extrapolacion(df, municipio, año, 2022)
        
        # Metodos
        arit = extrapolador.extrapolar_aritmetico()
        geo = extrapolador.extrapolar_geometrico()
        log = extrapolador.extrapolar_logaritmico()
        
        extrapolaciones = {
            "municipio": municipio,
            "año_base": 2022,
            "año_objetivo": año,
            "poblacion_base": int(extrapolador.poblacion_inicial),
            "estimacion_aritmetica": int(arit),
            "estimacion_geometrica": int(geo),
            "estimacion_logaritmica": int(log)
        }
        
        return jsonify(extrapolaciones) 
        
    except KeyError as e:
        return jsonify({"error": f"Campo requerido faltante: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
