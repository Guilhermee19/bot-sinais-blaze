import os
from dotenv import load_dotenv

load_dotenv()

# Configurações Gerais
token_telegram = os.getenv("TOKEN_TELEGRAM")
chat_id = os.getenv("CHAT_ID")
notificacoes_ativas = True

# Mensagens de status
msg_ativo = "✅ Bot Ativo"
aviso_falso = "🚫 Alarme falso \nAguardando novo padrão."
sinal_gale = "📢 GALE - Duplicar aposta repetindo a entrada."
proteger_branco_10 = "⚪ Lembrar de proteger patrimônio com 10% no Branco.⚪"
msg_encerrado = "❌ Bot Encerrado"

# Variáveis configuráveis pelo usuário
banca = 140.08  # Banca inicial em reais
banca_inicial = 140.08  # Armazena o valor inicial da banca para cálculo de vitórias e derrotas
aposta_inicial = 2
protecao_inicial = aposta_inicial * 0.10
aposta_gale = 2 * aposta_inicial
protecao_gale = protecao_inicial * 2  # Valor da aposta inicial
sequencia_para_entrada = 5 # Configuração inicial: N cores iguais para entrada

# Controle de Resultados
vitorias = 8
perdas = 0
protegido = 0

# Variáveis globais para controle
historico_cores = []
fazendo_gale = True
ultima_lista = []  # Armazena a última lista capturada
alertado = False
entrada_realizada = False  # Controla se a entrada foi realizada
aguardando_resultado = False  # Variável para aguardar o próximo giro após entrada
resetar_entrada = False  # Variável para resetar padrão após conclusão de Gale
cor_da_entrada = None  # Armazena a cor da entrada para verificar vitória
contador_atualizado = False  # Garante que vitória ou derrota seja contabilizada apenas uma vez
em_pausa = False
vitorias_consecutivas = 0