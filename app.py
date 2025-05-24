import cv2
import numpy as np
import mediapipe as mp
import random

# ===== Configurações Iniciais =====
# Configurações da câmera
largura, altura = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)

# Configurações do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Detecta apenas uma mão para simplificar
mp_draw = mp.solutions.drawing_utils

# ===== Configurações do Jogo =====
# Sistema de munição
municao_maxima = 1
municao_atual = municao_maxima
cor_municao = (0, 255, 0)  # Verde quando tem munição

# Elementos do jogo
tiros = []  # Cada tiro: [x, y, dx, dy]
alvos = []
pontuacao = 0

# Cores
COR_TEXTO = (255, 255, 255)
COR_FUNDO = (0, 0, 0)
COR_ALVO = (0, 0, 255)
COR_TIRO = (0, 255, 255)
COR_SEM_MUNICAO = (0, 0, 255)

# ===== Funções do Jogo =====
def criar_alvo():
    """Cria um novo alvo em posição aleatória"""
    x = random.randint(100, largura - 100)
    y = random.randint(100, altura - 100)
    return [x, y]

def desenhar_interface(img, municao, pontuacao):
    """Desenha a interface do jogo com informações de munição e pontuação"""
    # Fundo semitransparente para os textos
    cv2.rectangle(img, (0, 0), (300, 110), (0, 0, 0, 0.5), -1)
    
    # Textos de informação
    cv2.putText(img, f"Municao: {municao}/{municao_maxima}", (20, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, COR_TEXTO, 2)
    cv2.putText(img, f"Pontuacao: {pontuacao}", (20, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, COR_TEXTO, 2)
    
    # Indicador visual de munição
    for i in range(municao_maxima):
        cor = COR_TEXTO if i < municao_atual else COR_SEM_MUNICAO
        cv2.circle(img, (150 + i * 30, 100), 10, cor, -1)

def detectar_gestos(landmarks):
    """
    Detecta gestos de tiro e recarregar baseado nos landmarks da mão
    Retorna: (disparo, recarregar)
    """
    # Pontos de referência
    dedo_ind_ponta = landmarks[8]
    dedao_ponta = landmarks[4]
    
    # Coordenadas
    x_ind = int(dedo_ind_ponta.x * largura)
    y_ind = int(dedo_ind_ponta.y * altura)
    x_dedao = int(dedao_ponta.x * largura)
    y_dedao = int(dedao_ponta.y * altura)

    #Distancias
    Distanca_dedao_indicador_x = ((landmarks[3].x - landmarks[5].x)*largura)**2 
    Distanca_dedao_indicador_y = ((landmarks[3].y - landmarks[5].y)*altura)**2
    
    # Gesto de tiro: dedo indicador estendido e dedão para cima
    distancia_tiro = np.hypot(x_ind - x_dedao, y_ind - y_dedao)
    gesto_tiro = distancia_tiro > 100  # Ajuste este valor conforme necessário
    
    # Gesto de recarregar: dedos fechados (ponta do indicador perto da base)
    distancia_recarregar = np.hypot( Distanca_dedao_indicador_x , Distanca_dedao_indicador_y )
    gesto_recarregar = distancia_recarregar < 1500  # Ajuste este valor conforme necessário
    print(distancia_recarregar)
    
    return gesto_tiro, gesto_recarregar

# ===== Loop Principal do Jogo =====
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    
    # Processa a imagem com MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    # Cria uma cópia do frame para desenhar os elementos do jogo
    game_frame = frame.copy()
    
    # Desenha a interface
    desenhar_interface(game_frame, municao_atual, pontuacao)
    
    # Processa gestos se uma mão for detectada
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenha os landmarks da mão
            mp_draw.draw_landmarks(game_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Detecta gestos
            gesto_tiro, gesto_recarregar = detectar_gestos(hand_landmarks.landmark)
            
            # Gesto de recarregar
            if gesto_recarregar:
                municao_atual = municao_maxima
                cv2.putText(game_frame, "RECARREGANDO!", (largura//2 - 150, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Gesto de tiro (só dispara se tiver munição)
            elif gesto_tiro and municao_atual > 0:
                municao_atual -= 1
                
                # Obtém a posição e direção do dedo indicador
                dedo_ind = hand_landmarks.landmark[8]
                dedo_ind_base = hand_landmarks.landmark[5]
                
                x_ind = int(dedo_ind.x * largura)
                y_ind = int(dedo_ind.y * altura)
                x_base = int(dedo_ind_base.x * largura)
                y_base = int(dedo_ind_base.y * altura)
                
                # Calcula a direção do tiro
                dx = x_ind - x_base
                dy = y_ind - y_base
                norma = np.hypot(dx, dy)
                if norma > 0:
                    dx /= norma
                    dy /= norma
                
                # Adiciona o tiro à lista
                tiros.append([x_ind, y_ind, dx * 15, dy * 15])  # 15 = velocidade
    
    # Atualiza e desenha tiros
    for tiro in tiros:
        tiro[0] += int(tiro[2])
        tiro[1] += int(tiro[3])
        cv2.circle(game_frame, (int(tiro[0]), int(tiro[1])), 5, COR_TIRO, -1)
    
    # Remove tiros que saíram da tela
    tiros = [t for t in tiros if 0 <= t[0] < largura and 0 <= t[1] < altura]
    
    # Cria novos alvos se necessário
    if len(alvos) < 3:
        alvos.append(criar_alvo())
    
    # Verifica colisões entre tiros e alvos
    novos_alvos = []
    for alvo in alvos:
        atingido = False
        for tiro in tiros:
            dist = np.hypot(tiro[0] - alvo[0], tiro[1] - alvo[1])
            if dist < 30:  # Raio de colisão
                atingido = True
                pontuacao += 1
                break
        
        if not atingido:
            novos_alvos.append(alvo)
            cv2.circle(game_frame, tuple(alvo), 30, COR_ALVO, -1)
            cv2.circle(game_frame, tuple(alvo), 20, (255, 255, 255), -1)
            cv2.circle(game_frame, tuple(alvo), 10, COR_ALVO, -1)
    
    alvos = novos_alvos
    
    # Exibe o frame do jogo
    cv2.imshow("Jogo de Tiro com Gestos", game_frame)
    
    # Tecla ESC para sair
    if cv2.waitKey(1) == 27:
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()