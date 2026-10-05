import os
import tkinter as tk
from tkinter import ttk, messagebox

from servicios.restaurante_servicio import RestauranteServicio


class LoginView:
    """
    Ventana de inicio de sesión.
    """

    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login
        self.logo = None

        self.servicio = RestauranteServicio()

        self.root.title("Restaurante App - Inicio de sesión")
        self.root.geometry("420x460")
        self.root.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):

        # ---------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ---------------------------------------------

        contenedor = ttk.Frame(
            self.root,
            padding=30
        )

        contenedor.pack(
            fill="both",
            expand=True
        )

        # ---------------------------------------------
        # LOGOTIPO
        # ---------------------------------------------

        logo = self.cargar_logo()

        if logo is not None:
            ttk.Label(
                contenedor,
                image=logo
            ).pack(pady=(0, 5))

        # ---------------------------------------------
        # TÍTULO
        # ---------------------------------------------

        titulo = ttk.Label(
            contenedor,
            text="RESTAURANTE APP",
            font=("Arial", 20, "bold")
        )

        titulo.pack(pady=(10, 5))

        subtitulo = ttk.Label(
            contenedor,
            text="Sistema de gestión de productos"
        )

        subtitulo.pack(pady=(0, 20))

        # ---------------------------------------------
        # FORMULARIO
        # ---------------------------------------------

        formulario = ttk.LabelFrame(
            contenedor,
            text="Inicio de sesión",
            padding=20
        )

        formulario.pack(
            fill="x"
        )

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.usuario_entry = ttk.Entry(
            formulario,
            width=30
        )

        self.usuario_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            formulario,
            text="Contraseña:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.password_entry = ttk.Entry(
            formulario,
            width=30,
            show="*"
        )

        self.password_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        # ---------------------------------------------
        # BOTÓN
        # ---------------------------------------------

        boton = ttk.Button(
            formulario,
            text="Ingresar",
            command=self.iniciar_sesion
        )

        boton.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

        self.root.bind(
            "<Return>",
            lambda event: self.iniciar_sesion()
        )

        self.usuario_entry.focus()

    def cargar_logo(self):

        ruta_base = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        ruta_logo = os.path.join(
            ruta_base, "assets", "logo", "logo.png"
        )

        if not os.path.exists(ruta_logo):
            return None

        self.logo = tk.PhotoImage(
            file=ruta_logo
        ).subsample(2, 2)

        return self.logo

    def iniciar_sesion(self):

        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning(
                "Campos requeridos",
                "Ingrese usuario y contraseña."
            )
            return

        usuario_obj = self.servicio.validar_usuario(
            usuario,
            password
        )

        if usuario_obj:

            self.root.withdraw()

            self.on_login(usuario_obj)

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )
