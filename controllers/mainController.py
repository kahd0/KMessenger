import customtkinter as ctk
from controllers.configController import showSettings  # Updated import

def showWelcomeMessage(frame):
    # Limpa o frame principal
    for widget in frame.winfo_children():
        widget.destroy()

    # Adiciona mensagem de boas-vindas
    welcomeLabel = ctk.CTkLabel(frame, text="Bem-vindo ao KMessenger!")
    welcomeLabel.pack(pady=20)

def showMainMenu(menuFrame, mainFrame, config):
    inicioButton = ctk.CTkButton(menuFrame, text="Início", command=lambda: showWelcomeMessage(mainFrame))
    inicioButton.pack(pady=10, padx=10)

    contatosButton = ctk.CTkButton(menuFrame, text="Contatos", command=lambda: print("Contatos"))
    contatosButton.pack(pady=10, padx=10)

    mensagensButton = ctk.CTkButton(menuFrame, text="Mensagens", command=lambda: print("Mensagens"))
    mensagensButton.pack(pady=10, padx=10)

    imagensButton = ctk.CTkButton(menuFrame, text="Imagens", command=lambda: print("Imagens"))
    imagensButton.pack(pady=10, padx=10)

    settingsButton = ctk.CTkButton(menuFrame, text="Configurações", command=lambda: showSettings(mainFrame, config))
    settingsButton.pack(pady=10, padx=10)