"""Sistema Bancário Simples, como parte do Curso de Python da DIO
    Desenvolvido por Hugo Rebonato
"""

from datetime import datetime

def main():

    saldo = 0
    valor = 0

    lista_usuarios = []
    lista_contas = []
    extrato = []

    conta_selecionada = 0

    AGENCIA = "0001"
    LIMITE_SAQUE = 500
    LIMITE_SAQUES_DIARIOS = 10

    opcao = menu_inicial()

    while True:           

        if opcao == "u": # Exibe o Menu de Usuários
            opcao = menu_usuarios()

        elif opcao == "n": # Cria um novo Usuário
            criar_usuario(lista_usuarios)
            opcao = menu_usuarios()

        elif opcao == "l": # Listar Usuários
            listar_usuarios(lista_usuarios, lista_contas)
            opcao = menu_usuarios()

        elif opcao == "c": #Cria uma nova Conta
            print("Menu Contas")
            criar_conta(AGENCIA, lista_contas, lista_usuarios)
            opcao = menu_usuarios()

        elif opcao == "e": # Entra em uma conta para movimentar
            conta_digitada = input("Digite o número da conta: ")
            conta = seleciona_conta(conta_digitada, lista_contas, lista_usuarios)
            if conta :
                conta_selecionada = conta["numero_conta"]
                saldo = conta["saldo"]
                opcao = menu_contas(conta)
            else:
                opcao = menu_inicial()

        elif opcao == "d": # Realiza um Depósito
            numero_conta = input("Digite a conta de destino: ")
            conta = seleciona_conta(numero_conta, lista_contas, lista_usuarios)

            if conta:
                saldo = conta["saldo"]
                valor = input("Informe o valor do depósito: ")
                conta["saldo"] = depositar(conta["saldo"], valor, extrato, conta["numero_conta"])
            opcao = menu_inicial()

        elif opcao == "s": #Realiza um saque            
            if conta_selecionada == 0:
                mensagem_erro("Você precisa entrar em uma conta primeiro!")
                opcao = menu_inicial()
                continue

            print("##### Realizando um Saque: #####")
            valor = input("Informe o valor do saque: ")            

            saldo = sacar(
                conta = conta,
                saldo=conta["saldo"],
                valor=valor,
                extrato = extrato,
                limite_saque = LIMITE_SAQUE,
                numero_saques_feitos = conta["saques_feitos"],
                limite_saques_diarios = LIMITE_SAQUES_DIARIOS
            )
            opcao = menu_contas(conta)

        elif opcao == "i": # Imprime o Extrato
            if conta_selecionada == 0:
                mensagem_erro("Você precisa entrar em uma conta primeiro!")
                opcao = menu_inicial()
                continue
            imprimir_extrato(saldo,extrato=extrato,numero_conta=conta_selecionada)
            conta = verifica_conta(conta_selecionada, lista_contas)
            opcao = menu_contas(conta)

        elif opcao == "v": #Volta ao Menu Inicial
            opcao = menu_inicial()

        elif opcao == "q":
            print("#### Obrigado! Volte sempre! #####\n\n")
            break

        else:
            mensagem_erro("Operação inválida, por favor selecione novamente a operação desejada.")
            opcao = menu_inicial()

def menu_inicial():
    texto = """
    ################ SISTEMA BANCÁRIO #################
    [u] Menu de Usuários
    [e] Entrar em uma Conta
    [d] Depositar
    [q] Sair

    => """
    opcao = input(texto)
    return opcao

def menu_usuarios():
    texto = """
        ###### MENU DE USUÁRIO #######
            [n] Novo Usuário
            [l] Listar Usuários  
            [c] Nova Conta      
            [v] Voltar
    
            => """
    opcao = input(texto)
    return opcao

def menu_contas(conta):
    texto = f"""
        ###### MENU DA CONTA Nº {conta["numero_conta"]} #######
            [s] Sacar
            [i] Imprimir Extrato        
            [v] Voltar
    
            => """
    opcao = input(texto)
    return opcao

def mensagem_erro(texto="Você deve digitar um valor válido!"):
    print("\n")
    print(f"#".center(len(texto)+8,"#"))
    print(f"#", texto.center(len(texto)+4), "#")
    print(f"#".center(len(texto)+8,"#"))

def verifica_valor(valor):
    if valor.isdigit():
        if float(valor):
            valor = float(valor)
            if valor > 0:                
                return True
            else:        
                return False
        else:
            return False
    else:
        return False

def criar_usuario(lista_usuarios):
    print("##### CRIANDO UM NOVO USUÁRIO #####")
    cpf = input("Digite o CPF do usuário: ")
    if verifica_usuario(cpf, lista_usuarios) :
        mensagem_erro("Usuário já existe no sistema")
        return

    nome = input("Digite o Nome do usuário: ")
    data_nascimento = input("Digite a Data de Nascimento do usuário: ")
    endereco = input("Digite o Endereço do Usuário: ")
    lista_usuarios.append({
        "cpf": cpf, 
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "endereco": endereco
    })

