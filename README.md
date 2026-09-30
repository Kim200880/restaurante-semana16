# Restaurante Inti - Semana 16

## Descripción

Aplicación de escritorio desarrollada en Python y Tkinter para gestionar productos, usuarios y ventas del Restaurante Inti.

En la Semana 16 se incorpora la gestión de usuarios según su rol y el manejo de eventos del teclado y de selección. Se conserva la estructura modular y la persistencia mediante archivos JSON.

## Funcionalidades

- Inicio y cierre de sesión mediante identificación y contraseña.
- Visualización del nombre y rol del usuario conectado.
- Panel principal con la cantidad de productos y usuarios.
- Registro, consulta, actualización y eliminación de productos.
- Gestión de empleados y clientes exclusiva del administrador.
- Consulta de usuarios mediante una tabla, sin mostrar contraseñas.
- Carga de los datos del usuario al seleccionar su fila.
- Actualización de usuarios conservando la contraseña cuando el campo se deja vacío.
- Confirmación antes de eliminar un usuario.
- Registro de ventas seleccionando un usuario y un producto existentes.
- Consulta del historial de ventas.
- Logo e icono en la interfaz.
- Persistencia de productos, usuarios y ventas en archivos JSON.

## Roles de usuarios

El modelo Usuario incluye los roles Administrador, Empleado y Cliente.

Solo el administrador puede acceder a la pestaña Usuarios para registrar, consultar, actualizar y eliminar empleados y clientes. Los empleados y clientes no tienen acceso a esta pestaña.

Las cuentas de administrador pueden consultarse desde la tabla, pero no modificarse ni eliminarse mediante el formulario.

## Manejo de eventos

La sección Usuarios utiliza los siguientes eventos:

- `<<TreeviewSelect>>`: consulta el usuario seleccionado mediante el servicio y carga sus datos en el formulario.
- `<<ComboboxSelected>>`: muestra una explicación del rol elegido.
- `<Return>`: ejecuta el registro de un usuario desde los campos del formulario.
- `<Escape>`: limpia el formulario y quita la selección.

Los botones utilizan `command` para ejecutar sus acciones. El registro mediante Enter reutiliza el mismo método que el botón Registrar.

## Estructura del proyecto

La aplicación se organiza en:

- `assets/`: contiene `logo.png` e `icono_venta.png`.
- `datos/`: contiene `productos.json`, `usuarios.json` y `ventas.json`.
- `modelos/`: contiene `producto.py`, `usuario.py` y `venta.py`.
- `servicios/`: contiene `archivo_servicio.py` y `restaurante_servicio.py`.
- `ui/`: contiene `login_view.py` y `main_view.py`.
- `main.py`: inicia la aplicación.
- `README.md`: documenta el proyecto.

## Organización del código

Los modelos representan los productos, usuarios y ventas.

ArchivoServicio se encarga de leer y guardar la información en archivos JSON.

RestauranteServicio contiene las operaciones, las validaciones y el control de permisos para gestionar usuarios.

Las vistas muestran la interfaz y llaman a los servicios. La interfaz no modifica directamente los archivos JSON.

## Validaciones

- Los campos obligatorios no pueden estar vacíos.
- No se permiten identificaciones de usuarios duplicadas.
- El correo debe cumplir una validación básica de formato.
- El formulario permite registrar únicamente empleados y clientes.
- La gestión de usuarios requiere una cuenta de administrador.
- Las cuentas de administrador están protegidas contra modificación y eliminación desde el formulario.
- Las ventas requieren un usuario y un producto registrados.
- Los errores y resultados se comunican mediante mensajes en pantalla.

## Interfaz gráfica

La aplicación utiliza componentes de Tkinter y ttk como Frame, Label, Entry, Button, Combobox, Notebook y Treeview.

La tabla de usuarios muestra identificación, nombre, correo y rol. La contraseña permanece oculta y no se incluye en la tabla.

Al seleccionar un usuario, se habilitan las acciones correspondientes. El botón Limpiar o la tecla Escape permiten preparar el formulario para un nuevo registro.

## Ejecución

1. Instalar Python 3.10 o superior con Tkinter disponible.
2. Abrir en Visual Studio Code la carpeta que contiene `main.py`.
3. Ejecutar desde la terminal:

```bash
python main.py
```

4. Iniciar sesión con un usuario registrado en `datos/usuarios.json`.

## Persistencia

La información se guarda en:

- `datos/productos.json`
- `datos/usuarios.json`
- `datos/ventas.json`

Cada usuario conserva su rol en el archivo JSON. Los cambios permanecen disponibles después de cerrar y volver a ejecutar la aplicación.

## Pruebas realizadas

- Inicio de sesión como administrador y empleado.
- Acceso a la gestión de usuarios únicamente como administrador.
- Registro, consulta, actualización y eliminación de usuarios.
- Carga del formulario mediante la selección de una fila.
- Retroalimentación al seleccionar un rol.
- Limpieza del formulario mediante Escape.
- Conservación de los cambios de usuarios después de reiniciar.
- Consulta de un producto por su código.
- Registro de una nueva venta y visualización en la tabla.
- Conservación de las ventas después de reiniciar.