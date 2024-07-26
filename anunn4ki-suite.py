import random
import socket
import threading
import time
from colorama import Fore, Style, init

print(f"\n\n{Fore.YELLOW}                                           _L/L")
print(f"                                         _LT/l_L_")
print(f"                          {Fore.GREEN}Anunn4ki{Style.RESET_ALL}{Fore.YELLOW}     _LLl/L_T_lL_")
print(f"                   _T/L   {Fore.GREEN}Suite 0.2{Style.RESET_ALL}{Fore.YELLOW}  _LT|L/_|__L_|_L_")
print(f"                 _Ll/l_L_          _TL|_T/_L_|__T__|_l_")
print(f"               _TLl/T_l|_L_      _LL|_Tl/_|__l___L__L_|L_")
print(f"             _LT_L/L_|_L_l_L_  _'|_|_|T/_L_l__T _ l__|__|L_")
print(f"           _Tl_L|/_|__|_|__T _LlT_|_Ll/_l_ _|__[ ]__|__|_l_L_")
print(f"    ______LT_l_l/|__|__l_T _T_L|_|_|l/___|__ | _l__|_ |__|_T_L_____{Style.RESET_ALL}")

# Inicializa o colorama
init()

# Cria um lock para sincronizar as impressões
print_lock = threading.Lock()

# Faixas de IPs públicos conhecidos
faixas_ip_publicos = [
    (1, 126, 0, 0, 0, 255),   # Classe A: 1.0.0.0 - 126.255.255.255
    (128, 191, 0, 0, 0, 255), # Classe B: 128.0.0.0 - 191.255.255.255
    (192, 223, 0, 0, 0, 255), # Classe C: 192.0.0.0 - 223.255.255.255
]

def gerar_ip_aleatorio():
    """Gera um endereço IP aleatório dentro de faixas de IPs públicos conhecidos."""
    faixa = random.choice(faixas_ip_publicos)
    return f"{random.randint(faixa[0], faixa[1])}.{random.randint(faixa[2], faixa[3])}.{random.randint(faixa[4], faixa[5])}.{random.randint(0, 255)}"

def testar_porta(ip, porta):
    """Testa se a porta está aberta no IP fornecido."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, porta))
            return True
    except (socket.timeout, socket.error):
        return False

def obter_banner(ip, porta):
    """Obtém o banner de um serviço na porta fornecida."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, porta))
            s.send(b'HEAD / HTTP/1.0\r\n\r\n')  # Envia uma requisição HTTP simples
            banner = s.recv(4096).decode()  # Recebe e decodifica o banner
            return banner
    except (socket.timeout, socket.error):
        return None

def verificar_servico(ip, porta, servico, versao=None):
    """Verifica se um serviço específico está rodando na porta fornecida, com ou sem versão."""
    banner = obter_banner(ip, porta)
    if banner:
        banner_upper = banner.upper()
        servico_upper = servico.upper()

        # Verifica se o serviço está presente no banner com uma correspondência parcial
        if servico_upper in banner_upper:
            if versao:
                versao_upper = versao.upper()
                # Verifica se a versão fornecida está presente no banner
                if versao_upper in banner_upper:
                    return True, banner
            else:
                return True, banner
    return False, banner

def tarefa_por_porta(ip, porta, resultados):
    """Executa a tarefa de testar portas em um IP e obtém o banner se a porta estiver aberta."""
    if testar_porta(ip, porta):
        with print_lock:
            print(f"{Fore.GREEN}Porta {porta} está aberta em {ip}.{Style.RESET_ALL}")
        banner = obter_banner(ip, porta)
        if banner:
            with print_lock:
                print(f"{Fore.YELLOW}Banner: {banner}{Style.RESET_ALL}")
        else:
            with print_lock:
                print(f"{Fore.YELLOW}Banner não obtido.{Style.RESET_ALL}")
        resultados.append((ip, banner))
    else:
        with print_lock:
            print(f"{Fore.RED}Porta {porta} NÃO está aberta em {ip}.{Style.RESET_ALL}")

