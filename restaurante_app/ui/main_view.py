import os
import tkinter as tk
from tkinter import ttk, messagebox


class MainView:
    """
    Ventana principal de la aplicación.
    """

    def __init__(self, root, usuario, on_logout):

        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout

        from servicios.restaurante_servicio import RestauranteServicio

        self.servicio = RestauranteServicio()

        self.producto_seleccionado = None
        self.iconos = {}
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        self.usuario_seleccionado = None
        self.usuario_usuario_entry = None
        self.usuario_nombre_entry = None
        self.usuario_password_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_estado = None
        self.tabla_usuarios = None

        self.root.title(
            "Restaurante App - Gestión de productos"
        )

        self.root.geometry("1040x650")
        self.root.minsize(950, 550)

        self.crear_estilos()
        self.crear_interfaz()
        self.cargar_productos()

    # =================================================
    # ESTILOS
    # =================================================

    def crear_estilos(self):

        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Titulo.TLabel",
            font=("Arial", 22, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Arial", 11)
        )

        estilo.configure(
            "Accion.TButton",
            padding=8
        )

    # =================================================
    # INTERFAZ
    # =================================================

    def crear_interfaz(self):

        # ---------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ---------------------------------------------

        contenedor_principal = ttk.Frame(
            self.root,
            padding=15
        )

        contenedor_principal.pack(
            fill="both",
            expand=True
        )

        # ---------------------------------------------
        # ENCABEZADO
        # ---------------------------------------------

        encabezado = ttk.Frame(
            contenedor_principal
        )

        encabezado.pack(
            fill="x",
            pady=(0, 15)
        )

        logo = self.cargar_icono_header()

        if logo is not None:
            ttk.Label(
                encabezado,
                image=logo
            ).pack(
                side="left",
                padx=(0, 10)
            )

        ttk.Label(
            encabezado,
            text="Restaurante App",
            style="Titulo.TLabel"
        ).pack(
            side="left"
        )

        info_usuario = ttk.Label(
            encabezado,
            text=f"Usuario: {self.usuario.nombre} ({self.usuario.rol})"
        )

        info_usuario.pack(
            side="right",
            padx=10
        )

        boton_salir = ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        )

        boton_salir.pack(
            side="right"
        )

        # ---------------------------------------------
        # PESTAÑAS (Semana 15: Ventas | Semana 16: Usuarios con roles)
        # ---------------------------------------------

        notebook = ttk.Notebook(
            contenedor_principal
        )

        notebook.pack(
            fill="both",
            expand=True
        )

        tab_productos = ttk.Frame(
            notebook,
            padding=10
        )

        notebook.add(
            tab_productos,
            text="Productos"
        )

        tab_ventas = ttk.Frame(
            notebook,
            padding=10
        )

        notebook.add(
            tab_ventas,
            text="Ventas"
        )

        # Pestaña Usuarios (Semana 16): solo visible para el rol Administrador.
        tab_usuarios = None

        if self.usuario.rol == "Administrador":

            tab_usuarios = ttk.Frame(
                notebook,
                padding=10
            )

            notebook.add(
                tab_usuarios,
                text="Usuarios"
            )

        self.crear_pestana_productos(tab_productos)
        self.crear_pestana_ventas(tab_ventas)

        if tab_usuarios is not None:
            self.crear_pestana_usuarios(tab_usuarios)

        notebook.bind(
            "<<NotebookTabChanged>>",
            self.al_cambiar_pestana
        )

    def al_cambiar_pestana(self, event):

        pestana = event.widget.tab(
            event.widget.select(), "text"
        )

        if pestana == "Ventas":
            self.refrescar_opciones_venta()

    def refrescar_opciones_venta(self):

        self.opciones_usuarios_venta = {
            f"{u.usuario} - {u.nombre}": u.usuario
            for u in self.servicio.obtener_usuarios()
        }

        self.usuario_venta_combo["values"] = list(
            self.opciones_usuarios_venta.keys()
        )

        self.opciones_productos_venta = {
            f"{p.id} - {p.nombre}": p.id
            for p in self.servicio.obtener_productos()
        }

        self.producto_venta_combo["values"] = list(
            self.opciones_productos_venta.keys()
        )

    # =================================================
    # RECURSOS GRÁFICOS (assets/ - Semana 15)
    # =================================================

    def cargar_icono(self, nombre_archivo):

        if nombre_archivo in self.iconos:
            return self.iconos[nombre_archivo]

        ruta_base = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        ruta_icono = os.path.join(
            ruta_base, "assets", "icons", nombre_archivo
        )

        if not os.path.exists(ruta_icono):
            return None

        icono = tk.PhotoImage(file=ruta_icono)
        self.iconos[nombre_archivo] = icono

        return icono

    def cargar_icono_header(self):

        ruta_base = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        ruta_logo = os.path.join(
            ruta_base, "assets", "logo", "icono.png"
        )

        if not os.path.exists(ruta_logo):
            return None

        icono = tk.PhotoImage(file=ruta_logo)
        self.iconos["_header_logo"] = icono

        return icono

    def boton_con_icono(self, contenedor, texto, comando, nombre_icono=None, estilo=None):

        imagen = self.cargar_icono(nombre_icono) if nombre_icono else None

        opciones = {"text": texto, "command": comando}

        if estilo is not None:
            opciones["style"] = estilo

        if imagen is not None:
            opciones["image"] = imagen
            opciones["compound"] = "left"

        return ttk.Button(contenedor, **opciones)

    # =================================================
    # PESTAÑA: PRODUCTOS
    # =================================================

    def crear_pestana_productos(self, parent):

        contenedor_principal = parent

        # ---------------------------------------------
        # FORMULARIO
        # ---------------------------------------------

        formulario = ttk.LabelFrame(
            contenedor_principal,
            text="Datos del producto",
            padding=15
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        # ID

        ttk.Label(
            formulario,
            text="ID:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.id_entry = ttk.Entry(
            formulario,
            width=12,
            state="readonly"
        )

        self.id_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Nombre

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.nombre_entry = ttk.Entry(
            formulario,
            width=30
        )

        self.nombre_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # Categoría

        ttk.Label(
            formulario,
            text="Categoría:"
        ).grid(
            row=0,
            column=4,
            sticky="w",
            padx=5,
            pady=5
        )

        self.categoria_combo = ttk.Combobox(
            formulario,
            width=20,
            state="readonly",
            values=[
                "Hamburguesas",
                "Pizzas",
                "Ensaladas",
                "Bebidas",
                "Postres",
                "Otros"
            ]
        )

        self.categoria_combo.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        # Precio

        ttk.Label(
            formulario,
            text="Precio:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.precio_entry = ttk.Entry(
            formulario,
            width=12
        )

        self.precio_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Stock

        ttk.Label(
            formulario,
            text="Stock:"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.stock_entry = ttk.Entry(
            formulario,
            width=12
        )

        self.stock_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        # ---------------------------------------------
        # BOTONES DEL FORMULARIO
        # ---------------------------------------------

        botones_formulario = ttk.Frame(
            formulario
        )

        botones_formulario.grid(
            row=1,
            column=4,
            columnspan=2,
            padx=5,
            pady=5
        )

        ttk.Button(
            botones_formulario,
            text="Nuevo",
            style="Accion.TButton",
            command=self.nuevo_producto
        ).pack(
            side="left",
            padx=3
        )

        self.boton_con_icono(
            botones_formulario, "Guardar", self.guardar_producto, "add.png", "Accion.TButton"
        ).pack(
            side="left",
            padx=3
        )

        self.boton_con_icono(
            botones_formulario, "Editar", self.editar_producto, "edit.png", "Accion.TButton"
        ).pack(
            side="left",
            padx=3
        )

        # ---------------------------------------------
        # TABLA
        # ---------------------------------------------

        tabla_frame = ttk.LabelFrame(
            contenedor_principal,
            text="Listado de productos",
            padding=10
        )

        tabla_frame.pack(
            fill="both",
            expand=True
        )

        columnas = (
            "id",
            "nombre",
            "categoria",
            "precio",
            "stock"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla.heading(
            "categoria",
            text="Categoría"
        )

        self.tabla.heading(
            "precio",
            text="Precio"
        )

        self.tabla.heading(
            "stock",
            text="Stock"
        )

        self.tabla.column(
            "id",
            width=60,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=280
        )

        self.tabla.column(
            "categoria",
            width=180
        )

        self.tabla.column(
            "precio",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "stock",
            width=100,
            anchor="center"
        )

        scroll_vertical = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scroll_vertical.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_vertical.pack(
            side="right",
            fill="y"
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_producto
        )

        # ---------------------------------------------
        # CONTROLES INFERIORES
        # ---------------------------------------------

        controles = ttk.Frame(
            contenedor_principal
        )

        controles.pack(
            fill="x",
            pady=(10, 0)
        )

        self.boton_con_icono(
            controles, "Eliminar seleccionado", self.eliminar_producto, "delete.png"
        ).pack(
            side="left"
        )

        self.boton_con_icono(
            controles, "Limpiar formulario", self.limpiar_formulario, "clean.png"
        ).pack(
            side="left",
            padx=10
        )

        self.estado_label = ttk.Label(
            controles,
            text="Productos cargados: 0"
        )

        self.estado_label.pack(
            side="right"
        )

    # =================================================
    # PESTAÑA: VENTAS (Semana 15 - fundamentos de eventos)
    # =================================================

    def crear_pestana_ventas(self, parent):

        # ---------------------------------------------
        # FORMULARIO
        # ---------------------------------------------

        formulario = ttk.LabelFrame(
            parent,
            text="Registrar venta",
            padding=15
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.opciones_usuarios_venta = {
            f"{u.usuario} - {u.nombre}": u.usuario
            for u in self.servicio.obtener_usuarios()
        }

        self.usuario_venta_combo = ttk.Combobox(
            formulario,
            width=28,
            state="readonly",
            values=list(self.opciones_usuarios_venta.keys())
        )

        self.usuario_venta_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            formulario,
            text="Producto:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.opciones_productos_venta = {
            f"{p.id} - {p.nombre}": p.id
            for p in self.servicio.obtener_productos()
        }

        self.producto_venta_combo = ttk.Combobox(
            formulario,
            width=28,
            state="readonly",
            values=list(self.opciones_productos_venta.keys())
        )

        self.producto_venta_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        self.boton_con_icono(
            formulario, "Registrar venta", self.registrar_venta, "add.png", "Accion.TButton"
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(10, 0),
            sticky="ew"
        )

        # ---------------------------------------------
        # TABLA
        # ---------------------------------------------

        tabla_frame = ttk.LabelFrame(
            parent,
            text="Ventas registradas",
            padding=10
        )

        tabla_frame.pack(
            fill="both",
            expand=True
        )

        columnas_venta = (
            "id",
            "producto",
            "usuario",
            "fecha"
        )

        self.tabla_ventas = ttk.Treeview(
            tabla_frame,
            columns=columnas_venta,
            show="headings",
            selectmode="browse"
        )

        self.tabla_ventas.heading("id", text="ID")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.heading("usuario", text="Usuario")
        self.tabla_ventas.heading("fecha", text="Fecha")

        self.tabla_ventas.column("id", width=50, anchor="center")
        self.tabla_ventas.column("producto", width=260)
        self.tabla_ventas.column("usuario", width=220)
        self.tabla_ventas.column("fecha", width=110, anchor="center")

        scroll_ventas = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_ventas.yview
        )

        self.tabla_ventas.configure(
            yscrollcommand=scroll_ventas.set
        )

        self.tabla_ventas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_ventas.pack(
            side="right",
            fill="y"
        )

        self.cargar_ventas()

    def cargar_ventas(self):

        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        productos = {
            producto.id: producto
            for producto in self.servicio.obtener_productos()
        }

        usuarios = {
            usuario.usuario: usuario
            for usuario in self.servicio.obtener_usuarios()
        }

        for venta in self.servicio.obtener_ventas():

            producto = productos.get(venta.id_producto)
            usuario = usuarios.get(venta.usuario)

            texto_producto = (
                f"{producto.id} - {producto.nombre}"
                if producto else str(venta.id_producto)
            )

            texto_usuario = (
                f"{usuario.usuario} - {usuario.nombre}"
                if usuario else venta.usuario
            )

            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    venta.id,
                    texto_producto,
                    texto_usuario,
                    venta.fecha
                )
            )

    def registrar_venta(self):

        # El callback solo recolecta la seleccion de los combobox;
        # la validacion y la persistencia ocurren en RestauranteServicio.

        texto_usuario = self.usuario_venta_combo.get()
        texto_producto = self.producto_venta_combo.get()

        usuario_seleccionado = self.opciones_usuarios_venta.get(texto_usuario)
        producto_seleccionado = self.opciones_productos_venta.get(texto_producto)

        if not usuario_seleccionado or producto_seleccionado is None:

            messagebox.showwarning(
                "Validación",
                "Seleccione un usuario y un producto."
            )

            return

        venta = self.servicio.registrar_venta(
            producto_seleccionado,
            usuario_seleccionado
        )

        if venta is None:

            messagebox.showerror(
                "Error",
                "No fue posible registrar la venta."
            )

            return

        messagebox.showinfo(
            "Venta registrada",
            f"La venta #{venta.id} fue registrada correctamente."
        )

        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")

        self.cargar_ventas()

    # =================================================
    # PESTAÑA: USUARIOS (Semana 16 - CRUD, roles y eventos)
    # =================================================

    def crear_pestana_usuarios(self, parent):

        # ---------------------------------------------
        # FORMULARIO
        # ---------------------------------------------

        formulario = ttk.LabelFrame(
            parent,
            text="Datos del usuario",
            padding=15
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.usuario_usuario_entry = ttk.Entry(
            formulario,
            width=24
        )

        self.usuario_usuario_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.usuario_nombre_entry = ttk.Entry(
            formulario,
            width=24
        )

        self.usuario_nombre_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            formulario,
            text="Contraseña:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.usuario_password_entry = ttk.Entry(
            formulario,
            width=24,
            show="*"
        )

        self.usuario_password_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            formulario,
            text="Rol:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.usuario_rol_combo = ttk.Combobox(
            formulario,
            width=21,
            state="readonly",
            values=("Administrador", "Empleado", "Cliente")
        )

        self.usuario_rol_combo.grid(
            row=3,
            column=1,
            padx=5,
            pady=8
        )

        self.usuario_rol_combo.set("Cliente")

        self.usuario_rol_estado = ttk.Label(
            formulario,
            text="Rol seleccionado: Cliente"
        )

        self.usuario_rol_estado.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5
        )

        # ---------------------------------------------
        # BOTONES DEL FORMULARIO
        # ---------------------------------------------

        botones_formulario = ttk.Frame(
            formulario
        )

        botones_formulario.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(10, 0)
        )

        self.boton_con_icono(
            botones_formulario, "Registrar", self.registrar_usuario, "add.png", "Accion.TButton"
        ).pack(
            side="left",
            padx=3
        )

        self.boton_con_icono(
            botones_formulario, "Actualizar", self.actualizar_usuario, "edit.png", "Accion.TButton"
        ).pack(
            side="left",
            padx=3
        )

        self.boton_con_icono(
            botones_formulario, "Eliminar", self.eliminar_usuario, "delete.png"
        ).pack(
            side="left",
            padx=3
        )

        self.boton_con_icono(
            botones_formulario, "Limpiar", self.limpiar_formulario_usuario, "clean.png"
        ).pack(
            side="left",
            padx=3
        )

        # ---------------------------------------------
        # TABLA
        # ---------------------------------------------

        tabla_frame = ttk.LabelFrame(
            parent,
            text="Usuarios registrados",
            padding=10
        )

        tabla_frame.pack(
            fill="both",
            expand=True
        )

        columnas_usuario = (
            "usuario",
            "nombre",
            "rol"
        )

        self.tabla_usuarios = ttk.Treeview(
            tabla_frame,
            columns=columnas_usuario,
            show="headings",
            selectmode="browse"
        )

        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("rol", text="Rol")

        self.tabla_usuarios.column("usuario", width=150)
        self.tabla_usuarios.column("nombre", width=260)
        self.tabla_usuarios.column("rol", width=140, anchor="center")

        scroll_usuarios = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )

        self.tabla_usuarios.configure(
            yscrollcommand=scroll_usuarios.set
        )

        self.tabla_usuarios.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_usuarios.pack(
            side="right",
            fill="y"
        )

        # Evento virtual: al seleccionar una fila se carga el usuario en el formulario.
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_usuario
        )

        # Evento de teclado: Enter registra el usuario desde el formulario.
        self.usuario_password_entry.bind(
            "<Return>",
            self.al_presionar_enter_usuario
        )

        self.usuario_rol_combo.bind(
            "<Return>",
            self.al_presionar_enter_usuario
        )

        # Evento de teclado: Escape limpia el formulario y la selección actual.
        for widget in (
            self.usuario_usuario_entry,
            self.usuario_nombre_entry,
            self.usuario_password_entry,
            self.usuario_rol_combo,
            self.tabla_usuarios
        ):
            widget.bind(
                "<Escape>",
                self.al_presionar_escape_usuario
            )

        # Evento virtual: detecta el cambio de rol seleccionado en el Combobox.
        self.usuario_rol_combo.bind(
            "<<ComboboxSelected>>",
            self.al_seleccionar_rol
        )

        self.refrescar_usuarios()

    def obtener_datos_usuario(self):

        return (
            self.usuario_usuario_entry.get().strip(),
            self.usuario_password_entry.get().strip(),
            self.usuario_nombre_entry.get().strip(),
            self.usuario_rol_combo.get().strip()
        )

    def registrar_usuario(self):

        usuario, password, nombre, rol = self.obtener_datos_usuario()

        try:

            self.servicio.registrar_usuario(
                usuario,
                password,
                nombre,
                rol
            )

            messagebox.showinfo(
                "Usuarios",
                "Usuario registrado correctamente."
            )

            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()

        except ValueError as error:

            messagebox.showerror(
                "Usuarios",
                str(error)
            )

    def seleccionar_usuario(self, event=None):

        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        if not valores:
            return

        usuario_obj = self.servicio.buscar_usuario(valores[0])

        if usuario_obj is None:
            return

        self.usuario_seleccionado = usuario_obj.usuario

        self.usuario_usuario_entry.delete(0, tk.END)
        self.usuario_usuario_entry.insert(0, usuario_obj.usuario)

        self.usuario_nombre_entry.delete(0, tk.END)
        self.usuario_nombre_entry.insert(0, usuario_obj.nombre)

        self.usuario_password_entry.delete(0, tk.END)
        self.usuario_password_entry.insert(0, usuario_obj.password)

        self.usuario_rol_combo.set(usuario_obj.rol)
        self.actualizar_texto_rol(usuario_obj.rol)

    def actualizar_usuario(self):

        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Usuarios",
                "Seleccione un usuario de la tabla."
            )
            return

        usuario, password, nombre, rol = self.obtener_datos_usuario()

        if usuario != self.usuario_seleccionado:
            messagebox.showwarning(
                "Usuarios",
                "No cambie el nombre de usuario del registro seleccionado."
            )
            return

        try:

            self.servicio.actualizar_usuario(
                usuario,
                password,
                nombre,
                rol,
                self.usuario.usuario
            )

            messagebox.showinfo(
                "Usuarios",
                "Usuario actualizado correctamente."
            )

            self.refrescar_usuarios()

        except ValueError as error:

            messagebox.showerror(
                "Usuarios",
                str(error)
            )

    def eliminar_usuario(self):

        if self.usuario_seleccionado is None:
            messagebox.showwarning(
                "Usuarios",
                "Seleccione un usuario de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Usuarios",
            f"¿Desea eliminar al usuario '{self.usuario_seleccionado}'?"
        )

        if not confirmar:
            return

        try:

            self.servicio.eliminar_usuario(
                self.usuario_seleccionado,
                self.usuario.usuario
            )

            messagebox.showinfo(
                "Usuarios",
                "Usuario eliminado correctamente."
            )

            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()

        except ValueError as error:

            messagebox.showerror(
                "Usuarios",
                str(error)
            )

    def limpiar_formulario_usuario(self):

        self.usuario_seleccionado = None

        self.usuario_usuario_entry.delete(0, tk.END)
        self.usuario_nombre_entry.delete(0, tk.END)
        self.usuario_password_entry.delete(0, tk.END)

        self.usuario_rol_combo.set("Cliente")
        self.actualizar_texto_rol("Cliente")

        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)

        self.usuario_usuario_entry.focus()

    def al_presionar_enter_usuario(self, event):
        # Semana 16: Enter confirma el registro del usuario desde el formulario.
        self.registrar_usuario()

    def al_presionar_escape_usuario(self, event):
        # Semana 16: Escape cancela la selección y limpia el formulario.
        self.limpiar_formulario_usuario()

    def al_seleccionar_rol(self, event):
        # Semana 16: evento virtual del Combobox al cambiar de rol.
        self.actualizar_texto_rol(self.usuario_rol_combo.get())

    def actualizar_texto_rol(self, rol):
        self.usuario_rol_estado.config(
            text=f"Rol seleccionado: {rol}"
        )

    def refrescar_usuarios(self):

        self.limpiar_tabla_usuarios()

        for usuario in self.servicio.obtener_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(usuario.usuario, usuario.nombre, usuario.rol)
            )

    def limpiar_tabla_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)


    # =================================================
    # PRODUCTOS
    # =================================================

    def cargar_productos(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        productos = self.servicio.obtener_productos()

        for producto in productos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

        self.estado_label.config(
            text=f"Productos cargados: {len(productos)}"
        )

    def seleccionar_producto(self, event=None):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        if not valores:
            return

        self.producto_seleccionado = int(
            valores[0]
        )

        self.id_entry.config(
            state="normal"
        )

        self.id_entry.delete(
            0,
            tk.END
        )

        self.id_entry.insert(
            0,
            valores[0]
        )

        self.id_entry.config(
            state="readonly"
        )

        self.nombre_entry.delete(
            0,
            tk.END
        )

        self.nombre_entry.insert(
            0,
            valores[1]
        )

        self.categoria_combo.set(
            valores[2]
        )

        self.precio_entry.delete(
            0,
            tk.END
        )

        self.precio_entry.insert(
            0,
            valores[3].replace("$", "")
        )

        self.stock_entry.delete(
            0,
            tk.END
        )

        self.stock_entry.insert(
            0,
            valores[4]
        )

    # =================================================
    # VALIDACIÓN
    # =================================================

    def obtener_datos_formulario(self):

        nombre = self.nombre_entry.get().strip()
        categoria = self.categoria_combo.get().strip()
        precio = self.precio_entry.get().strip()
        stock = self.stock_entry.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre del producto."
            )
            return None

        if not categoria:
            messagebox.showwarning(
                "Validación",
                "Seleccione una categoría."
            )
            return None

        try:
            precio_numero = float(precio)

            if precio_numero <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Validación",
                "El precio debe ser un número mayor que cero."
            )

            return None

        try:
            stock_numero = int(stock)

            if stock_numero < 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Validación",
                "El stock debe ser un número entero mayor o igual a cero."
            )

            return None

        return (
            nombre,
            categoria,
            precio_numero,
            stock_numero
        )

    # =================================================
    # NUEVO
    # =================================================

    def nuevo_producto(self):

        self.limpiar_formulario()

        nuevo_id = self.servicio.obtener_siguiente_id()

        self.id_entry.config(
            state="normal"
        )

        self.id_entry.insert(
            0,
            str(nuevo_id)
        )

        self.id_entry.config(
            state="readonly"
        )

        self.nombre_entry.focus()

    # =================================================
    # GUARDAR
    # =================================================

    def guardar_producto(self):

        datos = self.obtener_datos_formulario()

        if datos is None:
            return

        nombre, categoria, precio, stock = datos

        try:

            producto = self.servicio.agregar_producto(
                nombre,
                categoria,
                precio,
                stock
            )

            messagebox.showinfo(
                "Producto guardado",
                f"El producto '{producto.nombre}' fue registrado correctamente."
            )

            self.cargar_productos()
            self.limpiar_formulario()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No fue posible guardar el producto.\n{error}"
            )

    # =================================================
    # EDITAR
    # =================================================

    def editar_producto(self):

        if self.producto_seleccionado is None:

            messagebox.showwarning(
                "Editar",
                "Seleccione un producto de la tabla."
            )

            return

        datos = self.obtener_datos_formulario()

        if datos is None:
            return

        nombre, categoria, precio, stock = datos

        actualizado = self.servicio.actualizar_producto(
            self.producto_seleccionado,
            nombre,
            categoria,
            precio,
            stock
        )

        if actualizado:

            messagebox.showinfo(
                "Producto actualizado",
                "El producto fue actualizado correctamente."
            )

            self.cargar_productos()
            self.limpiar_formulario()

        else:

            messagebox.showerror(
                "Error",
                "No se encontró el producto."
            )

    # =================================================
    # ELIMINAR
    # =================================================

    def eliminar_producto(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Eliminar",
                "Seleccione un producto de la tabla."
            )

            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        id_producto = int(
            valores[0]
        )

        nombre_producto = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar '{nombre_producto}'?"
        )

        if not confirmar:
            return

        eliminado = self.servicio.eliminar_producto(
            id_producto
        )

        if eliminado:

            messagebox.showinfo(
                "Producto eliminado",
                "El producto fue eliminado correctamente."
            )

            self.cargar_productos()
            self.limpiar_formulario()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible eliminar el producto."
            )

    # =================================================
    # LIMPIAR
    # =================================================

    def limpiar_formulario(self):

        self.producto_seleccionado = None

        self.id_entry.config(
            state="normal"
        )

        self.id_entry.delete(
            0,
            tk.END
        )

        self.id_entry.config(
            state="readonly"
        )

        self.nombre_entry.delete(
            0,
            tk.END
        )

        self.categoria_combo.set("")

        self.precio_entry.delete(
            0,
            tk.END
        )

        self.stock_entry.delete(
            0,
            tk.END
        )

        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

    # =================================================
    # CERRAR SESIÓN
    # =================================================

    def cerrar_sesion(self):

        confirmar = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea cerrar la sesión?"
        )

        if confirmar:

            self.root.destroy()

            self.on_logout()
