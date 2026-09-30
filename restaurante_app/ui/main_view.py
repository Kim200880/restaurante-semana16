import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

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
        self.es_administrador = usuario.rol == "Administrador"
        self.usuario_seleccionado = None

        self.ventana.geometry("1050x650")
        self.ventana.minsize(950, 600)

        self.carpeta_assets = (
            Path(__file__).resolve().parent.parent / "assets"
        )
        self.logo = None
        self.icono_venta = None

        estilo = ttk.Style(self.ventana)
        estilo.configure("Treeview", rowheight=26)
        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        self.frame = tk.Frame(self.ventana, bg="#F7F3EE")
        self.frame.pack(fill="both", expand=True)

        self.crear_encabezado()
        self.crear_pestanas()
        self.actualizar_tabla_productos()
        self.actualizar_usuarios()

    def cargar_imagen(self, nombre, tamano_maximo):
        ruta = self.carpeta_assets / nombre

        if not ruta.is_file():
            return None

        try:
            imagen = tk.PhotoImage(file=str(ruta))
            factor = max(
                1,
                (imagen.width() + tamano_maximo - 1) // tamano_maximo,
                (imagen.height() + tamano_maximo - 1) // tamano_maximo
            )
            return imagen.subsample(factor, factor)
        except tk.TclError:
            return None

    def crear_encabezado(self):
        encabezado = tk.Frame(
            self.frame,
            bg="#9C3D10",
            padx=20,
            pady=12
        )
        encabezado.pack(fill="x")

        self.logo = self.cargar_imagen("logo.png", 70)

        if self.logo is not None:
            tk.Label(
                encabezado,
                image=self.logo,
                bg="#9C3D10"
            ).pack(side="left", padx=(0, 15))

        bloque_titulo = tk.Frame(encabezado, bg="#9C3D10")
        bloque_titulo.pack(side="left")

        tk.Label(
            bloque_titulo,
            text="RESTAURANTE INTI",
            font=("Arial", 20, "bold"),
            bg="#9C3D10",
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            bloque_titulo,
            text=(
                f"Bienvenida, {self.usuario.nombre} "
                f"| Rol: {self.usuario.rol}"
            ),
            font=("Arial", 11),
            bg="#9C3D10",
            fg="white"
        ).pack(anchor="w")

        tk.Button(
            encabezado,
            text="Cerrar sesión",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#9C3D10",
            padx=12,
            command=self.cerrar_sesion
        ).pack(side="right", padx=5)

    def crear_pestanas(self):
        contenedor = tk.Frame(
            self.frame,
            bg="#F7F3EE",
            padx=20,
            pady=15
        )
        contenedor.pack(fill="both", expand=True)

        self.pestanas = ttk.Notebook(contenedor)
        self.pestanas.pack(fill="both", expand=True)

        self.pagina_resumen = tk.Frame(self.pestanas, bg="white")
        self.pagina_productos = tk.Frame(self.pestanas, bg="white")
        self.pagina_usuarios = tk.Frame(self.pestanas, bg="white")
        self.pagina_ventas = tk.Frame(self.pestanas, bg="white")

        self.pestanas.add(self.pagina_resumen, text="  Inicio  ")
        self.pestanas.add(self.pagina_productos, text="  Productos  ")

        if self.es_administrador:
            self.pestanas.add(
                self.pagina_usuarios,
                text="  Usuarios  "
            )

        self.pestanas.add(self.pagina_ventas, text="  Ventas  ")

        self.crear_resumen()
        self.crear_seccion_productos()

        if self.es_administrador:
            self.crear_seccion_usuarios()

        self.crear_seccion_ventas()

    def crear_resumen(self):
        tk.Label(
            self.pagina_resumen,
            text="Panel principal",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#9C3D10"
        ).pack(pady=(35, 20))

        tarjetas = tk.Frame(self.pagina_resumen, bg="white")
        tarjetas.pack()

        tarjeta_productos = tk.Frame(
            tarjetas,
            bg="#F4E1D2",
            width=250,
            height=130,
            bd=1,
            relief="solid"
        )
        tarjeta_productos.pack(side="left", padx=15)
        tarjeta_productos.pack_propagate(False)

        tk.Label(
            tarjeta_productos,
            text="PRODUCTOS",
            font=("Arial", 13, "bold"),
            bg="#F4E1D2",
            fg="#9C3D10"
        ).pack(pady=(22, 8))

        self.etiqueta_productos = tk.Label(
            tarjeta_productos,
            text="0",
            font=("Arial", 26, "bold"),
            bg="#F4E1D2",
            fg="#333333"
        )
        self.etiqueta_productos.pack()

        tarjeta_usuarios = tk.Frame(
            tarjetas,
            bg="#E5F1E3",
            width=250,
            height=130,
            bd=1,
            relief="solid"
        )
        tarjeta_usuarios.pack(side="left", padx=15)
        tarjeta_usuarios.pack_propagate(False)

        tk.Label(
            tarjeta_usuarios,
            text="USUARIOS",
            font=("Arial", 13, "bold"),
            bg="#E5F1E3",
            fg="#356A32"
        ).pack(pady=(22, 8))

        self.etiqueta_usuarios = tk.Label(
            tarjeta_usuarios,
            text="0",
            font=("Arial", 26, "bold"),
            bg="#E5F1E3",
            fg="#333333"
        )
        self.etiqueta_usuarios.pack()

        tk.Label(
            self.pagina_resumen,
            text="Utilice las pestañas para acceder a las funciones del sistema.",
            font=("Arial", 11),
            bg="white",
            fg="#555555"
        ).pack(pady=35)

    def crear_campo(self, contenedor, texto, variable, fila):
        tk.Label(
            contenedor,
            text=texto,
            font=("Arial", 10),
            bg="white"
        ).grid(row=fila, column=0, sticky="w", pady=7)

        entrada = tk.Entry(
            contenedor,
            textvariable=variable,
            width=24
        )
        entrada.grid(
            row=fila,
            column=1,
            padx=(10, 0),
            pady=7
        )
        return entrada

    def crear_seccion_productos(self):
        self.pagina_productos.columnconfigure(1, weight=1)
        self.pagina_productos.rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            self.pagina_productos,
            text="Datos del producto",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#9C3D10",
            padx=15,
            pady=12
        )
        formulario.grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="ns"
        )

        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        self.crear_campo(formulario, "Código:", self.codigo_var, 0)
        self.crear_campo(formulario, "Nombre:", self.nombre_var, 1)
        self.crear_campo(
            formulario, "Categoría:", self.categoria_var, 2
        )
        self.crear_campo(formulario, "Precio:", self.precio_var, 3)
        self.crear_campo(formulario, "Stock:", self.stock_var, 4)

        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=5, column=0, columnspan=2, pady=(15, 0))

        acciones = (
            ("Registrar", "#356A32", self.registrar_producto),
            ("Consultar", "#2F6690", self.consultar_producto),
            ("Actualizar", "#D7891C", self.actualizar_producto),
            ("Eliminar", "#B02A37", self.eliminar_producto)
        )

        for indice, (texto, color, callback) in enumerate(acciones):
            tk.Button(
                botones,
                text=texto,
                width=12,
                bg=color,
                fg="white",
                command=callback
            ).grid(
                row=indice // 2,
                column=indice % 2,
                padx=3,
                pady=3
            )

        tk.Button(
            botones,
            text="Limpiar",
            width=27,
            command=self.limpiar_formulario
        ).grid(row=2, column=0, columnspan=2, padx=3, pady=3)

        contenedor_tabla = tk.LabelFrame(
            self.pagina_productos,
            text="Productos registrados",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#9C3D10",
            padx=10,
            pady=10
        )
        contenedor_tabla.grid(
            row=0,
            column=1,
            padx=(0, 15),
            pady=15,
            sticky="nsew"
        )
        contenedor_tabla.rowconfigure(0, weight=1)
        contenedor_tabla.columnconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            contenedor_tabla,
            columns=columnas,
            show="headings"
        )

        for clave, titulo, ancho in (
            ("codigo", "Código", 85),
            ("nombre", "Nombre", 140),
            ("categoria", "Categoría", 110),
            ("precio", "Precio", 80),
            ("stock", "Stock", 65)
        ):
            self.tabla_productos.heading(clave, text=titulo)
            self.tabla_productos.column(clave, width=ancho)

        barra = ttk.Scrollbar(
            contenedor_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=barra.set)
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

    def crear_seccion_usuarios(self):
        self.pagina_usuarios.columnconfigure(1, weight=1)
        self.pagina_usuarios.rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            self.pagina_usuarios,
            text="Gestión de usuarios",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#9C3D10",
            padx=12,
            pady=10
        )
        formulario.grid(
            row=0, column=0, padx=15, pady=15, sticky="ns"
        )

        self.identificacion_usuario_var = tk.StringVar()
        self.nombre_usuario_var = tk.StringVar()
        self.correo_usuario_var = tk.StringVar()
        self.contrasena_usuario_var = tk.StringVar()
        self.rol_usuario_var = tk.StringVar(value="Cliente")
        self.mensaje_rol_var = tk.StringVar(
            value="Cliente: usuario que compra en el restaurante."
        )

        self.entrada_identificacion = self.crear_campo(
            formulario,
            "Identificación:",
            self.identificacion_usuario_var,
            0
        )
        entrada_nombre = self.crear_campo(
            formulario,
            "Nombre:",
            self.nombre_usuario_var,
            1
        )
        entrada_correo = self.crear_campo(
            formulario,
            "Correo:",
            self.correo_usuario_var,
            2
        )
        entrada_contrasena = self.crear_campo(
            formulario,
            "Contraseña:",
            self.contrasena_usuario_var,
            3
        )
        entrada_contrasena.config(show="*")

        tk.Label(
            formulario,
            text="Rol:",
            bg="white",
            font=("Arial", 10)
        ).grid(row=4, column=0, sticky="w", pady=7)

        self.selector_rol = ttk.Combobox(
            formulario,
            textvariable=self.rol_usuario_var,
            values=("Empleado", "Cliente"),
            state="readonly",
            width=21
        )
        self.selector_rol.grid(
            row=4, column=1, padx=(10, 0), pady=7
        )

        # Evento virtual: responder a un cambio de rol.
        self.selector_rol.bind(
            "<<ComboboxSelected>>",
            self.al_cambiar_rol
        )

        tk.Label(
            formulario,
            textvariable=self.mensaje_rol_var,
            bg="white",
            fg="#555555",
            wraplength=285,
            justify="left"
        ).grid(
            row=5, column=0, columnspan=2, sticky="w", pady=8
        )

        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=6, column=0, columnspan=2, pady=8)

        acciones = (
            ("Registrar", "#356A32", self.registrar_usuario),
            ("Actualizar", "#D7891C", self.actualizar_usuario),
            ("Eliminar", "#B02A37", self.eliminar_usuario),
            ("Limpiar", "#2F6690", self.limpiar_formulario_usuarios)
        )

        self.botones_usuarios = {}

        for indice, (texto, color, callback) in enumerate(acciones):
            boton = tk.Button(
                botones,
                text=texto,
                width=12,
                bg=color,
                fg="white",
                command=callback
            )
            boton.grid(
                row=indice // 2,
                column=indice % 2,
                padx=3,
                pady=3
            )
            self.botones_usuarios[texto] = boton

        tk.Label(
            formulario,
            text=(
                "Enter: registrar | Escape: limpiar\n"
                "Al actualizar, deje la contraseña vacía\n"
                "para conservar la actual."
            ),
            bg="white",
            fg="#555555",
            justify="left",
            font=("Arial", 9)
        ).grid(
            row=7, column=0, columnspan=2, sticky="w", pady=8
        )

        contenedor_tabla = tk.LabelFrame(
            self.pagina_usuarios,
            text="Seleccione un usuario para consultar sus datos",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#9C3D10",
            padx=10,
            pady=10
        )
        contenedor_tabla.grid(
            row=0,
            column=1,
            padx=(0, 15),
            pady=15,
            sticky="nsew"
        )
        contenedor_tabla.rowconfigure(0, weight=1)
        contenedor_tabla.columnconfigure(0, weight=1)

        self.tabla_usuarios = ttk.Treeview(
            contenedor_tabla,
            columns=("identificacion", "nombre", "correo", "rol"),
            show="headings",
            selectmode="browse"
        )

        for clave, titulo, ancho in (
            ("identificacion", "Identificación", 110),
            ("nombre", "Nombre", 140),
            ("correo", "Correo / usuario", 180),
            ("rol", "Rol", 100)
        ):
            self.tabla_usuarios.heading(clave, text=titulo)
            self.tabla_usuarios.column(
                clave, width=ancho, minwidth=70
            )

        self.tabla_usuarios.grid(row=0, column=0, sticky="nsew")

        barra = ttk.Scrollbar(
            contenedor_tabla,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )
        barra.grid(row=0, column=1, sticky="ns")
        self.tabla_usuarios.configure(yscrollcommand=barra.set)

        # La selección consulta el objeto mediante el servicio.
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.al_seleccionar_usuario
        )

        # Atajos limitados a los campos del formulario de usuarios.
        for campo in (
            self.entrada_identificacion,
            entrada_nombre,
            entrada_correo,
            entrada_contrasena,
            self.selector_rol
        ):
            campo.bind("<Return>", self.al_presionar_enter)
            campo.bind("<Escape>", self.al_presionar_escape)

        self.tabla_usuarios.bind(
            "<Escape>", self.al_presionar_escape
        )
        for boton in self.botones_usuarios.values():
            boton.bind("<Escape>", self.al_presionar_escape)

        self.limpiar_formulario_usuarios(enfocar=False)

    def actualizar_usuarios(self):
        if not self.es_administrador:
            return

        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

        for usuario in self.restaurante_servicio.listar_usuarios():
            # La contraseña no se almacena en el Treeview.
            self.tabla_usuarios.insert(
                "",
                tk.END,
                iid=usuario.identificacion,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.correo,
                    usuario.rol
                )
            )

        self.actualizar_resumen()
        self.actualizar_ventas()

    def al_seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        usuario = self.restaurante_servicio.buscar_usuario(
            seleccion[0]
        )
        if usuario is None:
            return

        self.usuario_seleccionado = usuario.identificacion
        self.entrada_identificacion.config(state="normal")
        self.identificacion_usuario_var.set(usuario.identificacion)
        self.entrada_identificacion.config(state="readonly")

        self.nombre_usuario_var.set(usuario.nombre)
        self.correo_usuario_var.set(usuario.correo)
        self.contrasena_usuario_var.set("")
        self.rol_usuario_var.set(usuario.rol)

        if usuario.rol == "Administrador":
            self.selector_rol.config(state="disabled")
            self.mensaje_rol_var.set(
                "La cuenta Administrador solo se puede consultar."
            )
            self.botones_usuarios["Actualizar"].config(
                state="disabled"
            )
            self.botones_usuarios["Eliminar"].config(
                state="disabled"
            )
        else:
            self.selector_rol.config(state="readonly")
            self.al_cambiar_rol(None)
            self.botones_usuarios["Actualizar"].config(
                state="normal"
            )
            self.botones_usuarios["Eliminar"].config(
                state="normal"
            )

        self.botones_usuarios["Registrar"].config(state="disabled")

    def al_cambiar_rol(self, event):
        mensajes = {
            "Empleado": "Empleado: integrante del personal del restaurante.",
            "Cliente": "Cliente: usuario que compra en el restaurante."
        }
        self.mensaje_rol_var.set(
            mensajes.get(self.rol_usuario_var.get(), "")
        )

    def al_presionar_enter(self, event):
        self.registrar_usuario()
        return "break"

    def al_presionar_escape(self, event):
        self.limpiar_formulario_usuarios()
        return "break"

    def registrar_usuario(self):
        if self.usuario_seleccionado is not None:
            messagebox.showwarning(
                "Usuario seleccionado",
                "Pulse Limpiar antes de registrar un nuevo usuario."
            )
            return

        try:
            self.restaurante_servicio.registrar_usuario(
                self.usuario,
                self.identificacion_usuario_var.get(),
                self.nombre_usuario_var.get(),
                self.correo_usuario_var.get(),
                self.contrasena_usuario_var.get(),
                self.rol_usuario_var.get()
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.actualizar_usuarios()
        self.limpiar_formulario_usuarios()
        messagebox.showinfo(
            "Registro exitoso",
            "El usuario fue registrado correctamente."
        )

    def actualizar_usuario(self):
        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Seleccione un usuario",
                "Seleccione una fila de la tabla para actualizar."
            )
            return

        try:
            self.restaurante_servicio.actualizar_usuario(
                self.usuario,
                self.usuario_seleccionado,
                self.nombre_usuario_var.get(),
                self.correo_usuario_var.get(),
                self.contrasena_usuario_var.get(),
                self.rol_usuario_var.get()
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo actualizar", str(error))
            return

        self.actualizar_usuarios()
        self.limpiar_formulario_usuarios()
        messagebox.showinfo(
            "Actualización exitosa",
            "El usuario fue actualizado correctamente."
        )

    def eliminar_usuario(self):
        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Seleccione un usuario",
                "Seleccione una fila de la tabla para eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Desea eliminar el usuario seleccionado?"
        )
        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_usuario(
                self.usuario,
                self.usuario_seleccionado
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo eliminar", str(error))
            return

        self.actualizar_usuarios()
        self.limpiar_formulario_usuarios()
        messagebox.showinfo(
            "Eliminación exitosa",
            "El usuario fue eliminado correctamente."
        )

    def limpiar_formulario_usuarios(self, enfocar=True):
        self.usuario_seleccionado = None
        seleccion = self.tabla_usuarios.selection()

        if seleccion:
            self.tabla_usuarios.selection_remove(*seleccion)

        self.tabla_usuarios.focus("")
        self.entrada_identificacion.config(state="normal")
        self.identificacion_usuario_var.set("")
        self.nombre_usuario_var.set("")
        self.correo_usuario_var.set("")
        self.contrasena_usuario_var.set("")
        self.rol_usuario_var.set("Cliente")
        self.selector_rol.config(state="readonly")
        self.al_cambiar_rol(None)

        self.botones_usuarios["Registrar"].config(state="normal")
        self.botones_usuarios["Actualizar"].config(state="disabled")
        self.botones_usuarios["Eliminar"].config(state="disabled")

        if enfocar:
            self.entrada_identificacion.focus_set()

    def crear_seccion_ventas(self):
        titulo = tk.Frame(self.pagina_ventas, bg="white")
        titulo.pack(pady=(18, 10))

        self.icono_venta = self.cargar_imagen("icono_venta.png", 45)
        if self.icono_venta is not None:
            tk.Label(
                titulo,
                image=self.icono_venta,
                bg="white"
            ).pack(side="left", padx=(0, 10))

        tk.Label(
            titulo,
            text="Registro de ventas",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#9C3D10"
        ).pack(side="left")

        formulario = tk.Frame(self.pagina_ventas, bg="white")
        formulario.pack(fill="x", padx=30)
        formulario.columnconfigure(1, weight=1)

        tk.Label(
            formulario, text="Usuario", bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.usuario_venta_var = tk.StringVar()
        self.selector_usuario = ttk.Combobox(
            formulario,
            textvariable=self.usuario_venta_var,
            state="readonly",
            width=45
        )
        self.selector_usuario.grid(
            row=0, column=1, sticky="ew", padx=12, pady=8
        )

        tk.Label(
            formulario, text="Producto", bg="white"
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.producto_venta_var = tk.StringVar()
        self.selector_producto = ttk.Combobox(
            formulario,
            textvariable=self.producto_venta_var,
            state="readonly",
            width=45
        )
        self.selector_producto.grid(
            row=1, column=1, sticky="ew", padx=12, pady=8
        )

        tk.Button(
            self.pagina_ventas,
            text="Registrar venta",
            bg="#9C3D10",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=16,
            pady=7,
            command=self.registrar_venta
        ).pack(pady=14)

        tabla_frame = tk.Frame(self.pagina_ventas, bg="white")
        tabla_frame.pack(
            fill="both", expand=True, padx=30, pady=(4, 22)
        )

        self.tabla_ventas = ttk.Treeview(
            tabla_frame,
            columns=("fecha", "usuario", "producto"),
            show="headings",
            height=9
        )
        for clave, titulo_columna in (
            ("fecha", "Fecha"),
            ("usuario", "Usuario"),
            ("producto", "Producto")
        ):
            self.tabla_ventas.heading(clave, text=titulo_columna)

        self.tabla_ventas.column("fecha", width=165, stretch=False)
        self.tabla_ventas.column("usuario", width=260)
        self.tabla_ventas.column("producto", width=260)

        barra = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=barra.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    def actualizar_ventas(self):
        usuarios = self.restaurante_servicio.listar_usuarios()
        productos = self.restaurante_servicio.listar_productos()

        self._usuarios_venta = {
            f"{u.identificacion} - {u.nombre}": u.identificacion
            for u in usuarios
        }
        self._productos_venta = {
            f"{p.codigo} - {p.nombre}": p.codigo
            for p in productos
        }

        self.selector_usuario["values"] = list(self._usuarios_venta)
        self.selector_producto["values"] = list(self._productos_venta)

        if self.usuario_venta_var.get() not in self._usuarios_venta:
            self.usuario_venta_var.set("")
        if self.producto_venta_var.get() not in self._productos_venta:
            self.producto_venta_var.set("")

        usuarios_por_id = {
            u.identificacion: u.nombre for u in usuarios
        }
        productos_por_codigo = {
            p.codigo: p.nombre for p in productos
        }

        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        for venta in self.restaurante_servicio.listar_ventas():
            nombre_usuario = usuarios_por_id.get(
                venta.identificacion_usuario,
                venta.identificacion_usuario
            )
            nombre_producto = productos_por_codigo.get(
                venta.codigo_producto,
                venta.codigo_producto
            )
            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(venta.fecha, nombre_usuario, nombre_producto)
            )

    def registrar_venta(self):
        identificacion = self._usuarios_venta.get(
            self.usuario_venta_var.get()
        )
        codigo = self._productos_venta.get(
            self.producto_venta_var.get()
        )

        try:
            venta = self.restaurante_servicio.registrar_venta(
                identificacion or "",
                codigo or ""
            )
        except (ValueError, OSError) as error:
            messagebox.showerror(
                "No se pudo registrar la venta", str(error)
            )
            return

        self.actualizar_tabla_productos()
        self.usuario_venta_var.set("")
        self.producto_venta_var.set("")
        messagebox.showinfo(
            "Venta registrada",
            f"Venta guardada: {venta.fecha}"
        )

    def actualizar_resumen(self):
        self.etiqueta_productos.config(
            text=str(self.restaurante_servicio.cantidad_productos())
        )
        self.etiqueta_usuarios.config(
            text=str(self.restaurante_servicio.cantidad_usuarios())
        )

    def actualizar_tabla_productos(self):
        for elemento in self.tabla_productos.get_children():
            self.tabla_productos.delete(elemento)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

        self.actualizar_resumen()
        self.actualizar_ventas()

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(
                self.codigo_var.get(),
                self.nombre_var.get(),
                self.categoria_var.get(),
                self.precio_var.get(),
                self.stock_var.get()
            )
            messagebox.showinfo(
                "Registro exitoso",
                "El producto fue registrado correctamente."
            )
            self.actualizar_tabla_productos()
            self.limpiar_formulario()
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo registrar", str(error))

    def consultar_producto(self):
        codigo = self.codigo_var.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Código requerido",
                "Ingrese el código del producto."
            )
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)

        if producto is None:
            messagebox.showwarning(
                "Producto no encontrado",
                "No existe un producto con ese código."
            )
            return

        self.codigo_var.set(producto.codigo)
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(str(producto.precio))
        self.stock_var.set(str(producto.stock))
        messagebox.showinfo(
            "Consulta",
            "Los datos del producto fueron cargados."
        )

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(
                self.codigo_var.get(),
                self.nombre_var.get(),
                self.categoria_var.get(),
                self.precio_var.get(),
                self.stock_var.get()
            )
            messagebox.showinfo(
                "Actualización exitosa",
                "El producto fue actualizado correctamente."
            )
            self.actualizar_tabla_productos()
            self.limpiar_formulario()
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo actualizar", str(error))

    def eliminar_producto(self):
        codigo = self.codigo_var.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Código requerido",
                "Ingrese el código del producto."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Desea eliminar este producto?"
        )
        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_producto(codigo)
            messagebox.showinfo(
                "Eliminación exitosa",
                "El producto fue eliminado correctamente."
            )
            self.actualizar_tabla_productos()
            self.limpiar_formulario()
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo eliminar", str(error))

    def limpiar_formulario(self):
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")

    def destruir(self):
        self.frame.destroy()