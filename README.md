# RESTAURANTE APP

Aplicación gráfica desarrollada en Python utilizando Tkinter para la
gestión de productos, usuarios y ventas de un restaurante.

Esta entrega corresponde a la **Semana 16**: Interacción con eventos en
Tkinter. Se parte de la aplicación de la Semana 15 (pestañas de
Productos y Ventas) sin reconstruirla, y se agrega una nueva pestaña de
**Usuarios**, con gestión completa (CRUD), roles y manejo de eventos
mediante `bind()`.

## 1. Objetivo

El proyecto tiene como objetivo aplicar los fundamentos de interfaces
gráficas y avanzar hacia la interacción real con eventos de la Semana
16:

- Componentes gráficos y contenedores.
- Formularios, tablas y controles de acción.
- Validación básica.
- Separación modular del proyecto.
- Uso de `command=` y callbacks (Semana 15) para coordinar una
  operación de negocio sin concentrar la lógica dentro de la interfaz.
- Uso de `bind()` y eventos reales de Tkinter (Semana 16): selección en
  `Treeview`, teclas `Enter`/`Escape` y cambio de valor en `Combobox`.
- Gestión de usuarios con roles (`Administrador`, `Empleado`,
  `Cliente`) y control de acceso básico a una sección de la interfaz.

La aplicación permite iniciar sesión, administrar los productos
registrados, registrar ventas que relacionan un usuario con un
producto, y ahora administrar los usuarios del sistema desde la propia
interfaz.

---

## 2. Tecnologías utilizadas

- Python 3
- Tkinter
- ttk
- JSON
- Programación orientada a objetos

Tkinter forma parte de la instalación estándar de Python, por lo que
normalmente no es necesario instalar paquetes adicionales.

---

## 3. Estructura del proyecto

