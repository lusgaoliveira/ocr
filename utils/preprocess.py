import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_input):
    # Aqui verifico se veio via upload na API ou está na memória (coloco em RGB)
    if isinstance(image_input, Image.Image):
        pil_img = image_input.convert('RGB')
    else:
        pil_img = Image.open(image_input).convert('RGB')

    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    'Upscaliing simples caso h ou w seja menor que 1000'
    h, w = img.shape[:2]
    if max(h, w) < 1000:
        scale = 1000 / max(h, w)
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
    
    '''
    Escala de cinza e remoção de ruído. Vi que você usou bilateralFilter no M-Reader, mas usei o medianBlur por ser mais leve e não 
    precisar de tanto processamento quanto ao outro porque aqui o kernel pega a mediana da área definida, sendo mais simples.
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.fastNlMeansDenoising(gray, h=10)

    # Ajuste de contraste local de forma autmomatica
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # Inverter imagem se o fundo for escuro
    if np.mean(gray) < 127:
        gray = cv2.bitwise_not(gray)

    '''
    Não encontrei nada do tipo no M-Reader, mas achei interessante. É um pouco pesado, mas vale a pena porque calcula o threshold local para cada pixel, assim
    cobre a varição por pixel e não glboal.
    '''          
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 11
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    
    """
    Apaga ruídos (pontos branco sozinhos na imagem) e engrossa os caracteres
    """
    eroded = cv2.erode(thresh, kernel, iterations=1)

    processed = cv2.dilate(eroded, kernel, iterations=1)

    return processed
