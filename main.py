import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
import threading
import time
from mutagen.mp3 import MP3
import pygame

pygame.mixer.init()

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Variáveis globais
biblioteca_musicas = {}
musica_atual = None
player_ativo = False
utilizador_atual = None

# Caminho da pasta onde as músicas serão armazenadas
pasta_biblioteca = os.path.join(os.getcwd(), "biblioteca_musicas")
if not os.path.exists(pasta_biblioteca):
    os.makedirs(pasta_biblioteca)

# Funções do gerenciador de música
def carregar_musica():
    global musica_atual
    caminhos_arquivos = filedialog.askopenfilenames(filetypes=[("Arquivos de Áudio", "*.mp3 *.wav")])
    if caminhos_arquivos:
        for caminho in caminhos_arquivos:
            nome_musica = os.path.basename(caminho)
            caminho_destino = os.path.join(pasta_biblioteca, nome_musica)

            if nome_musica not in biblioteca_musicas:
                shutil.copy2(caminho, caminho_destino)
                biblioteca_musicas[nome_musica] = {"caminho": caminho_destino, "like": False}

        musica_atual = caminhos_arquivos[0]
        status_label.configure(text=f"{len(caminhos_arquivos)} músicas carregadas.")
        atualizar_lista_musicas()

def selecionar_musica(nome):
    global musica_atual
    if nome in biblioteca_musicas:
        musica_atual = biblioteca_musicas[nome]["caminho"]
        status_label.configure(text=f"Selecionado: {nome}")

def tocar_musica():
    global player_ativo
    if musica_atual:
        parar_musica()
        try:
            pygame.mixer.music.load(musica_atual)
            pygame.mixer.music.play()
            player_ativo = True
            status_label.configure(text=f"Tocando: {os.path.basename(musica_atual)}")
            thread = threading.Thread(target=atualizar_barra_progresso)
            thread.daemon = True
            thread.start()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível tocar a música: {e}")
    else:
        messagebox.showwarning("Nenhuma música selecionada", "Por favor, selecione uma música para tocar.")

def parar_musica():
    global player_ativo
    if player_ativo:
        pygame.mixer.music.stop()
        player_ativo = False
    status_label.configure(text="Parado")
    barra_progresso.set(0.0)

def atualizar_barra_progresso():
    global musica_atual
    if musica_atual:
        try:
            audio = MP3(musica_atual)
            duracao = audio.info.length
            for i in range(int(duracao)):
                if not player_ativo:
                    break
                barra_progresso.set(i / duracao)
                time.sleep(1)
        except Exception as e:
            print(f"Erro ao atualizar a barra de progresso: {e}")

def atualizar_lista_musicas():
    for widget in music_grid_frame.winfo_children():
        widget.destroy()

    for nome, dados in biblioteca_musicas.items():
        cor = "red" if dados["like"] else "white"
        musica_button = ctk.CTkButton(music_grid_frame, 
                                      text=nome, 
                                      fg_color=cor, 
                                      text_color="black",
                                      command=lambda nome=nome: selecionar_musica(nome))
        musica_button.pack(padx=10, pady=10, fill="x")

# Funções de autenticação
def login():
    utilizador = utilizador_entry.get().strip()
    senha = senha_entry.get().strip()

    if not utilizador or not senha:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    caminho_utilizador = os.path.join("dados_utilizadores", utilizador)

    if os.path.exists(caminho_utilizador):
        f = open(os.path.join(caminho_utilizador, "dados.txt"), "r")
        dados = f.readlines()
        f.close()
        senha_correta = dados[1].split(": ")[1].strip()


        if senha == senha_correta:
                global utilizador_atual
                utilizador_atual = utilizador
                login_frame.pack_forget()
                app_frame.pack(expand=True, fill="both", padx=20, pady=20)
                return

    messagebox.showerror("Erro", "Utilizador ou senha incorretos.")

def criar_conta():
    novo_utilizador = novo_utilizador_entry.get().strip()
    nova_senha = nova_senha_entry.get().strip()
    confirmar_senha = confirmar_senha_entry.get().strip()

    caminho_utilizador = os.path.join("dados_utilizadores", novo_utilizador)

    if not novo_utilizador or not nova_senha or not confirmar_senha:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    if nova_senha != confirmar_senha:
        messagebox.showerror("Erro", "As senhas não coincidem.")
        return

    if os.path.exists(caminho_utilizador):
        messagebox.showerror("Erro", "Nome de utilizador já está em uso.")
        return

    os.makedirs(caminho_utilizador)
    f = open(os.path.join(caminho_utilizador, "dados.txt"), "w")
    f.write(f"Utilizador: {novo_utilizador}\nSenha: {nova_senha}")
    f.close()


    messagebox.showinfo("Sucesso", "Conta criada com sucesso.")
    criar_conta_frame.pack_forget()
    login_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Configuração da interface
def mostrar_tela_criar_conta():
    login_frame.pack_forget()
    criar_conta_frame.pack(expand=True, fill="both", padx=20, pady=20)

app = ctk.CTk()
app.title("MusicWave")
app.geometry("1024x640")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Tela de login
login_frame = ctk.CTkFrame(app, corner_radius=10)
login_frame.pack(expand=True, fill="both", padx=20, pady=20)

login_label = ctk.CTkLabel(login_frame, text="Login", font=("Roboto", 24, "bold"))
login_label.pack(pady=20)

utilizador_entry = ctk.CTkEntry(login_frame, placeholder_text="Utilizador", width=522, height=33)
utilizador_entry.pack(pady=10, padx=20)

