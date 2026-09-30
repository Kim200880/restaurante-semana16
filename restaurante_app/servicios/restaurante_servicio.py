from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio):
        self.archivo_servicio = archivo_servicio
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

        self.cargar_datos()

    def cargar_datos(self) -> None:
        self._productos = self.archivo_servicio.cargar_productos()
        self._usuarios = self.archivo_servicio.cargar_usuarios()
        self._ventas = self.archivo_servicio.cargar_ventas()

    def validar_acceso(
        self,
        identificacion: str,
        contrasena: str
    ) -> Usuario | None:
        identificacion = identificacion.strip()
        contrasena = contrasena.strip()

        for usuario in self._usuarios:
            if (
                usuario.identificacion == identificacion
                and usuario.contrasena == contrasena
            ):
                return usuario

        return None

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)

    # Gestión de productos

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = codigo.strip()

        for producto in self._productos:
            if producto.codigo.lower() == codigo.lower():
                return producto

        return None

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio,
        stock
    ) -> Producto:
        if self.buscar_producto(codigo):
            raise ValueError("Ya existe un producto con ese código.")

        try:
            precio_convertido = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")

        try:
            stock_convertido = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero.")

        producto = Producto(
            codigo,
            nombre,
            categoria,
            precio_convertido,
            stock_convertido
        )

        self._productos.append(producto)
        self.archivo_servicio.guardar_productos(self._productos)

        return producto

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio,
        stock
    ) -> Producto:
        producto_actual = self.buscar_producto(codigo)

        if producto_actual is None:
            raise ValueError(
                "No se encontró un producto con ese código."
            )

        try:
            precio_convertido = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")

        try:
            stock_convertido = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero.")

        producto_actualizado = Producto(
            codigo,
            nombre,
            categoria,
            precio_convertido,
            stock_convertido
        )

        posicion = self._productos.index(producto_actual)
        self._productos[posicion] = producto_actualizado

        self.archivo_servicio.guardar_productos(self._productos)

        return producto_actualizado

    def eliminar_producto(self, codigo: str) -> None:
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError(
                "No se encontró un producto con ese código."
            )

        self._productos.remove(producto)
        self.archivo_servicio.guardar_productos(self._productos)

    # Gestión de ventas

    def registrar_venta(
        self,
        identificacion_usuario: str,
        codigo_producto: str
    ) -> Venta:
        identificacion_usuario = identificacion_usuario.strip()
        codigo_producto = codigo_producto.strip()

        usuario = self.buscar_usuario(identificacion_usuario)

        if usuario is None:
            raise ValueError("Seleccione un usuario registrado.")

        producto = self.buscar_producto(codigo_producto)

        if producto is None:
            raise ValueError("Seleccione un producto registrado.")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        venta = Venta(
            usuario.identificacion,
            producto.codigo,
            fecha
        )

        ventas_actualizadas = self._ventas + [venta]
        self.archivo_servicio.guardar_ventas(ventas_actualizadas)
        self._ventas = ventas_actualizadas

        return venta

    # Gestión de usuarios

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        identificacion = identificacion.strip()

        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario

        return None

    def _validar_administrador(self, administrador: Usuario) -> None:
        usuario_registrado = self.buscar_usuario(
            administrador.identificacion
        )

        if (
            usuario_registrado is not administrador
            or usuario_registrado.rol != "Administrador"
        ):
            raise ValueError(
                "Solo el administrador puede gestionar usuarios."
            )

    def _validar_datos_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str
    ) -> Usuario:
        if rol not in ("Empleado", "Cliente"):
            raise ValueError(
                "Solo puede gestionar usuarios Empleado o Cliente."
            )

        usuario = Usuario(
            identificacion,
            nombre,
            correo,
            contrasena,
            rol
        )

        partes_correo = usuario.correo.split("@")

        if (
            len(partes_correo) != 2
            or not partes_correo[0]
            or "." not in partes_correo[1]
            or partes_correo[1].startswith(".")
            or partes_correo[1].endswith(".")
            or any(caracter.isspace() for caracter in usuario.correo)
        ):
            raise ValueError("Ingrese un correo válido.")

        return usuario

    def registrar_usuario(
        self,
        administrador: Usuario,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str
    ) -> Usuario:
        self._validar_administrador(administrador)

        if self.buscar_usuario(identificacion):
            raise ValueError(
                "Ya existe un usuario con esa identificación."
            )

        usuario = self._validar_datos_usuario(
            identificacion,
            nombre,
            correo,
            contrasena,
            rol
        )

        usuarios_actualizados = self._usuarios + [usuario]
        self.archivo_servicio.guardar_usuarios(usuarios_actualizados)
        self._usuarios = usuarios_actualizados

        return usuario

    def actualizar_usuario(
        self,
        administrador: Usuario,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str
    ) -> Usuario:
        self._validar_administrador(administrador)

        usuario_actual = self.buscar_usuario(identificacion)

        if usuario_actual is None:
            raise ValueError(
                "No se encontró el usuario seleccionado."
            )

        if usuario_actual.rol == "Administrador":
            raise ValueError(
                "La cuenta del administrador no se modifica "
                "desde esta sección."
            )

        # Una contraseña vacía conserva la contraseña actual.
        if not contrasena.strip():
            contrasena = usuario_actual.contrasena

        usuario_actualizado = self._validar_datos_usuario(
            usuario_actual.identificacion,
            nombre,
            correo,
            contrasena,
            rol
        )

        usuarios_actualizados = self._usuarios.copy()
        posicion = usuarios_actualizados.index(usuario_actual)
        usuarios_actualizados[posicion] = usuario_actualizado

        self.archivo_servicio.guardar_usuarios(usuarios_actualizados)
        self._usuarios = usuarios_actualizados

        return usuario_actualizado

    def eliminar_usuario(
        self,
        administrador: Usuario,
        identificacion: str
    ) -> None:
        self._validar_administrador(administrador)

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            raise ValueError(
                "No se encontró el usuario seleccionado."
            )

        if usuario.rol == "Administrador":
            raise ValueError(
                "No puede eliminar la cuenta del administrador."
            )

        usuarios_actualizados = [
            item for item in self._usuarios
            if item.identificacion != usuario.identificacion
        ]

        self.archivo_servicio.guardar_usuarios(usuarios_actualizados)
        self._usuarios = usuarios_actualizados