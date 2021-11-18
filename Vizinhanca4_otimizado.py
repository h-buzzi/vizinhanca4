# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 16:54:47 2021

@author: Henrique Buzzi
"""

import cv2
import matplotlib as mpl
import numpy as np
import sys

def two_pass(image, mode = 'default'):
    """Algoritmo de vizinhança 4 baseado no algoritmo 2 pass. 
    Possui 2 inputs, 'image' que é a imagem a ser analisada
    e 'mode', que é o modo de operação, possuindo as opções 'default' e 'reform'.
    
    o modo 'default', inserido automaticamente se não for dado nenhum modo, executa apenas o algoritmo two-pass, sem diminuir o valor numérico da label;
    Já o modo 'reform', que irá fazer com que aumente o tempo de execução, transforma o intervalo dos valores numéricos da label para o mesmo intervalo de objetos.
    
    Por exemplo, o modo default, o objeto 1 pode possuir label 1, o objeto 2 label 13, o objeto 3 o label 50 e assim por diante;
    Para o modo reform, o objeto 1 terá label 1, o objeto 2 label 2, e o objeto n label n.
    
    Para quesitos computacionais, o modo default é suficiente;
    Para fácil entendimento e manipulação do projetista, o modo reform pode ser mais interessante."""
    
    def smaller_labels(): #Função que diminui o intervalo numérico das labels para o intervalo de objetos
        labels = np.zeros(int(n_obj)) #Vetor para salvar as labels da imagem
        for i in range(h): #Percorre a imagem
            for j in range(w):
                if im_label[i,j]>0: #Se encontrar uma label
                    for k in range(int(n_obj)): #Percorre todas as labels
                        if labels[k] == 0: #Se está numa posição com 0, não tem essa label
                            labels[k] = im_label[i,j] #Salva a label
                            im_label[i,j] = k+1 #Aplica a equivalência de label
                            break #Termina o loop das labels
                        elif im_label[i,j] == labels[k]: #Se tiver uma label igual salva
                            im_label[i,j] = k+1 #Apenas aplica a posição de equivalência da label
                            break
                        else:
                            continue
                else:
                    continue
        return
                
    (h, w) = image.shape # Pega o tamanho da imagem
    im_label = np.zeros([h,w], dtype = np.uint8) #Criação da imagem de labels
    N = 0 #Inicialização número de objetos
    equiv = np.zeros(1, dtype = int) #pré-alocação do vetor de equivalências
    for i in range(h): #Percorre a imagem
        for j in range(w):
            if image[i,j]==255: #Se o pixel for foreground
                lft = im_label[i,j-1] #Salva label da esquerda
                up = im_label[i-1,j] #Salva label da direita
                if (lft == 0) and (up == 0): #Se ambos labels vizinhos forem 0
                    N += 1 #Novo objeto, adiciona
                    im_label[i,j] = N #Aplica label
                elif (lft == 0) and (up != 0): #Vizinho cima tem label
                    im_label[i,j] = up #Aplica o label do vizinho de cima
                elif (lft != 0) and (up == 0): #Vizinho lado tem label
                    im_label[i,j] = lft #Aplica label do vizinho do lado
                elif (lft != 0) and (up !=0): #Se ambos vizinhos tem label
                    if lft == up: #Se as labels forem iguais
                        im_label[i,j] = lft #Pode salvar qqlr uma das 2, nessa caso escolhido o esquerdo
                    else: #Se forem diferentes
                        low = min(lft,up) #Pega o min
                        high = max(lft,up) #E máx
                        im_label[i,j] = low #Define pixel atual como mín
                        if (low in equiv) and (high in equiv): #Verifica se ambos os valores estão no vetor de equivalências
                            continue #Se estão, nada precisa ser feito, pois esses valores já serão cobridos
                        else: #Caso algum deles não esteja
                            equiv = np.append(equiv,[low, high]) #Salva as equivalências
                            
    equiv = equiv[1:] #Elimina valor inicial usado para pré-alocação
    
    for k in range(equiv.shape[0]-1,-1,-2): #Percorre o vetor de equivalência de trás pra frente
        im_label[im_label == equiv[k]] = equiv[k-1] #Nas posições onde existe equivalência o valor maior, substitui pelo valor equivalente menor (1 posição antes no vetor)
                        
    n_obj = N - equiv.shape[0]/2 #Calcula a qtd de objetos
    
    if mode == 'default': #Se o modo for o default
        I = np.uint8(im_label*(255/N)) #Apenas cria a imagem a partir do im_label
        return n_obj,I
    elif mode == 'reform': #Se o modo for o reform
        smaller_labels() #Chama a função responsável por diminuir o intervalo numérico das labels
        I = np.uint8(im_label*(255/n_obj)) #Cria a imagem a partir do im_label
        return n_obj,I
    else: #Se inseriu um modo inválido
        print("Invalid mode inserted") #Printa erro
        sys.exit() #Cancela o código

def imshow_close_withAny(image,text): #Função que mostra a imagem e permite fechá-la com qualquer tecla
    """Função que mostra uma imagem e permite que seja fechada quando qualquer tecla for pressionada.

    Input: Imagem a ser mostrada, Título da imagem.

    Output: None"""
    cv2.imshow(text, image) #Mostra imagem
    key = cv2.waitKey(0) #Espera tecla
    if key != None:  #Se tiver alguma tecla
        cv2.destroyWindow(text) #Fecha a imagem
        return
    
################# CODE START #################
## Imagem binária inserida pelo usuário
image = cv2.imread("imagem2.png",0)
##Mostra a imagem original
imshow_close_withAny(image,'Original')
## Chama função de Connected-componentes / vizinhança 4
numero_objetos, I1 = two_pass(image,'default')

## Mostra os resultados
imshow_close_withAny(I1, 'Resultado escala de cinza')
cm_jet = mpl.cm.get_cmap('jet_r') #Cria o mapa jet
imshow_close_withAny(cm_jet(I1), 'Resultado escala jet')                   