from datetime import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

def mensagem_erro(texto="Você deve digitar um valor válido!"):    
    print("\n")
    print(f"#".center(len(texto)+8,"#"))
    print(f"#", texto.center(len(texto)+4), "#")
    print(f"#".center(len(texto)+8,"#"))


def verifica_valor(quantia):    
    if isinstance(quantia,float) :       
        if quantia > 0:
            return True
        else:
            return False
    else:
        return False
    

def depositar(quantia):
    if verifica_valor(quantia):       
            global saldo
            saldo += quantia
            agora = datetime.now().strftime("%H:%M:%S")
            texto = f"{agora}\tD\tR$ {quantia:.2f}"
            extrato.append(texto) 
    else:
        mensagem_erro()

def sacar(quantia):
    global limite
    global numero_saques
    global saldo
    if verifica_valor(quantia):
            if ( quantia > saldo ):
                mensagem_erro("Você não tem sado suficiente. Tente novamente.")
            elif ( numero_saques >= LIMITE_SAQUES ):
                mensagem_erro("Limite diário de Saques atingido.")
            elif ( quantia > limite ):
                mensagem_erro(f"O limite máximo para saques é de R$ {limite}")
            else:
                saldo -= quantia
                agora = datetime.now().strftime("%H:%M:%S")
                texto = f"{agora}\tS\tR$ {quantia:.2f}"
                extrato.append(texto)
                numero_saques += 1
    else:
        mensagem_erro()


def exibir_extrato():
    print(" EXTRATO ".center(36,"#"))
    if (len(extrato) > 0):
        for item in extrato:
            print(item)
        print(f"\nSaldo:\t R$ {saldo}")
    else:
        mensagem_erro("Não há moviimentações na sua conta ainda.")




while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        depositar(valor)
        

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        sacar(valor)

    elif opcao == "e":
        exibir_extrato()

    elif opcao == "q":
        break

    else:
        mensagem_erro("Operação inválida, por favor selecione novamente a operação desejada.")
