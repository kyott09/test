from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

ARCHIVO = "usuarios.json"

@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse("static/index.html")


class Usuario(BaseModel):
    DNI: str
    NOMBRE_USUARIO: str
    TELEFONO: str
    EMAIL: EmailStr

def cargar_usuarios():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            usuarios = json.load(f)
            print(f"Usuarios cargados: {usuarios}")  # Imprimir usuarios cargados
            return usuarios
    print("No se encontró el archivo o está vacío.")  # Mensaje si el archivo no existe
    return {}

def guardar_usuarios(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Datos guardados: {data}")  # Imprimir los datos guardados

@app.get("/usuarios")
def listar_usuarios():
    usuarios = cargar_usuarios()
    print(f"Usuarios listados: {usuarios}")  # Imprimir usuarios listados
    return usuarios

@app.get("/usuarios/{dni}")
def obtener_usuario(dni: str):
    usuarios = cargar_usuarios()
    if dni in usuarios:
        return usuarios[dni]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: Usuario):
    usuarios = cargar_usuarios()
    if usuario.DNI in usuarios:
        raise HTTPException(status_code=409, detail="El DNI ya está registrado")
    usuarios[usuario.DNI] = usuario.dict()
    guardar_usuarios(usuarios)
    return usuario

@app.put("/usuarios/{dni}")
def actualizar_usuario(dni: str, datos: Usuario):
    usuarios = cargar_usuarios()
    if dni not in usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuarios[dni] = datos.dict()
    guardar_usuarios(usuarios)
    return {"mensaje": "Usuario actualizado", "usuario": datos}

@app.delete("/usuarios/{dni}")
def eliminar_usuario(dni: str):
    usuarios = cargar_usuarios()
    if dni in usuarios:
        eliminado = usuarios.pop(dni)
        guardar_usuarios(usuarios)
        return {"mensaje": "Usuario eliminado", "usuario": eliminado}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Este bloque es para asegurar que `uvicorn` ejecute tu app correctamente en entornos locales o en despliegue
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
