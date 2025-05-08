from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client  # Importar para conectarse a Supabase
import os  # Importar os para acceder a las variables de entorno

app = FastAPI()

# Obtener las variables de entorno de Supabase
url = os.getenv("SUPABASE_URL")  # Obtiene la URL de Supabase desde las variables de entorno
key = os.getenv("SUPABASE_KEY")  # Obtiene la clave pública de Supabase desde las variables de entorno

# Crear el cliente de Supabase utilizando las variables de entorno
supabase: Client = create_client(url, key)

class Usuario(BaseModel):
    DNI: str
    NOMBRE_USUARIO: str
    TELEFONO: str
    EMAIL: EmailStr

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: Usuario):
    # Verificar si el DNI ya existe en la base de datos de Supabase
    existing_user = supabase.table("usuarios").select("*").eq("DNI", usuario.DNI).execute()
    if len(existing_user.data) > 0:
        raise HTTPException(status_code=409, detail="El DNI ya está registrado")
    
    # Insertar el nuevo usuario en la tabla "usuarios"
    supabase.table("usuarios").insert(usuario.dict()).execute()
    return usuario

@app.put("/usuarios/{dni}")
def actualizar_usuario(dni: str, datos: Usuario):
    # Verificar si el usuario existe en Supabase
    existing_user = supabase.table("usuarios").select("*").eq("DNI", dni).execute()
    if len(existing_user.data) == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar el usuario en la tabla "usuarios"
    supabase.table("usuarios").update(datos.dict()).eq("DNI", dni).execute()
    return {"mensaje": "Usuario actualizado", "usuario": datos}

@app.get("/usuarios")
def listar_usuarios():
    # Obtener todos los usuarios desde la tabla "usuarios"
    usuarios = supabase.table("usuarios").select("*").execute()
    return usuarios.data

@app.get("/usuarios/{dni}")
def obtener_usuario(dni: str):
    # Obtener un usuario específico por DNI desde la tabla "usuarios"
    usuario = supabase.table("usuarios").select("*").eq("DNI", dni).execute()
    if len(usuario.data) == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.data[0]

@app.delete("/usuarios/{dni}")
def eliminar_usuario(dni: str):
    # Eliminar un usuario por DNI de la tabla "usuarios"
    usuario = supabase.table("usuarios").select("*").eq("DNI", dni).execute()
    if len(usuario.data) == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    supabase.table("usuarios").delete().eq("DNI", dni).execute()
    return {"mensaje": "Usuario eliminado", "usuario": usuario.data[0]}

