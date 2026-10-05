import os
from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Contiene la lógica principal del restaurante.
    """

    def __init__(self):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.ruta_productos = os.path.join(
            base_dir, "datos", "productos.json"
        )

        self.ruta_usuarios = os.path.join(
            base_dir, "datos", "usuarios.json"
        )

        self.ruta_ventas = os.path.join(
            base_dir, "datos", "ventas.json"
        )

    # -------------------------------------------------
    # PRODUCTOS
    # -------------------------------------------------

    def obtener_productos(self):
        """
        Obtiene todos los productos almacenados.
        """
        datos = ArchivoServicio.leer_json(self.ruta_productos)

        return [
            Producto.from_dict(item)
            for item in datos
        ]

    def guardar_productos(self, productos):
        """
        Guarda la lista completa de productos.
        """
        datos = [
            producto.to_dict()
            for producto in productos
        ]

        ArchivoServicio.guardar_json(
            self.ruta_productos,
            datos
        )

    def obtener_siguiente_id(self):
        """
        Genera automáticamente el siguiente ID.
        """
        productos = self.obtener_productos()

        if not productos:
            return 1

        return max(producto.id for producto in productos) + 1

    def agregar_producto(
        self,
        nombre,
        categoria,
        precio,
        stock
    ):
        """
        Agrega un nuevo producto.
        """
        productos = self.obtener_productos()

        nuevo_producto = Producto(
            self.obtener_siguiente_id(),
            nombre,
            categoria,
            precio,
            stock
        )

        productos.append(nuevo_producto)
        self.guardar_productos(productos)

        return nuevo_producto

    def actualizar_producto(
        self,
        id_producto,
        nombre,
        categoria,
        precio,
        stock
    ):
        """
        Actualiza un producto existente.
        """
        productos = self.obtener_productos()

        for producto in productos:
            if producto.id == id_producto:
                producto.nombre = nombre
                producto.categoria = categoria
                producto.precio = float(precio)
                producto.stock = int(stock)

                self.guardar_productos(productos)
                return True

        return False

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto mediante su ID.
        """
        productos = self.obtener_productos()

        productos_filtrados = [
            producto
            for producto in productos
            if producto.id != id_producto
        ]

        if len(productos_filtrados) == len(productos):
            return False

        self.guardar_productos(productos_filtrados)

        return True

    # -------------------------------------------------
    # USUARIOS (Semana 16: CRUD completo y roles)
    # -------------------------------------------------

    def validar_usuario(self, usuario, password):
        """
        Verifica las credenciales del usuario.
        """
        for user in self.obtener_usuarios():
            if (
                user.usuario == usuario
                and user.password == password
            ):
                return user

        return None

    def obtener_usuarios(self):
        """
        Obtiene todos los usuarios registrados.
        """
        datos = ArchivoServicio.leer_json(self.ruta_usuarios)

        return [
            Usuario.from_dict(item)
            for item in datos
        ]

    def guardar_usuarios(self, usuarios):
        """
        Guarda la lista completa de usuarios.
        """
        datos = [
            usuario.to_dict()
            for usuario in usuarios
        ]

        ArchivoServicio.guardar_json(
            self.ruta_usuarios,
            datos
        )

    def buscar_usuario(self, usuario):
        """
        Busca un usuario mediante su nombre de usuario (login).
        """
        for user in self.obtener_usuarios():
            if user.usuario == usuario:
                return user

        return None

    def registrar_usuario(
        self,
        usuario,
        password,
        nombre,
        rol
    ):
        """
        Registra un nuevo usuario del sistema.
        """
        usuarios = self.obtener_usuarios()

        nuevo_usuario = Usuario(usuario, password, nombre, rol)

        if self.buscar_usuario(nuevo_usuario.usuario) is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")

        usuarios.append(nuevo_usuario)
        self.guardar_usuarios(usuarios)

        return nuevo_usuario

    def actualizar_usuario(
        self,
        usuario,
        password,
        nombre,
        rol,
        usuario_actual=None
    ):
        """
        Actualiza los datos de un usuario existente mediante su login.
        """
        usuarios = self.obtener_usuarios()

        for user in usuarios:
            if user.usuario == usuario:

                datos_validados = Usuario(usuario, password, nombre, rol)

                if (
                    usuario == usuario_actual
                    and user.rol == "Administrador"
                    and datos_validados.rol != "Administrador"
                ):
                    raise ValueError(
                        "No puede cambiar el rol del administrador con el que inicio sesion."
                    )

                user.password = datos_validados.password
                user.nombre = datos_validados.nombre
                user.rol = datos_validados.rol

                self.guardar_usuarios(usuarios)
                return user

        raise ValueError("No existe un usuario con ese nombre de usuario.")

    def eliminar_usuario(self, usuario, usuario_actual=None):
        """
        Elimina un usuario mediante su nombre de usuario (login).
        """
        if usuario == usuario_actual:
            raise ValueError("No puede eliminar el usuario con el que inicio sesion.")

        usuarios = self.obtener_usuarios()

        usuarios_filtrados = [
            user
            for user in usuarios
            if user.usuario != usuario
        ]

        if len(usuarios_filtrados) == len(usuarios):
            raise ValueError("No existe un usuario con ese nombre de usuario.")

        self.guardar_usuarios(usuarios_filtrados)

    # -------------------------------------------------
    # VENTAS (Semana 15: fundamentos de manejo de eventos)
    # -------------------------------------------------

    def obtener_ventas(self):
        """
        Obtiene todas las ventas almacenadas.
        """
        datos = ArchivoServicio.leer_json(self.ruta_ventas)

        return [
            Venta.from_dict(item)
            for item in datos
        ]

    def guardar_ventas(self, ventas):
        """
        Guarda la lista completa de ventas.
        """
        datos = [
            venta.to_dict()
            for venta in ventas
        ]

        ArchivoServicio.guardar_json(
            self.ruta_ventas,
            datos
        )

    def obtener_siguiente_id_venta(self):
        """
        Genera automáticamente el siguiente ID de venta.
        """
        ventas = self.obtener_ventas()

        if not ventas:
            return 1

        return max(venta.id for venta in ventas) + 1

    def registrar_venta(self, id_producto, usuario):
        """
        Registra una venta relacionando un producto existente
        con el usuario que la realiza.
        """
        producto = next(
            (p for p in self.obtener_productos() if p.id == id_producto),
            None
        )

        if producto is None:
            return None

        usuario_valido = next(
            (u for u in self.obtener_usuarios() if u.usuario == usuario),
            None
        )

        if usuario_valido is None:
            return None

        ventas = self.obtener_ventas()

        nueva_venta = Venta(
            self.obtener_siguiente_id_venta(),
            id_producto,
            usuario,
            date.today().isoformat()
        )

        ventas.append(nueva_venta)
        self.guardar_ventas(ventas)

        return nueva_venta
