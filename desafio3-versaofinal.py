import textwrap
from abc import ABC, abstractclassmethod, abstractproperty, abstractmethod
from datetime import datetime

class contasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.nuemro}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("----------------------------")
            print("Operação falhou! Você excedeu o limite de transações permitidas por dia")
            return

        transacao.registra(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nasc = data_nasc
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "1008"
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
        if valor > self.saldo:
            print("Você não tem limite para executar esta operação!")
        elif valor > 0:
            self._saldo -= valor
            print("--------------------------------------")
            print(f"Saque realizado no valor de R${valor:.2f}")
            print("--------------------------------------")
            return True
        else:
            print("----------------------------------------------")
            print("Operação falhou! O valor informado é inválido.")
            print("----------------------------------------------")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("--------------------------------------------")
            print(f"Depósito realizado no valor de R${valor:.2f}")
            print("--------------------------------------------")
            return True
        else:
            print("Valor inválido para depósito.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)


    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self.limite:
            print("---------------------------------------------------")
            print("Operação falhou! O valor informado excede o limite.")
            print("---------------------------------------------------")
        elif numero_saques >= self.limite_saques:
            print("---------------------------------------------------")
            print("Operação falhou! Número máximo de saques excedido.")
            print("---------------------------------------------------")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao['tipo'].lower == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes



class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}:{func.__name__.upper()}")
        return envelope


def menu():
    menu = """
    -------- BEM-VINDO ---------

    [1] - DEPOSITAR
    [2] - SACAR
    [3] - EXTRATO
    [4] - NOVO USUÁRIO
    [5] - CRIAR NOVA CONTA
    [6] - LISTAR CONTAS
    [7] - SAIR

    ----------------------------
      DIGITE A OPÇÃO DESEJADA:

    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return None
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor a ser depositado: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return


    valor = float(input("Informe o valor a ser sacado: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("---------- EXTRATO -------------")
    extrato = " "
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extarto = "Não foram realizadas movimentações nesta conta"

    print(extrato)
    print(f"nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("--------------------------------")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente os números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço completo: ")

    cliente = PessoaFisica(nome=nome, data_nasc=data_nasc, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    print("---------------------------")
    print("Cliente criado com sucesso!")
    print("---------------------------")

@log_transacao
def criar_nova_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF (somente os números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite =500, limite_saques=50)
    contas.append(conta)
    cliente.contas.append(conta)

    print("-------------------------")
    print("Conta criada com sucesso!")
    print("-------------------------")


def listar_contas(contas):
    for conta in contasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_nova_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


main()