def verifica_usuario(cpf, lista_usuarios):    
    nome_usuario = False
    for usuario in lista_usuarios :
        if usuario["cpf"] == cpf :            
            nome_usuario = usuario["nome"]            
    return nome_usuario

def criar_conta(AGENCIA, lista_contas, lista_usuarios):
    print("##### ABRINDO UMA NOVA CONTA #####")
    cpf = input("Digite o CPF do titular da conta: ")
    nome_titular = verifica_usuario(cpf, lista_usuarios)
    if nome_titular :
        numero_conta = len(lista_contas) + 1
        lista_contas.append({
            "agencia": AGENCIA,
            "numero_conta": numero_conta,
            "cpf_titular": cpf,
            "saldo": 0,
            "saques_feitos": 0
        })
        print("\n### Conta criada!")
        print(f"### Agência: {AGENCIA}, Titular: {nome_titular}, Número da conta: {numero_conta}")
    else :
        mensagem_erro("Este usuáro não existe no sistema!")

def verifica_conta(numero_conta, lista_contas):    
    conta_encontrada = False
    for conta in lista_contas:
        #print(f"Agência: {conta["agencia"]} \t Número da conta: {conta["numero_conta"]} \t CPF do titular: {conta["cpf_titular"]} \t Saldo: {conta["saldo"]}")
        if int(conta["numero_conta"]) == int(numero_conta) :            
            conta_encontrada = conta            
    return conta_encontrada

def seleciona_conta(numero_conta, lista_contas, lista_usuarios):
    conta = verifica_conta(numero_conta, lista_contas)
    if conta:
        nome_titular = verifica_usuario(conta["cpf_titular"], lista_usuarios)
        opcao = input(f"\n\tO titular da Conta Selecionada é {nome_titular}.\n\tConfirma? (s/n)")

        if opcao == 's':                   
            return conta
        else: 
            mensagem_erro("Operação Cancelada!")     
            return False
    else:
        mensagem_erro("Conta não encontrada")
        return False

def depositar(saldo, valor, extrato, numero_conta, /):
    if verifica_valor(valor):
        valor = float(valor)
        saldo += valor
        agora = datetime.now().strftime("%H:%M:%S")
        texto = f"{agora}\tD\tR$ {valor:.2f}"
        extrato.append([numero_conta,texto])
    else:
        mensagem_erro()
    return saldo

def sacar(*,conta, saldo, valor, extrato, limite_saque, numero_saques_feitos, limite_saques_diarios):

    if verifica_valor(valor):
        valor = float(valor)
        if valor > float(saldo) :
            mensagem_erro("Você não tem sado suficiente. Tente novamente.")
        elif numero_saques_feitos >= limite_saques_diarios :
            mensagem_erro("Limite diário de Saques atingido.")
        elif valor > limite_saque :
            mensagem_erro(f"O limite máximo para saques é de R$ {limite_saque:.2f}")
        else:
            saldo -= valor
            conta["saldo"] = saldo
            agora = datetime.now().strftime("%H:%M:%S")
            texto = f"{agora}\tS\tR$ {valor:.2f}"
            extrato.append([conta["numero_conta"],texto])
            numero_saques_feitos += 1
            conta["saques_feitos"] = numero_saques_feitos
    else:
        mensagem_erro()

    return saldo

def listar_usuarios(lista_usuarios, lista_contas):    
    if len(lista_usuarios) <= 0:
        print("Não há usuários no Sistema Ainda.")
        return
    
    print("##### Lista de Usuários do Sistema #####")
    for usuario in lista_usuarios:
        print("____________")
        print(f"CPF: {usuario["cpf"]}, Nome: {usuario["nome"]},  Data de Nascimento: {usuario["data_nascimento"]}, Endereço: {usuario["endereco"]}")    
        conta_aberta = 0
        for conta in lista_contas:
            if conta["cpf_titular"] == usuario["cpf"]:
                conta_aberta = 1
                print(f"\tConta: {conta["numero_conta"]}, Agência: {conta["agencia"]}, Saldo: {conta["saldo"]}")
        if conta_aberta == 0:
            print("\tExte usuário não tem nenhuma conta aberta ainda.")

def imprimir_extrato(saldo, /, *, extrato, numero_conta):
    print(" EXTRATO ".center(36,"#"))    
    if len(extrato) > 0 :
        for item in extrato:
            if item[0] == numero_conta:                
                print(item[1])
        print(f"\nSaldo:\t R$ {saldo}")

    else:
        mensagem_erro("Não há moviimentações na sua conta ainda.")


main()