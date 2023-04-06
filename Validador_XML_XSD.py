# coding=latin-1 -*-
import tkinter as tk
from tkinter import filedialog
from xml.etree import ElementTree
from lxml import etree


def browse_xml():
    file_path.set(filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")]))


def browse_xsd():
    xsd_path.set(filedialog.askopenfilename(filetypes=[("Arquivos XSD", "*.xsd")]))


def validate():
    xml_file = file_path.get()
    xsd_file = xsd_path.get()

    try:
        with open(xml_file, "rb") as f:
            xml_content = f.read()
        xml_doc = etree.fromstring(xml_content)

        with open(xsd_file, "rb") as f:
            xsd_content = f.read()
        xsd_doc = etree.fromstring(xsd_content)

        schema = etree.XMLSchema(xsd_doc)

        # Validação do documento com registro de erros
        validation_log = []
        if not schema.validate(xml_doc):
            for error in schema.error_log:
                validation_log.append(str(error))

            with open("log.txt", "w") as log_file:
                log_file.write("\n".join(validation_log))

            validation_result.set(
                "Falha na validação. Verifique o arquivo log.txt para detalhes."
            )
        else:
            validation_result.set("XML validado com sucesso!")
            with open("log.txt", "w") as log_file:
                log_file.write("XML validado com sucesso!")

    except etree.DocumentInvalid as e:
        validation_result.set("Falha na validação:\n" + str(e))
    except Exception as e:
        validation_result.set("Erro:\n" + str(e))


app = tk.Tk()
app.title("Validador XML/XSD")

file_path = tk.StringVar()
xsd_path = tk.StringVar()
validation_result = tk.StringVar()

tk.Label(app, text="Arquivo XML:").grid(row=0, column=0, sticky="W")
tk.Entry(app, textvariable=file_path).grid(row=0, column=1)
tk.Button(app, text="Procurar...", command=browse_xml).grid(row=0, column=2)

tk.Label(app, text="Arquivo XSD:").grid(row=1, column=0, sticky="W")
tk.Entry(app, textvariable=xsd_path).grid(row=1, column=1)
tk.Button(app, text="Procurar...", command=browse_xsd).grid(row=1, column=2)

tk.Button(app, text="VALIDAR", command=validate).grid(row=2, column=0, columnspan=3)
tk.Label(app, textvariable=validation_result).grid(row=3, column=0, columnspan=3)

app.mainloop()
