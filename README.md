# Restaurante Inti - Semana 15

## Descripción

Aplicación de escritorio desarrollada en Python y Tkinter para gestionar productos, consultar usuarios y registrar ventas del Restaurante Inti. La información se conserva en archivos JSON.

## Funcionalidades

- Inicio y cierre de sesión.
- Registro, consulta, actualización y eliminación de productos.
- Visualización de productos y usuarios.
- Registro de ventas seleccionando un usuario y un producto existentes.
- Visualización de ventas en una tabla.
- Actualización del stock al realizar una venta.
- Logo e icono visibles en la interfaz.
- Persistencia de productos, usuarios y ventas en archivos JSON.

## Estructura del proyecto

```text
restaurante_app/
├── assets/
│   ├── logo.png
│   └── icono_venta.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

## Organización

Los modelos representan los productos, usuarios y ventas. `ArchivoServicio` lee y guarda los archivos JSON. `RestauranteServicio` contiene las operaciones y validaciones. Las vistas de `ui` muestran la interfaz y llaman al servicio mediante los botones.

## Interfaz gráfica

La aplicación utiliza componentes de Tkinter y ttk como `Frame`, `Label`, `Entry`, `Button`, `Combobox`, `Notebook` y `Treeview`. La pestaña Ventas permite seleccionar un usuario y un producto para registrar la venta y consultar el historial.

## Ejecución

1. Instalar Python.
2. Abrir la carpeta `restaurante_app` en Visual Studio Code.
3. Ejecutar desde la terminal:

```bash
python main.py
```

4. Iniciar sesión con un usuario registrado en `datos/usuarios.json`.

## Persistencia

Los datos se guardan en `datos/productos.json`, `datos/usuarios.json` y `datos/ventas.json`, por lo que permanecen disponibles después de cerrar la aplicación.