import re
import json

ARCHIVO_USUARIOS = "usuarios.json"
USUARIOS = {}

def guardar_datos():
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(USUARIOS, f)

def cargar_datos():
    try:
        with open(ARCHIVO_USUARIOS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# ─── menus ───

def mostrar_menu():
    print("\n--- / --- Menú de Gestión de Usuarios --- / ---\n")
    print("     1. Alta de Usuario")
    print("     2. Búsqueda de Usuario")
    print("     3. Actualizar Usuario")
    print("     4. Eliminar Usuario")
    print("     5. Mostrar Todos los Usuarios")
    print("     6. Salir\n")

def actualizar_menu():
    print("\n--- / Menú Actualización de Usuarios / ---\n")
    print("     1. Cambiar Nombre de Usuario")
    print("     2. Cambiar DNI")
    print("     3. Cambiar Teléfono")
    print("     4. Cambiar Email")
    print("     5. Volver al menú\n")

# ─── validaciones ────

def validar_email(correo):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo)

def input_dni(mensaje="Ingrese el DNI: "):
    while True:
        dni = input(mensaje)
        if dni.isdigit() and len(dni) <= 8:
            return dni
        else:
            print("     Error: DNI inválido. Debe ser numérico de hasta 8 dígitos.")

def input_telefono(mensaje="Ingrese el Número de teléfono: "):
    while True:
        tel = input(mensaje)
        if tel.isdigit() and 8 <= len(tel) <= 12:
            return tel
        else:
            print("     Error: Teléfono inválido. Debe ser numérico de 8 a 12 dígitos.")

def input_nombre_usuario(mensaje="Ingrese el nombre de usuario: "):
    while True:
        nombre_usuario = input(mensaje).strip()
        if nombre_usuario and " " not in nombre_usuario:
            return nombre_usuario
        else:
            print("     Error: El nombre de usuario no puede estar vacío ni contener espacios.")

# ─── Operaciones ───

def alta_usuario():
    dni = input_dni()
    if dni in USUARIOS:
        print("     El DNI ingresado ya existe.")
    else:
        nombre_usuario = input_nombre_usuario()
        tel = input_telefono()
        while True:
            email = input("   Ingrese el Email: ").strip()
            if validar_email(email):
                break
            print("   El correo ingresado no es válido.")
        USUARIOS[dni] = {
            "DNI": dni,
            "NOMBRE_USUARIO": nombre_usuario,
            "TELEFONO": tel,
            "EMAIL": email,
        }
        guardar_datos()
        print("✅ Alta de usuario realizada con éxito.")

def buscar_usuario():
    dni = input_dni("Ingrese el DNI del usuario a buscar: ")
    if dni in USUARIOS:
        u = USUARIOS[dni]
        print(f"\n--- DATOS DEL USUARIO ---")
        print(f"Nombre:   {u['NOMBRE_USUARIO']}")
        print(f"DNI:      {u['DNI']}")
        print(f"Teléfono: {u['TELEFONO']}")
        print(f"Email:    {u['EMAIL']}")
    else:
        print("     El DNI no está registrado.")

def eliminar_usuario():
    dni = input_dni("Ingrese el DNI del usuario a ELIMINAR: ")
    if dni in USUARIOS:
        print(f"\nUsuario: {USUARIOS[dni]['NOMBRE_USUARIO']}")
        confirmacion = input("¿Desea ELIMINAR el Usuario? (si/no): ").strip().lower()
        if confirmacion == "si":
            del USUARIOS[dni]
            guardar_datos()
            print("     El usuario se eliminó correctamente ✅")
    else:
        print("     El usuario no existe.")

def mostrar_usuarios():
    if not USUARIOS:
        print("     No hay usuarios registrados.")
    else:
        print(f"\n{'DNI':<10} {'Nombre':<20} {'Teléfono':<15} {'Email':<30}")
        print("-" * 75)
        for u in USUARIOS.values():
            print(f"{u['DNI']:<10} {u['NOMBRE_USUARIO']:<20} {u['TELEFONO']:<15} {u['EMAIL']:<30}")

def modificar_nombre_usuario():
    dni = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni in USUARIOS:
        nuevo_nombre = input_nombre_usuario("Ingrese el NUEVO nombre de usuario: ")
        USUARIOS[dni]["NOMBRE_USUARIO"] = nuevo_nombre
        guardar_datos()
        print("     Nombre actualizado con éxito ✅")
    else:
        print("     El DNI no existe.")

def modificar_dni():
    dni = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni in USUARIOS:
        nuevo_dni = input_dni("Ingrese el nuevo DNI: ")
        if nuevo_dni in USUARIOS:
            print("     Error: El nuevo DNI ya existe.")
        else:
            USUARIOS[nuevo_dni] = USUARIOS.pop(dni)
            USUARIOS[nuevo_dni]["DNI"] = nuevo_dni
            guardar_datos()
            print("     DNI actualizado con éxito ✅")
    else:
        print("     El DNI no existe.")

def modificar_telefono():
    dni = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni in USUARIOS:
        nuevo_tel = input_telefono("Ingrese el nuevo número de teléfono: ")
        USUARIOS[dni]["TELEFONO"] = nuevo_tel
        guardar_datos()
        print("     Teléfono actualizado con éxito ✅")
    else:
        print("     El DNI no existe.")

def modificar_email():
    dni = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni in USUARIOS:
        while True:
            nuevo_email = input("Ingrese el nuevo Email: ").strip()
            if validar_email(nuevo_email):
                USUARIOS[dni]["EMAIL"] = nuevo_email
                guardar_datos()
                print("     Email actualizado con éxito ✅")
                break
            else:
                print("     Email inválido. Intente nuevamente.")
    else:
        print("     El DNI no existe.")

def actualizar_usuario():
    while True:
        actualizar_menu()
        opcion = input("Selecciona una opción: ").strip()
        match opcion:
            case "1":
                modificar_nombre_usuario()
            case "2":
                modificar_dni()
            case "3":
                modificar_telefono()
            case "4":
                modificar_email()
            case "5":
                return
            case _:
                print("     Opción inválida.")

# ─── Main ───

def main():
    global USUARIOS
    USUARIOS = cargar_datos()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        match opcion:
            case "1":
                alta_usuario()
            case "2":
                buscar_usuario()
            case "3":
                actualizar_usuario()
            case "4":
                eliminar_usuario()
            case "5":
                mostrar_usuarios()
            case "6":
                print("\n     ---------- ¡Gracias! ----------")
                guardar_datos()
                break
            case _:
                print("     Opción inválida.")

if __name__ == "__main__":
    main()
