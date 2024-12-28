import customtkinter as ctk
from tkinter import filedialog
import os
from tkinter import messagebox

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")  # Modos: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# Funções de controle
musica_atual = None
player_ativo = False

def carregar_musica():
    global musica_atual
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Áudio", "*.mp3 *.wav")])
    if caminho_arquivo:
        musica_atual = caminho_arquivo
        lista_musicas.insert("end", caminho_arquivo.split("/")[-1])
        status_label.configure(text=f"Carregado: {caminho_arquivo.split('/')[-1]}")

def tocar_musica():
    global player_ativo
    if musica_atual:
        parar_musica()  # Garantir que nenhuma música anterior esteja a tocar
        os.system(f"start {musica_atual}")
        player_ativo = True
        status_label.configure(text=f"Tocando: {musica_atual.split('/')[-1]}")
    else:
        messagebox.showwarning("Nenhuma música selecionada", "Por favor, carregue uma música para tocar.")

def pausar_musica():
    messagebox.showinfo("Pausar", "Pausar música não é suportado com este método.")

def retomar_musica():
    messagebox.showinfo("Retomar", "Retomar música não é suportado com este método.")

def parar_musica():
    global player_ativo
    if player_ativo:
        os.system("taskkill /im wmplayer.exe /f")  # Para o Windows Media Player
        player_ativo = False
    status_label.configure(text="Parado")

# Janela principal
app = ctk.CTk()
app.title("Gerenciador de Música")
app.geometry("800x600")

# Frame lateral (menu)
menu_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
menu_frame.pack(side="left", fill="y")

menu_label = ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 20, "bold"))
menu_label.pack(pady=20)

btn_biblioteca = ctk.CTkButton(menu_frame, text="Biblioteca", width=180, command=carregar_musica)
btn_biblioteca.pack(pady=10)

btn_playlists = ctk.CTkButton(menu_frame, text="Playlists", width=180)
btn_playlists.pack(pady=10)

btn_configuracoes = ctk.CTkButton(menu_frame, text="Configurações", width=180)
btn_configuracoes.pack(pady=10)

# Frame principal (conteúdo)
conteudo_frame = ctk.CTkFrame(app)
conteudo_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

conteudo_label = ctk.CTkLabel(conteudo_frame, text="Tocando Agora", font=("Arial", 24, "bold"))
conteudo_label.pack(pady=10)

lista_musicas = ctk.CTkTextbox(conteudo_frame, height=300)
lista_musicas.pack(fill="both", expand=True, pady=10)
lista_musicas.insert("1.0", "Carregue músicas para exibir aqui")

status_label = ctk.CTkLabel(conteudo_frame, text="Status: Ocioso", font=("Arial", 16))
status_label.pack(pady=10)

# Barra inferior (controles)
controles_frame = ctk.CTkFrame(app, height=80)
controles_frame.pack(side="bottom", fill="x")

btn_tocar = ctk.CTkButton(controles_frame, text="Tocar", width=100, command=tocar_musica)
btn_tocar.pack(side="left", padx=10, pady=10)

btn_pausar = ctk.CTkButton(controles_frame, text="Pausar", width=100, command=pausar_musica)
btn_pausar.pack(side="left", padx=10, pady=10)

btn_retomar = ctk.CTkButton(controles_frame, text="Retomar", width=100, command=retomar_musica)
btn_retomar.pack(side="left", padx=10, pady=10)

btn_parar = ctk.CTkButton(controles_frame, text="Parar", width=100, command=parar_musica)
btn_parar.pack(side="left", padx=10, pady=10)

barra_progresso = ctk.CTkProgressBar(controles_frame, width=400)
barra_progresso.set(0.0)  # Configuração inicial (0%)
barra_progresso.pack(side="left", padx=20)

# Inicializar a aplicação
app.mainloop()
