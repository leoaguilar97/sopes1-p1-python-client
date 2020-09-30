from re import error
import sys
import time
import random
from colored import colors
from requests.sessions import Request
import spacy
import colored
import names
import requests
import json

from terminaltables import DoubleTable
from colored import stylize
from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *

author_names = []
all_author_colors = [163, 154, 9, 4, 1, 13, 17, 18, 22, 23, 25, 38, 40, 50, 52, 53, 94, 166, 8, 63, 27, 75, 124, 147, 88, 2, 6, 110, 160, 200, 202, 102, 130, 86]

data = []
ip = ""
url = "/data"

blue = colored.fg("dark_blue") + colored.bg("light_blue") + \
    colored.attr("bold")

magenta = colored.fg("light_magenta") + colored.attr("blink")

green = colored.fg("dark_green") + \
    colored.bg("light_green") + colored.attr("bold")

orange = colored.fg("white") + \
    colored.bg("dark_orange_3a") + colored.attr("bold")

red = colored.fg("dark_red_1") + colored.bg("light_red") + colored.attr("bold")

def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == "...":
            doc[token.i+1].is_sent_start = True
        if token.text == "–":
            doc[token.i].is_sent_start = True
        if token.text == "-":
            doc[token.i].is_sent_start = True
    return doc

nlp = spacy.load("es_core_news_sm")
nlp.add_pipe(set_custom_boundaries, before="parser")

def print_data():

    print("")
    print(stylize(" ORACIONES ", blue))
    print("")
    print(stylize(str(len(data)) +
                  " oraciones encontradas y emparejadas con su autor", magenta))

    print("")
    print(stylize(" AUTORES ", blue))
    print("")
    print(stylize("Hay " + str(len(author_names)) + " emparejados...", magenta))

    for author in author_names:
        print("*", stylize(" " + author["name"] + " ", colored.fg("white") + colored.bg(author["color"]) + colored.attr("bold")))

def progress(count, total, status=''):
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def leer_archivo():

    print(stylize(" ABRIENDO ARCHIVO ", green))
    print("")

    while (True):
        fname = ''

        try:
            print(stylize(" ELIGIENDO ARCHIVO ", green))
            print("")
            fname = Screen().input(">> Ingresar una ruta completa (sin comillas encerrandolo): ")
            if (fname == ""):
                #fname = "C:\\Users\\leoag\\OneDrive\\Documents\\Universidad\\SOPES1\\Proyecto 1\\texto3.txt"
                fname = "../data.txt"
            f = open(fname, 'r', encoding='utf-8')

            print(stylize(" ARCHIVO ACEPTADO ", green))
            print("")
            with f:
                text = f.read()

            print(stylize(" << " + fname + " >> ",
                          blue, colored.attr("underlined")))
            print("")
            print(text)
            print(stylize(" << " + fname + " >>",
                          blue, colored.attr("underlined")))
            print("")

            option = Screen().input(">> ¿Desea cambiar el archivo? (y/n): ")
            if (option != "y"):
                break

        except OSError as e:
            print(stylize(" ¡ERROR! ", red))
            print(
                stylize("El archivo [" + fname + "] no se puede procesar.", colored.fg("red")))
            if hasattr(e, 'message'):
                print(stylize(e.message, colored.fg("red_3a")))
            else:
                print(stylize(e, colored.fg("red_3a")))

            Screen().input('Presiona [Enter] para continuar')

            print("")
            print("")

    print("")
    print(stylize(" SEPARANDO POR ORACIONES ", green))
    print("")

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    time.sleep(1)
    print(stylize(str(len(sentences)) + " oraciones encontradas", magenta))

    print("")
    print(stylize(" CARGANDO AUTORES ", green))
    print("")

    autors_length = random.randint(3, 10)
    author_names.clear()

    for x in range(autors_length):
        author_name = names.get_full_name()
        author_names.append({ "name" : author_name, "color": random.choice(all_author_colors) })
        progress(x, autors_length, status='Buscando un autor')
        time.sleep(0.1)

    progress(autors_length, autors_length, status='Autores agregados')
    time.sleep(0.1)

    sys.stdout.flush()
    print("")
    print(stylize(str(autors_length) + " autores asignados", magenta))

    print("")
    print(stylize(" SEPARANDO POR ORACIONES ", green))
    print("")
    i = 1
    total = len(sentences)
    data.clear()
    for sent in sentences:
        i = i + 1
        data.append([str(sent).strip(), random.choice(author_names)])
        progress(i, total, status='Emparejando oraciones')
        #time.sleep(0.05)

    progress(total, total, status='Oraciones emparejadas')

    sys.stdout.flush()
    print("")
    print(stylize(" CARGA FINALIZADA ", green))
    print("")

    print_data()
    print("")
    Screen().input('Presiona [Enter] para continuar')

