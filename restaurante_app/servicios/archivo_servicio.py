import json
import os


class ArchivoServicio:
    """
    Servicio encargado de leer y escribir archivos JSON.
    """

    @staticmethod
    def leer_json(ruta):
        """
        Lee un archivo JSON y devuelve su contenido.
        """
        if not os.path.exists(ruta):
            return []

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def guardar_json(ruta, datos):
        """
        Guarda información en formato JSON.
        """
        directorio = os.path.dirname(ruta)

        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
