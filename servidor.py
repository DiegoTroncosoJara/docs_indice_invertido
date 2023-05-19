from flask import Flask

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Definir una ruta y una función de vista asociada
@app.route("/")
def hello():
    return "¡Hola,skdkskdsd mundo!"

# Ejecutar el servidor web si el script se ejecuta directamente
if __name__ == "__main__":
    app.run()
