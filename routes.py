from flask import Blueprint, request, jsonify, render_template, url_for
import os
from gerador import gerar_imagem

routes = Blueprint('routes', __name__)

# Rota para a página inicial
@routes.route('/')
def index():
    return render_template('index.html')


# Rota para gerar imagem
@routes.route('/gerar-imagem', methods=['POST'])
def gerar_imagem_route():
    prompt = request.form.get('prompt')
    imagem_base = request.files.get('imagem_base')

    if not prompt:
        return jsonify({'error': 'Prompt não fornecido'}), 400

    # Define o modo de geração com base na presença da imagem base
    modo = 'img2img' if imagem_base else 'text2img'

    nome_arquivo = "imagem_gerada.png"
    imagem_base_path = None

    os.makedirs('uploads', exist_ok=True)

    # Salvar a imagem base se fornecida
    if imagem_base:
        imagem_base_path = os.path.join('uploads', imagem_base.filename)
        imagem_base.save(imagem_base_path)

    try:
        gerar_imagem(
            prompt=prompt,
            nome_arquivo=nome_arquivo,
            modo=modo,
            imagem_base_path=imagem_base_path
        )

        caminho_url = url_for('static', filename=f'imagens/{nome_arquivo}', _external=False)
        return jsonify({'message': 'Imagem gerada com sucesso', 'url': caminho_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
