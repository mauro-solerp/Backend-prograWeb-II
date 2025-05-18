# Respuestas

## 1. ¿Qué ventajas ofrece GraphQL sobre REST en este contexto?



### 1. Consultas específicas
- **REST**: Devuelve todos los campos definidos en el endpoint, aunque no todos sean necesarios
- **GraphQL**: Permite solicitar únicamente los campos requeridos, optimizando el ancho de banda

### 2. Agregación de datos
- **REST**: Requiere múltiples llamadas a diferentes endpoints para obtener datos relacionados
- **GraphQL**: Permite obtener datos complejos y relacionados en una sola consulta

### 3. Evolución del API
- **REST**: Suele necesitar versionado
- **GraphQL**: Los nuevos campos pueden añadirse sin afectar las consultas existentes

### 4. Sistema de tipos
- **GraphQL** ofrece:
  - Esquema bien definido
  - Validación automática de consultas
  - Documentación autogenerada
- **REST** depende más de:
  - Documentación externa
  - Convenciones de implementación

### 5. Flexibilidad para clientes
GraphQL es particularmente útil cuando:
- Diferentes clientes necesitan distintas vistas de los datos
- Las aplicaciones requieren combinaciones variables de información
- Se busca minimizar el número de solicitudes al servidor


## 2. ¿Cómo se definen los tipos y resolvers en una API con GraphQL?

### Definición de Tipos y Resolvers en GraphQL

#### Estructura básica de tipos

Los tipos en GraphQL se definen mediante un sistema de esquemas:

```python
class ProductoType(graphene.ObjectType):
    id = graphene.Int()
    nombre = graphene.String()
    precio = graphene.Float()
    stock = graphene.Int()
    disponible = graphene.Boolean()
```

---

- Cada campo tiene un tipo específico (Int, String, Float, Boolean...)

- Pueden crearse tipos personalizados para estructuras complejas

- Los tipos pueden tener campos obligatorios (con required=True)


### Resolvers

Los resolvers son métodos que obtienen los datos para cada campo:

```python
class Query(graphene.ObjectType):
    productos = graphene.List(ProductoType)
    
    def resolve_productos(self, info):
        # Lógica para obtener los productos
        return lista_de_productos
```

#### Funcionamiento:

- Cada campo en el tipo Query/Mutation necesita su resolver

- Por convención, se nombran resolve_<nombre_campo>

- Reciben parámetros estándar:

  - self: Instancia del objeto

  - info: Metadatos sobre la ejecución
  
  - Argumentos definidos en el esquema


## 3. ¿Por qué es importante que el backend también actualice disponible y no depender solo del frontend?


### 1. Consistencia de datos
- **Problema**: Si solo el frontend calcula `disponible = stock > 0`, diferentes clientes podrían tener lógicas inconsistentes
- **Solución**: El backend garantiza que la regla `disponible` se aplique uniformemente para todos los consumidores del API

### 2. Integridad del negocio

- **Regla de negocio**: La disponibilidad es un concepto fundamental que afecta:
  - Procesos de compra

  - Gestión de inventario

  - Reportes analíticos

- **Riesgo**: Un frontend mal implementado podría mostrar productos sin stock como disponibles

### 3. Seguridad

- **Vulnerabilidad**: Un cliente malintencionado podría modificar la lógica frontend para mostrar productos agotados como disponibles

- **Protección**: El backend actúa como fuente única de verdad

### 4. Eficiencia en sistemas distribuidos

- **Escenario**: Múltiples clientes (web, móvil, otros servicios) accediendo al mismo dato

- **Ventaja**: Evita que cada cliente replique la misma lógica de cálculo

### 5. Sincronización en tiempo real


- **Caso de uso**: Cuando el stock llega a cero:

  - El backend puede actualizar inmediatamente `disponible=False`

  - Todos los clientes reciben el cambio simultáneamente

## 4. ¿Cómo garantizas que la lógica de actualización de stock y disponibilidad sea coherente?

La coherencia en la lógica de actualización del stock y la disponibilidad se garantiza mediante los siguientes mecanismos implementados en la mutación `ModificarStock`:

### 1. **Validación de stock negativo**
Antes de aplicar una modificación, se verifica que el nuevo stock no sea negativo:

```python
if nuevo_stock < 0:
    return ModificarStock(
        ok=False,
        mensaje="El stock no puede ser negativo",
        producto=None
    )
```
Esto impide reducir el stock por debajo de cero, asegurando que siempre se mantenga un valor coherente.

### 2. Actualización de disponibilidad

La propiedad disponible se actualiza automáticamente en función del nuevo stock

```python
producto_en_lista["disponible"] = nuevo_stock > 0
```

- Si el stock es mayor a 0, el producto se marca como disponible (True).

- Si el stock es 0, el producto se marca como no disponible (False).

Esto garantiza que la disponibilidad esté siempre sincronizada con el stock actual.

###  3. Respuesta detallada en la mutación

Después de una actualización exitosa, se devuelve el estado actualizado del producto, junto con un mensaje y un indicador de éxito:

```python
return ModificarStock(
    ok=True,
    mensaje="Stock actualizado correctamente",
    producto=producto_actualizado
)
```

Esto permite al cliente verificar fácilmente que los datos retornados reflejan la lógica aplicada.

