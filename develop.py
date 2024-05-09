import pytesseract
from PIL import Image
import cv2
import os
import re
import easyocr
import urllib.request
import base64
import numpy as np

def prepare_image(base64):
    image = base64_to_image(base64)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def base64_to_image(base64_string):
    # Decodifica a string base64 em uma matriz de bytes
    decoded_data = base64.b64decode(base64_string)
    # Converte a matriz de bytes em um array numpy
    np_data = np.frombuffer(decoded_data, dtype=np.uint8)
    # Decodifica a imagem usando cv2.imdecode
    image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    return image


def pytesseract_process(image):
    text = pytesseract.image_to_string(image, config='--psm 4')
    return text


def get_valor_total(text):
    ptr = 'R. *(\\d+,\\d{2})'
    reMatch = re.search(ptr, str(text))

    if reMatch:
        return reMatch.group(1)


def get_CNPJ(text):
    ptr = '\\d{2}\\D\\d{3}\\D\\d{3}\\D\\d{4}\\D\\d{2}'
    reMatch = re.search(ptr, str(text))

    if reMatch:
        return reMatch.group(0)


def get_from_CNPJ(cnpj):
    cnpj = re.sub("\\D", "", cnpj)
    print(cnpj)
    contents = urllib.request.urlopen(f"https://api-publica.speedio.com.br/buscarcnpj?cnpj={cnpj}").read()
    # contents = '{"NOME FANTASIA":"MILANO COMERCIO VAREJISTA DE ALIMENTOS S.A.","RAZAO SOCIAL":"MILANO COMERCIO VAREJISTA DE ALIMENTOS S.A.","CNPJ":"11950487010314","STATUS":"ATIVA","CNAE PRINCIPAL DESCRICAO":"Lanchonetes, casas de ch\xc3\xa1, de sucos e similares","CNAE PRINCIPAL CODIGO":"5611203","CEP":"03310000","DATA ABERTURA":"27/03/2019","DDD":"11","TELEFONE":"47668200","EMAIL":"baciodilatte@baciodilatte.com.br","TIPO LOGRADOURO":"RUA","LOGRADOURO":"ITAPURA","NUMERO":"1390","COMPLEMENTO":"","BAIRRO":"VILA GOMES CARDIM","MUNICIPIO":"S\xc3\xa3o paulo","UF":"SP"}'
    return contents


def run_tesseract(base64):
    image = prepare_image(base64)
    text = pytesseract_process(image)

    total = get_valor_total(text)
    print(total)
    cnpj = get_CNPJ(text)
    print(cnpj)
    dados = get_from_CNPJ(cnpj)
    return total, dados
    # print(text)

