from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# "Banco de dados" temporário
usuarios = []

# Modelo com validação
class Usuario(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr
    senha: str = Field(min_length=6)

# Rota inicial
@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}

# Criar usuário
@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    usuarios.append(usuario)
    return {"mensagem": "Usuário criado com sucesso!"}

# Listar usuários (sem mostrar senha)
@app.get("/usuarios")
def listar_usuarios():
    return [{"nome": u.nome, "email": u.email} for u in usuarios]

# Buscar usuário por email
@app.get("/usuarios/{email}")
def buscar_usuario(email: str):
    for usuario in usuarios:
        if usuario.email == email:
            return {"nome": usuario.nome, "email": usuario.email}
    return {"erro": f"Usuário com email {email} não encontrado"}

# Atualizar usuário
@app.put("/usuarios/{email}")
def atualizar_usuario(email: str, usuario_atualizado: Usuario):
    for usuario in usuarios:
        if usuario.email == email:
            usuario.nome = usuario_atualizado.nome
            usuario.email = usuario_atualizado.email
            usuario.senha = usuario_atualizado.senha
            return {"mensagem": "Usuário atualizado com sucesso!"}
    return {"erro": f"Usuário com email {email} não encontrado"}

# Deletar usuário
@app.delete("/usuarios/{email}")
def deletar_usuario(email: str):
    for usuario in usuarios:
        if usuario.email == email:
            usuarios.remove(usuario)
            return {"mensagem": "Usuário deletado com sucesso!"}
    return {"erro": f"Usuário com email {email} não encontrado"}