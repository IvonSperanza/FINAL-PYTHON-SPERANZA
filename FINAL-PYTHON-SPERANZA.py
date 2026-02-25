from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


# ── Clases ────────────────────────────────────────────────────────────────────

class Transaccion:
    def __init__(self, tipo, monto, descripcion):
        self.tipo = tipo
        self.monto = monto
        self.descripcion = descripcion
        self.hora = datetime.now().strftime("%H:%M")

    def __str__(self):
        signo = "+" if self.monto >= 0 else ""
        return f"[{self.hora}] {self.tipo}: {signo}${self.monto:,.2f} - {self.descripcion}"


class Billetera:
    def __init__(self):
        self.saldo = 0.0
        self.historial = []

    def depositar(self, monto, descripcion="Deposito"):
        if monto <= 0:
            return False, "El monto debe ser mayor a cero."
        self.saldo += monto
        self.historial.append(Transaccion("Deposito", monto, descripcion))
        return True, f"Deposito exitoso. Nuevo saldo: ${self.saldo:,.2f}"

    def debitar(self, monto, tipo, descripcion):
        if monto <= 0:
            return False, "El monto debe ser mayor a cero."
        if monto > self.saldo:
            return False, f"Saldo insuficiente. Tenes: ${self.saldo:,.2f}"
        self.saldo -= monto
        self.historial.append(Transaccion(tipo, -monto, descripcion))
        return True, "OK"


class Usuario:
    def __init__(self, nombre, email, dni):
        self.nombre = nombre
        self.email = email
        self.dni = dni
        self.billetera = Billetera()

    def depositar(self, monto):
        return self.billetera.depositar(monto, "Deposito recibido")

    def transferir(self, monto, destinatario):
        ok, msg = self.billetera.debitar(monto, "Transferencia", f"Transferencia a {destinatario.nombre}")
        if ok:
            destinatario.billetera.depositar(monto, f"Transferencia de {self.nombre}")
            return True, f"Transferencia exitosa! Nuevo saldo: ${self.billetera.saldo:,.2f}"
        return False, msg

    def pagar_qr(self, monto, comercio):
        ok, msg = self.billetera.debitar(monto, "Pago QR", f"Pago en {comercio}")
        if ok:
            return True, f"Pago exitoso en {comercio}. Nuevo saldo: ${self.billetera.saldo:,.2f}"
        return False, msg

    def __str__(self):
        return f"{self.nombre} ({self.email})"


# ── Datos de ejemplo ──────────────────────────────────────────────────────────

usuarios = {
    "1": Usuario("Maria Garcia", "maria@email.com", "30111222"),
    "2": Usuario("Carlos Lopez", "carlos@email.com", "28333444"),
}
usuarios["1"].billetera.depositar(25000, "Pago por logo disenado")
usuarios["2"].billetera.depositar(5000, "Saldo inicial")

contador = [3]

# ── Colores y fuentes ─────────────────────────────────────────────────────────

BG     = "#0f0f1a"
PANEL  = "#1a1a2e"
CARD   = "#16213e"
MORADO = "#7c3aed"
CYAN   = "#06b6d4"
VERDE  = "#10b981"
ROJO   = "#ef4444"
AMBAR  = "#f59e0b"
TEXTO  = "#f1f5f9"
GRIS   = "#94a3b8"
BORDE  = "#2d2d4e"

F_TITULO = ("Segoe UI", 20, "bold")
F_NORMAL = ("Segoe UI", 10)
F_BOLD   = ("Segoe UI", 10, "bold")
F_TABLA  = ("Consolas", 10)


# ── Funciones helper ──────────────────────────────────────────────────────────

def lbl(parent, texto, color=GRIS, fuente=F_BOLD, fondo=None):
    if fondo is None:
        fondo = parent.cget("bg")
    return tk.Label(parent, text=texto, fg=color, bg=fondo, font=fuente)