def tarefa_por_servico(ip, porta, servico, versao, resultados):
    """Executa a tarefa de testar serviços em um IP e coleta o banner se o serviço e a versão estiverem presentes."""
    if testar_porta(ip, porta):
        with print_lock:
            print(f"{Fore.GREEN}Porta {porta} está aberta em {ip}.{Style.RESET_ALL}")
        encontrado, banner = verificar_servico(ip, porta, servico, versao)
        if encontrado:
            with print_lock:
                print(f"{Fore.BLUE}O serviço {servico} com versão {versao} está rodando na porta {porta} em {ip}.{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Banner: {banner}{Style.RESET_ALL}")
            resultados.append((ip, banner))
            return True
        else:
            with print_lock:
                print(f"{Fore.RED}O serviço {servico} com versão {versao} NÃO está rodando na porta {porta} em {ip}.{Style.RESET_ALL}")
                if banner:
                    print(f"{Fore.YELLOW}Banner: {banner}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Banner não obtido.{Style.RESET_ALL}")
    else:
        with print_lock:
            print(f"{Fore.RED}Porta {porta} NÃO está aberta em {ip}.{Style.RESET_ALL}")
    return False

def main():
    print("\n\nEscolha uma opção:")
    print("\n1 - Buscar apenas portas abertas")
    print("2 - Buscar serviços e suas versões")

    opcao = input("\nDigite o número da opção escolhida: ")

    if opcao == "1":
        porta = int(input("Porta: "))
        numero_de_ips = int(input("Digite o número de IPs: "))

        resultados = []

        start_time = time.time()  # Início do tempo

        def buscar_por_porta():
            while len(resultados) < numero_de_ips:
                ip = gerar_ip_aleatorio()
                tarefa_por_porta(ip, porta, resultados)

        # Cria e inicia múltiplas threads para buscar portas
        threads = [threading.Thread(target=buscar_por_porta) for _ in range(20)]  # Ajuste o número de threads conforme necessário
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        end_time = time.time()  # Fim do tempo
        elapsed_time = end_time - start_time

        # Imprime a lista final com os IPs com a porta aberta
        print(f"\n{Fore.CYAN}Lista de IPs com a porta {porta} aberta:{Style.RESET_ALL}")
        if resultados:
            for ip, banner in resultados:
                if banner:
                    print(f"IP: {ip} - {Fore.YELLOW}Banner: {banner}{Style.RESET_ALL}")
                else:
                    print(f"IP: {ip} - {Fore.YELLOW}Banner não obtido.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Nenhum IP encontrou a porta {porta} aberta.{Style.RESET_ALL}")

        print(f"{Fore.CYAN}Tempo total para encontrar IPs: {elapsed_time:.2f} segundos.{Style.RESET_ALL}")

    elif opcao == "2":
        servico = input("Digite o serviço a ser verificado (por exemplo, 'apache'): ")
        versao = input("Digite a versão do serviço (opcional, deixe em branco se não souber): ")
        porta = int(input("Digite o número da porta: "))
        numero_de_ips = int(input("Quantos IPs capturar: "))

        resultados = []
        encontrado = 0

        start_time = time.time()  # Início do tempo

        def buscar_por_servico():
            nonlocal encontrado
            while encontrado < numero_de_ips:
                ip = gerar_ip_aleatorio()
                if tarefa_por_servico(ip, porta, servico, versao, resultados):
                    encontrado += 1

        # Cria e inicia múltiplas threads para buscar o serviço
        threads = [threading.Thread(target=buscar_por_servico) for _ in range(20)]  # Ajuste o número de threads conforme necessário
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        end_time = time.time()  # Fim do tempo
        elapsed_time = end_time - start_time

        # Imprime a lista final com os IPs e seus banners
        print(f"\n{Fore.CYAN}Lista de IPs com o serviço {servico} e seus banners:{Style.RESET_ALL}\n")
        if resultados:
            for ip, banner in resultados:
                print(f"IP: {ip} - {Fore.GREEN}Banner: {banner}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Nenhum IP encontrou o serviço {servico} com a versão {versao}.{Style.RESET_ALL}")

        print(f"{Fore.CYAN}Tempo total para encontrar IPs: {elapsed_time:.2f} segundos.{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}Opção inválida.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
