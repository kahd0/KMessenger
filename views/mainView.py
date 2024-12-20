import customtkinter as ctk
from controllers.configController import loadConfig, saveConfig, applyTheme, getCurrentUser
from controllers.logController import setupLogger
from controllers.loginController import showLogin, logout  
from controllers.dbController import initializeDatabase
from controllers.mainController import showSettings  # Added import
from constants import LOGO_IMAGE_PATH, LOGO_ICO_PATH
from PIL import Image

def createMainWindow():
    setupLogger()
    initializeDatabase()
    config = loadConfig()
    applyTheme(config["tema"])

    # Configuração da janela principal
    root = ctk.CTk()
    root.title("KMessenger")
    root.geometry("800x600")
    root.iconbitmap(LOGO_ICO_PATH)

    # Centraliza a janela na tela
    windowWidth = 800
    windowHeight = 600
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    positionTop = int(screenHeight / 2 - windowHeight / 2)
    positionRight = int(screenWidth / 2 - windowWidth / 2)
    root.geometry(f"{windowWidth}x{windowHeight}+{positionRight}+{positionTop}")

    # Criação dos frames com borda de 10px
    menuFrame = ctk.CTkFrame(root, width=200, corner_radius=10)
    menuFrame.pack(side="left", fill="y", padx=10, pady=10)

    mainFrame = ctk.CTkFrame(root, corner_radius=10)
    mainFrame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    # Adiciona botão de login no menu
    logo_image = ctk.CTkImage(Image.open(LOGO_IMAGE_PATH), size=(150, 150))
    loginButton = ctk.CTkButton(menuFrame, text="Entrar", command=lambda: showLogin(mainFrame, loginButton, menuFrame, logo_image))
    loginButton.pack(pady=10, padx=10)

    # Exibe a tela de login ao iniciar a aplicação
    showLogin(mainFrame, loginButton, menuFrame, logo_image)

    # Inicia o loop principal da aplicação
    root.mainloop()

