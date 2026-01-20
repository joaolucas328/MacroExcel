import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import keyboard
import pyautogui
import pyperclip


# ESTADO GLOBAL


macro_rodando = False

teclas = {
    "iniciar_parar": "f8",
    "sair": "f10"
}

hotkeys = []


# FUNÇÕES


def copiar_valor():
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.05)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.1)

    texto = pyperclip.paste()
    texto = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()

    try:
        return float(texto)
    except:
        return None


def clique_duplo_seguro(x, y, tempo):
    pyautogui.mouseUp()
    time.sleep(0.05)
    pyautogui.moveTo(x, y)
    time.sleep(0.05)
    pyautogui.doubleClick()
    time.sleep(tempo)


def clique_simples_seguro(x, y, tempo):
    pyautogui.mouseUp()
    time.sleep(0.05)
    pyautogui.moveTo(x, y)
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(tempo)


# CONTROLE


def iniciar_parar():
    global macro_rodando
    macro_rodando = not macro_rodando
    label_status.config(
        text=f"Status: {'Rodando' if macro_rodando else 'Parado'}",
        fg="green" if macro_rodando else "red"
    )

def sair():
    janela.destroy()

def registrar_hotkeys():
    for hk in hotkeys:
        keyboard.remove_hotkey(hk)
    hotkeys.clear()

    hotkeys.append(keyboard.add_hotkey(teclas["iniciar_parar"], iniciar_parar))
    hotkeys.append(keyboard.add_hotkey(teclas["sair"], sair))

# INTERFACE


janela = tk.Tk()
janela.title("Macro Excel")
janela.geometry("320x500")
janela.resizable(True, True)

tk.Label(janela, text="Macro Excel", font=("Arial", 14, "bold")).pack(pady=8)

label_status = tk.Label(
    janela, text="Status: Parado", fg="red", font=("Arial", 11, "bold")
)
label_status.pack()


# CLIQUES


frame_cliques = ttk.LabelFrame(janela, text="Cliques")
frame_cliques.pack(fill="x", padx=10, pady=10)

cliques = []

def capturar_posicao(x_var, y_var):
    messagebox.showinfo("Capturar", "Posicione o mouse e pressione ENTER")
    keyboard.wait("enter")
    pos = pyautogui.position()
    x_var.set(pos.x)
    y_var.set(pos.y)

for i in range(11):
    linha = ttk.Frame(frame_cliques)
    linha.pack(fill="x", pady=4)

    ttk.Label(linha, text=f"Clique {i+1}", width=10).pack(side="left")

    x = tk.IntVar(value=0)
    y = tk.IntVar(value=0)
    tempo = tk.DoubleVar(value=1.5)

    ttk.Entry(linha, width=6, textvariable=x).pack(side="left", padx=3)
    ttk.Entry(linha, width=6, textvariable=y).pack(side="left", padx=3)
    ttk.Entry(linha, width=6, textvariable=tempo).pack(side="left", padx=3)

    ttk.Button(
        linha,
        text="Capturar",
        command=lambda xv=x, yv=y: capturar_posicao(xv, yv)
    ).pack(side="left", padx=5)

    cliques.append((x, y, tempo))


# LOOP DO MACRO


def loop_macro():
    while True:
        if not macro_rodando:
            time.sleep(0.1)
            continue

        # 1
        clique_duplo_seguro(cliques[0][0].get(), cliques[0][1].get(), cliques[0][2].get())
        valor_base = copiar_valor()
        if valor_base is None:
            continue
        valor_base *= 2.77

        # 2
        clique_duplo_seguro(cliques[1][0].get(), cliques[1][1].get(), cliques[1][2].get())
        copiar_valor()

        # 3
        clique_simples_seguro(cliques[2][0].get(), cliques[2][1].get(), cliques[2][2].get())

        # 4
        clique_simples_seguro(cliques[3][0].get(), cliques[3][1].get(), 0.1)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        time.sleep(cliques[3][2].get())

        # 5
        clique_duplo_seguro(cliques[4][0].get(), cliques[4][1].get(), cliques[4][2].get())

        # 6
        clique_simples_seguro(cliques[5][0].get(), cliques[5][1].get(), cliques[5][2].get())
        valor_atual = copiar_valor()
        if valor_atual is None:
            continue

        # 7
        clique_simples_seguro(cliques[6][0].get(), cliques[6][1].get(), cliques[6][2].get())

        # 8
        clique_simples_seguro(cliques[7][0].get(), cliques[7][1].get(), cliques[7][2].get())

        # 9
        clique_simples_seguro(cliques[8][0].get(), cliques[8][1].get(), cliques[8][2].get())

        # CONDIÇÃO
        if valor_atual < valor_base:
            clique_simples_seguro(cliques[9][0].get(), cliques[9][1].get(), cliques[9][2].get())
            pyautogui.scroll(-100)
        else:
            clique_simples_seguro(cliques[10][0].get(), cliques[10][1].get(), cliques[10][2].get())
            pyautogui.scroll(-100)

        time.sleep(2)


# INICIALIZAÇÃO

registrar_hotkeys()
threading.Thread(target=loop_macro, daemon=True).start()
janela.mainloop()
