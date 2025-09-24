# OCR

API simples para Reconhecimento Óptico de Caracteres (OCR) usando Python, Flask, Tesseract OCR e OpenCV.  
Permite enviar imagens ou PDFs e retornar o texto extraído, além de salvar os resultados em arquivos txt.

---

## Implementação
O projeto possui algumas funcionalidades principais que permitem processar imagens e PDFs para extrair texto de forma automatizada:

- **Upload de imagens ou arquivos PDF para OCR**  
  Permite enviar arquivos através da API e as imagens podem estar em diferentes formatos (PNG, JPG, JPEG e PDF).  

- **Pré-processamento de imagem com OpenCV**  
  Antes de extrair o texto, a imagem passa por técnicas de pré-processamento, como:
  - Conversão para escala de cinza
  - Redimensionamento (se a imagem é pequena)
  - Remoção de ruído (medianBlur)
  - Aplicação de threshold adaptativo, que ajuda o OCR a lidar com diferentes condições de iluminação (Pesa um pouco)


- **Extração de texto usando Tesseract OCR em português**  
  O OCR (Optical Character Recognition) é feito pelo Tesseract, que reconhece os caracteres (PT) da imagem e converte em texto.

- **Armazenamento dos textos em arquivos**  
  Todo texto extraído é salvo em arquivos `.txt` dentro da pasta `texts`. Se o arquivo já existir com o mesmo título, o novo texto é acrescentado ao final do arquivo existente.

- **Endpoint para recuperar textos já processados**  
  Possibildiade de recuperar os textos extraídos anteriormente usando o título do arquivo, sem precisar enviar novamente a imagem ou PDF.

## Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/lusgaoliveira/ocr.git
cd ocr
```

### 2. Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar depedências
```bash
pip install -r requirements.txt
```

### 4. Rodar a aplicação
```bash
python app.py
```


## Uso
```bash
curl -X POST -F "image=@./test_images/foto1.png" -F "title=teste1" http://127.0.0.1:5000/api/ocr
```


## Referências

- [Playlist - OCR com Python](https://youtube.com/playlist?list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i&si=54Gl88YpDAzjWZWN)
- [Visão Computacional: O Guia Completo](https://www.udemy.com/share/105kta3@ewrF9cPJpC2gLwIyWJhjnC6fFaqBybNsIBs7e-abUhcgO4FdBsqHszGUfYtsCpYk6A==/)
- Tutoriais:
    - [OCR com Tesseract (Nanonets)](https://nanonets-com.translate.goog/blog/ocr-with-tesseract/?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)  
    - [Python OCR – Awari](https://awari.com.br/python-ocr-aprenda-a-utilizar-a-tecnologia-de-reconhecimento-optico-de-caracteres/?utm_source=blog&utm_campaign=projeto+blog&utm_medium=Python%20OCR:%20Aprenda%20a%20utilizar%20a%20tecnologia%20de%20reconhecimento%20%C3%B3ptico%20de%20caracteres)  
    - [Pré-processamento de imagens para OCR – Tech for Humans](https://blog.techforhumans.com.br/post/tecnicas-de-pre-processamento-de-imagens-para-ocr)  