class Usuario:
    ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str = "Cliente"
    ):
        if not identificacion.strip():
            raise ValueError("La identificación no puede estar vacía.")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not correo.strip():
            raise ValueError("El correo no puede estar vacío.")

        if not contrasena.strip():
            raise ValueError("La contraseña no puede estar vacía.")

        rol = rol.strip()
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )

        self.identificacion = identificacion.strip()
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.contrasena = contrasena.strip()
        self.rol = rol

    def a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            correo=datos["correo"],
            contrasena=datos["contrasena"],
            rol=datos.get("rol", "Cliente")
        )

    def __str__(self) -> str:
        return (
            f"Identificación: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Rol: {self.rol}"
        )