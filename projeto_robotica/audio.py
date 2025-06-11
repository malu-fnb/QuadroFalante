import pyttsx3

# Inicializar o motor de voz
engine = pyttsx3.init()

# Função para falar a palavra
def falar_palavra(palavra):
    engine.say(palavra)
    engine.runAndWait()