```text
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

La estructura no cambió respecto a la Semana 15: se reutilizan las
mismas carpetas y se extiende el contenido de `modelos/usuario.py`,
`servicios/restaurante_servicio.py` y `ui/main_view.py`.

## 4. Funcionalidades

### Inicio de sesión

La aplicación dispone de una pantalla de inicio de sesión con el
logotipo del sistema.

Usuarios de prueba:

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `1234` | Administrador |
| `mesero` | `1234` | Empleado |
| `cliente1` | `1234` | Cliente |

### Gestión de productos

La ventana principal, en la pestaña **Productos**, permite:

- Visualizar productos.
- Registrar productos.
- Editar productos.
- Eliminar productos.
- Limpiar el formulario.
- Cerrar sesión.

### Gestión de ventas (Semana 15)

La pestaña **Ventas** permite:

- Seleccionar un usuario existente.
- Seleccionar un producto existente.
- Registrar la venta mediante un botón asociado con `command=`.
- Consultar el historial de ventas registradas.

### Gestión de usuarios (nuevo — Semana 16)

La pestaña **Usuarios** solo aparece en el menú cuando la sesión activa
pertenece al rol `Administrador`; es el control de acceso básico que
pide la actividad. Desde allí se puede:

- Registrar un nuevo usuario indicando usuario, contraseña, nombre y
  rol (`Administrador`, `Empleado` o `Cliente`).
- Consultar los usuarios registrados en una tabla (`Treeview`).
- Seleccionar un usuario de la tabla para cargar automáticamente sus
  datos en el formulario.
- Actualizar los datos del usuario seleccionado.
- Eliminar el usuario seleccionado, con confirmación previa.
- Limpiar el formulario y cancelar la selección actual.

El servicio impide eliminar el usuario con el que se inició sesión y
cambiar el rol del administrador actualmente conectado, para evitar
que la aplicación quede sin acceso administrativo.

---

## 5. Formularios

### Formulario de productos

- ID (generado automáticamente).
- Nombre.
- Categoría (Combobox).
- Precio.
- Stock.

### Formulario de ventas

- Usuario (Combobox de solo lectura).
- Producto (Combobox de solo lectura).

El ID de la venta y la fecha se generan automáticamente.

### Formulario de usuarios (nuevo)

- Usuario (nombre de inicio de sesión).
- Nombre.
- Contraseña.
- Rol (Combobox de solo lectura: `Administrador`, `Empleado`,
  `Cliente`).
- Una etiqueta junto al Combobox muestra el rol actualmente
  seleccionado y se actualiza con el evento `<<ComboboxSelected>>`.

---

## 6. Tablas

Los productos se muestran mediante un componente Treeview con las
columnas ID, Nombre, Categoría, Precio y Stock. Al seleccionar un
producto de la tabla, sus datos se cargan en el formulario para poder
editarlos (evento `<<TreeviewSelect>>`, ya presente desde la Semana
14).

Las ventas se muestran en un segundo Treeview con las columnas ID,
Producto, Usuario y Fecha.

Los usuarios se muestran en un tercer Treeview (nuevo) con las columnas
Usuario, Nombre y Rol. La contraseña no se incluye como columna de la
tabla por buena práctica, aunque sí se carga en el formulario al
seleccionar un registro.

---

## 7. Manejo de eventos (nuevo — Semana 16)

La pestaña **Usuarios** es el ejemplo principal de manejo de eventos de
esta entrega. Se mantiene el uso de `command=` (Semana 15) y se agrega
`bind()` para responder a eventos reales generados por el usuario:

```text
Interacción del usuario -> evento -> bind() -> callback(event) -> servicio -> JSON -> interfaz actualizada
```

| Evento | Widget | Acción |
|---|---|---|
| `<<TreeviewSelect>>` | Tabla de usuarios | Carga el usuario seleccionado en el formulario |
| `<Return>` | Contraseña / Rol | Registra el usuario desde el formulario |
| `<Escape>` | Todos los campos y la tabla | Limpia el formulario y cancela la selección |
| `<<ComboboxSelected>>` | Combobox de rol | Actualiza la etiqueta "Rol seleccionado" |

Botones con `command=` en la pestaña Usuarios: `Registrar`,
`Actualizar`, `Eliminar`, `Limpiar`. Ninguno de los callbacks contiene
lógica de negocio: todos delegan la validación y la persistencia a
`RestauranteServicio`, reutilizando el mismo patrón ya usado en
Productos y Ventas.

---

## 8. Contenedores utilizados

**Frame**
Se utiliza para agrupar componentes relacionados.

**LabelFrame**
Se utiliza para crear secciones visuales:

- Datos del producto.
- Listado de productos.
- Registrar venta.
- Ventas registradas.
- Datos del usuario (nuevo).
- Usuarios registrados (nuevo).
- Inicio de sesión.

**Notebook**
Se utiliza para separar la gestión de Productos, Ventas y (cuando el
usuario conectado es Administrador) Usuarios dentro de la misma
ventana principal, sin perder el encabezado compartido (usuario
conectado, rol y botón de cerrar sesión).

---

## 9. Componentes utilizados

La aplicación utiliza:

- Label
- Entry
- Button
- Combobox
- Treeview
- Scrollbar
- Frame
- LabelFrame
- Notebook

---

## 10. Persistencia

Los productos se almacenan en `datos/productos.json`.

Los usuarios se almacenan en `datos/usuarios.json`, incluyendo ahora el
campo `rol`.

Las ventas se almacenan en `datos/ventas.json`.

La clase `ArchivoServicio` se encarga de realizar la lectura y
escritura de los tres archivos JSON. `RestauranteServicio` vuelve a
leer el archivo correspondiente en cada operación, por lo que la
interfaz nunca mantiene una copia desactualizada de los datos. Al
registrar, actualizar o eliminar un usuario, el servicio reescribe
`usuarios.json` con la colección completa.

Ejemplo de usuario persistido:

```json
{
    "usuario": "mesero",
    "password": "1234",
    "nombre": "Mesero",
    "rol": "Empleado"
}
```

---

## 11. Arquitectura

El proyecto mantiene la arquitectura modular construida desde semanas
anteriores; no se reconstruyó nada desde cero.

**modelos/**
Contiene las clases que representan los datos: `Producto`, `Venta` y
`Usuario`. `Usuario` incorpora el atributo `rol` y el validador estático
`validar_rol`, que restringe el valor a `Administrador`, `Empleado` o
`Cliente`.

**servicios/**
Contiene la lógica relacionada con archivos y operaciones del
restaurante. `RestauranteServicio` incorpora el CRUD completo de
usuarios (`registrar_usuario`, `actualizar_usuario`,
`eliminar_usuario`, `buscar_usuario`) reutilizando el mismo patrón ya
usado para productos (`agregar_producto`, `actualizar_producto`,
`eliminar_producto`).

**ui/**
Contiene las ventanas y componentes de la interfaz gráfica. Los
callbacks solo recolectan los datos de los formularios o del evento
recibido; la validación y la persistencia siempre ocurren en
`RestauranteServicio`.

**datos/**
Contiene los archivos JSON utilizados para almacenar la información.

**assets/**
Contiene el logotipo del sistema y los íconos utilizados en los
botones y en el encabezado de la aplicación, incluido el ícono de la
nueva pestaña Usuarios (`users.png`, ya incorporado desde la Semana
15).

**main.py**
Es el punto de entrada de la aplicación; no se modificó esta semana.

---

## 12. Control de acceso

La aplicación usa el objeto `usuario` recibido tras un inicio de sesión
correcto para decidir qué secciones mostrar:

- `Administrador`: ve y puede usar la pestaña `Usuarios`.
- `Empleado` y `Cliente`: no ven la pestaña `Usuarios` en el Notebook.

No se implementa un sistema avanzado de permisos; el objetivo es
demostrar un control de acceso básico basado en el rol del usuario
conectado.

---

## 13. Ejecución

Abrir una terminal dentro de la carpeta del proyecto:

```bash
cd restaurante_app
```

Ejecutar:

```bash
python main.py
```

En algunos sistemas puede ser necesario utilizar:

```bash
python3 main.py
```

---

## 14. Flujo de funcionamiento

1. Se ejecuta `main.py`.
2. Se muestra la pantalla de inicio de sesión, con el logotipo del
   sistema.
3. El usuario introduce sus credenciales.
4. El sistema valida los datos mediante `RestauranteServicio`.
5. Si las credenciales son correctas, se abre la ventana principal.
6. Los productos se cargan desde `productos.json` en la pestaña
   Productos.
7. El usuario puede registrar, editar o eliminar productos.
8. En la pestaña Ventas, el usuario selecciona un usuario y un producto
   existentes y presiona **Registrar venta**.
9. Si la sesión activa es de rol `Administrador`, aparece la pestaña
   **Usuarios**.
10. Al seleccionar una fila de la tabla de usuarios (`<<TreeviewSelect>>`)
    los datos se cargan en el formulario.
11. El administrador puede registrar, actualizar o eliminar usuarios;
    también puede usar `Enter` para registrar y `Escape` para limpiar
    el formulario.
12. El Combobox de rol muestra, mediante `<<ComboboxSelected>>`, el rol
    actualmente seleccionado.
13. El usuario puede cerrar sesión y regresar al formulario de acceso.

---

## 15. Validaciones

La aplicación realiza validaciones básicas:

- El nombre, la categoría, el precio y el stock del producto son
  obligatorios y deben ser coherentes (precio > 0, stock ≥ 0).
- Para editar o eliminar un producto se debe seleccionar uno de la
  tabla.
- Para registrar una venta se debe seleccionar un usuario y un
  producto existentes.
- El rol de un usuario debe ser `Administrador`, `Empleado` o
  `Cliente` (validado en el modelo `Usuario`).
- No se puede registrar dos usuarios con el mismo nombre de usuario.
- Para actualizar o eliminar un usuario se debe seleccionar uno de la
  tabla.
- No se puede eliminar el usuario con el que se inició sesión.
- No se puede cambiar el rol del administrador actualmente conectado.

---

## 16. Conclusión

El proyecto aplica los fundamentos de interfaces gráficas mediante
componentes y contenedores, manteniendo una arquitectura modular. Con
la incorporación de la pestaña de Usuarios, se demuestra el manejo real
de eventos en Tkinter: además de los botones con `command=` ya
utilizados en Productos y Ventas, la pestaña Usuarios responde a
eventos generados por el usuario mediante `bind()` — selección en una
tabla, teclas del teclado y cambio de valor en un Combobox — delegando
siempre la lógica de negocio y la persistencia a
`RestauranteServicio`.

---

## 17. ¿Qué puntos de la actividad quedan cubiertos?

| Requisito | Implementación |
|---|---|
| Evolución sin reconstrucción | Se parte del proyecto de la Semana 15 y se extiende |
| Arquitectura modular | `modelos`, `servicios`, `ui`, `datos`, `assets` |
| Gestión de usuarios | Registrar, consultar, actualizar y eliminar usuarios |
| Roles | `Administrador`, `Empleado`, `Cliente` (validados en `Usuario`) |
| Control de acceso | Pestaña Usuarios visible solo para `Administrador` |
| Eventos con `bind()` | `<<TreeviewSelect>>`, `<Return>`, `<Escape>`, `<<ComboboxSelected>>` |
| Eventos con `command=` | Botones de Productos, Ventas y Usuarios |
| Componentes | `Label`, `Entry`, `Button`, `Combobox`, `Treeview` |
| Contenedores | `Frame`, `LabelFrame` y `Notebook` |
| Datos | Archivos JSON (`productos.json`, `usuarios.json`, `ventas.json`) |
| Modelos | `Producto`, `Usuario` (con rol) y `Venta` |
| Servicios | `ArchivoServicio` y `RestauranteServicio` |
| Punto de entrada | `main.py` |
| Persistencia | Lectura/escritura de los tres archivos JSON |
| Recursos gráficos | Logotipo e íconos en `assets/`, incluido `users.png` |
| README | Incluido y actualizado para la Semana 16 |

### Para ejecutarlo

Crea exactamente las carpetas y archivos anteriores, copia cada código
en su archivo correspondiente y finalmente ejecuta:

```bash
python main.py
```

Credenciales de prueba: `admin` / `1234` (Administrador), `mesero` /
`1234` (Empleado) o `cliente1` / `1234` (Cliente).
