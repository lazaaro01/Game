import cv2
import numpy as np
import mediapipe as mp
import random
import time

# ===== Funções Gerais =====
largura, altura = 1280, 720
tempo_total = 30  # segundos

def criar_alvo():
    x = random.randint(100, largura - 100)
    y = random.randint(100, altura - 100)
    return [x, y]

def desenhar_interface(img, pontuacao, tempo_restante):
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (largura, 80), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

    cv2.putText(img, f"Pontuacao: {pontuacao}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    texto_tempo = f"Tempo: {int(tempo_restante)}s"
    texto_tamanho = cv2.getTextSize(texto_tempo, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
    pos_x = largura - texto_tamanho[0] - 20
    cv2.putText(img, texto_tempo, (pos_x, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

def detectar_toque(x_dedo, y_dedo, alvos, pontuacao):
    novos_alvos = []
    for alvo in alvos:
        distancia = np.hypot(x_dedo - alvo[0], y_dedo - alvo[1])
        if distancia < 40:
            pontuacao += 1
        else:
            novos_alvos.append(alvo)
    return novos_alvos, pontuacao

# Botão de reinício
botao_reiniciar = [(largura//2 - 150, altura//2 + 50), (largura//2 + 150, altura//2 + 130)]
clicou_reiniciar = False

def verificar_clique_botao(event, x, y, flags, param):
    global clicou_reiniciar
    if event == cv2.EVENT_LBUTTONDOWN:
        if botao_reiniciar[0][0] < x < botao_reiniciar[1][0] and botao_reiniciar[0][1] < y < botao_reiniciar[1][1]:
            clicou_reiniciar = True

# ===== Loop principal =====
while True:
    clicou_reiniciar = False
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils
    pontuacao = 0
    alvos = []
    inicio_jogo = time.time()

    while True:
        tempo_decorrido = time.time() - inicio_jogo
        tempo_restante = tempo_total - tempo_decorrido
        if tempo_restante <= 0:
            break

        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        game_frame = frame.copy()

        desenhar_interface(game_frame, pontuacao, tempo_restante)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(game_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                dedo = hand_landmarks.landmark[8]
                x_dedo = int(dedo.x * largura)
                y_dedo = int(dedo.y * altura)

                alvos, pontuacao = detectar_toque(x_dedo, y_dedo, alvos, pontuacao)
                cv2.circle(game_frame, (x_dedo, y_dedo), 10, (0, 255, 255), -1)

        while len(alvos) < 3:
            alvos.append(criar_alvo())

        for alvo in alvos:
            cv2.circle(game_frame, tuple(alvo), 30, (0, 0, 255), -1)
            cv2.circle(game_frame, tuple(alvo), 20, (255, 255, 255), -1)
            cv2.circle(game_frame, tuple(alvo), 10, (0, 0, 255), -1)

        cv2.imshow("Toque no Alvo", game_frame)
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cap.release()
    cv2.destroyAllWindows()

    # Tela final
    tela_final = np.zeros((altura, largura, 3), dtype=np.uint8)
    mensagem = f"Fim de Jogo! Pontuacao final: {pontuacao}"
    tamanho_texto = cv2.getTextSize(mensagem, cv2.FONT_HERSHEY_SIMPLEX, 2, 4)[0]
    pos_x = (largura - tamanho_texto[0]) // 2
    pos_y = (altura + tamanho_texto[1]) // 2 - 50
    cv2.putText(tela_final, mensagem, (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    cv2.rectangle(tela_final, botao_reiniciar[0], botao_reiniciar[1], (255, 255, 255), -1)
    cv2.putText(tela_final, "REINICIAR", (botao_reiniciar[0][0] + 30, botao_reiniciar[0][1] + 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    cv2.namedWindow("Fim de Jogo")
    cv2.setMouseCallback("Fim de Jogo", verificar_clique_botao)

    while True:
        cv2.imshow("Fim de Jogo", tela_final)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            cv2.destroyAllWindows()
            exit()
        if clicou_reiniciar:
            cv2.destroyWindow("Fim de Jogo")
            break
