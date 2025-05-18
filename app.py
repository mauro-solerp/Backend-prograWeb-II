from flask import Flask, request, jsonify
from flask_cors import CORS
import graphene

lista_de_productos = [
    {"id": 1, "nombre": "Producto A", "precio": 10.0, "stock": 5, "disponible": True},
    {"id": 2, "nombre": "Producto B", "precio": 20.0, "stock": 0, "disponible": False},
    {"id": 3, "nombre": "Producto C", "precio": 15.0, "stock": 10, "disponible": True},
]

class ProductoType(graphene.ObjectType):
    id = graphene.Int()
    nombre = graphene.String()
    precio = graphene.Float()
    stock = graphene.Int()
    disponible = graphene.Boolean()

class Query(graphene.ObjectType):
    productos = graphene.List(ProductoType)

    def resolve_productos(self, info):
        resultado = []
        for producto in lista_de_productos:
            producto_objeto = ProductoType(
                id=producto["id"],
                nombre=producto["nombre"],
                precio=producto["precio"],
                stock=producto["stock"],
                disponible=producto["disponible"]
            )
            resultado.append(producto_objeto)
        return resultado

class ModificarStock(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        cantidad = graphene.Int(required=True)

    producto = graphene.Field(ProductoType)
    ok = graphene.Boolean()
    mensaje = graphene.String()

    def mutate(self, info, id, cantidad):
        for producto_en_lista in lista_de_productos:
            if producto_en_lista["id"] == id:
                nuevo_stock = producto_en_lista["stock"] + cantidad
                if nuevo_stock < 0:
                    return ModificarStock(
                        ok=False,
                        mensaje="El stock no puede ser negativo",
                        producto=None
                    )
                producto_en_lista["stock"] = nuevo_stock
                producto_en_lista["disponible"] = nuevo_stock > 0

                producto_actualizado = ProductoType(
                    id=producto_en_lista["id"],
                    nombre=producto_en_lista["nombre"],
                    precio=producto_en_lista["precio"],
                    stock=producto_en_lista["stock"],
                    disponible=producto_en_lista["disponible"]
                )

                return ModificarStock(
                    ok=True,
                    mensaje="Stock actualizado correctamente",
                    producto=producto_actualizado
                )

        return ModificarStock(
            ok=False,
            mensaje="Producto no encontrado",
            producto=None
        )

class Mutation(graphene.ObjectType):
    modificar_stock = ModificarStock.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route("/graphql", methods=["POST"])
def graphql():
    data = request.get_json()
    resultado = schema.execute(
        data.get("query"),
        variables=data.get("variables")
    )
    if resultado.errors:
        lista_de_errores = [str(error) for error in resultado.errors]
        return jsonify({"errors": lista_de_errores}), 400
    return jsonify(resultado.data)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
