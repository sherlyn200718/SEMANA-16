import os
import tkinter as tk

from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    """
    Controlador principal de la aplicación.
    """

    def __init__(self):

        self.root = tk.Tk()

        self.icono_app = None
        self.configurar_icono(self.root)

        self.mostrar_login()

        self.root.mainloop()

    def configurar_icono(self, ventana):

        ruta_icono = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets", "logo", "icono.png"
        )

        if not os.path.exists(ruta_icono):
            return

        try:
            self.icono_app = tk.PhotoImage(file=ruta_icono)
            ventana.iconphoto(True, self.icono_app)
        except tk.TclError:
            pass

    def mostrar_login(self):

        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.deiconify()

        LoginView(
            self.root,
            self.iniciar_aplicacion
        )

    def iniciar_aplicacion(self, usuario):

        self.abrir_ventana_principal(
            usuario
        )

    def abrir_ventana_principal(self, usuario):

        # Crear nueva ventana principal
        ventana_principal = tk.Toplevel(
            self.root
        )

        self.configurar_icono(ventana_principal)

        # Ocultar ventana raíz
        self.root.withdraw()

        MainView(
            ventana_principal,
            usuario,
            self.regresar_login
        )

    def regresar_login(self):

        self.mostrar_login()


if __name__ == "__main__":
    RestauranteApp()
