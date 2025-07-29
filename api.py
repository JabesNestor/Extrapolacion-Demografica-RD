from flask import Flask, request, jsonify 
app = Flask(__name__)
# Mas adelante, agregare la ruta de la api
@app.route("/")
def hello():
    return #agregar mas adelante
if __name__ == "__main__":
    app.run(debug=True)