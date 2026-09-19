from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio):
        self.archivo_servicio = archivo_servicio
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []

        self.cargar_datos()

    def cargar_datos(self) -> None:
        self._productos = self.archivo_servicio.cargar_productos()
        self._usuarios = self.archivo_servicio.cargar_usuarios()

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

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)

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
            raise ValueError(
                "Ya existe un producto con ese código."
            )

        try:
            precio_convertido = float(precio)
        except (TypeError, ValueError):
            raise ValueError(
                "El precio debe ser un número válido."
            )

        try:
            stock_convertido = int(stock)
        except (TypeError, ValueError):
            raise ValueError(
                "El stock debe ser un número entero."
            )

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
            raise ValueError(
                "El precio debe ser un número válido."
            )

        try:
            stock_convertido = int(stock)
        except (TypeError, ValueError):
            raise ValueError(
                "El stock debe ser un número entero."
            )

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