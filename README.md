# Restaurante Inti - Semana 14

## Descripción

Este proyecto corresponde a la Semana 14 de Programación Orientada a Objetos. La aplicación permite gestionar los productos del Restaurante Inti mediante una interfaz gráfica desarrollada con Tkinter, aplicando componentes, contenedores y gestores de geometría.

El sistema conserva una arquitectura modular que separa los modelos, servicios, datos e interfaz gráfica. También mantiene la persistencia de la información mediante archivos JSON.

## Funcionalidades

La aplicación incluye las siguientes funciones:

- Inicio de sesión mediante identificación y contraseña.
- Panel principal con la cantidad de productos y usuarios.
- Consulta de usuarios registrados.
- Registro de nuevos productos.
- Consulta de productos mediante su código.
- Actualización de productos.
- Eliminación de productos.
- Visualización de productos en una tabla.
- Almacenamiento permanente en productos.json.
- Cierre de sesión.

## Estructura del proyecto

    restaurante_app/
    ├── datos/
    │   ├── productos.json
    │   └── usuarios.json
    ├── modelos/
    │   ├── __init__.py
    │   ├── producto.py
    │   └── usuario.py
    ├── servicios/
    │   ├── __init__.py
    │   ├── archivo_servicio.py
    │   └── restaurante_servicio.py
    ├── ui/
    │   ├── __init__.py
    │   ├── login_view.py
    │   └── main_view.py
    └── main.py

## Componentes y contenedores utilizados

Para construir la interfaz se utilizaron los siguientes componentes de Tkinter y ttk:

- Tk: ventana principal.
- Frame: organización de las secciones.
- LabelFrame: agrupación del formulario y de la tabla.
- Label: presentación de títulos y textos.
- Entry: ingreso de datos.
- Button: ejecución de operaciones mediante command.
- Notebook: navegación mediante pestañas.
- Treeview: presentación organizada de productos.
- Scrollbar: desplazamiento vertical.
- Text: presentación de los usuarios registrados.
- Messagebox: mensajes de confirmación, advertencia y error.

Los componentes se distribuyeron mediante los gestores de geometría pack y grid.

## Mejoras realizadas

Durante la Semana 14 se mejoró la organización visual de la aplicación mediante un encabezado, un panel principal y pestañas para productos y usuarios.

La sección de productos incorpora un formulario con los campos código, nombre, categoría, precio y stock. También contiene botones de acción y una tabla que se actualiza después de realizar cada operación.

La interfaz solicita las operaciones a RestauranteServicio y no manipula directamente los archivos JSON. Las validaciones y reglas del sistema permanecen dentro de los modelos y servicios.

## Gestión de productos

La aplicación permite realizar las siguientes operaciones:

1. Registrar un producto nuevo.
2. Consultar un producto mediante su código.
3. Actualizar los datos de un producto existente.
4. Eliminar un producto.
5. Visualizar todos los productos registrados.
6. Limpiar los campos del formulario.

## Persistencia

Los productos se almacenan en el archivo datos/productos.json. Las operaciones de lectura y escritura se realizan mediante ArchivoServicio.

Gracias a esta persistencia, los cambios permanecen disponibles después de cerrar y volver a ejecutar la aplicación.

## Separación de responsabilidades

- Los modelos representan los productos y usuarios.
- ArchivoServicio se encarga de leer y guardar los archivos JSON.
- RestauranteServicio contiene las validaciones y operaciones del sistema.
- LoginView administra la interfaz de inicio de sesión.
- MainView organiza el panel principal, los formularios y las tablas.
- main.py inicia la aplicación y conecta sus componentes.

## Validaciones

El sistema verifica:

- Campos obligatorios.
- Código de producto no repetido.
- Precio numérico y no negativo.
- Stock entero y no negativo.
- Existencia del producto antes de actualizarlo o eliminarlo.
- Identificación y contraseña para permitir el acceso.

## Ejecución

1. Tener Python instalado.
2. Abrir el proyecto en Visual Studio Code.
3. Abrir la carpeta restaurante_app.
4. Ejecutar el archivo main.py.
5. Ingresar una identificación y contraseña registradas en usuarios.json.
6. Utilizar las pestañas para gestionar productos o consultar usuarios.

La aplicación también puede ejecutarse desde la terminal con el comando:

    python main.py