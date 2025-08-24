#!/bin/bash
# SCRIPT PARA RODAR NA VPS

# ----------------------------------------------------

# Esse script instala o python os pacotes que estão em requirements.txt
# Se você reiniciar o container do Coolify, terá que executar esse script novamente.

# 1️⃣ Rode no terminal:
# chmod +x vps_script.sh

# 2️⃣ Execute o script:
# ./vps_script.sh

# 3️⃣ Ative a venv:
# source venv/bin/activate

# 4️⃣ Inicie o robô:
# python src/main.py

# ----------------------------------------------------
# Nome da virtualenv
VENV_NAME="venv"

echo "🤖 Configurando VPS..."

echo ""
echo "🧪 Atualizando repositórios..."
sudo apt update

echo ""
echo "🐍 Instalando Python e venv..."
sudo apt install -y python3 python3-venv python3-pip

echo ""
echo "📦 Criando ambiente virtual: $VENV_NAME"
python3 -m venv $VENV_NAME

echo ""
echo "🚀 Ativando a venv..."
source $VENV_NAME/bin/activate
echo ""
echo "📚 Instalando pacotes do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Ambiente configurado com sucesso!"
echo ""
echo "➡️  RODE NO TERMINAL: source $VENV_NAME/bin/activate"
echo ""
echo "--------------------------------------------------"