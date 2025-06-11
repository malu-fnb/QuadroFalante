# Função para retornar o significado de uma palavra
def obter_significado(palavra):
    # Dicionário básico para significados
    significados = {
        "cachorro": "Um animal de estimação que late.",
        "gato": "Um animal de estimação que mia.",
        "livro": "Objeto usado para ler e aprender.",
        "bola": "Objeto redondo utilizado em vários jogos."
    }
    return significados.get(palavra.lower(), "Significado não encontrado.")
