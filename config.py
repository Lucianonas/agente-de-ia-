# config.py
# ================================================
# PAINEL DE CONTROLE CENTRAL DO JARVIS
# ================================================
# Todo módulo que precisar de uma configuração
# importa daqui. Nunca fica espalhado pelo código.
# ================================================

# os: acessa o sistema operacional
import os

# Path: forma moderna de trabalhar com caminhos
# Funciona igual no Windows, Linux e Mac
from pathlib import Path

# load_dotenv: lê o .env e carrega as variáveis no Python
from dotenv import load_dotenv

# BaseSettings: lê configs automaticamente do .env
from pydantic_settings import BaseSettings

# Field: define valor padrão de cada variável
from pydantic import Field

# Optional: a variável pode ser None (não obrigatória)
from typing import Optional

# -----------------------------------------------
# Carrega o arquivo .env para dentro do Python
# A partir daqui os.getenv('QUALQUER_CHAVE') funciona
# -----------------------------------------------
load_dotenv()

# Caminho absoluto da raiz do projeto
# __file__ = caminho deste arquivo (config.py)
# .parent  = a pasta que contém este arquivo
BASE_DIR = Path(__file__).parent


# -----------------------------------------------
# CLASSE DE CONFIGURAÇÕES
# -----------------------------------------------
class Settings(BaseSettings):
    """
    Configurações centrais do JARVIS.

    A mágica do BaseSettings:
    Você declara  → jarvis_name: str = 'JARVIS'
    Pydantic lê   → variável JARVIS_NAME do .env
    Se não achar  → usa o valor padrão 'JARVIS'
    """

    # -----------------------------------------------
    # IDENTIDADE
    # -----------------------------------------------

    # Nome do assistente (lido de JARVIS_NAME no .env)
    jarvis_name: str = Field(default='JARVIS')

    # Versão atual do sistema
    jarvis_version: str = Field(default='1.0.0')

    # Idioma das respostas
    jarvis_language: str = Field(default='pt-BR')

    # Modo debug — mostra mais informações no terminal
    jarvis_debug: bool = Field(default=False)

    # -----------------------------------------------
    # APIs DE IA — todas opcionais (Optional = pode ser None)
    # -----------------------------------------------

    # Chave da OpenAI (GPT-4)
    openai_api_key: Optional[str] = Field(default=None)
    openai_model_default: str = Field(default='gpt-4o-mini')

    # Chave da Anthropic (Claude)
    anthropic_api_key: Optional[str] = Field(default=None)
    anthropic_model_default: str = Field(default='claude-3-haiku-20240307')

    # Chave do Google (Gemini)
    google_api_key: Optional[str] = Field(default=None)
    gemini_model_default: str = Field(default='gemini-1.5-flash')

    # Chave do ElevenLabs (voz realista)
    elevenlabs_api_key: Optional[str] = Field(default=None)
    elevenlabs_voice_id: Optional[str] = Field(default=None)

    # -----------------------------------------------
    # OLLAMA — IA local sem internet
    # -----------------------------------------------

    # Endereço do servidor Ollama na sua máquina
    ollama_base_url: str = Field(default='http://localhost:11434')
    ollama_model_default: str = Field(default='llama3.2')

    # -----------------------------------------------
    # BANCO DE DADOS
    # -----------------------------------------------

    database_url: str = Field(default='sqlite:///./database/jarvis.db')
    redis_url: str = Field(default='redis://localhost:6379/0')
    chroma_db_path: str = Field(default='./database/chroma_db')

    # -----------------------------------------------
    # SERVIDOR
    # -----------------------------------------------

    api_host: str = Field(default='0.0.0.0')
    api_port: int = Field(default=8000)
    secret_key: str = Field(default='troque-em-producao')

    # -----------------------------------------------
    # VOZ
    # -----------------------------------------------

    wake_word: str = Field(default='jarvis')
    tts_engine: str = Field(default='pyttsx3')
    stt_engine: str = Field(default='whisper')
    whisper_model_size: str = Field(default='base')

    # -----------------------------------------------
    # SEGURANÇA
    # -----------------------------------------------

    sandbox_enabled: bool = Field(default=True)

    # -----------------------------------------------
    # PROPRIEDADES CALCULADAS
    # @property = transforma método em variável
    # Uso: settings.is_openai_available (sem parênteses!)
    # -----------------------------------------------

    @property
    def is_openai_available(self) -> bool:
        # Verifica se a chave existe E tem tamanho mínimo válido
        return self.openai_api_key is not None and len(self.openai_api_key) > 10

    @property
    def is_anthropic_available(self) -> bool:
        # Mesma verificação para o Claude
        return self.anthropic_api_key is not None and len(self.anthropic_api_key) > 10

    @property
    def is_elevenlabs_available(self) -> bool:
        # ElevenLabs precisa de chave E id da voz
        return (
            self.elevenlabs_api_key is not None
            and len(self.elevenlabs_api_key) > 10
            and self.elevenlabs_voice_id is not None
        )

    @property
    def base_dir(self) -> Path:
        # Retorna o caminho raiz do projeto
        return BASE_DIR

    class Config:
        # Lê variáveis do arquivo .env
        env_file = '.env'

        # Ignora maiúsculas: JARVIS_NAME = jarvis_name
        case_sensitive = False

        # Variável extra no .env que não declaramos? Ignora.
        extra = 'ignore'


# -----------------------------------------------
# CRIA PASTAS NECESSÁRIAS
# -----------------------------------------------
def ensure_directories():
    """
    Garante que as pastas essenciais existem.
    parents=True  → cria subpastas também
    exist_ok=True → não dá erro se já existir
    """
    paths_needed = [
        BASE_DIR / 'logs',           # Pasta de logs
        BASE_DIR / 'database',       # Banco de dados
        BASE_DIR / 'database' / 'chroma_db',  # Memória vetorial
        BASE_DIR / 'temp',           # Arquivos temporários
        BASE_DIR / 'temp' / 'uploads',  # Uploads temporários
    ]

    for path in paths_needed:
        # Cria a pasta se não existir
        path.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------
# SINGLETON — Uma única instância pra todo projeto
# -----------------------------------------------
# Qualquer arquivo faz: from config import settings
# E usa: settings.jarvis_name → 'JARVIS'
settings = Settings()

# Garante que as pastas existem ao importar config.py
ensure_directories()


# -----------------------------------------------
# TESTE VISUAL — só roda com: python config.py
# -----------------------------------------------
if __name__ == '__main__':
    # Rich: deixa o terminal bonito com cores
    from rich.console import Console
    from rich.table import Table

    console = Console()

    # Cria uma tabela colorida no terminal
    table = Table(title='⚙️  Configurações do JARVIS')
    table.add_column('Chave', style='cyan')
    table.add_column('Valor', style='green')

    # Adiciona cada configuração na tabela
    table.add_row('Nome', settings.jarvis_name)
    table.add_row('Versão', settings.jarvis_version)
    table.add_row('Idioma', settings.jarvis_language)
    table.add_row('Debug', str(settings.jarvis_debug))
    table.add_row('OpenAI', '✅ OK' if settings.is_openai_available else '❌ não configurado')
    table.add_row('Anthropic', '✅ OK' if settings.is_anthropic_available else '❌ não configurado')
    table.add_row('ElevenLabs', '✅ OK' if settings.is_elevenlabs_available else '❌ não configurado')
    table.add_row('Servidor', f'{settings.api_host}:{settings.api_port}')
    table.add_row('Voz', settings.tts_engine)
    table.add_row('Wake word', settings.wake_word)

    console.print(table)