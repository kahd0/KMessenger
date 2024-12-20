from tkinter import messagebox, Listbox  # Updated import
import customtkinter as ctk
from controllers.dbController import getAllMessages, getMessageText, addMessage, updateMessage, deleteMessage  # Updated import

def showMessages(frame):
    # Limpa o frame principal
    for widget in frame.winfo_children():
        widget.destroy()

    messages = getAllMessages()

    listbox = Listbox(frame)  # Changed to tkinter.Listbox
    listbox.grid(row=0, column=0, rowspan=1, sticky="ns", padx=10, pady=10)

    for message in messages:
        listbox.insert("end", message[1])

    text_area = ctk.CTkTextbox(frame, state="disabled")
    text_area.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

    def onSelect(event):
        selected_index = listbox.curselection()
        if selected_index:
            message_id = messages[selected_index[0]][0]
            text_area.configure(state="normal")
            text_area.delete("1.0", "end")
            text_area.insert("1.0", getMessageText(message_id))
            text_area.configure(state="disabled")

    listbox.bind("<<ListboxSelect>>", onSelect)

    def newMessage():
        top = ctk.CTkToplevel(frame)
        top.title("Nova Mensagem")
        top.grab_set()  # Prevent interaction with mainView
        top.geometry(f"+{frame.winfo_rootx() + 50}+{frame.winfo_rooty() + 50}")  # Center the modal

        name_label = ctk.CTkLabel(top, text="Nome:")
        name_label.pack(pady=5)
        name_entry = ctk.CTkEntry(top)
        name_entry.pack(pady=5)

        text_label = ctk.CTkLabel(top, text="Texto:")
        text_label.pack(pady=5)
        text_entry = ctk.CTkTextbox(top)
        text_entry.pack(pady=5)

        def saveNewMessage():
            addMessage(name_entry.get(), text_entry.get("1.0", "end").strip())
            messagebox.showinfo("Sucesso", "Mensagem salva com sucesso!")
            top.destroy()
            showMessages(frame)

        save_button = ctk.CTkButton(top, text="Salvar", command=saveNewMessage)
        save_button.pack(side="left", padx=10, pady=10)

        cancel_button = ctk.CTkButton(top, text="Cancelar", command=top.destroy)
        cancel_button.pack(side="right", padx=10, pady=10)

    def editMessage():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Nenhuma mensagem selecionada.")
            return

        message_id = messages[selected_index[0]][0]
        text_area.configure(state="normal")

        listbox.configure(state="disabled")
        new_button.configure(state="disabled")
        delete_button.configure(state="disabled")
        edit_button.configure(state="disabled")

        def saveEdit():
            updateMessage(message_id, text_area.get("1.0", "end").strip())
            messagebox.showinfo("Sucesso", "Mensagem atualizada com sucesso!")
            text_area.configure(state="disabled")
            listbox.configure(state="normal")
            new_button.configure(state="normal")
            delete_button.configure(state="normal")
            edit_button.configure(state="normal")
            save_button.destroy()
            cancel_button.destroy()
            showMessages(frame)

        def cancelEdit():
            text_area.configure(state="disabled")
            listbox.configure(state="normal")
            new_button.configure(state="normal")
            delete_button.configure(state="normal")
            edit_button.configure(state="normal")
            save_button.destroy()
            cancel_button.destroy()
            showMessages(frame)

        save_button = ctk.CTkButton(frame, text="Salvar", command=saveEdit)
        save_button.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        cancel_button = ctk.CTkButton(frame, text="Cancelar", command=cancelEdit)
        cancel_button.grid(row=1, column=2, sticky="ew", padx=10, pady=10)

    def handleDeleteMessage():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Nenhuma mensagem selecionada.")
            return

        message_id = messages[selected_index[0]][0]
        if messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir a mensagem selecionada?"):
            deleteMessage(message_id)
            messagebox.showinfo("Sucesso", "Mensagem excluída com sucesso!")
            showMessages(frame)

    new_button = ctk.CTkButton(frame, text="Nova Mensagem", command=newMessage)
    new_button.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    edit_button = ctk.CTkButton(frame, text="Editar", command=editMessage)
    edit_button.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

    delete_button = ctk.CTkButton(frame, text="Excluir", command=handleDeleteMessage)
    delete_button.grid(row=2, column=2, sticky="ew", padx=10, pady=10)

    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)
