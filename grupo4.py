import customtkinter as ctk
from PIL import Image  # Para carregar imagens com a biblioteca PIL

# Configurações gerais da janela
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AplicacaoMusica(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("Aplicação de Música")
        self.geometry(f"{self.winfo_screenwidth()}x{self. winfo_screenheight()}")
        self.resizable(True, True)

        # Ativar modo de tela cheia
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        self.fullscreen = False

        # Configurar layout responsivo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Carregar as imagens para os botões
        self.icon_home = ctk.CTkImage(Image.open("images/home_icon.png"), size=(30, 30))
        self.icon_playlists = ctk.CTkImage(Image.open("images/playlists_icon.png"), size=(30, 30))
        self.icon_albuns = ctk.CTkImage(Image.open("images/albuns_icon.png"), size=(30, 30))
        self.icon_artistas = ctk.CTkImage(Image.open("images/artistas_icon.png"), size=(30, 30))

        # Barra lateral
        self.barra_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.barra_lateral.grid(row=0, column=0, sticky="nswe")
        self.barra_lateral.grid_rowconfigure(7, weight=1)  # Para empurrar o botão "Conta" para baixo

        self.label_barra_lateral = ctk.CTkLabel(self.barra_lateral, text="Música", font=("Arial", 20, "bold"))
        self.label_barra_lateral.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.campo_pesquisa = ctk.CTkEntry(self.barra_lateral, placeholder_text="Pesquisar...")
        self.campo_pesquisa.grid(row=1, column=0, padx=20, pady=(10, 20))

        # Alterando os botões para usar as imagens
        self.botao_home = ctk.CTkButton(self.barra_lateral, text="Home", image=self.icon_home, compound="left", fg_color="#6c63ff", hover_color="#5752d1", command=self.mostrar_home)
        self.botao_home.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.botao_playlists = ctk.CTkButton(self.barra_lateral, text="Playlists", image=self.icon_playlists, compound="left", command=self.mostrar_playlists)
        self.botao_playlists.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.botao_albuns = ctk.CTkButton(self.barra_lateral, text="Álbuns", image=self.icon_albuns, compound="left", command=self.mostrar_albuns)
        self.botao_albuns.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.botao_artistas = ctk.CTkButton(self.barra_lateral, text="Artistas", image=self.icon_artistas, compound="left", command=self.mostrar_artistas)
        self.botao_artistas.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.botao_conta = ctk.CTkButton(self.barra_lateral, text="Conta")
        self.botao_conta.grid(row=7, column=0, padx=20, pady=10, sticky="sw")

        # Área principal
        self.area_principal = ctk.CTkFrame(self, corner_radius=10)
        self.area_principal.grid(row=0, column=1, sticky="nswe", padx=(0, 20), pady=20)
        self.area_principal.grid_rowconfigure(0, weight=1)
        self.area_principal.grid_columnconfigure(0, weight=1)

        self.frames = {
            "home": self.criar_frame_home(),
            "playlists": self.criar_frame_playlists(),
            "albuns": self.criar_frame_albuns(),
            " artistas": self.criar_frame_artistas()
        }

        self.mostrar_home()

    def criar_frame_home(self):
        frame = ctk.CTkFrame(self.area_principal, corner_radius=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.label_bem_vindo = ctk.CTkLabel(frame, text="Bem-vindo", font=("Arial", 24, "bold"))
        self.label_bem_vindo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.label_ouvido_recentemente = ctk.CTkLabel(frame, text="Ouvido recentemente:", font=("Arial", 16))
        self.label_ouvido_recentemente.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="w")

        self.frame_recentes = ctk.CTkFrame(frame)
        self.frame_recentes.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nswe")
        self.frame_recentes.grid_columnconfigure((0, 1, 2), weight=1)

        for i in range(3):
            placeholder = ctk.CTkFrame(self.frame_recentes, corner_radius=10)
            placeholder.grid(row=0, column=i, padx=10, sticky="nswe")

        self.frame_player = ctk.CTkFrame(frame, height=50, corner_radius=10)
        self.frame_player.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.label_musica = ctk.CTkLabel(self.frame_player, text="What was I made for - Billie Eilish")
        self.label_musica.grid(row=0, column=0, padx=10, pady=10)

        self.botao_play = ctk.CTkButton(self.frame_player, text="⏯", width=40)
        self.botao_play.grid(row=0, column=1, padx=5)

        self.botao_next = ctk.CTkButton(self.frame_player, text="⏭", width=40)
        self.botao_next.grid(row=0, column=2, padx=5)

        self.botao_prev = ctk.CTkButton(self.frame_player, text="⏮", width=40)
        self.botao_prev.grid(row=0, column=3, padx=5)

        return frame

    def criar_frame_playlists(self):
        frame = ctk.CTkFrame(self.area_principal, corner_radius=10)
        frame.grid_rowconfigure((0, 1), weight=1)
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        label = ctk.CTkLabel(frame, text="Playlists", font=("Arial", 24, "bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w")

        for i in range(2):
            for j in range(3):
                placeholder = ctk.CTkFrame(frame, corner_radius=10)
                placeholder.grid(row=i+1, column=j, padx=20, pady=10, sticky="nswe")

        return frame

    def criar_frame_albuns(self):
        frame = ctk.CTkFrame(self.area_principal, corner_radius=10)
        frame.grid_rowconfigure((0, 1), weight=1)
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        label = ctk.CTkLabel(frame, text="Álbuns", font=("Arial", 24, "bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w")

        for i in range(2):
            for j in range(3):
                placeholder = ctk.CTkFrame(frame, corner_radius=10)
                placeholder.grid(row=i+1, column=j, padx=20, pady=10, sticky="nswe")

        return frame

    def criar_frame_artistas(self):
        frame = ctk.CTkFrame(self.area_principal, corner_radius=10)
        frame.grid_rowconfigure((0, 1), weight=1)
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        label = ctk.CTkLabel(frame, text="Artistas", font=("Arial", 24, "bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w")

        for i in range(2):
            for j in range(3):
                placeholder = ctk.CTkFrame(frame, corner_radius=10)
                placeholder.grid(row=i+1, column=j, padx=20, pady=10, sticky="nswe")

        return frame

    def mostrar_home(self):
        self.alternar_frame("home")

    def mostrar_playlists(self):
        self.alternar_frame("playlists")

    def mostrar_albuns(self):
        self.alternar_frame("albuns")

    def mostrar_artistas(self):
        self.alternar_frame("artistas")

    def alternar_frame(self, frame_nome):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[frame_nome].grid(row=0, column=0, sticky="nswe")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)

# Executar aplicação
if __name__ == "__main__":
    app = AplicacaoMusica()
    app.mainloop()