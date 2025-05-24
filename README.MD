# 🖐️ Hand Blaster - Jogo de Tiro com Controle por Gestos

Um jogo interativo de **visão computacional** onde o jogador controla uma arma virtual usando **gestos de mão** detectados pela webcam. O objetivo é acertar alvos que aparecem na tela, gerenciando a munição e recarregando com gestos.

---

## 📸 Tecnologias Utilizadas

- **Python 3.10** – Linguagem principal do projeto
- **OpenCV** – Para capturar e processar a imagem da webcam
- **MediaPipe** – Para detecção e rastreamento das mãos e dedos
- **NumPy** – Para cálculos e manipulação de arrays

---

## 🎮 Como Funciona

- A webcam capta os movimentos da sua mão.
- O **MediaPipe** detecta a posição dos dedos.
- Quando você faz o gesto de disparo (por exemplo, **indicador esticado e polegar levantado**), um tiro é disparado.
- O jogo detecta se você acertou os alvos.
- Quando a munição acaba, um gesto específico (como mão fechada) pode ser usado para **recarregar**.

---

## ▶️ Como Rodar o Projeto

### 1. Clone o repositório

git clone https://github.com/lazaaro01/Game.git

cd game

###

## ▶️ Crie e Ative o Ambiente Virtual

### 2. Crie o Ambiente Virtual
python -m venv venv

## ▶️ 3. Instale as depedências

###
pip install -r requirements.txt

Se não tiver o requirements.txt, use:

pip install opencv-python mediapipe numpy

## ▶️ 4. Rode o Projeto

###
python app.py

## 📜 Licença

### Feito por Lázaro Vasconcelos

![Licenca](https://img.shields.io/badge/License-MIT-yellow.svg)