senha_entry = ctk.CTkEntry(login_frame, placeholder_text="Senha", show="*", width=522, height=33)
senha_entry.pack(pady=10, padx=20)

login_button = ctk.CTkButton(login_frame, text="Entrar", command=login, fg_color="#5B299B", text_color="white", width=522, height=33, corner_radius=15)
login_button.pack(pady=10)

criar_conta_button = ctk.CTkButton(login_frame, text="Criar Conta", command=mostrar_tela_criar_conta, fg_color="#5B299B", text_color="white", width=522, height=33, corner_radius=15)
criar_conta_button.pack(pady=10)

# Tela de criação de conta
criar_conta_frame = ctk.CTkFrame(app, corner_radius=10)

criar_conta_label = ctk.CTkLabel(criar_conta_frame, text="Criar Conta", font=("Roboto", 24, "bold"))
criar_conta_label.pack(pady=20)

novo_utilizador_entry = ctk.CTkEntry(criar_conta_frame, placeholder_text="Novo Utilizador", width=522, height=33)
novo_utilizador_entry.pack(pady=10, padx=20)


nova_senha_entry = ctk.CTkEntry(criar_conta_frame, placeholder_text="Senha", show="*", width=522, height=33)
nova_senha_entry.pack(pady=10, padx=20)


confirmar_senha_entry = ctk.CTkEntry(criar_conta_frame, placeholder_text="Confirmar Senha", show="*", width=522, height=33)
confirmar_senha_entry.pack(pady=10, padx=20)

salvar_conta_button = ctk.CTkButton(criar_conta_frame, text="Criar Conta", command=criar_conta, fg_color="#5B299B", text_color="white", width=522, height=43, corner_radius=15)
salvar_conta_button.pack(pady=20)

btn_voltar_login = ctk.CTkButton(criar_conta_frame, fg_color="#5B299B", text_color="white", width=522, height=41, corner_radius=15, text="Voltar", command=lambda: [criar_conta_frame.pack_forget(), login_frame.pack(expand=True, fill="both", padx=20, pady=20)])
btn_voltar_login.pack(pady=10)

# Tela principal
app_frame = ctk.CTkFrame(app)

# Cabeçalho da tela principal
app_label = ctk.CTkLabel(app_frame, text="Gerenciador de Música", font=("Roboto", 24, "bold"))
app_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

logout_button = ctk.CTkButton(app_frame, text="Terminar Sessão", command=lambda: logout())
logout_button.grid(row=0, column=1, padx=20, pady=10, sticky="e")

# Menu lateral 
menu_frame = ctk.CTkFrame(app_frame, width=200, corner_radius=10)
menu_frame.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)

menu_label = ctk.CTkLabel(menu_frame, text="Música", font=("Roboto", 20, "bold"))
menu_label.pack(pady=20)

search_entry = ctk.CTkEntry(menu_frame, placeholder_text="Pesquisar...")
search_entry.pack(pady=10, padx=20, fill="x")

btn_home = ctk.CTkButton(menu_frame, text="Home", width=180, corner_radius=5, fg_color="purple")
btn_home.pack(pady=5)

btn_playlists = ctk.CTkButton(menu_frame, text="Playlists", width=180, corner_radius=5)
btn_playlists.pack(pady=5)

btn_albums = ctk.CTkButton(menu_frame, text="Álbuns", width=180, corner_radius=5)
btn_albums.pack(pady=5)

btn_artists = ctk.CTkButton(menu_frame, text="Artistas", width=180, corner_radius=5)
btn_artists.pack(pady=5)

# Conteúdo principal da tela de música
conteudo_frame = ctk.CTkFrame(app_frame, corner_radius=10)
conteudo_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

conteudo_label = ctk.CTkLabel(conteudo_frame, text="Bem-vindo", font=("Roboto", 26, "bold"))
conteudo_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

recent_label = ctk.CTkLabel(conteudo_frame, text="Ouvido recentemente", font=("Roboto", 18))
recent_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

# Placeholder de músicas recentes
for i in range(3):
    placeholder = ctk.CTkFrame(conteudo_frame, width=150, height=150, fg_color="gray")
    placeholder.grid(row=2, column=i, padx=10, pady=10)

# Grid para exibir músicas
music_grid_frame = ctk.CTkScrollableFrame(conteudo_frame, width=600, height=300)
music_grid_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)

# Controles de reprodução
controles_frame = ctk.CTkFrame(app_frame, height=80, corner_radius=10)
controles_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

barra_progresso = ctk.CTkProgressBar(controles_frame, height=10)
barra_progresso.set(0.0)
barra_progresso.pack(fill="x", padx=20, pady=10)

status_label = ctk.CTkLabel(controles_frame, text="Bem-vindo ao Gerenciador de Música", font=("Roboto", 14))
status_label.pack(side="left", padx=20)

btn_prev = ctk.CTkButton(controles_frame, text="\u23ee\ufe0f", width=50)
btn_prev.pack(side="left", padx=5)

btn_play = ctk.CTkButton(controles_frame, text="\u25b6\ufe0f", width=50, command=tocar_musica)
btn_play.pack(side="left", padx=5)

btn_next = ctk.CTkButton(controles_frame, text="\u23ed\ufe0f", width=50)
btn_next.pack(side="left", padx=5)

# Função para sair
def logout():
    global utilizador_atual
    utilizador_atual = None
    app_frame.pack_forget()
    login_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Configuração do grid
app_frame.grid_rowconfigure(1, weight=1)
app_frame.grid_columnconfigure(1, weight=1)

# Inicializar o app
app.mainloop()
