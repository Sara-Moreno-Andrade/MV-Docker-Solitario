import tkinter as tk
import random

class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.color = 'red' if palo in ['♥', '♦'] else 'black'
        self.volteada = False

    def __str__(self):
        return f"{self.valor}{self.palo}" if self.volteada else "??"

class Solitario:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitario Klondike Básico")
        self.root.geometry("1000x600")

        self.inicio_frame = tk.Frame(self.root, bg="darkgreen")
        self.inicio_frame.place(relwidth=1, relheight=1)

        titulo = tk.Label(self.inicio_frame, text="Solitario Klondike", font=("Arial", 36, "bold"), fg="white", bg="darkgreen")
        titulo.pack(pady=100)

        boton_inicio = tk.Button(self.inicio_frame, text="Empezar Juego", font=("Arial", 18), command=self.iniciar_juego)
        boton_inicio.pack()

    def iniciar_juego(self):
        self.inicio_frame.destroy()

        self.palos = ['♠', '♥', '♦', '♣']
        self.valores = ['A'] + list(map(str, range(2, 11))) + ['J', 'Q', 'K']
        self.baraja = self.crear_baraja()

        self.pilas_tablero = [[] for _ in range(7)]
        self.mazo = []
        self.descarte = []
        self.fundaciones = [[] for _ in range(4)]

        self.cartas_widgets = {}
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="green")
        self.canvas.pack()

        self.canvas.create_text(100, 30, text="Mazo", fill="white", font=("Arial", 14))
        self.canvas.create_text(250, 30, text="Descarte", fill="white", font=("Arial", 14))
        self.canvas.create_text(700, 30, text="Fundaciones", fill="white", font=("Arial", 14))

        self.btn_mazo = tk.Button(self.root, text="Robar", command=self.robar_carta)
        self.canvas.create_window(100, 60, window=self.btn_mazo)

        self.repartir_cartas()

        self.carta_seleccionada = None
        self.origen = None

    def crear_baraja(self):
        baraja = [Carta(v, p) for p in self.palos for v in self.valores]
        random.shuffle(baraja)
        return baraja

    def repartir_cartas(self):
        for i in range(7):
            for j in range(i+1):
                carta = self.baraja.pop()
                carta.volteada = (j == i)
                self.pilas_tablero[i].append(carta)
        self.mazo = self.baraja
        self.actualizar_tablero()

    def robar_carta(self):
        if self.mazo:
            carta = self.mazo.pop()
            carta.volteada = True
            self.descarte.append(carta)
            self.actualizar_tablero()

    def seleccionar_carta(self, pila_idx, carta_idx):
        if self.carta_seleccionada is None:
            self.carta_seleccionada = carta_idx
            self.origen = pila_idx
        else:
            self.mover_carta(self.origen, self.carta_seleccionada, pila_idx)
            self.carta_seleccionada = None
            self.origen = None

    def mover_carta(self, origen_idx, carta_idx, destino_idx):
        origen = self.pilas_tablero[origen_idx]
        destino = self.pilas_tablero[destino_idx]
        cartas_a_mover = origen[carta_idx:]

        if not destino:
            if cartas_a_mover[0].valor == 'K':
                destino.extend(cartas_a_mover)
                del origen[carta_idx:]
        else:
            dest_carta = destino[-1]
            if self.validar_movimiento(dest_carta, cartas_a_mover[0]):
                destino.extend(cartas_a_mover)
                del origen[carta_idx:]

        if origen and not origen[-1].volteada:
            origen[-1].volteada = True

        self.actualizar_tablero()

    def validar_movimiento(self, carta_dest, carta_mov):
        colores_opuestos = carta_dest.color != carta_mov.color
        valores_consecutivos = self.valores.index(carta_dest.valor) == self.valores.index(carta_mov.valor) + 1
        return colores_opuestos and valores_consecutivos

    def actualizar_tablero(self):
        self.canvas.delete("carta")

        x = 220
        y = 60
        if self.descarte:
            carta = self.descarte[-1]
            self.dibujar_carta(x, y, carta)

        for i, pila in enumerate(self.pilas_tablero):
            for j, carta in enumerate(pila):
                x = 100 + i*120
                y = 150 + j*30
                self.dibujar_carta(x, y, carta, i, j)

    def dibujar_carta(self, x, y, carta, pila_idx=None, carta_idx=None):
        color_texto = carta.color if carta.volteada else 'gray'
        texto = str(carta)
        rect = self.canvas.create_rectangle(x, y, x+60, y+90, fill="white", tags="carta")
        texto_id = self.canvas.create_text(x+30, y+45, text=texto, fill=color_texto, font=("Arial", 12, "bold"), tags="carta")

        if pila_idx is not None and carta.volteada:
            self.canvas.tag_bind(rect, "<Button-1>", lambda e, pi=pila_idx, ci=carta_idx: self.seleccionar_carta(pi, ci))
            self.canvas.tag_bind(texto_id, "<Button-1>", lambda e, pi=pila_idx, ci=carta_idx: self.seleccionar_carta(pi, ci))

if __name__ == "__main__":
    root = tk.Tk()
    app = Solitario(root)
    root.mainloop()

