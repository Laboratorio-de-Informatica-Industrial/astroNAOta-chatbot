# -*- coding: utf-8 -*-
import google.generativeai as genai
import os
import logging
import json
import pyaudio
import threading
import time
from vosk import Model, KaldiRecognizer
from flask import Flask, jsonify

# --- Configuração de Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')

# --- Configuração da API do Gemini ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai_configured_successfully = False
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        logging.info("API Key do Google configurada.")
        genai_configured_successfully = True
    except Exception as e:
        logging.critical(f"Erro CRÍTICO ao configurar a API Key do Google: {e}")
else:
    logging.warning("Variável de ambiente GOOGLE_API_KEY não definida.")

# --- Persona e Modelo Gemini ---
PERSONA_ASTRO_INFANTIL_GEMINI = """
Você é o AstroNAOta, um robô guia espacial super divertido, amigável e muito inteligente!
Sua missão é explicar astronomia para crianças de aproximadamente 6 a 10 anos.
Responda sempre de forma clara, com frases curtas (idealmente 2-3 frases, no máximo 4) e muito entusiasmo. Use analogias simples que crianças entendam.
Mantenha um tom positivo e encorajador. Evite temas que possam ser assustadores e nunca invente informações.
Seja preciso, mas sempre de um jeito leve e divertido!
IMPORTANTE: Não use emojis ou caracteres especiais em suas respostas, apenas texto simples.
Suas respostas devem ter no máximo 2-3 frases para serem fáceis de acompanhar.

Aqui estão alguns exemplos de como você fala e responde:
Usuário: O que é o Sol?
AstroNAOta: Oi! O Sol é nossa estrela mais próxima! Uma bola gigante de gás super quente que nos dá luz e calor para brincar e para as plantinhas crescerem!
Usuário: Por que a Lua parece mudar de forma?
AstroNAOta: Que pergunta legal! A Lua não muda de verdade, nós só vemos partes diferentes dela iluminadas pelo Sol enquanto ela dança ao redor da Terra! Às vezes é um sorrisão, outras vezes uma bolona!
"""
model_gemini = None
if genai_configured_successfully:
    try:
        model_gemini = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
        logging.info(f"Modelo Gemini '{model_gemini.model_name}' carregado.")
    except Exception as e:
        logging.error(f"Erro ao carregar o modelo Gemini: {e}")
        model_gemini = None

# --- Configuração do Vosk ---
VOSK_MODEL_PATH = "../vosk-model-pt-fb-v0.1.1-20220516_2113" # <<< AJUSTE ESTE CAMINHO SE NECESSÁRIO
SAMPLE_RATE = 16000
CHUNK_SIZE = 4096
vosk_model_obj = None
if os.path.exists(VOSK_MODEL_PATH) and os.path.isdir(VOSK_MODEL_PATH):
    try:
        logging.info("Carregando modelo Vosk...")
        vosk_model_obj = Model(VOSK_MODEL_PATH)
        logging.info("Modelo Vosk principal carregado com sucesso.")
    except Exception as e:
        logging.critical(f"Falha CRÍTICA ao carregar modelo Vosk: {e}")
        vosk_model_obj = None
else:
    logging.critical(f"ERRO CRÍTICO: Caminho para o modelo Vosk NÃO encontrado: '{VOSK_MODEL_PATH}'")

# --- Variáveis de Estado Globais e Lock ---
resposta_pronta_para_nao = ""
lock_resposta = threading.Lock()
chat_gemini_session = None

# --- API Flask ---
app = Flask(__name__)
@app.route('/get_robot_response', methods=['GET'])
def get_robot_speech():
    global resposta_pronta_para_nao
    with lock_resposta:
        if resposta_pronta_para_nao:
            resposta_para_enviar = resposta_pronta_para_nao
            resposta_pronta_para_nao = ""
            logging.info(f"FLASK: Enviando para NAO falar: '{resposta_para_enviar[:70]}...'")
            return jsonify({"status": "new_response", "speech": resposta_para_enviar})
        else:
            return jsonify({"status": "no_new_response", "speech": ""})

# --- Funções de IA (Vosk e Gemini) ---
def iniciar_sessao_chat():
    global chat_gemini_session
    with lock_resposta:
        if chat_gemini_session is None and model_gemini:
            try:
                logging.info("Iniciando NOVA sessão de chat com o Gemini...")
                chat_gemini_session = model_gemini.start_chat(history=[
                    {"role": "user", "parts": [{"text": PERSONA_ASTRO_INFANTIL_GEMINI}]},
                    {"role": "model", "parts": [{"text": "Entendido! Sou o AstroNAOta e estou pronto para uma aventura espacial!"}]}
                ])
                logging.info("Sessão de chat pronta.")
            except Exception as e:
                logging.error(f"Falha ao iniciar sessão de chat com Gemini: {e}")
                chat_gemini_session = None
    return chat_gemini_session

