class Usuario:
    """
    Modelo que representa un usuario del sistema.
    """

    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, usuario, password, nombre, rol="Cliente"):
        self.usuario = usuario
        self.password = password
        self.nombre = nombre
        self.rol = self.validar_rol(rol)

    @staticmethod
    def validar_rol(rol):
        """
        Restringe el rol a los valores permitidos del sistema.
        """
        rol_normalizado = (rol or "").strip()

        if rol_normalizado not in Usuario.ROLES_PERMITIDOS:
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )

        return rol_normalizado

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "password": self.password,
            "nombre": self.nombre,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            data["usuario"],
            data["password"],
            data["nombre"],
            data.get("rol", "Cliente")
        )
