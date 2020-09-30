import spacy
from consolemenu import *
from consolemenu.items import *

menu = ConsoleMenu("Sentencer", "Divisor de oraciones", exit_option_text='Salir', prologue_text='Hola!', epilogue_text='epilogo')
menu_item = MenuItem("Menu Item")

function_item = FunctionItem("Call a Python function", input, ["Enter an input"])
command_item = CommandItem("Run a console command",  "touch hello.txt")

selection_menu = SelectionMenu(["item1", "item2", "item3"])

submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

menu.append_item(menu_item)
menu.append_item(function_item)
menu.append_item(command_item)
menu.append_item(submenu_item)

menu.show()

def split_sentences(): 
    text = ""
    with open('../data.txt', 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', '')

    nlp = spacy.load("es_core_news_sm")

    def set_custom_boundaries(doc):
        for token in doc[:-1]:
            if token.text == "...":
                doc[token.i+1].is_sent_start = True
            if token.text == "–":
                doc[token.i+1].is_sent_start = True
        return doc

    nlp.add_pipe(set_custom_boundaries, before="parser")
    doc = nlp(text)

    sentences = [sent.text for sent in doc.sents]

    print(sentences)
    print(len(sentences))
