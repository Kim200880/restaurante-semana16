import tkinter as tk
from tkinter import messagebox

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView:
    def __init__(
        self,
        ventana: tk.Tk,
        restaurante_servicio: RestauranteServicio,
        usuario: Usuario,
        cerrar_sesion
    ):
        self.ventana = ventana
        self.restaurante_servicio = restaurante_servicio
        self.usuario = usuario
        self.cerrar_sesion = cerrar_sesion

        self.frame = tk.Frame(
            self.ventana,
            padx=25,
            pady=20
        )
        self.frame.pack(fill="both", expand=True)

        titulo = tk.Label(
            self.frame,
            text="RESTAURANTE INTI",
            font=("Arial", 20, "bold"),
            fg="#9C3D10"
        )
        titulo.pack(pady=(0, 5))

        bienvenida = tk.Label(
            self.frame,
            text=f"Bienvenida, {self.usuario.nombre}",
            font=("Arial", 12)
        )
        bienvenida.pack(pady=(0, 20))

        menu = tk.Frame(self.frame)
        menu.pack(fill="x", pady=(0, 15))

        tk.Button(
            menu,
            text="Productos",
            width=15,
            command=self.mostrar_productos
        ).pack(side="left", padx=5)

        tk.Button(
            menu,
            text="Usuarios",
            width=15,
            command=self.mostrar_usuarios
        ).pack(side="left", padx=5)

        tk.Button(
            menu,
            text="Ventas",
            width=15,
            command=self.mostrar_ventas_pendientes
        ).pack(side="left", padx=5)

        tk.Button(
            menu,
            text="Cerrar sesión",
            width=15,
            bg="#9C3D10",
            fg="white",
            command=self.cerrar_sesion
        ).pack(side="right", padx=5)

        self.titulo_contenido = tk.Label(
            self.frame,
            text="Panel principal",
            font=("Arial", 14, "bold")
        )
        self.titulo_contenido.pack(pady=5)

        self.area_informacion = tk.Text(
            self.frame,
            width=85,
            height=18,
            state="disabled"
        )
        self.area_informacion.pack(fill="both", expand=True)

        self.mostrar_resumen()

    def escribir_informacion(self, titulo: str, contenido: str):
        self.titulo_contenido.config(text=titulo)
        self.area_informacion.config(state="normal")
        self.area_informacion.delete("1.0", tk.END)
        self.area_informacion.insert(tk.END, contenido)
        self.area_informacion.config(state="disabled")

    def mostrar_resumen(self):
        cantidad_productos = (
            self.restaurante_servicio.cantidad_productos()
        )
        cantidad_usuarios = (
            self.restaurante_servicio.cantidad_usuarios()
        )

        contenido = (
            f"Productos registrados: {cantidad_productos}\n"
            f"Usuarios registrados: {cantidad_usuarios}\n"
            "Ventas: funcionalidad pendiente para próximas semanas."
        )

        self.escribir_informacion(
            "Resumen del restaurante",
            contenido
        )

    def mostrar_productos(self):
        productos = self.restaurante_servicio.listar_productos()

        if not productos:
            contenido = "No existen productos registrados."
        else:
            contenido = "\n\n".join(
                str(producto) for producto in productos
            )

        self.escribir_informacion(
            "Productos registrados",
            contenido
        )

    def mostrar_usuarios(self):
        usuarios = self.restaurante_servicio.listar_usuarios()

        if not usuarios:
            contenido = "No existen usuarios registrados."
        else:
            contenido = "\n\n".join(
                str(usuario) for usuario in usuarios
            )

        self.escribir_informacion(
            "Usuarios registrados",
            contenido
        )

    def mostrar_ventas_pendientes(self):
        messagebox.showinfo(
            "Ventas",
            "Esta funcionalidad se implementará próximamente."
        )

    def destruir(self):
        self.frame.destroy()