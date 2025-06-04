import pytesseract # type: ignore
from PIL import Image
import cv2
import os
import re

# Substitua este caminho pelo caminho real do seu sistema:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def capturar_imagem():
    caminho = input("Digite o caminho da imagem ou pressione ENTER para capturar a tela: ")
    if caminho:
        return caminho
    else:
        from mss import mss
        with mss() as sct:
            sct.shot(output="screenshot.png")
        return "screenshot.png"

def extrair_texto_da_imagem(caminho):
    imagem = Image.open(caminho)
    texto = pytesseract.image_to_string(imagem)
    return texto

def detectar_erros_em_fracoes(texto):
    erros = []
    padrao_fracao = r'(\d+)\s*/\s*(\d+)'  # detectar frações

    linhas = texto.split('\n')
    for linha in linhas:
        expressao = linha.strip().replace(" ", "")
        if '+' in expressao:
            partes = expressao.split('=')
            if len(partes) != 2:
                continue
            esquerda, direita = partes
            try:
                f1, f2 = esquerda.split('+')
                n1, d1 = map(int, re.findall(r'\d+', f1))
                n2, d2 = map(int, re.findall(r'\d+', f2))
                nr, dr = map(int, re.findall(r'\d+', direita))
                
                # Erro clássico: soma direta
                if nr == n1 + n2 and dr == d1 + d2:
                    erros.append(f"Erro de soma direta em: {linha}")
            except:
                continue
        elif '*' in expressao:
            partes = expressao.split('=')
            if len(partes) != 2:
                continue
            esquerda, direita = partes
            try:
                f1, f2 = esquerda.split('*')
                n1, d1 = map(int, re.findall(r'\d+', f1))
                n2, d2 = map(int, re.findall(r'\d+', f2))
                nr, dr = map(int, re.findall(r'\d+', direita))
                if nr != n1 * n2 or dr != d1 * d2:
                    erros.append(f"Erro de multiplicação incorreta em: {linha}")
            except:
                continue

    return erros if erros else ["Não foram encontrados erros comuns em frações."]

def main():
    caminho_imagem = capturar_imagem()
    print("\n📷 Imagem capturada. Extraindo texto...")
    texto = extrair_texto_da_imagem(caminho_imagem)
    print(f"\n📝 Texto extraído:\n{texto}")

    print("\n🔎 Analisando possíveis erros em frações...")
    erros = detectar_erros_em_fracoes(texto)
    for erro in erros:
        print(f"❌ {erro}")

if __name__ == "__main__":
    main()