def leer_ip():
    global ip
    global url

    print(stylize(" INTRODUCIR DIRECCION IP ", green))
    print("")
    print(stylize(" Ejemplo: http://127.0.0.1", magenta))
    print("")

    while True:
        try:
            ip = str(Screen().input(">> Dirección: ")).lower()
            if (ip == ""):
                ip = "127.0.0.1:3000"
            if not "http" in ip:
                ip = "http://" + ip
            break
        except Exception:
            print("")
            print(stylize(" ERROR ", red))
            print(stylize("Ingrese un IP válido", colored.fg("red")))

        print("")
        print(stylize(" INTRODUCIR DIRECCION IP ", green))

    print("")

    print(stylize(" COMPROBANDO LA DIRECCIÓN [" + ip + "] ", green))
    print("")
    try:
        x = requests.get(ip)

        print(stylize(" PETICION CORRECTA ", blue))
        print("")
        print(stylize("Respuesta: " + str(x.json()), magenta))
        print(stylize("Codigo: " + str(x.status_code), magenta))

    except requests.exceptions.Timeout:
        print(stylize(" ERROR ", red))
        print(stylize("La conexion se tardo demasiado en responder", colored.fg("red")))

    except requests.exceptions.RequestException as e:
        print(stylize(" ERROR ", red))
        print(stylize("Hubo un error con la peticion", colored.fg("red")))
        if hasattr(e, 'message'):
            print(stylize(e.message, colored.fg("red_3a")))
        else:
            print(stylize(e, colored.fg("red_3a")))

    except requests.exceptions.InvalidURL as e:
        print(stylize(" ERROR ", red))
        print(stylize("La direccion proporcionada no es valida", colored.fg("red")))

    except Exception as e:
        print(stylize(" ERROR ", red))
        print(stylize("Hubo un error con la peticion", colored.fg("red")))
        if hasattr(e, 'message'):
            print(stylize(e.message, colored.fg("red_3a")))
        else:
            print(stylize(e, colored.fg("red_3a")))

    print("")

    print(stylize(" INTRODUCIR URL AL QUE DEBE HACER POST ", green))
    print("")
    print(stylize(" Ejemplo-Default: /data", magenta))
    print("")

    tmp_url = str(Screen().input(">> Url: ")).lower()
    
    if tmp_url != "" and not "/" in tmp_url:
        tmp_url = "/" + tmp_url

    url = url if tmp_url == "" else tmp_url

    print(stylize(" SE UTILIZARÁ EL URL [" + url + "] ", blue))
    print("")
    
    Screen().input('Presiona [Enter] para continuar')

def table_data():
    if (len(data) == 0):
        print(stylize(" POR FAVOR INGRESA LOS DATOS DEL ARCHIVO ", orange))
        print("")
        leer_archivo()

    sys.stdout.flush()
    print("")
    print(stylize(" DATOS RECOLECTADOS DEL ARCHIVO ", green))
    print("")
    tbl_data = [None] * (len(data) + 1)
    tbl_data[0] = ['#', 'Oración', 'Autor']

    for i in range(0, len(data)):
        tbl_data[i + 1] = [i + 1, data[i][0], data[i][1]["name"]]

    table = DoubleTable(tbl_data, " Datos ")
    if not table.ok:
        print(stylize(" NO SE MUESTRAN LAS ORACIONES COMPLETAS (Debido al espacio) ", orange))
        for i in range(0, len(tbl_data)):
            msg = tbl_data[i][1]

            if (len(msg) >= 48):
                msg = msg[0:48] + " [...]"

            tbl_data[i][1] = msg
        table = DoubleTable(tbl_data, " Datos ")

    print(table.table)

    print("")
    print_data()
    print("")
    Screen().input('Presiona [Enter] para continuar')

