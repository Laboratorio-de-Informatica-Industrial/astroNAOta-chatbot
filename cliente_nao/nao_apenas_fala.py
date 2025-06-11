#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import logging
import json
import urllib2
from naoqi import ALProxy

# ===== CONFIGURAÇÃO =====
ROBOT_IP = '192.168.100.228' # <<< IP REAL DO SEU NAO
ROBOT_PORT = 9559
FLASK_SERVER_IP = '192.168.100.79' # <<< IP REAL DO SEU NOTEBOOK
FLASK_SERVER_PORT = 5000
API_GET_RESPONSE_URL = "http://{}:{}/get_robot_response".format(FLASK_SERVER_IP, FLASK_SERVER_PORT)

POLLING_INTERVAL_SECONDS = 2.0 # A cada 2 segundos o NAO pergunta se há algo novo

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Módulos NAOqi ---
tts = None
leds = None
motion = None

try:
    tts = ALProxy('ALTextToSpeech', ROBOT_IP, ROBOT_PORT)
    leds = ALProxy("ALLeds", ROBOT_IP, ROBOT_PORT)
    motion = ALProxy("ALMotion", ROBOT_IP, ROBOT_PORT)
    logging.info("Conectado aos módulos NAOqi.")
except Exception as e:
    logging.error("Erro ao conectar aos módulos NAOqi: %s", e)
    exit(1)

# --- Funções Auxiliares ---
def set_led_state(state):
    if not leds: return
    try:
        if state == "idle":
            leds.fadeRGB("FaceLeds", 0x0077FF, 0.3) # Azul
        elif state == "speaking":
            leds.rasta(2.0) # Efeito colorido por 2 segundos enquanto fala
    except Exception as e_led:
        logging.warning("Erro LED: %s", e_led)

def check_for_new_speech():
    logging.debug("Verificando API Flask para nova fala...")
    try:
        req = urllib2.Request(API_GET_RESPONSE_URL)
        response = urllib2.urlopen(req, timeout=5)
        response_data = json.loads(response.read())
        
        if response_data and response_data.get("status") == "new_response":
            speech_to_say = response_data.get("speech")
            if speech_to_say and isinstance(speech_to_say, unicode):
                speech_to_say = speech_to_say.encode('utf-8', 'replace')
            return speech_to_say
    except Exception as e:
        logging.error("Falha ao verificar API Flask: %s", str(e))
    return None

# --- Função Principal do NAO ---
def main_nao_speaker():
    motion.wakeUp()
    tts.setLanguage("Brazilian")
    tts.setVolume(0.9)
    tts.setParameter("speed", 90)

    # <<< APRESENTAÇÃO MAIS CURTA >>>
    presentation_text = "AstroNAOta pronto!"
    logging.info("Apresentação: %s", presentation_text)
    set_led_state("speaking")
    tts.say(presentation_text)
    set_led_state("idle")

    logging.info("Iniciando loop de verificação de respostas...")

    try:
        while True:
            time.sleep(POLLING_INTERVAL_SECONDS)
            new_speech = check_for_new_speech()
            
            if new_speech:
                logging.info("Nova fala recebida: '%s'", new_speech)
                set_led_state("speaking")
                tts.say(new_speech)
                set_led_state("idle")

    except KeyboardInterrupt:
        logging.info('Encerrando interface de fala do NAO...')
    finally:
        logging.info("Desligando sistemas...")
        if motion: motion.rest()
        if leds: leds.off("FaceLeds")
        if tts: tts.say("Desligando!")

if __name__ == '__main__':
    main_nao_speaker()