# main.py
# ================================================
# PONTO DE ENTRADA PRINCIPAL DO JARVIS
# ================================================
# Como rodar:
#   python main.py         ← modo interativo
#   python main.py --api   ← inicia servidor API
#   python main.py --debug ← ativa modo debug
# ================================================

# sys: encerra o programa e verifica versão do Python
import sys

# os: limpa o terminal (cls Windows, clear Linux)
import os

# asyncio: permite rodar código assíncrono
# Assíncrono = várias coisas ao mesmo tempo sem travar
# Como um garçom que anota vários pedidos antes de ir à cozinha
import asyncio

# click: cria interface de linha de comando elegante
# Sem ele você teria que ler sys.argv manualmente
import click

# rich: deixa o terminal bonito com cores
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Importa as configurações centrais do projeto
from config import settings

# Instância do console Rich para prints coloridos
console = Console()

# -----------------------------------------------
# BANNER ASCII — Arte exibida ao ligar o JARVIS
# {version} será substituído pela versão real
# -----------------------------------------------
BANNER = """
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝

     Just A Rather Very Intelligent System
              v{version}
"""


def show_banner():
    """Limpa o terminal e exibe o banner do JARVIS."""

    # 'nt' = Windows | qualquer outra coisa = Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

    # Exibe o banner dentro de um painel azul centralizado
    console.print(
        Panel(
            Align.center(
                # Formata o banner com a versão real e cor ciano
                Text(BANNER.format(version=settings.jarvis_version),
                     style='bold cyan')
            ),
            border_style='blue'
        )
    )


async def check_system():
    """
    Verifica o que está disponível antes de ligar tudo.
    Melhor saber agora do que travar no meio de uma conversa.
    """

    console.print('[bold blue]🔍 Verificando sistema...[/bold blue]\n')

    # Lista de verificações: (nome, resultado, é crítico?)
    # crítico = sem isso o JARVIS não funciona de jeito nenhum
    checks = [
        ('Python 3.10+', sys.version_info >= (3, 10), True),
        ('OpenAI API', settings.is_openai_available, False),
        ('Anthropic API', settings.is_anthropic_available, False),
        ('ElevenLabs', settings.is_elevenlabs_available, False),
    ]

    # Percorre cada verificação e exibe o resultado
    for name, passed, critical in checks:
        if passed:
            # Verde = OK
            console.print(f'  [green]✅[/green] {name}')
        elif critical:
            # Vermelho = erro crítico — sem isso não funciona
            console.print(f'  [red]❌[/red] {name} [red](necessário)[/red]')
        else:
            # Amarelo = aviso — opcional, mas recomendado
            console.print(f'  [yellow]⚠️ [/yellow] {name} [dim](opcional)[/dim]')

    console.print()


async def interactive_mode():
    """
    Loop principal de conversa pelo terminal.
    Pede input → processa → responde. Repete até sair.
    Esse é o núcleo de qualquer chatbot.
    """

    console.print(
        Panel(
            '[bold cyan]💬 Modo interativo ativo[/bold cyan]\n'
            '[dim]Digite sua mensagem. Para sair: sair[/dim]',
            border_style='cyan'
        )
    )

    # Loop infinito — fica rodando até o usuário digitar 'sair'
    while True:
        try:
            # Pede input com prompt colorido
            # .strip() remove espaços: '  olá  ' → 'olá'
            user_input = console.input(
                '\n[bold cyan]Você →[/bold cyan] '
            ).strip()

            # Usuário apertou Enter sem digitar nada
            # continue = pula pro próximo ciclo do while
            if not user_input:
                continue

            # Verifica se o usuário quer sair
            if user_input.lower() in ['sair', 'exit', 'quit']:
                console.print('\n[cyan]JARVIS →[/cyan] Até logo.')
                break  # Sai do loop while

            # -----------------------------------------------
            # RESPOSTA DO JARVIS
            # Por enquanto é placeholder.
            # Na Etapa 2 virá: response = await ai_engine.chat(user_input)
            # -----------------------------------------------
            console.print(
                f'[cyan]JARVIS →[/cyan] '
                f'[dim]Processando: "{user_input}"... '
                f'(Motor de IA vem na Etapa 2)[/dim]'
            )

        except KeyboardInterrupt:
            # Ctrl+C capturado — sai sem mensagem de erro feia
            console.print('\n[cyan]JARVIS →[/cyan] Encerrando.')
            break


# -----------------------------------------------
# CLI — Interface de linha de comando
# @click.command() → transforma em comando de terminal
# @click.option()  → adiciona opções como --debug
# -----------------------------------------------
@click.command()
@click.option('--api', is_flag=True, help='Inicia o servidor de API')
@click.option('--debug', is_flag=True, help='Ativa modo debug')
def cli(api: bool, debug: bool):
    """JARVIS AI — Assistente de Inteligência Artificial"""

    if debug:
        # Sobrescreve a config do .env em tempo real
        os.environ['JARVIS_DEBUG'] = 'true'
        console.print('[yellow]⚡ Modo debug ativado[/yellow]')

    # asyncio.run() = ponte entre código normal e assíncrono
    # É como apertar o botão de ligar que inicia tudo
    asyncio.run(main(api=api))


async def main(api: bool = False):
    """Orquestra a inicialização completa do JARVIS."""

    # Exibe o banner no terminal
    show_banner()

    # Verifica o sistema antes de começar
    # 'await' = espera isso terminar antes de continuar
    # Como pedir um café: faz o pedido, espera, depois bebe
    await check_system()

    if api:
        # Servidor API vem na Etapa 9
        console.print('[yellow]🌐 Servidor API vem na Etapa 9.[/yellow]')
    else:
        # Inicia o modo de conversa pelo terminal
        await interactive_mode()


# -----------------------------------------------
# Só executa se você rodar: python main.py
# NÃO executa se outro arquivo fizer: import main
# -----------------------------------------------
if __name__ == '__main__':
    cli()