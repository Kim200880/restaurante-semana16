# Restaurante App - Semana 13

## Descripción

Restaurante App es una aplicación desarrollada en Python que incorpora una interfaz gráfica de usuario mediante Tkinter. Esta versión permite realizar un acceso simulado y consultar los productos y usuarios registrados en archivos JSON.

El proyecto mantiene separadas las responsabilidades mediante modelos, servicios, archivos de datos y vistas gráficas.

## Estructura del proyecto

```text
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
```

## Componentes principales

- **Producto:** representa los productos disponibles en el restaurante.
- **Usuario:** representa los usuarios que pueden acceder a la aplicación.
- **ArchivoServicio:** lee los datos almacenados en archivos JSON.
- **RestauranteServicio:** valida el acceso y proporciona las listas de productos y usuarios.
- **LoginView:** muestra la pantalla de inicio de sesión.
- **MainView:** presenta el panel principal y permite consultar la información registrada.
- **main.py:** crea la ventana principal, prepara los servicios y controla el cambio entre las vistas.

## Flujo de la aplicación

1. La aplicación inicia mostrando la pantalla de acceso.
2. El usuario ingresa su identificación y contraseña.
3. RestauranteServicio valida las credenciales.
4. Si los datos son correctos, se muestra el panel principal.
5. El usuario puede consultar los productos registrados.
6. El usuario puede consultar los usuarios registrados.
7. La opción Ventas se presenta como una funcionalidad pendiente.
8. El botón Cerrar sesión permite regresar al login dentro de la misma ventana.

## Vistas implementadas

### Pantalla de acceso

Permite ingresar la identificación y la contraseña. También presenta mensajes visuales cuando existen campos vacíos, las credenciales son incorrectas o el acceso es correcto.

### Panel principal

Muestra un resumen de los productos y usuarios registrados. Además, incluye las opciones Productos, Usuarios, Ventas y Cerrar sesión.

## Forma de ejecución

1. Tener Python instalado en el equipo.
2. Abrir el proyecto en Visual Studio Code.
3. Abrir la carpeta `restaurante_app`.
4. Ejecutar el archivo `main.py`.

También puede ejecutarse desde la terminal con el siguiente comando:

```bash
python main.py
```

## Funcionalidades implementadas

- Interfaz gráfica desarrollada con Tkinter.
- Validación de campos vacíos.
- Validación simulada de identificación y contraseña.
- Mensajes para credenciales correctas e incorrectas.
- Lectura de productos desde `productos.json`.
- Lectura de usuarios desde `usuarios.json`.
- Visualización de productos registrados.
- Visualización de usuarios registrados.
- Ventas identificada como funcionalidad pendiente.
- Cierre de sesión dentro de la misma ventana principal.

## Consideraciones

La aplicación utiliza una única instancia de `Tk()` y un solo ciclo `mainloop()`. Las vistas solicitan la información a `RestauranteServicio` y no acceden directamente a los archivos JSON. La autenticación implementada es únicamente una simulación con fines académicos.