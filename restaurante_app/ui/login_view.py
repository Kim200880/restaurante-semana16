import tkinter as tk
from tkinter import messagebox

from servicios.restaurante_servicio import RestauranteServicio


class LoginView:
    def __init__(
        self,
        ventana: tk.Tk,
        restaurante_servicio: RestauranteServicio,
        mostrar_principal
    ):
        self.ventana = ventana
        self.restaurante_servicio = restaurante_servicio
        self.mostrar_principal = mostrar_principal

        self.frame = tk.Frame(
            self.ventana,
            padx=40,
            pady=30
        )
        self.frame.pack(expand=True)

        titulo = tk.Label(
            self.frame,
            text="RESTAURANTE INTI",
            font=("Arial", 20, "bold"),
            fg="#9C3D10"
        )
        titulo.pack(pady=(0, 25))

        subtitulo = tk.Label(
            self.frame,
            text="Inicio de sesión",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=(0, 20))

        tk.Label(
            self.frame,
            text="Identificación:"
        ).pack(anchor="w")

        self.entrada_identificacion = tk.Entry(
            self.frame,
            width=32
        )
        self.entrada_identificacion.pack(pady=(5, 15))

        tk.Label(
            self.frame,
            text="Contraseña:"
        ).pack(anchor="w")

        self.entrada_contrasena = tk.Entry(
            self.frame,
            width=32,
            show="*"
        )
        self.entrada_contrasena.pack(pady=(5, 20))

        boton_ingresar = tk.Button(
            self.frame,
            text="Ingresar",
            width=20,
            bg="#9C3D10",
            fg="white",
            command=self.validar_ingreso
        )
        boton_ingresar.pack()

        self.ventana.bind(
            "<Return>",
            lambda evento: self.validar_ingreso()
        )

        self.entrada_identificacion.focus()

    def validar_ingreso(self):
        identificacion = self.entrada_identificacion.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not identificacion or not contrasena:
            messagebox.showwarning(
                "Campos incompletos",
                "Ingrese la identificación y la contraseña."
            )
            return

        usuario = self.restaurante_servicio.validar_acceso(
            identificacion,
            contrasena
        )

        if usuario is None:
            messagebox.showerror(
                "Acceso incorrecto",
                "La identificación o la contraseña son incorrectas."
            )
            return

        messagebox.showinfo(
            "Acceso correcto",
            f"Bienvenida, {usuario.nombre}."
        )

        self.mostrar_principal(usuario)

    def destruir(self):
        self.ventana.unbind("<Return>")
        self.frame.destroy()