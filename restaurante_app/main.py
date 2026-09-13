import tkinter as tk

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Restaurante Inti")
        self.ventana.geometry("800x500")
        self.ventana.minsize(650, 420)

        self.archivo_servicio = ArchivoServicio()
        self.restaurante_servicio = RestauranteServicio(
            self.archivo_servicio
        )

        self.vista_actual = None
        self.mostrar_login()

    def mostrar_login(self):
        self.limpiar_vista()
        self.ventana.geometry("450x420")

        self.vista_actual = LoginView(
            self.ventana,
            self.restaurante_servicio,
            self.mostrar_principal
        )

    def mostrar_principal(self, usuario: Usuario):
        self.limpiar_vista()
        self.ventana.geometry("900x550")

        self.vista_actual = MainView(
            self.ventana,
            self.restaurante_servicio,
            usuario,
            self.mostrar_login
        )

    def limpiar_vista(self):
        if self.vista_actual is not None:
            self.vista_actual.destruir()
            self.vista_actual = None

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    aplicacion = RestauranteApp()
    aplicacion.ejecutar()