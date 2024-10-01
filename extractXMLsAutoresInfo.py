import xml.etree.ElementTree as ET
import requests
import os
import pandas as pd

pasta = 'C:\\Users\\tinho\\OneDrive\\Área de Trabalho\\LACA\\curriculos_xmls\\curriculos_xmls\\produtividade_lattes_TAIA\\1A_novo' 
#arquivo = "curriculo.xml"

# Lista todos os arquivos na pasta
arquivos_xml = [f for f in os.listdir(pasta) if f.endswith('.xml')]

#tree =  ET.parse(arquivo)

#root = tree.getroot()

cols = ["nome", "atual_instituicao", "instituicao_doutorado", "ano_doutorado", "areas", "artigos_periodicos", "capitulos_livros"]
rows = []
areas_sub = []


for arquivo in arquivos_xml:
    caminho_completo = os.path.join(pasta, arquivo)
    tree = ET.parse(caminho_completo)
    root = tree.getroot()


    for item in root.findall("DADOS-GERAIS"):
        #Dados gerais
        nome = item.attrib.get("NOME-COMPLETO")
        atual_instituicao = item.find("ENDERECO/ENDERECO-PROFISSIONAL").attrib.get("NOME-INSTITUICAO-EMPRESA")
        instituicao_doutorado = item.find("FORMACAO-ACADEMICA-TITULACAO/DOUTORADO").attrib.get("NOME-INSTITUICAO")
        ano_doutorado = item.find("FORMACAO-ACADEMICA-TITULACAO/DOUTORADO").attrib.get("ANO-DE-CONCLUSAO")

        #Areas
        areas_element = item.find("AREAS-DE-ATUACAO")
        if areas_element is not None:
            subareas = [area.attrib.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO") for area in areas_element.findall("AREA-DE-ATUACAO")]
            areas_string = ", ".join(subareas)
        else:
            areas_string = ""

        #Artigos
        artigos_publicados = root.findall("PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO")

        titulos = []
        for artigo in artigos_publicados:
            titulo = artigo.attrib.get("TITULO-DO-ARTIGO")
            if titulo:
                titulos.append(titulo)


        #Livros
        livros_publicados = root.findall("PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/CAPITULOS-DE-LIVROS-PUBLICADOS/CAPITULO-DE-LIVRO-PUBLICADO/DADOS-BASICOS-DO-CAPITULO")

        cap = []
        for livro in livros_publicados:
            titulo = livro.attrib.get("TITULO-DO-CAPITULO-DO-LIVRO")
            if titulo:
                cap.append(titulo)

        rows.append({'nome': nome, 'atual_instituicao': atual_instituicao, 'instituicao_doutorado': instituicao_doutorado,
                    'ano_doutorado': ano_doutorado, 'areas': areas_string, 'artigos_periodicos': titulos, 'capitulos_livros': cap})

df = pd.DataFrame(rows, columns=cols)

# Writing dataframe to csv
df.to_csv('output.csv')