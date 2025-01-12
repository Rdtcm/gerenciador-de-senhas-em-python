from cryptography.fernet import Fernet
import json
import os

def gerar_chave_mestra():
    print("[+] Gerando chave mestra...")
    chave = Fernet.generate_key()
    print(f"Chave: {chave.decode()}")
    return chave.decode()

def guardar_senha(chave_mestra):
    fernet = Fernet(chave_mestra.encode())

    nome_servico = input("Informe o servico: ")
    login = input("Informe o login: ")
    senha = input("Informe a senha: ")
    print()

    print("[+] Criptografando a senha...")
    senha_criptografada = fernet.encrypt(senha.encode()).decode()
    print("[+] Senha criptografada")

    try:
        with open("senhas.json", "r") as file:
             dados = json.load(file)
    except FileNotFoundError:
        dados = {}
    
    dados[nome_servico] = senha_criptografada
    
    print("[+] Guardando senha criptografada no arquivo...")
    with open("senhas.json", "w") as file:
        json.dump(dados, file, indent=4)
        print(f"[+] Senha para o servico {nome_servico} guardada com sucesso!")


def ler_senhas(chave_mestra):
    fernet = Fernet(chave_mestra.encode())

    try:
        print("[+] Abrindo o arquivo...")
        with open("senhas.json", "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        print("Nenhuma senha foi encontrada, verifique se o arquivo existe.")
        return
    
    print("\n ---- Suas Senhas ----")
    for servico, senha_criptografada in dados.items():
        try:
            senha = fernet.decrypt(senha_criptografada.encode()).decode()
            print(f"Servico: {servico} | senha: {senha}")
        except Exception as e:
            print(f"Erro ao descriptografar a senha para {servico}: {e}")

def remover_servico(chave_mestra):
    fernet = Fernet(chave_mestra)

    try:
        print("[+] Abrindo o arquivo...")
        with open("senhas.json", "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        print("Nenhuma senha foi encontrada, verifique se o arquivo existe.")
        return
    
    print("---- Servicos Salvos ----")
    for servico in dados:
        print(f"- {servico}")

    print()
    remove_servico = input("Informe o servico a ser removido: ")

    if remove_servico in dados:
        del dados[remove_servico]
        print(f"O servico {servico} foi removido com sucesso!")

        with open("senhas.json", "w") as file:
            json.dump(dados, file, indent=4)
        
    else:
        print(f"[-] Servico {servico} nao encontrado.")


def main(): #PROGRAMA PRINCIPAL

    while True:
        # ---- MENU ----
        print("---- Gerenciador de Senhas ---- \n")
        print("Op. 1 - gerar uma chave mestra")
        print("Op. 2 - guardar um nova senha")
        print("Op. 3 - ler suas senhas")
        print("op. 4 - remover um senha")
        print("Op. 5 - Sair")

        op = int(input("Digite a opcao desejada: "))

        if op == 1:
            chave_mestra = gerar_chave_mestra()
            print("Guarde a chave mestra em um local seguro")

        elif op == 2:
            chave_mestra = input("Informe sua chave mestra: ")
            guardar_senha(chave_mestra)

        elif op == 3:
            chave_mestra = input("Informe sua chave mestra: ")
            ler_senhas(chave_mestra)

        elif op == 4:
            chave_mestra = input("Informe sua chave mestra: ")
            remover_servico(chave_mestra)
        
        elif op == 5:
            break

if __name__ == '__main__':
    main()