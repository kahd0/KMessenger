from controllers.logController import logInfo, logError
from controllers.mainController import showWelcomeMessage, showMainMenu, showSettings  # Added import
from controllers.dbController import checkUserCredentials
from controllers.configController import setCurrentUser, loadConfig
import customtkinter as ctk

def attemptLogin(username, password, loginButton, mainFrame, menuFrame, logo_image):
    if checkUserCredentials(username, password):
        setCurrentUser(username)
        loginButton.configure(text="Sair", fg_color="red", hover_color="darkred", command=lambda: logout(mainFrame, loginButton, menuFrame, logo_image))
        config = loadConfig()  # Load the config
        showMainMenu(menuFrame, mainFrame, config)  # Pass the config
        showWelcomeMessage(mainFrame)
        logInfo(f"Login bem-sucedido para o usuário: {username}")
        print("Login bem-sucedido!")

    else:
        logError(f"Falha no login para o usuário: {username}")
        print("Falha no login!")

def logout(mainFrame, loginButton, menuFrame, logo_image):
    loginButton.configure(text="Entrar", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"], command=lambda: showLogin(mainFrame, loginButton, menuFrame, logo_image))
    for widget in menuFrame.winfo_children():
        if widget.cget("text") not in ["Entrar"]:
            widget.destroy()
    showLogin(mainFrame, loginButton, menuFrame, logo_image)
    logInfo("Logout bem-sucedido!")
    print("Logout bem-sucedido!")

def showLogin(frame, loginButton, menuFrame, logo_image):
    # Limpa o frame principal
    for widget in frame.winfo_children():
        widget.destroy()

    # Adiciona a logo
    logoLabel = ctk.CTkLabel(frame, image=logo_image, text="")
    logoLabel.pack(pady=20)

    # Adiciona conteúdo de boas-vindas e campos de login
    welcomeLabel = ctk.CTkLabel(frame, text="Bem-vindo ao KMessenger!")
    welcomeLabel.pack(pady=20)

    usernameEntry = ctk.CTkEntry(frame, placeholder_text="Usuário")
    usernameEntry.pack(pady=10)
    usernameEntry.bind("<Return>", lambda event: passwordEntry.focus())

    passwordEntry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
    passwordEntry.pack(pady=10)
    passwordEntry.bind("<Return>", lambda event: attemptLogin(usernameEntry.get(), passwordEntry.get(), loginButton, frame, menuFrame, logo_image))

    loginSubmitButton = ctk.CTkButton(frame, text="Entrar", command=lambda: attemptLogin(usernameEntry.get(), passwordEntry.get(), loginButton, frame, menuFrame, logo_image))
    loginSubmitButton.pack(pady=10)

