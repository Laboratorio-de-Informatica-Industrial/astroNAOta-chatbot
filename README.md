# 🤖 AstroNAOta: Robô Guia de Astronomia com IA 🌠

Bem-vindo ao repositório do projeto **AstroNAOta**! Esta iniciativa visa transformar o robô social NAOv6 em um guia interativo, educativo e seguro sobre astronomia para crianças, utilizando tecnologias modernas de Inteligência Artificial Conversacional.

> Este projeto foi documentado e estruturado para submissão ao **VIII Congresso Nacional de Inovação e Tecnologia (INOVA 2025)**.

---

## 🎯 Visão Geral do Projeto

A interação natural entre humanos e robôs representa um desafio significativo, especialmente em contextos educativos. Este projeto aborda diretamente as limitações de hardware e a incompatibilidade de software (Python 2.7 no NAOqi vs. Python 3+ para IA) de plataformas robóticas como o NAO.

A solução implementada é uma **arquitetura modular e desacoplada** que delega o processamento pesado para um computador servidor, permitindo que o robô NAO atue como uma interface física carismática enquanto a "inteligência" é executada remotamente.

---

## 🛠️ Arquitetura e Tecnologias

O sistema é dividido em dois componentes principais que se comunicam através de uma API REST local:

| Componente | Ambiente / Tecnologias Principais | Responsabilidades |
| :--- | :--- | :--- |
| 🧠 **Servidor de IA (Computador)** | ![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python) `Flask` `Vosk` `Gemini API` | **Ouvir** (ASR), **Pensar** (LLM), **Servir** (API) |
| 🗣️ **Cliente Robótico (NAO)** | ![Python 2.7](https://img.shields.io/badge/Python-2.7-orange?logo=python) `NAOqi` `urllib2` | **Falar** (`ALTextToSpeech`), **Interagir Fisicamente**, **Fornecer Feedback Visual** (`ALLeds`) |

Este design desacoplado permite que o projeto seja flexível, escalável e facilmente atualizável, alinhando-se aos princípios da **Indústria 4.0** e da **Tecnologia da Informação**.

*(Sugestão: Crie um diagrama de fluxo simples da arquitetura e adicione a imagem aqui)*

---

## 📂 Estrutura do Repositório

```
AstroNAOta-Project/
├── 📁 Artigos/
│   └── 📄 artigo_inova_2025.docx   # Documentação de pesquisa do projeto
├── 📁 cliente_nao/
│   └── 📜 nao_apenas_fala.py        # Script para ser executado no robô NAOv6
├── 📁 datasets/
│   └── 📄 dataset_astronomia.jsonl  # Exemplos que guiaram a engenharia de prompts
├── 📁 servidor_ia/
│   └── 📜 servidor_astro.py        # Script principal do servidor (Flask + Vosk + Gemini)
├── .gitignore
└── README.md
```

---

## 🚀 Como Executar

#### **Pré-requisitos**
- [ ] Um robô **NAOv6** configurado na mesma rede local que o computador servidor.
- [ ] Um computador (**Linux/Ubuntu**) com Python 3.10+ e acesso à internet.
- [ ] O [modelo Vosk para português do Brasil](https://alphacephei.com/vosk/models) baixado e descompactado.
- [ ] Uma **chave de API** para o Google Gemini.

---

### **Instruções de Execução**

<details>
<summary><strong>Pilar 1️⃣: Iniciar o Computador Servidor (Terminal 1)</strong></summary>

1.  Navegue até a pasta do projeto e crie/ative um ambiente virtual:
    ```bash
    cd /caminho/para/AstroNAOta-Project
    python3 -m venv env_llm_py3
    source env_llm_py3/bin/activate
    ```
2.  Instale as dependências:
    ```bash
    pip install google-generativeai vosk pyaudio flask
    ```
3.  Defina sua chave de API do Google como uma variável de ambiente:
    ```bash
    export GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
    ```
4.  No script `servidor_ia/servidor_astro.py`, ajuste a variável `VOSK_MODEL_PATH` para o caminho correto da sua pasta do modelo Vosk.
5.  Inicie o servidor e aguarde a mensagem de "SERVIDOR PRONTO":
    ```bash
    python3 servidor_ia/servidor_astro.py
    ```
    > **Nota:** Deixe este terminal rodando. Ele é o cérebro do AstroNAOta!

</details>

<details>
<summary><strong>Pilar 2️⃣: Iniciar o Cliente Robótico (Terminal 2 ou Robô NAO)</strong></summary>

1.  Transfira o script `cliente_nao/nao_apenas_fala.py` para o seu robô.
2.  **IMPORTANTE:** Edite o script e ajuste as variáveis `ROBOT_IP` e `FLASK_SERVER_IP` para os IPs corretos da sua rede.
3.  Execute o script no robô:
    ```bash
    python nao_apenas_fala.py
    ```
    > O AstroNAOta fará sua apresentação e começará a verificar o servidor.

</details>

<details>
<summary><strong>Pilar 3️⃣: Iniciar a Interação</strong></summary>

1.  No terminal do **servidor** (Terminal 1), pressione **Enter**.
2.  A mensagem `... Microfone ATIVADO...` aparecerá.
3.  **Fale sua pergunta de astronomia** claramente para o microfone do computador.
4.  O robô NAO receberá e falará a resposta gerada pelo AstroNAOta!
5.  Para fazer uma nova pergunta, basta pressionar `Enter` novamente no terminal do servidor.

</details>

---

## 📄 Artigo e Pesquisa

A fundamentação teórica, a metodologia detalhada e os resultados deste projeto estão consolidados em um artigo preparado para o VIII Congresso Nacional de Inovação e Tecnologia (INOVA 2025).

---

## 🌟 Contribuições

Este projeto oferece uma solução prática e inovadora para modernizar plataformas robóticas legadas, demonstrando a eficácia da engenharia de prompts para criar interações humano-robô ricas, seguras e personalizadas no contexto educacional.

---
> *Este projeto é desenvolvido no âmbito do Laboratório de Informática Industrial.*