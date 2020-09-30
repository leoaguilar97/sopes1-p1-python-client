# Proyecto 1 - SOPES 1

Se deberá crear un programa escrito en Python. 

Este deberá leer el contenido de un archivo de texto, dividirlo en oraciones, luego creará un objeto por cada oración y le asociará un autor. 

Cada uno de estos elementos debe ser enviado al Balanceador de carga como una petición POST, debe hacerse una petición por cada objeto. 

El programa solicitará la ruta del archivo a dividir y la dirección a donde realizará las peticiones (la dirección del Balanceador ), almacenará los objetos
obtenidos del último análisis y podrá mostrarlos. 

## FORMATO DE ENVIO DE DATOS:

Se envían los datos de la siguiente manera:

```json 
{
    "author": "valor",
    "sentence": "valor"
}
```

## PARA CORRER EL CÓDIGO

Se requiere Python3 de 64 bits.
Se utilizó Python 3.8.6 y pip 20.2.3

`$ ​pip install virtualenv​`
`$ . venv/Scripts/activate`
`$ pip install --upgrade pip`
`$ pip install -r requirements.txt`
`$ cd code`
`$ python app.py`