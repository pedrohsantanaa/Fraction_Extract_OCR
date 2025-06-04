import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

imagem = Image.open("img2.png")
texto = pytesseract.image_to_string(imagem)
print("Texto extraído:")
print(texto)
