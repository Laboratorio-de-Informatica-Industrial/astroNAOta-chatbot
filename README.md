# AstroNAOta: Robô Guia de Astronomia com IA

Bem-vindo ao repositório do projeto **AstroNAOta**! Esta iniciativa visa transformar o robô social NAOv6 em um guia interativo, educativo e seguro sobre astronomia para crianças, utilizando tecnologias modernas de Inteligência Artificial Conversacional.

Este projeto foi documentado e estruturado para submissão ao VIII Congresso Nacional de Inovação e Tecnologia (INOVA 2025).

## 🎯 Visão Geral do Projeto

A interação natural entre humanos e robôs representa um desafio significativo, especialmente em contextos educativos. Este projeto aborda diretamente as limitações de hardware e a incompatibilidade de software (Python 2.7 no NAOqi vs. Python 3+ para IA) de plataformas robóticas como o NAO.

A solução implementada é uma **arquitetura modular e desacoplada** que delega o processamento pesado para um computador servidor, permitindo que o robô NAO atue como uma interface física carismática enquanto a "inteligência" é executada remotamente.

## 🛠️ Arquitetura e Tecnologias

O sistema é dividido em dois componentes principais que se comunicam através de uma API REST local:

1.  **Servidor de IA (Computador Local - Python 3+):**
    * **Reconhecimento de Fala (ASR):** Utiliza o modelo **Vosk** para português do Brasil, rodando localmente no servidor para transcrever a fala do usuário capturada por um microfone externo, garantindo alta precisão.
    * **Geração de Linguagem (LLM):** Envia o texto transcrito para a API do **Google Gemini**. A personalidade, o tom e a segurança do "AstroNAOta" são moldados através de uma robusta **Engenharia de Prompts**.
    * **API Web:** Um servidor **Flask** expõe um endpoint (`/get_robot_response`) que o robô consulta para obter as respostas a serem faladas.

2.  **Cliente Robótico (NAO - Python 2.7):**
    * **Vocalização e Presença Física:** Um script Python 2.7 minimalista (`nao_apenas_fala.py`) é executado no robô. Sua única função é fazer requisições periódicas (polling) ao servidor Flask e usar o módulo `ALTextToSpeech` para vocalizar as respostas recebidas.
    * **Feedback Visual:** Utiliza o módulo `ALLeds` para fornecer feedback visual ao usuário.

Este design desacoplado permite que o projeto seja flexível, escalável e facilmente atualizável, alinhando-se aos princípios da **Indústria 4.0** e da **Tecnologia da Informação**.

*(Sugestão: Crie um diagrama de fluxo simples da arquitetura e adicione a imagem aqui)*

## 📂 Estrutura do Repositório

-   `servidor_ia/servidor_astro.py`: Script principal do servidor (Flask + Vosk + Gemini) para ser executado no computador local.
-   `cliente_nao/nao_apenas_fala.py`: Script para ser executado no robô NAOv6.
-   `Artigos/`: Contém publicações e a documentação de pesquisa do projeto.
-   `datasets/`: Contém os arquivos `.jsonl` ou `.txt` com exemplos de interações que guiaram a engenharia de prompts.
-   `.gitignore`: Arquivo de configuração para ignorar arquivos e pastas desnecessários (como ambientes virtuais e modelos de ASR).
-   `README.md`: Este arquivo.

## 🚀 Como Executar

**Pré-requisitos:**
* Um robô NAOv6 configurado na mesma rede local que o computador servidor.
* Um computador (Linux/Ubuntu) com Python 3.10+ e acesso à internet.
* O [modelo Vosk para português do Brasil](https://alphacephei.com/vosk/models) baixado e descompactado.
* Uma chave de API para o Google Gemini.

**Instruções:**

1.  **No Computador Servidor (Terminal 1):**
    * Navegue até a pasta do projeto.
    * Crie e ative um ambiente virtual Python 3: `python3 -m venv env_llm_py3 && source env_llm_py3/bin/activate`.
    * Instale as dependências: `pip install google-generativeai vosk pyaudio flask`.
    * Defina sua chave de API do Google como uma variável de ambiente:
        ```bash
        export GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
        ```
    * No script `servidor_astro.py`, ajuste a variável `VOSK_MODEL_PATH` para o caminho correto da sua pasta do modelo Vosk.
    * Inicie o servidor:
        ```bash
        python3 servidor_ia/servidor_astro.py
        ```
    * O servidor fará uma chamada de "aquecimento" e ficará aguardando seu comando no terminal.

2.  **No Robô NAO (ou Terminal 2 para simulação):**
    * Transfira o script `cliente_nao/nao_apenas_fala.py` para o seu robô.
    * **IMPORTANTE:** Edite o script e ajuste as variáveis `ROBOT_IP` e `FLASK_SERVER_IP` para os IPs corretos da sua rede.
    * Execute o script no robô:
        ```bash
        python nao_apenas_fala.py
        ```
    * O AstroNAOta fará sua apresentação e começará a verificar o servidor.

3.  **Interação:**
    * No terminal do servidor (Terminal 1), pressione **Enter** para ativar o microfone.
    * Fale sua pergunta de astronomia claramente para o microfone do computador.
    * O robô NAO receberá e falará a resposta gerada pelo AstroNAOta.
    * Pressione Enter novamente no terminal do servidor para cada nova pergunta.

## 📄 Artigo e Pesquisa

A fundamentação teórica, a metodologia detalhada e os resultados deste projeto estão consolidados em um artigo preparado para o VIII Congresso Nacional de Inovação e Tecnologia (INOVA 2025).



## 🌟 Contribuições

Este projeto oferece uma solução prática e inovadora para modernizar plataformas robóticas legadas, demonstrando a eficácia da engenharia de prompts para criar interações humano-robô ricas, seguras e personalizadas no contexto educacional.

---
*Este projeto é desenvolvido no âmbito do Laboratório de Informática Industrial.*