def list_data():
    if (len(data) == 0):
        print(stylize(" POR FAVOR INGRESA LOS DATOS DEL ARCHIVO ", orange))
        print("")
        leer_archivo()

    sys.stdout.flush()
    print("")

    i = 1
    biggest = 0
    for row in data: 
        sent = str(" " + row[0] + " ").strip()
        sl = len(sent)
        biggest = biggest if biggest > sl else sl

        author = str(" " + str(i) + ". " + row[1]["name"] + " >> ").strip()
        al = len(author)
        
        biggest = biggest if biggest > al else al

    for row in data:
        color = colored.fg("white") + colored.bg(row[1]["color"])
        author = str(" " + str(i) + ". " + row[1]["name"] + " >> ").strip()
        sent = str(" " + row[0] + " ")

        author = author.strip().ljust(biggest)
        sent = sent.strip().ljust(biggest)

        print(stylize(author, color))
        print(stylize(sent, color))

        i = i + 1

    print("")
    Screen().input('Presiona [Enter] para continuar')

def post_data():
    if (ip == ""):
        print(stylize(" POR FAVOR INGRESA LA DIRECCIÓN ", orange))
        print("")
        leer_ip()
    
    sys.stdout.flush()
    print("")

    if (len(data) == 0):
        print(stylize(" POR FAVOR INGRESA LOS DATOS DEL ARCHIVO ", orange))
        print("")
        leer_archivo()

    sys.stdout.flush()
    print("")
    print(stylize(" PUBLICANDO DATOS AL SERVIDOR ", green))
    print("")
    total = len(data)
    i = 1
    errored = 0
    success = 0
    for s in data:
        pd = { "author": s[1]["name"], "sentence": s[0] }
        pdn = len(pd["sentence"])
        pdn = pdn if pdn < 10 else 10
        
        status = ""
        try:
            print("Enviando a la dirección: {}{}".format(ip, url))
            print(pd)

            x = requests.post('{}{}'.format(ip, url), json= pd)
            code = x.status_code
            recieved_data = x.json()
            
            if (code == 200):
                print(stylize(" OK 200 ", green))
                status = str(recieved_data)
                success = success + 1
            else:
                print(stylize(" ERROR " + str(code) + " ", red))
                status = str(recieved_data)
                errored = errored + 1
                
        except Exception as e:
            print(stylize(" ERROR ", red))
            status = "Posting... ERROR"
            if hasattr(e, 'message'):
                print(stylize(e.message, colored.fg("red_3a")))
            else:
                print(stylize(e, colored.fg("red_3a")))
            errored = errored + 1

        progress(i, total, status)

        i = i + 1
        time.sleep(0.25)

    sys.stdout.flush()
    print("")
    print("")
    print("")
    print(stylize(" TODOS LOS DATOS FUERON ENVIADOS ", blue))
    print("")
    correct_percent = round(100 * success / total, 2)
    incorrect_percent = round(100 * errored / total, 2)
    print(stylize(" ENVIADOS CORRECTAMENTE: {}% ({} de {}) ".format(correct_percent, success, total), green))
    print("")
    print(stylize(" ENVIADOS CON ERROR: {}% ({} de {}) ".format(incorrect_percent, errored, total), red))

    print("")
    Screen().input('Presiona [Enter] para continuar')

def create_menu():

    menu = ConsoleMenu("Sentencer", "Asignador de autores y separador de oraciones", exit_option_text="Salir",
                       prologue_text="Selecciona un archivo, se dividira en oraciones y se le asociariá un autor. Se convertirán en objetos que luego se enviarán a la dirección IP definida.",
                       epilogue_text="Luis Leonel Aguilar Sánchez - 201603029 - SO1 2S2020",
                       formatter=MenuFormatBuilder()

                       .set_prompt("Selecciona>>")
                       .set_title_align('center')
                       .set_subtitle_align('center')
                       .set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_BORDER)
                       .show_prologue_top_border(True)
                       .show_epilogue_top_border(True)
                       .show_prologue_bottom_border(True))

    read_file_item = FunctionItem("Ingresar ruta del archivo", leer_archivo)
    read_ip_item = FunctionItem(
        "Ingresar dirección del servidor", leer_ip)
    tbl_show_item = FunctionItem(
        "Mostrar datos recolectados del archivo (como tabla)", table_data)

    list_show_item = FunctionItem(
        "Mostrar datos recolectados del archivo (como lista)", list_data)

    post_data_item = FunctionItem(
        "Publicar datos al servidor", post_data)

    menu.append_item(read_file_item)
    menu.append_item(read_ip_item)
    menu.append_item(tbl_show_item)
    menu.append_item(list_show_item)
    menu.append_item(post_data_item)

    menu.start()
    menu.join()

if __name__ == '__main__':
    for x in range(10):
        author_names.append(names.get_full_name())
    try:
        create_menu()
    except (KeyboardInterrupt, SystemExit):
        print(stylize("Gracias por usar el programa.", green))
