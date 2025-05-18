# API de Productos con Flask y GraphQL

Este proyecto es una API sencilla para gestionar una lista de productos usando Flask, Graphene (GraphQL para Python) y Flask-CORS para habilitar el acceso desde un cliente frontend.

---

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

---

## Instalación

1. Clona este repositorio o copia el código en un archivo, por ejemplo `app.py`.

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
bash
Copiar
Editar
pip install Flask graphene Flask-CORS
```

## Ejecución
```bash
python app.py
```
El servidor correrá en:
http://localhost:5000

## Endpoint GraphQL

- URL: /graphql

- Método: POST

- Content-Type: application/json

## Ejemplo de Query (obtener productos)

```bash
{
  productos {
    id
    nombre
    precio
    stock
    disponible
  }
}
```

