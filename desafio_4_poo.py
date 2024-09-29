from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento,endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def __str__(self):
        return f"""
        Nome: {self._nome} \t CPF: {self._cpf} \t Data Nasc: {self._data_nascimento}
        Endereço: {self._endereco}
        """

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        valor = float(valor)
        if valor > saldo:
            mensagem_erro("Você não tem saldo suficiente para esta operação.")
            return False
        else:
            self._saldo -= valor
            print("\n === Saque realizado com sucesso! ===")
            return True
        
    def depositar(self, valor):        
        self._saldo += float(valor)
        print("\n === Depósito realizado com sucesso! ===")
        return True
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 5):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):        
        numero_saques = 0
        
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                numero_saques +1

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""        
        \t Ag: {self.agencia} \tC/C: {self.numero} """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self.transacoes

    def adicionar_transacao(self, transacao):
        agora = datetime.now().strftime("%H:%M:%S")
        self._transacoes.append(
            {   
                "data": agora,
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor                
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def menu_inicial():
    texto = """
    ################ SISTEMA BANCÁRIO #################
    [d] Depositar
    [s] Sacar
    [u] Novo Usuário
    [c] Nova Conta  
    [l] Listar Usuários  
    [i] Imprimir Extrato        
    
    [q] Sair

    => """
    opcao = input(texto)
    return opcao

def criar_cliente(clientes):
    print("##### CRIANDO UM NOVO CLIENTE #####")
    cpf = input("Digite o CPF do cliente: ")
    if verifica_cliente(cpf, clientes) :
        mensagem_erro("Usuário já existe no sistema")
        return

    nome = input("Digite o Nome do cliente: ")
    data_nascimento = input("Digite a Data de Nascimento do cliente: ")
    endereco = input("Digite o Endereço do cliente: ")
    cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)

    print(" === Cliente criado com sucesso! ===")        

def verifica_cliente(cpf, clientes):    
    cliente_encontrado = False
    for cliente in clientes :
        if cliente._cpf == cpf :
            cliente_encontrado = cliente
    return cliente_encontrado

def criar_conta(numero_conta, clientes, contas):
    print("##### ABRINDO UMA NOVA CONTA #####")
    cpf = input("Digite o CPF do titular da conta: ")
    cliente = verifica_cliente(cpf, clientes)
    if cliente :        
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
        contas.append(conta)
        cliente._contas.append(conta)
        print("\n### Conta criada!")
    else :
        mensagem_erro("Este usuáro não existe no sistema!")

def verifica_conta(numero_conta, contas):    
    conta_encontrada = False
    for conta in contas:
        #print(f"Agência: {conta["agencia"]} \t Número da conta: {conta["numero_conta"]} \t CPF do titular: {conta["cpf_titular"]} \t Saldo: {conta["saldo"]}")
        if int(conta._numero == int(numero_conta)) :            
            conta_encontrada = conta
    return conta_encontrada

def seleciona_conta(numero_conta, contas):
    conta = verifica_conta(numero_conta, contas)
    if conta:        
        nome_cliente = conta._cliente._nome        
        opcao = input(f"\n\tO titular da Conta Selecionada é {nome_cliente}.\n\tConfirma? (s/n)")

        if opcao == 's':                   
            return conta
        else: 
            mensagem_erro("Operação Cancelada!")     
            return False
    else:
        mensagem_erro("Conta não encontrada")
        return False

def efetuar_transacao(tipo, contas):
    numero_conta = input("Digite o número da conta: ")
    conta = seleciona_conta(numero_conta, contas)
    if not conta:
        return False
    
    valor = input("Digite o valor da operação: ")
    if not verifica_valor(valor):
        mensagem_erro()
        return False
    
    valor = float(valor)
    
    if tipo == 'd':        
        transacao = Deposito(valor)        

    if tipo == 's':
        transacao = Saque(valor)

    conta._cliente.realizar_transacao(conta, transacao)

def listar_clientes(clientes, contas):
    for cliente in clientes:
        print(textwrap.dedent(str(cliente)))
        num_contas = 0
        for conta in contas:
            if conta._cliente == cliente:
                print(str(conta))
                num_contas += 1
        
        if num_contas == 0:
            print("\t !!! Cliente não tem contas cadastradas !!!")

def imprimir_extrato(contas):
    numero_conta = input("Digite o número da conta: ")
    conta = seleciona_conta(numero_conta, contas)
    if not conta:
        return False
    
    print(f"=== EXTRATO PARA A CONTA Nº {conta._numero}")
    transacoes = conta.historico.transacoes
    extrato = ""

    if not transacoes:
        mensagem_erro("Não foram feitas movimentações para a conta")
        return False
    
    for transacao in transacoes:
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: \t\t R$ {conta.saldo:.2f}")
    

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

def main():
    clientes = []
    contas = []
    conta_selecionada = 0
    num_conta = 0

    while True:
        opcao = menu_inicial()

        if opcao == "d":
            efetuar_transacao('d', contas)

        elif opcao == "s":
            efetuar_transacao('s', contas)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)    
        
        elif opcao == "l":
            listar_clientes(clientes, contas)

        elif opcao == "i":
            imprimir_extrato(contas)

        elif opcao == "q":
            break

        else:
            mensagem_erro("Operação inválida, por favor digite novamente.")


main()