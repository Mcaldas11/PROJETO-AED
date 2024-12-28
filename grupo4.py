import customtkinter as ctk
from tkinter import filedialog
import os
from tkinter import messagebox

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")  # Modos: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# Funções de controle
current_song = None
player_running = False

def load_music():
    global current_song
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        current_song = file_path
        song_listbox.insert("end", file_path.split("/")[-1])
        status_label.configure(text=f"Loaded: {file_path.split('/')[-1]}")

def play_music():
    global player_running
    if current_song:
        stop_music()  # Garantir que nenhuma música anterior esteja a ser tocada
        os.system(f"start {current_song}")
        player_running = True
        status_label.configure(text=f"Playing: {current_song.split('/')[-1]}")
    else:
        messagebox.showwarning("No song selected", "Please load a song to play.")

def pause_music():
    messagebox.showinfo("Pause", "Pausing music is not supported with this method.")

def resume_music():
    messagebox.showinfo("Resume", "Resuming music is not supported with this method.")

def stop_music():
    global player_running
    if player_running:
        os.system("taskkill /im wmplayer.exe /f")  # Para o Windows Media Player
        player_running = False
    status_label.configure(text="Stopped")

# Janela principal
app = ctk.CTk()
app.title("Music Manager")
app.geometry("800x600")

# Frame lateral (menu)
menu_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
menu_frame.pack(side="left", fill="y")

menu_label = ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 20, "bold"))
menu_label.pack(pady=20)

btn_library = ctk.CTkButton(menu_frame, text="Library", width=180, command=load_music)
btn_library.pack(pady=10)

btn_playlists = ctk.CTkButton(menu_frame, text="Playlists", width=180)
btn_playlists.pack(pady=10)

btn_settings = ctk.CTkButton(menu_frame, text="Settings", width=180)
btn_settings.pack(pady=10)

# Frame principal (conteúdo)
content_frame = ctk.CTkFrame(app)
content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

content_label = ctk.CTkLabel(content_frame, text="Now Playing", font=("Arial", 24, "bold"))
content_label.pack(pady=10)

song_listbox = ctk.CTkTextbox(content_frame, height=300)
song_listbox.pack(fill="both", expand=True, pady=10)
song_listbox.insert("1.0", "Load songs to display here")

status_label = ctk.CTkLabel(content_frame, text="Status: Idle", font=("Arial", 16))
status_label.pack(pady=10)

# Barra inferior (controles)
control_frame = ctk.CTkFrame(app, height=80)
control_frame.pack(side="bottom", fill="x")

play_button = ctk.CTkButton(control_frame, text="Play", width=100, command=play_music)
play_button.pack(side="left", padx=10, pady=10)

pause_button = ctk.CTkButton(control_frame, text="Pause", width=100, command=pause_music)
pause_button.pack(side="left", padx=10, pady=10)

resume_button = ctk.CTkButton(control_frame, text="Resume", width=100, command=resume_music)
resume_button.pack(side="left", padx=10, pady=10)

stop_button = ctk.CTkButton(control_frame, text="Stop", width=100, command=stop_music)
stop_button.pack(side="left", padx=10, pady=10)

progress_bar = ctk.CTkProgressBar(control_frame, width=400)
progress_bar.set(0.0)  # Configuração inicial (0%)
progress_bar.pack(side="left", padx=20)

# Inicializar a aplicação
app.mainloop()
