class Venta:
    """
    Modelo que representa una venta del restaurante.
    """

    def __init__(self, id, id_producto, usuario, fecha):
        self.id = id
        self.id_producto = id_producto
        self.usuario = usuario
        self.fecha = fecha

    def to_dict(self):
        """
        Convierte el objeto Venta a un diccionario
        para poder almacenarlo en JSON.
        """
        return {
            "id": self.id,
            "id_producto": self.id_producto,
            "usuario": self.usuario,
            "fecha": self.fecha
        }

    @staticmethod
    def from_dict(data):
        """
        Crea una Venta a partir de un diccionario.
        """
        return Venta(
            data["id"],
            data["id_producto"],
            data["usuario"],
            data["fecha"]
        )

    def __str__(self):
        return f"Venta {self.id} - Producto {self.id_producto}"
