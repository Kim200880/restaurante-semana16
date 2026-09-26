class Venta:
    def __init__(self, identificacion_usuario: str, codigo_producto: str, fecha: str):
        if not identificacion_usuario.strip():
            raise ValueError("Debe seleccionar un usuario.")

        if not codigo_producto.strip():
            raise ValueError("Debe seleccionar un producto.")

        if not fecha.strip():
            raise ValueError("La fecha de la venta es obligatoria.")

        self.identificacion_usuario = identificacion_usuario.strip()
        self.codigo_producto = codigo_producto.strip()
        self.fecha = fecha.strip()

    def a_diccionario(self) -> dict:
        return {
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "fecha": self.fecha
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            datos["identificacion_usuario"],
            datos["codigo_producto"],
            datos["fecha"]
        )