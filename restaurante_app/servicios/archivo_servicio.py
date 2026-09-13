import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario


class ArchivoServicio:
    def __init__(self):
        carpeta_proyecto = Path(__file__).resolve().parent.parent
        self.carpeta_datos = carpeta_proyecto / "datos"

        self.carpeta_datos.mkdir(exist_ok=True)

        self.archivo_productos = self.carpeta_datos / "productos.json"
        self.archivo_usuarios = self.carpeta_datos / "usuarios.json"

        self._crear_archivo_si_no_existe(self.archivo_productos)
        self._crear_archivo_si_no_existe(self.archivo_usuarios)

    def _crear_archivo_si_no_existe(self, ruta: Path) -> None:
        if not ruta.exists():
            ruta.write_text("[]", encoding="utf-8")

    def _leer_json(self, ruta: Path) -> list:
        try:
            contenido = ruta.read_text(encoding="utf-8")
            datos = json.loads(contenido)

            if isinstance(datos, list):
                return datos

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def cargar_productos(self) -> list[Producto]:
        datos = self._leer_json(self.archivo_productos)
        productos = []

        for elemento in datos:
            try:
                producto = Producto.desde_diccionario(elemento)
                productos.append(producto)
            except (KeyError, TypeError, ValueError):
                continue

        return productos

    def cargar_usuarios(self) -> list[Usuario]:
        datos = self._leer_json(self.archivo_usuarios)
        usuarios = []

        for elemento in datos:
            try:
                usuario = Usuario.desde_diccionario(elemento)
                usuarios.append(usuario)
            except (KeyError, TypeError, ValueError):
                continue

        return usuarios