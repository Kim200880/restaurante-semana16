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

        self.ventana.geometry("950x620")
        self.ventana.minsize(850, 550)

        self.carpeta_assets = Path(__file__).resolve().parent.parent / "assets"
        self.logo = None
        self.icono_venta = None

        self.frame = tk.Frame(self.ventana, bg="#F7F3EE")
        self.frame.pack(fill="both", expand=True)

        self.crear_encabezado()
        self.crear_pestanas()
        self.actualizar_resumen()
        self.actualizar_tabla_productos()
        self.actualizar_usuarios()
        self.actualizar_ventas()

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
            self.frame, bg="#9C3D10", padx=20, pady=12
        )
        encabezado.pack(fill="x")

        self.logo = self.cargar_imagen("logo.png", 70)
        if self.logo is not None:
            tk.Label(
                encabezado, image=self.logo, bg="#9C3D10"
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
            text=f"Bienvenida, {self.usuario.nombre}",
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
            self.frame, bg="#F7F3EE", padx=20, pady=15
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
        self.pestanas.add(self.pagina_usuarios, text="  Usuarios  ")
        self.pestanas.add(self.pagina_ventas, text="  Ventas  ")

        self.crear_resumen()
        self.crear_seccion_productos()
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
            text="Utilice las pestañas para consultar usuarios, productos y ventas.",
            font=("Arial", 11),
            bg="white",
            fg="#555555"
        ).pack(pady=35)

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
            row=0, column=0, padx=15, pady=15, sticky="ns"
        )

        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        self.crear_campo(formulario, "Código:", self.codigo_var, 0)
        self.crear_campo(formulario, "Nombre:", self.nombre_var, 1)
        self.crear_campo(formulario, "Categoría:", self.categoria_var, 2)
        self.crear_campo(formulario, "Precio:", self.precio_var, 3)
        self.crear_campo(formulario, "Stock:", self.stock_var, 4)

        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=5, column=0, columnspan=2, pady=(15, 0))

        tk.Button(
            botones, text="Registrar", width=12,
            bg="#356A32", fg="white",
            command=self.registrar_producto
        ).grid(row=0, column=0, padx=3, pady=3)

        tk.Button(
            botones, text="Consultar", width=12,
            bg="#2F6690", fg="white",
            command=self.consultar_producto
        ).grid(row=0, column=1, padx=3, pady=3)

        tk.Button(
            botones, text="Actualizar", width=12,
            bg="#D7891C", fg="white",
            command=self.actualizar_producto
        ).grid(row=1, column=0, padx=3, pady=3)

        tk.Button(
            botones, text="Eliminar", width=12,
            bg="#B02A37", fg="white",
            command=self.eliminar_producto
        ).grid(row=1, column=1, padx=3, pady=3)

        tk.Button(
            botones, text="Limpiar", width=27,
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
            row=0, column=1, padx=(0, 15),
            pady=15, sticky="nsew"
        )
        contenedor_tabla.rowconfigure(0, weight=1)
        contenedor_tabla.columnconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            contenedor_tabla, columns=columnas, show="headings"
        )

        for clave, titulo in (
            ("codigo", "Código"),
            ("nombre", "Nombre"),
            ("categoria", "Categoría"),
            ("precio", "Precio"),
            ("stock", "Stock")
        ):
            self.tabla_productos.heading(clave, text=titulo)

        self.tabla_productos.column("codigo", width=85, anchor="center")
        self.tabla_productos.column("nombre", width=140)
        self.tabla_productos.column("categoria", width=110)
        self.tabla_productos.column("precio", width=80, anchor="center")
        self.tabla_productos.column("stock", width=65, anchor="center")

        barra = ttk.Scrollbar(
            contenedor_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=barra.set)
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

    def crear_campo(self, contenedor, texto, variable, fila):
        tk.Label(
            contenedor, text=texto, font=("Arial", 10), bg="white"
        ).grid(row=fila, column=0, sticky="w", pady=7)

        tk.Entry(
            contenedor, textvariable=variable, width=24
        ).grid(row=fila, column=1, padx=(10, 0), pady=7)

    def crear_seccion_usuarios(self):
        tk.Label(
            self.pagina_usuarios,
            text="Usuarios registrados",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#9C3D10"
        ).pack(pady=(25, 12))

        contenedor = tk.Frame(self.pagina_usuarios, bg="white")
        contenedor.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        self.area_usuarios = tk.Text(
            contenedor,
            font=("Arial", 11),
            state="disabled",
            padx=12,
            pady=12
        )
        self.area_usuarios.pack(fill="both", expand=True)

    def crear_seccion_ventas(self):
        titulo = tk.Frame(self.pagina_ventas, bg="white")
        titulo.pack(pady=(18, 10))

        self.icono_venta = self.cargar_imagen("icono_venta.png", 45)
        if self.icono_venta is not None:
            tk.Label(
                titulo, image=self.icono_venta, bg="white"
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

        self.actualizar_ventas()
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

    def actualizar_usuarios(self):
        usuarios = self.restaurante_servicio.listar_usuarios()

        if usuarios:
            contenido = "\n\n".join(str(usuario) for usuario in usuarios)
        else:
            contenido = "No existen usuarios registrados."

        self.area_usuarios.config(state="normal")
        self.area_usuarios.delete("1.0", tk.END)
        self.area_usuarios.insert(tk.END, contenido)
        self.area_usuarios.config(state="disabled")

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