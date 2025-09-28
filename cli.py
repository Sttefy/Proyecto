from inventario import Inventario
from models import Producto

def pedir_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Ingrese un número entero válido.")

def pedir_float(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Ingrese un número (ej. 12.5).")

def main():
    inv = Inventario()
    try:
        while True:
            print("\n=== Sistema de Gestión de Inventario (CLI) ===")
            print("1) Agregar producto")
            print("2) Eliminar producto")
            print("3) Actualizar producto")
            print("4) Buscar por nombre")
            print("5) Mostrar todos")
            print("6) Ver por ID")
            print("0) Salir")
            op = input("Seleccione una opción: ").strip()

            if op == "1":
                pid = pedir_int("ID único: ")
                nombre = input("Nombre: ").strip()
                cantidad = pedir_int("Cantidad: ")
                precio = pedir_float("Precio: ")
                try:
                    inv.agregar_producto(Producto(pid, nombre, cantidad, precio))
                    print("✔ Producto agregado.")
                except Exception as e:
                    print("✖", e)

            elif op == "2":
                pid = pedir_int("ID a eliminar: ")
                print("✔ Eliminado." if inv.eliminar_producto(pid) else "✖ No existe ese ID.")

            elif op == "3":
                pid = pedir_int("ID a actualizar: ")
                print("Dejar vacío para no cambiar.")
                nombre = input("Nuevo nombre: ").strip()
                cantidad_txt = input("Nueva cantidad: ").strip()
                precio_txt = input("Nuevo precio: ").strip()

                nombre = nombre if nombre else None
                cantidad = int(cantidad_txt) if cantidad_txt else None
                precio = float(precio_txt) if precio_txt else None

                try:
                    ok = inv.actualizar_producto(pid, nombre=nombre, cantidad=cantidad, precio=precio)
                    print("✔ Actualizado." if ok else "✖ ID no encontrado.")
                except Exception as e:
                    print("✖", e)

            elif op == "4":
                q = input("Texto a buscar en el nombre: ").strip()
                res = inv.buscar_por_nombre(q)
                if not res:
                    print("(Sin resultados)")
                for p in res:
                    print(" - ", p)

            elif op == "5":
                for p in inv.listar_todos():
                    print(" - ", p)

            elif op == "6":
                pid = pedir_int("ID a consultar: ")
                p = inv.get_product_by_id(pid)
                print(p if p else "No encontrado." )

            elif op == "0":
                print("Hasta luego.")
                break

            else:
                print("Opción inválida.")
    finally:
        inv.cerrar()

if __name__ == "__main__":
    main()
