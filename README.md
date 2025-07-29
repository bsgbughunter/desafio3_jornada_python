Sistema Bancário em Python (Desafio DIO Santander)

Este projeto é um sistema bancário simples desenvolvido em Python, utilizando conceitos de programação orientada a objetos (POO). Ele simula operações básicas de banco como criação de clientes, abertura de contas, depósitos, saques e consulta de extrato.

Funcionalidades
Cadastro de clientes (Pessoa Física) com dados pessoais e endereço.

Criação de contas correntes associadas a clientes.

Depósito e saque com validações de saldo, limite e número máximo de saques.

Histórico de transações para cada conta.

Exibição de extrato bancário com o detalhamento dos depósitos e saques realizados.

Listagem das contas cadastradas no sistema.

Estrutura do Projeto
Cliente e PessoaFisica: classes que representam os clientes do banco.

Conta, ContaCorrente: classes que representam as contas bancárias.

Transacao, Deposito e Saque: classes abstratas e concretas para as operações financeiras.

Historico: mantém o registro das transações feitas na conta.

Funções de interação com o usuário para realizar operações via menu de texto.

Regras e Restrições
Cada cliente pode ter várias contas.

Limite padrão de saque por operação: R$ 500,00.

Número máximo de saques por conta corrente: 3 saques.

O sistema valida se o cliente existe antes de realizar operações.

Saques não podem exceder o saldo disponível.

Depósitos e saques só aceitam valores positivos.

Como usar
Execute o script Python.

Utilize o menu para:

Criar novos clientes.

Abrir contas para clientes existentes.

Realizar depósitos e saques.

Consultar extratos.

Listar todas as contas do banco.

Para sair, escolha a opção 7.

Tecnologias
Python 3.x

Programação Orientada a Objetos

Biblioteca padrão (datetime, abc, textwrap)


Autor
Beatriz Soares
