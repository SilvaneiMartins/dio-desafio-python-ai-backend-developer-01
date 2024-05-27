import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExibir Extrato
    [nc]\tCriar nova Conta
    [lc]\tListar Contas
    [nu]\tCriar novo Usuário
    [q]\tSair
    => """

    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
    else:
        print("\n@@@ Operação não pode ser concluído, valor inválido para depósito! @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação não pode ser concluído, saldo insuficiente! @@@")
    elif excedeu_limite:
        print("\n@@@ Operação não pode ser concluído, valor excede o limite de saque! @@@")
    elif excedeu_saques:
        print("\n@@@ Operação não pode ser concluído, limite de saques excedido! @@@")
    elif valor > 0:
        valor -= valor
        extrato += f"Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
    else:
        print("\n@@@ Operação não pode ser concluído, valor inválido para saque! @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ Inicio do Extrato ================")
    print("Não foram realizado movimentações." if not extrato else extrato)
    print(f"\n=== Saldo atual:\tR$ {saldo:.2f} ===")
    print("\n================== Fim do Extrato ==================")


def criar_usuario(usuarios):
    cpf = input("Digite o CPF do usuário (Somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Usuário já cadastrado com o cpf! @@@")
        return

    nome = input("Digite o nome do usuário: ")
    data_nascimento = input(
        "Digite a data de nascimento do usuário (dd-mm-aaaa): ")
    endereco = input(
        "Digite o endereço do usuário (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })

    print("\n=== Usuário cadastrado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário (Somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, criação de conta foi encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência:\t{conta["agencia"]}
        C/C:\t{conta["numero_conta"]}
        Titular:\t{conta["usuario"]["nome"]}
        """
    print("=" * 100)
    print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "s":
            valor = float(input("Digite o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            contas = criar_conta(AGENCIA, numero_conta, usuarios)

            if contas:
                contas.append(contas)
        elif opcao == "lc":
            listar_contas(usuarios)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamete a operação desejada!")


main()
