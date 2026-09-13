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