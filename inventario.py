class Inventario:
    def __init__(self):
        self.producto_repo = []  # lista de productos
        self.categoria_repo = {}  # diccionario de categorías, por nombre

    def agregar_producto(self, nombre, categoria_nombre, cantidad, precio):
        if categoria_nombre not in self.categoria_repo:
            self.categoria_repo[categoria_nombre] = {"nombre": categoria_nombre, "productos": []}

        producto = {
            "nombre": nombre,
            "categoria": categoria_nombre,
            "cantidad": cantidad,
            "precio": precio
        }
        self.producto_repo.append(producto)
        self.categoria_repo[categoria_nombre]["productos"].append(producto)
        return producto

    def listar_productos(self):
        return self.producto_repo

    def buscar_productos_por_categoria(self, categoria_nombre):
        if categoria_nombre in self.categoria_repo:
            return self.categoria_repo[categoria_nombre]["productos"]
        return []
       