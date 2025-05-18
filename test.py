import unittest
import requests

URL_GRAPHQL = "http://localhost:5000/graphql"

class PruebasBackendGraphQL(unittest.TestCase):

    def test_consultar_productos(self):
        consulta = """
        query {
            productos {
                id
                nombre
                precio
                stock
                disponible
            }
        }
        """
        respuesta = requests.post(URL_GRAPHQL, json={"query": consulta})
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()

        self.assertNotIn("errors", datos, "La consulta GraphQL no debería tener errores")

        lista_productos = datos["data"]["productos"]
        self.assertTrue(len(lista_productos) > 0, "Debe haber al menos un producto")

        primer_producto = lista_productos[0]
        self.assertIn("id", primer_producto)
        self.assertIn("nombre", primer_producto)
        self.assertIn("precio", primer_producto)
        self.assertIn("stock", primer_producto)
        self.assertIn("disponible", primer_producto)

    def test_modificar_stock_valido(self):

        mutacion = """
        mutation ($id: Int!, $cantidad: Int!) {
            modificarStock(id: $id, cantidad: $cantidad) {
                ok
                mensaje
                producto {
                    id
                    nombre
                    stock
                    disponible
                }
            }
        }
        """
        variables = {"id": 1, "cantidad": 3}

        respuesta = requests.post(URL_GRAPHQL, json={"query": mutacion, "variables": variables})
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()

        self.assertNotIn("errors", datos, "La mutación GraphQL no debería tener errores")
        resultado = datos["data"]["modificarStock"]
        self.assertTrue(resultado["ok"], "La mutación debería ser exitosa")
        self.assertEqual(resultado["producto"]["id"], 1)
        self.assertGreaterEqual(resultado["producto"]["stock"], 3, "El stock debe haberse incrementado")

if __name__ == "__main__":
    print("------------- Iniciando pruebas del backend GraphQL --------")
    unittest.main()
