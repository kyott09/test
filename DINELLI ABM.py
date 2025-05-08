USUARIOS = {}

import re

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

def validar_email(correo):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo)

def input_dni(mensaje="Ingrese el DNI: "):
    while True:
        dni = input(mensaje)
        if dni.isdigit() and len(dni) <= 8:
            return int(dni)
        else:
            print("\n     Error: DNI inválido. Debe ser numérico de hasta 8 dígitos.")

def input_telefono(mensaje="Ingrese el Número de teléfono: "):
    while True:
        tel = input(mensaje)
        if tel.isdigit() and 8 <= len(tel) <= 12:
            return tel
        else:
            print("\n     Error: Teléfono inválido. Debe ser numérico de 8 a 12 dígitos.")

def input_nombre_usuario(mensaje="Ingrese el nombre de usuario: "):
    while True:
        nombre_usuario = input(mensaje).strip()
        if nombre_usuario and " " not in nombre_usuario:
            return nombre_usuario
        else:
            print("\n     Error: El nombre de usuario no puede estar vacío ni contener espacios.")

def alta_usuario():
    dni = input_dni()
    if dni in USUARIOS:
        print("\n     El DNI ingresado ya existe.")
    else:
        nombre_usuario = input_nombre_usuario()
        tel = input_telefono()
        while True:
            email = input("Ingrese el Email: ").strip()
            if not validar_email(email):
                print("\n   El correo ingresado no es válido. Intente nuevamente.")
            else:
                break

        USUARIOS[dni] = {
            "DNI": dni,
            "NOMBRE_USUARIO": nombre_usuario,
            "TELEFONO": tel,
            "EMAIL": email,
        }
        print("\n✅ Alta de usuario realizada con éxito.")

def buscar_usuario():
    dni_buscar = input_dni("\nIngrese el DNI del usuario a buscar: ")
    if dni_buscar in USUARIOS:
        usuario = USUARIOS[dni_buscar]
        print(f"\n{'DNI':<10} {'Nombre de Usuario':<20} {'Teléfono':<15} {'Email':<30}")
        print("-" * 75)
        for valor, dato in USUARIOS.items():
            print(f"{valor:<10} {dato['NOMBRE_USUARIO']:<20} {dato['TELEFONO']:<15} {dato['EMAIL']:<30}")
    else:
        print("\n     El DNI no está registrado, intente nuevamente.")

def eliminar_usuario():
    dni_eliminar = input_dni("\nIngrese el DNI del usuario a ELIMINAR: ")
    if dni_eliminar in USUARIOS:
        usuario = USUARIOS[dni_eliminar]
        print("\n-     ", usuario["NOMBRE_USUARIO"])
        print("-     ", usuario["DNI"])
        respuesta = input("\n    --- ¿Desea ELIMINAR el Usuario? (si/no) ---  \n").strip().lower()
        if respuesta == "si":
            del USUARIOS[dni_eliminar]
            print("\n     El usuario se eliminó correctamente ✅\n")
    else:
        print("\n     El usuario no existe, intente nuevamente ❌")

def mostrar_usuarios():
    if not USUARIOS:
        print("\n     No hay usuarios registrados.")
    else:
        print(f"\n{'DNI':<10} {'Nombre de Usuario':<20} {'Teléfono':<15} {'Email':<30}")
        print("-" * 75)
        for valor, dato in USUARIOS.items():
            print(f"{valor:<10} {dato['NOMBRE_USUARIO']:<20} {dato['TELEFONO']:<15} {dato['EMAIL']:<30}")

def modificar_nombre_usuario():
    dni_actualizar = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni_actualizar in USUARIOS:
        print("\n     El nombre de usuario registrado es -", USUARIOS[dni_actualizar]["NOMBRE_USUARIO"])
        nuevo_nombre = input_nombre_usuario("\nIngrese el NUEVO nombre de usuario: ")
        USUARIOS[dni_actualizar]["NOMBRE_USUARIO"] = nuevo_nombre
        print("\n     El nuevo nombre de usuario fue registrado con éxito! ✅-")
    else:
        print("\nEl DNI ingresado no existe")

def modificar_dni():
    dni_actualizar = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni_actualizar in USUARIOS:
        print("\n     El DNI registrado es -", USUARIOS[dni_actualizar]["DNI"])
        nuevo_dni = input_dni("\nIngrese el nuevo DNI: ")
        if nuevo_dni in USUARIOS:
            print("\n     Error: El nuevo DNI ya está registrado.")
        else:
            USUARIOS[nuevo_dni] = USUARIOS.pop(dni_actualizar)
            USUARIOS[nuevo_dni]["DNI"] = nuevo_dni
            print("\n     El nuevo DNI se registró con éxito!")
    else:
        print("\n     El DNI ingresado no existe")

def modificar_telefono():
    dni_actualizar = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni_actualizar in USUARIOS:
        print("\n- El número de teléfono registrado es: ", USUARIOS[dni_actualizar]["TELEFONO"])
        nuevo_tel = input_telefono("\nIngrese el nuevo número de teléfono: ")
        USUARIOS[dni_actualizar]["TELEFONO"] = nuevo_tel
        print("\n     El nuevo número de teléfono fue registrado con éxito!")
    else:
        print("\n     El DNI ingresado no existe")

def modificar_email():
    dni_actualizar = input_dni("Ingrese el DNI del usuario a modificar: ")
    if dni_actualizar in USUARIOS:
        print("\n   El Email registrado es -", USUARIOS[dni_actualizar]["EMAIL"])
        while True:
            email = input("   Ingrese el nuevo Email: ").strip()
            if not validar_email(email):
                print("\n   El correo ingresado no es válido. Intente nuevamente.")
            else:
                USUARIOS[dni_actualizar]["EMAIL"] = email
                print("\n   El nuevo EMAIL fue registrado con éxito! ✅-")
                break
    else:
        print("\n     El DNI ingresado no existe")

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
                print("\nOpción inválida.")


def main():
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
                print("\n     ---------- ¡Gracias! ----------\n")
                break
            case _:
                print("\nOpción inválida.")

if __name__ == "__main__":
    main()