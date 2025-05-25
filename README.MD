# 🖐️ Toque no Alvo - Jogo com Visão Computacional

Este é um jogo interativo desenvolvido com **Python**, **OpenCV** e **MediaPipe** que utiliza **detecção das mãos em tempo real** para permitir que o usuário interaja com alvos na tela. O objetivo do jogo é simples: **tocar os alvos com o dedo indicador** antes que o tempo acabe.

---

## 🎮 Como Funciona

- A webcam é utilizada para capturar a imagem ao vivo.
- O MediaPipe detecta a mão do jogador e rastreia a posição do dedo indicador.
- Sempre há **três alvos circulares** na tela.
- Quando o dedo toca um alvo, o alvo desaparece e o jogador ganha um ponto.
- O jogo dura **30 segundos**, e no final, a pontuação é exibida.
- Uma **tela final** mostra a pontuação e oferece um botão para **reiniciar o jogo**.

---

## 🛠️ Tecnologias Usadas

- **Python 3**
- **OpenCV** (`cv2`)
- **MediaPipe**
- **NumPy**


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



