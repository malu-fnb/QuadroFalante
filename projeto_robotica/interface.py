import tkinter as tk
from tkinter import ttk
import pyttsx3
import speech_recognition as sr
import threading
from PIL import Image, ImageTk
import palavras  # Importa o arquivo palavras.py

# Inicializando o motor de fala
engine = pyttsx3.init()

# Ajustando a taxa de fala (quanto maior o valor, mais rápido será)
rate = engine.getProperty('rate')  # Pega a taxa atual
engine.setProperty('rate', rate - 50)  # Reduz a taxa para 50 unidades mais rápidas

# Ajustando o volume (padrão é 1.0, sendo o máximo)
engine.setProperty('volume', 1)  # Volume máximo

# Variáveis globais para acessar os elementos da interface
palavra_entry = None
escrita_label = None
feedback_label = None
letras_botoes = []  # Lista para armazenar os botões de letras

# Função para falar a letra com a associação
def falar_letra(letra):
    associacoes = {
        "a": "A de abacaxi",
        "b": "B de bola",
        "c": "C de casa",
        "d": "D de dado",
        "e": "E de elefante",
        "f": "F de faca",
        "g": "G de galinha",
        "h": "H de homem",
        "i": "I de igreja",
        "j": "J de jacaré",
        "k": "K de kiwi",
        "l": "L de leão",
        "m": "M de macaco",
        "n": "N de navio",
        "o": "O de ovo",
        "p": "P de pato",
        "q": "Q de queijo",
        "r": "R de rato",
        "s": "S de sapato",
        "t": "T de tigre",
        "u": "U de urso",
        "v": "V de vaca",
        "w": "W de waffle",
        "x": "X de xadrez",
        "y": "Y de yoga",
        "z": "Z de zebra"
    }
    
    frase = associacoes.get(letra.lower(), f"{letra.upper()} não tem associação conhecida")
    engine.say(frase)
    engine.runAndWait()

# Função para falar a palavra com feedback visual
def falar_palavra(event=None):  # Agora aceita o evento passado pelo bind
    palavra = palavra_entry.get().strip()
    if palavra:
        feedback_label.config(text="Falando a palavra...", fg="green")  # Feedback visual
        engine.say(palavra)
        engine.runAndWait()
        feedback_label.config(text="Pronto!", fg="blue")  # Resetando o feedback visual após a fala

# Função para escutar a fala e transcrever com feedback visual
def escutar_fala(event=None):  # Agora aceita o evento passado pelo bind
    feedback_label.config(text="Escutando... Fale agora.", fg="yellow")  # Feedback visual de escuta
    falar_pode_falar()  # Fala "Pode falar" quando o app começa a escutar
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        reconhecedor.adjust_for_ambient_noise(fonte)  # Ajuste para o ruído ambiente
        try:
            audio = reconhecedor.listen(fonte, timeout=10)  # Timeout para evitar travamento eterno
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            feedback_label.config(text=f"Você disse: {texto}", fg="blue")  # Exibe a transcrição
            palavra_entry.delete(0, tk.END)  # Limpa o campo de entrada
            palavra_entry.insert(0, texto)  # Insere a palavra transcrita na entrada
        except sr.UnknownValueError:
            feedback_label.config(text="Não entendi o que você disse.", fg="red")
        except sr.RequestError as e:
            feedback_label.config(text=f"Erro de reconhecimento: {e}", fg="red")
        except Exception as e:
            feedback_label.config(text=f"Erro desconhecido: {e}", fg="red")
        finally:
            # Após a escuta, restaurar o texto de feedback
            feedback_label.config(text="Pronto!", fg="blue")

# Função para falar "Pode falar"
def falar_pode_falar():
    engine.say("Pode falar")  # Fala a frase "Pode falar"
    engine.runAndWait()  # Executa a fala

# Função para soletrar a palavra com feedback visual
def soletrar_palavra(event=None):  # Agora aceita o evento passado pelo bind
    palavra = palavra_entry.get().strip()
    if palavra:
        feedback_label.config(text="Soletrando a palavra...", fg="green")
        for i, letra in enumerate(palavra):
            palavra_completa = palavra
            escrita_label.config(text=f"Palavra: {palavra_completa} | Letra: {letra}")  # Exibe a palavra e a letra sendo falada
            engine.say(letra)  # Fala a letra
            engine.runAndWait()  # Executa a fala
            root.after(i * 500)  # Atraso de 0.5 segundo por letra
        feedback_label.config(text="Soletração concluída", fg="blue")  # Feedback após completar

# Função para explicar a palavra usando o arquivo palavras.py
def explicar_palavra(event=None):  # Agora aceita o evento passado pelo bind
    try:
        palavra = palavra_entry.get().strip()
        if palavra:
            explicacao = palavras.obter_explicacao(palavra)
            if explicacao:
                feedback_label.config(text=f"Explicação: {explicacao}", fg="blue")
                engine.say(explicacao)  # Fala a explicação
                engine.runAndWait()  # Executa a fala
            else:
                feedback_label.config(text="Desculpe, não tenho explicação para essa palavra.", fg="red")
    except Exception as e:
        print(f"Erro ao explicar a palavra: {e}")
        feedback_label.config(text="Erro ao explicar a palavra", fg="red")

# Função para processar a palavra (Soletrar)
def processar_palavra():
    palavra = palavra_entry.get().strip()
    if palavra:
        soletrar_palavra()

