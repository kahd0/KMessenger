import json
import os
import customtkinter as ctk
from tkinter import messagebox  # Added import
from constants import CONFIG_FILE
from controllers.dbController import addUser, changePassword, deleteUser, getAllUsers  # Updated import

def loadConfig():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            if "tema" not in config:
                config["tema"] = "sistema"
            return config
    return {"tema": "sistema"}

def saveConfig(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def applyTheme(tema):
    import customtkinter as ctk
    if tema == "claro":
        ctk.set_appearance_mode("light")
    elif tema == "escuro":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("system")

def setCurrentUser(username):
    config = loadConfig()
    config["current_user"] = username
    saveConfig(config)

def getCurrentUser():
    config = loadConfig()
    return config.get("current_user", None)

def handleAddUser(username, password):
    try:
        addUser(username, password)
        print("Usuário criado com sucesso!")
    except ValueError as e:
        print(e)

def applyAndSaveTheme(config, tema):
    config["tema"] = tema
    saveConfig(config)
    applyTheme(tema)
    print("Configurações salvas!")

def showSettings(frame, config):
    # Limpa o frame principal
    for widget in frame.winfo_children():
        widget.destroy()

    current_user = getCurrentUser()

    # Adiciona opções de configuração de tema
    themeLabel = ctk.CTkLabel(frame, text="Escolha o tema:")
    themeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    themeVar = ctk.StringVar(value=config["tema"])
    themeComboBox = ctk.CTkComboBox(frame, values=["claro", "escuro", "sistema"], variable=themeVar)
    themeComboBox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    saveButton = ctk.CTkButton(frame, text="Salvar", command=lambda: applyAndSaveTheme(config, themeVar.get().lower()))
    saveButton.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    if current_user:
        # Adiciona opção para alterar a senha
        passwordLabel = ctk.CTkLabel(frame, text="Alterar senha:")
        passwordLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        newPasswordEntry = ctk.CTkEntry(frame, placeholder_text="Nova senha", show="*")
        newPasswordEntry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        confirmPasswordEntry = ctk.CTkEntry(frame, placeholder_text="Confirmar nova senha", show="*")
        confirmPasswordEntry.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        def handleChangePassword():
            if newPasswordEntry.get() == confirmPasswordEntry.get():
                changePassword(current_user, newPasswordEntry.get())
                messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
                newPasswordEntry.delete(0, 'end')
                confirmPasswordEntry.delete(0, 'end')
            else:
                messagebox.showerror("Erro", "As senhas não coincidem")

        changePasswordButton = ctk.CTkButton(frame, text="Alterar", command=handleChangePassword)
        changePasswordButton.grid(row=1, column=3, padx=10, pady=10, sticky="e")

        # Adiciona opção para criar um novo usuário
        newUserLabel = ctk.CTkLabel(frame, text="Criar novo usuário:")
        newUserLabel.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        newUsernameEntry = ctk.CTkEntry(frame, placeholder_text="Usuário")
        newUsernameEntry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        newUserPasswordEntry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
        newUserPasswordEntry.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        def handleCreateUser():
            try:
                handleAddUser(newUsernameEntry.get(), newUserPasswordEntry.get())
                messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
                newUsernameEntry.delete(0, 'end')
                newUserPasswordEntry.delete(0, 'end')
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

        createUserButton = ctk.CTkButton(frame, text="Criar", command=handleCreateUser)
        createUserButton.grid(row=3, column=3, padx=10, pady=10, sticky="e")

        # Adiciona opção para excluir um usuário
        deleteUserLabel = ctk.CTkLabel(frame, text="Excluir usuário:")
        deleteUserLabel.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        all_users = getAllUsers()
        all_users.remove(current_user)  # Remove the current user from the list
        deleteUserVar = ctk.StringVar()
        deleteUserComboBox = ctk.CTkComboBox(frame, values=all_users, variable=deleteUserVar)
        deleteUserComboBox.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        def handleDeleteUser():
            user_to_delete = deleteUserVar.get()
            if user_to_delete == current_user:
                messagebox.showerror("Erro", "Não é possível excluir o usuário logado.")
            elif messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir o usuário '{user_to_delete}'?"):
                deleteUser(user_to_delete)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                deleteUserComboBox.set("")  # Clear the combobox selection
                deleteUserComboBox.configure(values=getAllUsers())  # Refresh the combobox values

        deleteUserButton = ctk.CTkButton(frame, text="Excluir", command=handleDeleteUser)
        deleteUserButton.grid(row=4, column=2, padx=10, pady=10, sticky="e")

    # Ajusta as colunas para expandirem corretamente
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