def entry(parent, variable, ancho=30):
    style = ttk.Style()
    style.configure("E.TEntry", fieldbackground=PANEL, foreground=TEXTO,
                    insertcolor=TEXTO, bordercolor=BORDE, padding=6)
    return ttk.Entry(parent, textvariable=variable, width=ancho, style="E.TEntry", font=F_NORMAL)

def combo(parent, ancho=32):
    style = ttk.Style()
    style.configure("C.TCombobox", fieldbackground=PANEL, foreground=TEXTO,
                    selectbackground=MORADO, bordercolor=BORDE, padding=6)
    style.map("C.TCombobox", fieldbackground=[("readonly", PANEL)], foreground=[("readonly", TEXTO)])
    return ttk.Combobox(parent, width=ancho, state="readonly", style="C.TCombobox", font=F_NORMAL)

def boton(parent, texto, accion, color=MORADO, ancho=16):
    b = tk.Button(parent, text=texto, command=accion, bg=color, fg=TEXTO,
                  font=F_BOLD, relief="flat", padx=12, pady=7,
                  cursor="hand2", activebackground=color, activeforeground=TEXTO, width=ancho)
    b.bind("<Enter>", lambda e: b.config(bg=_oscurecer(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def _oscurecer(hex_color):
    r, g, b = int(hex_color[1:3],16), int(hex_color[3:5],16), int(hex_color[5:7],16)
    return f"#{int(r*.75):02x}{int(g*.75):02x}{int(b*.75):02x}"

def notificacion(ventana, mensaje, color=VERDE):
    pop = tk.Toplevel(ventana)
    pop.overrideredirect(True)
    pop.attributes("-topmost", True)
    pop.configure(bg=color)
    x = ventana.winfo_x() + ventana.winfo_width()//2 - 180
    y = ventana.winfo_y() + ventana.winfo_height() - 80
    pop.geometry(f"360x45+{x}+{y}")
    tk.Label(pop, text=mensaje, bg=color, fg="white", font=F_BOLD, wraplength=340).pack(expand=True)
    pop.after(2500, pop.destroy)

def lista_usuarios():
    return [f"{k}. {u.nombre}" for k, u in usuarios.items()]

def usuario_del_combo(valor):
    if not valor:
        return None
    clave = valor.split(".")[0].strip()
    return usuarios.get(clave), clave


# ── Ventana principal ─────────────────────────────────────────────────────────

ventana = tk.Tk()
ventana.title("MiWallet")
ventana.geometry("980x660")
ventana.configure(bg=BG)
ventana.resizable(True, True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=CARD, foreground=TEXTO,
                fieldbackground=CARD, font=F_TABLA, rowheight=26, borderwidth=0)
style.configure("Treeview.Heading", background=PANEL, foreground=GRIS, font=F_BOLD, relief="flat")
style.map("Treeview", background=[("selected", MORADO)])

# ── Sidebar ───────────────────────────────────────────────────────────────────

sidebar = tk.Frame(ventana, bg=PANEL, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="💳", font=("Segoe UI", 26), bg=PANEL, fg=MORADO).pack(pady=(20,2))
tk.Label(sidebar, text="MiWallet", font=("Segoe UI", 15, "bold"), bg=PANEL, fg=TEXTO).pack()
tk.Frame(sidebar, bg=BORDE, height=1).pack(fill="x", padx=14, pady=12)

nav_btns = {}
secciones = [
    ("inicio",     "🏠  Inicio"),
    ("depositar",  "💰  Depositar"),
    ("transferir", "↔️   Transferir"),
    ("pagar_qr",   "📲  Pagar con QR"),
    ("historial",  "📋  Historial"),
    ("usuarios",   "👥  Usuarios"),
]

def mostrar(seccion):
    for k, f in frames.items():
        f.pack_forget()
        nav_btns[k].config(bg=PANEL, fg=GRIS)
    frames[seccion].pack(fill="both", expand=True)
    nav_btns[seccion].config(bg=MORADO, fg=TEXTO)
    if seccion == "inicio":
        actualizar_inicio()
    if seccion == "historial":
        actualizar_historial()
    if seccion == "usuarios":
        actualizar_lista()

for key, label in secciones:
    b = tk.Button(sidebar, text=label, anchor="w", bg=PANEL, fg=GRIS, font=F_BOLD,
                  relief="flat", padx=18, pady=10, cursor="hand2",
                  activebackground=MORADO, activeforeground=TEXTO,
                  command=lambda k=key: mostrar(k))
    b.pack(fill="x")
    nav_btns[key] = b

# ── Area principal ────────────────────────────────────────────────────────────

area = tk.Frame(ventana, bg=BG)
area.pack(side="left", fill="both", expand=True)
frames = {}

# ── Frame Inicio ──────────────────────────────────────────────────────────────

frames["inicio"] = tk.Frame(area, bg=BG)
lbl(frames["inicio"], "Panel Principal", TEXTO, F_TITULO, BG).pack(anchor="w", padx=30, pady=(26,2))
lbl(frames["inicio"], "Resumen de billeteras", fondo=BG).pack(anchor="w", padx=30)
tarjetas_frame = tk.Frame(frames["inicio"], bg=BG)
tarjetas_frame.pack(fill="x", padx=24, pady=18)

def actualizar_inicio():
    for w in tarjetas_frame.winfo_children():
        w.destroy()
    for clave, u in usuarios.items():
        c = tk.Frame(tarjetas_frame, bg=CARD, padx=18, pady=14)
        c.pack(side="left", padx=8)
        tk.Label(c, text="👤", font=("Segoe UI", 20), bg=CARD, fg=CYAN).pack()
        lbl(c, u.nombre, TEXTO, ("Segoe UI", 11, "bold"), CARD).pack(pady=(4,0))
        lbl(c, u.email, fondo=CARD).pack()
        tk.Frame(c, bg=BORDE, height=1).pack(fill="x", pady=8)
        lbl(c, "Saldo", fondo=CARD).pack()
        lbl(c, f"${u.billetera.saldo:,.2f}", VERDE, ("Segoe UI", 17, "bold"), CARD).pack(pady=2)
        lbl(c, f"{len(u.billetera.historial)} transacciones", fondo=CARD).pack()

# ── Frame Depositar ───────────────────────────────────────────────────────────

frames["depositar"] = tk.Frame(area, bg=BG)
lbl(frames["depositar"], "Depositar Dinero", TEXTO, F_TITULO, BG).pack(anchor="w", padx=30, pady=(26,2))
lbl(frames["depositar"], "Acredita saldo en una billetera", fondo=BG).pack(anchor="w", padx=30)

card_dep = tk.Frame(frames["depositar"], bg=CARD, padx=28, pady=24)
card_dep.pack(padx=28, pady=18, fill="x")

lbl(card_dep, "Usuario", fondo=CARD).grid(row=0, column=0, sticky="w", pady=(0,3))
dep_combo = combo(card_dep)
dep_combo.grid(row=1, column=0, sticky="w", pady=(0,14))

lbl(card_dep, "Monto ($)", fondo=CARD).grid(row=2, column=0, sticky="w", pady=(0,3))
dep_monto = tk.StringVar()
entry(card_dep, dep_monto).grid(row=3, column=0, sticky="w", pady=(0,18))

def hacer_deposito():
    dep_combo["values"] = lista_usuarios()
    u, _ = usuario_del_combo(dep_combo.get())
    if not u:
        messagebox.showerror("Error", "Selecciona un usuario.")
        return
    try:
        monto = float(dep_monto.get())
    except:
        messagebox.showerror("Error", "Ingresa un monto valido.")
        return
    ok, msg = u.depositar(monto)
    if ok:
        notificacion(ventana, msg)
        dep_monto.set("")
    else:
        messagebox.showerror("Error", msg)

boton(card_dep, "💰  Confirmar Deposito", hacer_deposito, VERDE).grid(row=4, column=0, sticky="w")

# ── Frame Transferir ──────────────────────────────────────────────────────────

frames["transferir"] = tk.Frame(area, bg=BG)
lbl(frames["transferir"], "Transferir Dinero", TEXTO, F_TITULO, BG).pack(anchor="w", padx=30, pady=(26,2))
lbl(frames["transferir"], "Envia dinero a otro usuario", fondo=BG).pack(anchor="w", padx=30)

card_tra = tk.Frame(frames["transferir"], bg=CARD, padx=28, pady=24)
card_tra.pack(padx=28, pady=18, fill="x")

lbl(card_tra, "Quien envia", fondo=CARD).grid(row=0, column=0, sticky="w", pady=(0,3))
tra_origen = combo(card_tra)
tra_origen.grid(row=1, column=0, sticky="w", pady=(0,14), padx=(0,20))

lbl(card_tra, "Quien recibe", fondo=CARD).grid(row=0, column=1, sticky="w", pady=(0,3))
tra_destino = combo(card_tra)
tra_destino.grid(row=1, column=1, sticky="w", pady=(0,14))

lbl(card_tra, "Monto ($)", fondo=CARD).grid(row=2, column=0, sticky="w", pady=(0,3))
tra_monto = tk.StringVar()
entry(card_tra, tra_monto).grid(row=3, column=0, sticky="w", pady=(0,18))

def hacer_transferencia():
    lista = lista_usuarios()
    tra_origen["values"] = lista
    tra_destino["values"] = lista
    origen, _ = usuario_del_combo(tra_origen.get())
    destino, _ = usuario_del_combo(tra_destino.get())
    if not origen or not destino:
        messagebox.showerror("Error", "Selecciona ambos usuarios.")
        return
    if origen is destino:
        messagebox.showerror("Error", "No podes transferirte a vos mismo.")
        return
    try:
        monto = float(tra_monto.get())
    except:
        messagebox.showerror("Error", "Ingresa un monto valido.")
        return
    ok, msg = origen.transferir(monto, destino)
    if ok:
        notificacion(ventana, msg)
        tra_monto.set("")
    else:
        messagebox.showerror("Error", msg)

boton(card_tra, "↔️  Transferir", hacer_transferencia, CYAN).grid(row=4, column=0, sticky="w")

# ── Frame Pagar QR ────────────────────────────────────────────────────────────

frames["pagar_qr"] = tk.Frame(area, bg=BG)
lbl(frames["pagar_qr"], "Pagar con QR", TEXTO, F_TITULO, BG).pack(anchor="w", padx=30, pady=(26,2))
lbl(frames["pagar_qr"], "Realiza un pago en un comercio", fondo=BG).pack(anchor="w", padx=30)

card_qr = tk.Frame(frames["pagar_qr"], bg=CARD, padx=28, pady=24)
card_qr.pack(padx=28, pady=18, fill="x")

lbl(card_qr, "Usuario que paga", fondo=CARD).grid(row=0, column=0, sticky="w", pady=(0,3))
qr_combo = combo(card_qr)
qr_combo.grid(row=1, column=0, sticky="w", pady=(0,14))

lbl(card_qr, "Nombre del comercio", fondo=CARD).grid(row=2, column=0, sticky="w", pady=(0,3))
qr_comercio = tk.StringVar()
entry(card_qr, qr_comercio).grid(row=3, column=0, sticky="w", pady=(0,14))

lbl(card_qr, "Monto ($)", fondo=CARD).grid(row=4, column=0, sticky="w", pady=(0,3))
qr_monto = tk.StringVar()
entry(card_qr, qr_monto).grid(row=5, column=0, sticky="w", pady=(0,18))

def hacer_pago_qr():
    qr_combo["values"] = lista_usuarios()
    u, _ = usuario_del_combo(qr_combo.get())
    if not u:
        messagebox.showerror("Error", "Selecciona un usuario.")
        return
    comercio = qr_comercio.get().strip()
    if not comercio:
        messagebox.showerror("Error", "Ingresa el nombre del comercio.")
        return
    try:
        monto = float(qr_monto.get())
    except:
        messagebox.showerror("Error", "Ingresa un monto valido.")
        return
    ok, msg = u.pagar_qr(monto, comercio)
    if ok:
        notificacion(ventana, msg)
        qr_monto.set("")
        qr_comercio.set("")
    else:
        messagebox.showerror("Error", msg)

boton(card_qr, "📲  Confirmar Pago", hacer_pago_qr, AMBAR).grid(row=6, column=0, sticky="w")

# ── Frame Historial ───────────────────────────────────────────────────────────

frames["historial"] = tk.Frame(area, bg=BG)
lbl(frames["historial"], "Historial", TEXTO, F_TITULO, BG).pack(anchor="w", padx=30, pady=(26,4))

top_hist = tk.Frame(frames["historial"], bg=BG)
top_hist.pack(fill="x", padx=28, pady=(0,10))
lbl(top_hist, "Usuario:", fondo=BG).pack(side="left")
hist_combo = combo(top_hist, 28)
hist_combo.pack(side="left", padx=8)
boton(top_hist, "Buscar", lambda: actualizar_historial(), MORADO, 10).pack(side="left")

tabla_frame = tk.Frame(frames["historial"], bg=BG)
tabla_frame.pack(fill="both", expand=True, padx=28)

tabla = ttk.Treeview(tabla_frame, columns=("hora","tipo","monto","descripcion"), show="headings", height=15)
tabla.heading("hora", text="Hora")
tabla.heading("tipo", text="Tipo")
tabla.heading("monto", text="Monto")
tabla.heading("descripcion", text="Descripcion")
tabla.column("hora", width=65, anchor="center")
tabla.column("tipo", width=120, anchor="center")
tabla.column("monto", width=110, anchor="e")
tabla.column("descripcion", width=320)

scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)
tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

saldo_lbl = tk.Label(frames["historial"], text="", font=("Segoe UI",12,"bold"), bg=BG, fg=VERDE)
saldo_lbl.pack(anchor="e", padx=28, pady=8)

def actualizar_historial():
    hist_combo["values"] = lista_usuarios()
    u, _ = usuario_del_combo(hist_combo.get())
    for row in tabla.get_children():
        tabla.delete(row)
    if not u:
        return
    for t in u.billetera.historial:
        signo = "+" if t.monto >= 0 else ""
        tag = "pos" if t.monto >= 0 else "neg"
        tabla.insert("", "end", values=(t.hora, t.tipo, f"{signo}${t.monto:,.2f}", t.descripcion), tags=(tag,))
    tabla.tag_configure("pos", foreground=VERDE)
    tabla.tag_configure("neg", foreground=ROJO)
    saldo_lbl.config(text=f"Saldo actual: ${u.billetera.saldo:,.2f}")

# ── Frame Usuarios ────────────────────────────────────────────────────────────

frames["usuarios"] = tk.Frame(area, bg=BG)
lbl(frames["usuarios"], "Gestion de Usuarios", TEXTO, F_TITULO, BG).pack(anchor="w", padx=30, pady=(26,2))
lbl(frames["usuarios"], "Crear, modificar y eliminar usuarios", fondo=BG).pack(anchor="w", padx=30)

usr_content = tk.Frame(frames["usuarios"], bg=BG)
usr_content.pack(fill="both", expand=True, padx=24, pady=14)

# Lista
lista_card = tk.Frame(usr_content, bg=CARD, padx=14, pady=14)
lista_card.pack(side="left", fill="both", expand=True, padx=(0,10))
lbl(lista_card, "Usuarios registrados", TEXTO, fondo=CARD).pack(anchor="w")
tk.Frame(lista_card, bg=BORDE, height=1).pack(fill="x", pady=6)

listbox = tk.Listbox(lista_card, bg=PANEL, fg=TEXTO, font=F_NORMAL,
                     selectbackground=MORADO, relief="flat", bd=0, highlightthickness=0)
listbox.pack(fill="both", expand=True)

boton(lista_card, "🗑  Eliminar seleccionado", lambda: eliminar_usuario(), ROJO, 22).pack(pady=(10,0), anchor="w")

# Formulario
form_card = tk.Frame(usr_content, bg=CARD, padx=20, pady=20)
form_card.pack(side="left", fill="y")
lbl(form_card, "Datos del usuario", TEXTO, fondo=CARD).pack(anchor="w")
tk.Frame(form_card, bg=BORDE, height=1).pack(fill="x", pady=6)

usr_nombre = tk.StringVar()
usr_email  = tk.StringVar()
usr_dni    = tk.StringVar()
usr_clave_sel = tk.StringVar()

lbl(form_card, "Nombre", fondo=CARD).pack(anchor="w", pady=(4,2))
entry(form_card, usr_nombre, 26).pack(anchor="w")
lbl(form_card, "Email", fondo=CARD).pack(anchor="w", pady=(10,2))
entry(form_card, usr_email, 26).pack(anchor="w")
lbl(form_card, "DNI", fondo=CARD).pack(anchor="w", pady=(10,2))
entry(form_card, usr_dni, 26).pack(anchor="w")

tk.Frame(form_card, bg=CARD, height=14).pack()

btn_row = tk.Frame(form_card, bg=CARD)
btn_row.pack(fill="x")
boton(btn_row, "➕ Crear", lambda: crear_usuario(), VERDE, 10).pack(side="left", padx=(0,6))
boton(btn_row, "✏️ Modificar", lambda: modificar_usuario(), MORADO, 10).pack(side="left")

def actualizar_lista():
    listbox.delete(0, "end")
    for clave, u in usuarios.items():
        listbox.insert("end", f"  {clave}. {u.nombre}  |  {u.email}")

def on_seleccionar(event):
    sel = listbox.curselection()
    if not sel:
        return
    texto = listbox.get(sel[0])
    clave = texto.strip().split(".")[0]
    usr_clave_sel.set(clave)
    u = usuarios.get(clave)
    if u:
        usr_nombre.set(u.nombre)
        usr_email.set(u.email)
        usr_dni.set(u.dni)

listbox.bind("<<ListboxSelect>>", on_seleccionar)

def crear_usuario():
    nombre = usr_nombre.get().strip()
    email  = usr_email.get().strip()
    dni    = usr_dni.get().strip()
    if not nombre or not email or not dni:
        messagebox.showerror("Error", "Completa todos los campos.")
        return
    clave = str(contador[0])
    contador[0] += 1
    usuarios[clave] = Usuario(nombre, email, dni)
    actualizar_lista()
    usr_nombre.set("")
    usr_email.set("")
    usr_dni.set("")
    notificacion(ventana, f"Usuario '{nombre}' creado!", VERDE)

def modificar_usuario():
    clave = usr_clave_sel.get()
    if not clave or clave not in usuarios:
        messagebox.showerror("Error", "Selecciona un usuario de la lista.")
        return
    nombre = usr_nombre.get().strip()
    email  = usr_email.get().strip()
    dni    = usr_dni.get().strip()
    if not nombre or not email or not dni:
        messagebox.showerror("Error", "Completa todos los campos.")
        return
    usuarios[clave].nombre = nombre
    usuarios[clave].email  = email
    usuarios[clave].dni    = dni
    actualizar_lista()
    notificacion(ventana, "Usuario modificado!", CYAN)

def eliminar_usuario():
    clave = usr_clave_sel.get()
    if not clave or clave not in usuarios:
        messagebox.showerror("Error", "Selecciona un usuario de la lista.")
        return
    nombre = usuarios[clave].nombre
    if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre}?"):
        del usuarios[clave]
        usr_clave_sel.set("")
        usr_nombre.set("")
        usr_email.set("")
        usr_dni.set("")
        actualizar_lista()
        notificacion(ventana, f"Usuario '{nombre}' eliminado.", ROJO)


# ── Arrancar en inicio ────────────────────────────────────────────────────────

mostrar("inicio")
ventana.mainloop()