# Função para lidar com pressionamento de teclas
def tecla_press(event):
    if event.char == '0':
        escutar_fala()
    elif event.char == '1':
        falar_palavra()
    elif event.char == '2':
        soletrar_palavra()
    elif event.char == '3':
        explicar_palavra()
    else:
        letra = event.char.lower()
        falar_letra(letra)  # Fala a letra correspondente

# Função para criar a interface gráfica
def criar_interface():
    global palavra_entry, escrita_label, root, feedback_label, letras_botoes, fundo_label

    root = tk.Tk()
    root.title("Alfabetização Infantil Inclusiva")
    root.geometry("600x600")
    root.config(bg="#f4c542")  # Cor de fundo alegre e vibrante

     # Carregar imagem de fundo
    fundo_img = Image.open("images/meu_fundo.png")  # Altere para o caminho correto da imagem
    fundo_img = fundo_img.resize((600, 600), Image.Resampling.LANCZOS)  # Usando LANCZOS em vez de ANTIALIAS
    fundo_tk = ImageTk.PhotoImage(fundo_img)
    fundo_label = tk.Label(root, image=fundo_tk)
    fundo_label.place(x=0, y=0)  # Define a posição da imagem como fundo
    fundo_label.image = fundo_tk  # Evita que a imagem seja coletada pelo garbage collector

    # Carregar o logo da UNICAP
    logo_img = Image.open("images/unicap.png")  # Altere para o caminho correto da imagem
    logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)  # Redimensiona o logo para tamanho pequeno
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_tk, bg="#f4c542")
    logo_label.place(x=500, y=10)  # Posição do logo no canto superior direito
    logo_label.image = logo_tk  # Evita que a imagem seja coletada pelo garbage collector

    # Label de instrução
    instrucoes_label = tk.Label(root, text="Digite uma palavra ou fale para ver a mágica acontecer!", font=("Comic Sans MS", 14), bg="#f4c542", fg="white")
    instrucoes_label.pack(pady=10)

    # Entrada para a palavra
    palavra_label = tk.Label(root, text="Digite ou fale a palavra:", font=("Comic Sans MS", 12), bg="#f4c542", fg="white")
    palavra_label.pack()

    palavra_entry = ttk.Entry(root, font=("Comic Sans MS", 12), width=20)  # Usando ttk.Entry para uma aparência mais moderna
    palavra_entry.pack(pady=10)

    # Botão para processar a palavra (Soletrar a palavra)
    processar_button = ttk.Button(root, text="Processar", command=processar_palavra)
    processar_button.pack(pady=10)

    # Botão para falar a palavra
    falar_button = ttk.Button(root, text="Falar Palavra", command=falar_palavra)
    falar_button.pack(pady=10)

    # Botão para escutar e transcrever a palavra
    escutar_button = ttk.Button(root, text="Escutar Palavra", command=lambda: threading.Thread(target=escutar_fala).start())
    escutar_button.pack(pady=10)

    # Botão para explicar a palavra
    explicar_button = ttk.Button(root, text="Explicar Palavra", command=explicar_palavra)
    explicar_button.pack(pady=10)

    # Feedback visual para ações
    feedback_label = tk.Label(root, text="Pronto para começar!", font=("Comic Sans MS", 12), fg="blue", bg="#f4c542")
    feedback_label.pack(pady=20)

    # Exibir a escrita da palavra
    escrita_label = tk.Label(root, text="", font=("Comic Sans MS", 12, "bold"), fg="blue", bg="#f4c542")
    escrita_label.pack(pady=10)

    # Exibir os botões para cada letra da palavra
    def exibir_botoes_letras(palavra):
        for button in letras_botoes:
            button.destroy()  # Limpa os botões anteriores
        letras_botoes.clear()

        for letra in palavra:
            botao_letra = ttk.Button(root, text=letra.upper(), command=lambda letra=letra: falar_letra(letra))
            botao_letra.pack(pady=5)
            letras_botoes.append(botao_letra)  # Adiciona o botão à lista de botões

    # Botão para exibir as letras da palavra
    mostrar_botoes_button = ttk.Button(root, text="Mostrar Letras", command=lambda: exibir_botoes_letras(palavra_entry.get().strip()))
    mostrar_botoes_button.pack(pady=10)

    # Instruções para o usuário sobre os comandos do teclado
    teclado_instrucoes_label = tk.Label(root, text="Pressione as teclas para realizar ações:\n"
                                                  "0 - Escutar Palavra\n"
                                                  "1 - Falar Palavra\n"
                                                  "2 - Soletrar Palavra\n"
                                                  "3 - Explicar Palavra", 
                                        font=("Comic Sans MS", 12), bg="#f4c542", fg="white")
    teclado_instrucoes_label.pack(pady=20)

    # Bind para as teclas de 0 a 3
    root.bind("<KeyPress-0>", escutar_fala)  # Pressionar 0 para escutar a palavra
    root.bind("<KeyPress-1>", falar_palavra)  # Pressionar 1 para falar a palavra
    root.bind("<KeyPress-2>", soletrar_palavra)  # Pressionar 2 para soletrar a palavra
    root.bind("<KeyPress-3>", explicar_palavra)  # Pressionar 3 para explicar a palavra

    # Rodar o app
    root.mainloop()

# Rodar a função para criar a interface
criar_interface()
