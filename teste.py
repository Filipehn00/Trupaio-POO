import bcrypt

# Cadastro: Gerando o hash da senha
def criar_senha(senha):
    # Gera o hash da senha fornecida
    salt = bcrypt.gensalt()  # Gera o "sal" de forma automática
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hash

# Login: Verificando a senha fornecida
def verificar_senha(senha, senha_hash):
    # Compara a senha fornecida com o hash armazenado
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)

# Exemplo de uso:
if __name__ == "__main__":
    # Cadastro: Criar o hash da senha
    senha_original = "minha_senha_super_segura"
    hash_armazenado = criar_senha(senha_original)
    print(f"Hash armazenado: {hash_armazenado}")

    # Login: Conferir a senha fornecida
    senha_fornecida = input("Digite sua senha: ")
    if verificar_senha(senha_fornecida, hash_armazenado):
        print("Senha correta! Acesso permitido.")
    else:
        print("Senha incorreta! Acesso negado.")

