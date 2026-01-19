import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import keyboard
import pyautogui

# =========================
# ESTADO GLOBAL
# =========================
macro_rodando = False
escutando_rebind = None

teclas = {
    "iniciar_parar": "f8",
    "sair": "f10"
}

hotkeys = []

# =========================
# FUNÇÕES DE CONTROLE
# =========================
def iniciar_parar():
    global macro_rodando
    macro_rodando = not macro_rodando
    atualizar_status()

def sair():
    janela.destroy()

def atualizar_status():
    label_status.config(
        text=f"Status: {'Rodando' if macro_rodando else 'Parado'}",
        fg="green" if macro_rodando else "red"
    )

# =========================
# HOTKEYS
# =========================
def registrar_hotkeys():
    for hk in hotkeys:
        keyboard.remove_hotkey(hk)
    hotkeys.clear()

    hotkeys.append(
        keyboard.add_hotkey(teclas["iniciar_parar"], iniciar_parar)
    )
    hotkeys.append(
        keyboard.add_hotkey(teclas["sair"], sair)
    )

def iniciar_rebind(acao):
    global escutando_rebind
    escutando_rebind = acao
    messagebox.showinfo(
        "Redefinir tecla",
        f"Pressione a nova tecla para {acao.replace('_',' ')}"
    )
    keyboard.on_press(tratar_rebind)

def tratar_rebind(event):
    global escutando_rebind
    if not escutando_rebind:
        return

    teclas[escutando_rebind] = event.name
    atualizar_labels_teclas()
    registrar_hotkeys()

    keyboard.unhook_all()
    escutando_rebind = None

# =========================
# INTERFACE
# =========================
janela = tk.Tk()
janela.title("Macro de Cliques")
janela.geometry("680x520")
janela.resizable(False, False)

tk.Label(
    janela,
    text="Macro de Cliques - Excel",
    font=("Arial", 14, "bold")
).pack(pady=8)

label_status = tk.Label(
    janela,
    text="Status: Parado",
    fg="red",
    font=("Arial", 11, "bold")
)
label_status.pack()

# =========================
# TECLAS
# =========================
frame_teclas = ttk.LabelFrame(janela, text="Teclas de Atalho")
frame_teclas.pack(fill="x", padx=10, pady=10)

labels_teclas = {}

def atualizar_labels_teclas():
    labels_teclas["iniciar_parar"].config(text=teclas["iniciar_parar"].upper())
    labels_teclas["sair"].config(text=teclas["sair"].upper())

def criar_linha_tecla(texto, acao):
    f = ttk.Frame(frame_teclas)
    f.pack(fill="x", pady=4)

    ttk.Label(f, text=texto, width=18).pack(side="left")
    lbl = ttk.Label(f, width=8)
    lbl.pack(side="left")
    labels_teclas[acao] = lbl

    ttk.Button(
        f,
        text="Redefinir",
        command=lambda: iniciar_rebind(acao)
    ).pack(side="left", padx=5)

criar_linha_tecla("Iniciar / Pausar:", "iniciar_parar")
criar_linha_tecla("Sair:", "sair")
atualizar_labels_teclas()

# =========================
# CLIQUES (FOR RANGE MANTIDO)
# =========================
frame_cliques = ttk.LabelFrame(janela, text="Cliques")
frame_cliques.pack(fill="x", padx=10, pady=10)

cliques = []

def capturar_posicao(x_var, y_var):
    messagebox.showinfo(
        "Capturar posição",
        "Posicione o mouse e pressione ENTER"
    )
    keyboard.wait("enter")
    pos = pyautogui.position()
    x_var.set(pos.x)
    y_var.set(pos.y)

for i in range(6):
    linha = ttk.Frame(frame_cliques)
    linha.pack(fill="x", pady=5)

    ttk.Label(linha, text=f"Clique {i+1}", width=10).pack(side="left")

    x = tk.IntVar(value=0)
    y = tk.IntVar(value=0)
    tempo = tk.DoubleVar(value=1.0)

    ttk.Entry(linha, width=6, textvariable=x).pack(side="left", padx=3)
    ttk.Entry(linha, width=6, textvariable=y).pack(side="left", padx=3)
    ttk.Entry(linha, width=6, textvariable=tempo).pack(side="left", padx=3)

    ttk.Button(
        linha,
        text="Capturar",
        command=lambda xv=x, yv=y: capturar_posicao(xv, yv)
    ).pack(side="left", padx=5)

    ttk.Label(linha, text="X  Y  Tempo").pack(side="left", padx=5)

    cliques.append((x, y, tempo))

# =========================
# LOOP
# =========================
frame_loop = ttk.LabelFrame(janela, text="Loop")
frame_loop.pack(fill="x", padx=10, pady=10)

tempo_loop = tk.DoubleVar(value=5.0)

ttk.Label(frame_loop, text="Tempo para repetir tudo:").pack(side="left", padx=5)
ttk.Entry(frame_loop, width=6, textvariable=tempo_loop).pack(side="left")
ttk.Label(frame_loop, text="segundos").pack(side="left")

# =========================
# LOOP DA MACRO
# =========================
def loop_macro():
    while True:
        if macro_rodando:
            for x, y, tempo in cliques:
                pyautogui.click(x.get(), y.get())
                time.sleep(tempo.get())
            time.sleep(tempo_loop.get())
        else:
            time.sleep(0.1)

# =========================
# INICIALIZAÇÃO
# =========================
registrar_hotkeys()
threading.Thread(target=loop_macro, daemon=True).start()

janela.mainloop()
