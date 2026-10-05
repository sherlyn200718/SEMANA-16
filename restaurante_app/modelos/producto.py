class Producto:
    """
    Modelo que representa un producto del restaurante.
    """

    def __init__(self, id, nombre, categoria, precio, stock):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = float(precio)
        self.stock = int(stock)

    def to_dict(self):
        """
        Convierte el objeto Producto a un diccionario
        para poder almacenarlo en JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un Producto a partir de un diccionario.
        """
        return Producto(
            data["id"],
            data["nombre"],
            data["categoria"],
            data["precio"],
            data["stock"]
        )

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"