def obter_resposta_do_astro(prompt_usuario):
    global chat_gemini_session
    if not chat_gemini_session:
        iniciar_sessao_chat()
        if not chat_gemini_session:
            return "Ops! Não consegui me conectar à minha central de inteligência."
    try:
        logging.info(f"Enviando para Gemini: '{prompt_usuario}'")
        response = chat_gemini_session.send_message(prompt_usuario)
        resposta_texto = "".join(part.text for part in response.parts if hasattr(part, 'text'))
        if not resposta_texto:
             logging.warning(f"Resposta do Gemini vazia. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'N/A'}")
             return "Hum, não consegui formular uma resposta para isso. Podemos tentar outro assunto?"
        return resposta_texto
    except Exception as e:
        logging.error(f"Erro ao chamar a API Gemini: {e}")
        with lock_resposta:
            chat_gemini_session = None
        return "Ops! Meus circuitos espaciais tiveram uma interferência. Tente de novo!"

def ouvir_pergunta_e_processar():
    """
    Função que ouve UMA pergunta com o Vosk, a processa com o Gemini e prepara a resposta.
    """
    global resposta_pronta_para_nao
    
    if not vosk_model_obj:
        logging.error("Modelo Vosk não está carregado. Não posso ouvir.")
        return

    p_audio = pyaudio.PyAudio()
    stream = None
    recognized_text = None
    
    try:
        stream = p_audio.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                              input=True, frames_per_buffer=CHUNK_SIZE)
        
        print("\n... Microfone ATIVADO. Pode falar sua pergunta agora ...")
        
        vosk_recognizer = KaldiRecognizer(vosk_model_obj, SAMPLE_RATE)
        vosk_recognizer.SetWords(False)

        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            if vosk_recognizer.AcceptWaveform(data):
                result_dict = json.loads(vosk_recognizer.Result())
                text = result_dict.get("text", "").strip()
                if text:
                    recognized_text = text
                    break
        
        print(f"... Microfone DESATIVADO. Processando: '{recognized_text}'")

        if recognized_text and len(recognized_text) > 3 and recognized_text not in ["<unk>", "unk"]:
            if model_gemini and genai_configured_successfully:
                resposta_llm = obter_resposta_do_astro(recognized_text)
            else:
                resposta_llm = "Não estou conectado à minha central de inteligência para responder agora."
            
            with lock_resposta:
                resposta_pronta_para_nao = resposta_llm
            logging.info("Resposta pronta para o NAO.")
        else:
            if recognized_text:
                logging.info(f"Vosk ignorou transcrição curta/inválida: '{recognized_text}'")
            print("Não consegui entender a pergunta. Tente de novo.")

    except Exception as e:
        logging.error(f"Erro durante a escuta com Vosk: {e}")
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        p_audio.terminate()

def warm_up_gemini_task():
    """Função para rodar o aquecimento do Gemini em uma thread."""
    logging.info("Thread de aquecimento: Iniciando chamada de aquecimento para a API do Gemini...")
    response = obter_resposta_do_astro("Olá, apenas testando a conexão.")
    logging.info(f"Thread de aquecimento: Resposta do aquecimento: {response[:100]}...") # Log um trecho
    print("--- CHAMADA DE AQUECIMENTO CONCLUÍDA (ver logs para detalhes) ---\n")
# --- Função Principal de Execução ---
def executar_servidor():
    # Inicia o Flask em uma thread separada para não bloquear o loop principal
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False), name="Flask-Thread")
    flask_thread.daemon = True
    flask_thread.start()
    
    print(">>> SERVIDOR FLASK INICIADO. O robô NAO já pode se conectar. <<<")
    
    if model_gemini and genai_configured_successfully:
        print("\n--- INICIANDO CHAMADA DE AQUECIMENTO PARA A API DO GEMINI ---")
        # Executa o aquecimento em uma thread para não bloquear
        warm_up_thread = threading.Thread(target=warm_up_gemini_task, name="WarmUp-Gemini-Thread")
        warm_up_thread.daemon = True
        warm_up_thread.start()
    else:
        logging.warning("Aquecimento pulado. API do Gemini não está configurada ou o modelo não carregou.")

    print(">>> SERVIDOR PRONTO E AGUARDANDO COMANDOS <<<")

    while True:
        try:
            # CORREÇÃO: Usa input() que é a função correta para Python 3.
            # O try/except foi removido pois este script deve ser executado com Python 3.
            user_input = input("\n--> Pressione ENTER para ativar o microfone e fazer uma pergunta... (ou digite 'sair' e ENTER para encerrar)\n")
            if user_input.strip().lower() == 'sair':
                print("Encerrando servidor...")
                break
            
            # Executa o processamento da pergunta em uma nova thread
            processing_thread = threading.Thread(target=ouvir_pergunta_e_processar, name="ProcessQuestion-Thread")
            processing_thread.daemon = True
            processing_thread.start()
            
        except KeyboardInterrupt:
            print("\nEncerrando servidor...")
            break
        except Exception as e_loop:
            logging.error(f"Erro no loop principal: {e_loop}")
            break

if __name__ == '__main__':
    if not GOOGLE_API_KEY or not vosk_model_obj:
        logging.critical("ERRO: Verifique a API Key do Google e o caminho do modelo Vosk. Encerrando.")
    else:
        iniciar_sessao_chat()
        executar_servidor()