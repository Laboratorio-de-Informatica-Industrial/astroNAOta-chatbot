🤖 AstroNAOta: Robô Guia de Astronomia com IA 🌠
Bem-vindo ao repositório do projeto AstroNAOta! Esta iniciativa transforma o robô social NAOv6 em um guia interativo, educativo e seguro sobre astronomia para crianças, utilizando tecnologias modernas de Inteligência Artificial Conversacional.

Este projeto foi documentado e estruturado para submissão ao VIII Congresso Nacional de Inovação e Tecnologia (INOVA 2025).

🎯 Visão Geral do Projeto
A interação natural entre humanos e robôs representa um desafio significativo, especialmente em contextos educativos. Este projeto aborda diretamente as limitações de hardware e a incompatibilidade de software (Python 2.7 no NAOqi vs. Python 3+ para IA) de plataformas robóticas como o NAO.

A solução implementada é uma arquitetura modular e desacoplada que delega o processamento pesado para um computador servidor, permitindo que o robô NAO atue como uma interface física carismática enquanto a "inteligência" é executada remotamente.

🛠️ Arquitetura e Tecnologias
O sistema é dividido em dois componentes principais que se comunicam através de uma API REST local:

Componente	Ambiente / Tecnologias Principais	Responsabilidades
🧠 Servidor de IA (Computador)	&lt;img src="[link suspeito removido]" alt="Python 3.10+"> Flask Vosk Gemini API	Ouvir (ASR), Pensar (LLM), Servir (API)
🗣️ Cliente Robótico (NAO)	&lt;img src="[link suspeito removido]" alt="Python 2.7"> NAOqi urllib2	Falar (ALTextToSpeech), Interagir Fisicamente, Fornecer Feedback Visual (ALLeds)
Este design desacoplado permite que o projeto seja flexível, escalável e facilmente atualizável, alinhando-se aos princípios da Indústria 4.0 e da Tecnologia da Informação.

(Sugestão: Crie um diagrama de fluxo simples da arquitetura e adicione a imagem aqui)

📂 Estrutura do Repositório
AstroNAOta-Project/
├── 📁 servidor_ia/
│   └── 📜 servidor_astro.py        # Script principal do servidor (Flask + Vosk + Gemini)
├── 📁 cliente_nao/
│   └── 📜 nao_apenas_fala.py        # Script para ser executado no robô NAOv6
├── 📁 Artigos/
│   └── 📄 artigo_inova_2025.docx   # Documentação de pesquisa do projeto
├── 📁 datasets/
│   └── 📄 dataset_astronomia.jsonl  # Exemplos que guiaram a engenharia de prompts
├── .gitignore
└── README.md
🚀 Como Executar
Pré-requisitos
[ ] Um robô NAOv6 configurado na mesma rede local que o computador servidor.
[ ] Um computador (Linux/Ubuntu) com Python 3.10+ e acesso à internet.
[ ] O modelo Vosk para português do Brasil baixado e descompactado.
[ ] Uma chave de API para o Google Gemini.
Instruções de Execução
&lt;details>
&lt;summary>&lt;strong>Pilar 1️⃣: Iniciar o Computador Servidor (Terminal 1)&lt;/strong>&lt;/summary>

Navegue até a pasta do projeto e crie/ative um ambiente virtual:
Bash

cd /caminho/para/AstroNAOta-Project
python3 -m venv env_llm_py3
source env_llm_py3/bin/activate
Instale as dependências:
Bash

pip install google-generativeai vosk pyaudio flask
Defina sua chave de API do Google como uma variável de ambiente:
Bash

export GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
No script servidor_ia/servidor_astro.py, ajuste a variável VOSK_MODEL_PATH para o caminho correto da sua pasta do modelo Vosk.
Inicie o servidor e aguarde a mensagem de "SERVIDOR PRONTO":
Bash

python3 servidor_ia/servidor_astro.py
Nota: Deixe este terminal rodando. Ele é o cérebro do AstroNAOta!

&lt;/details>

&lt;details>
&lt;summary>&lt;strong>Pilar 2️⃣: Iniciar o Cliente Robótico (Terminal 2 ou Robô NAO)&lt;/strong>&lt;/summary>

Transfira o script cliente_nao/nao_apenas_fala.py para o seu robô.
IMPORTANTE: Edite o script e ajuste as variáveis ROBOT_IP e FLASK_SERVER_IP para os IPs corretos da sua rede.
Execute o script no robô:
Bash

python nao_apenas_fala.py
O AstroNAOta fará sua apresentação e começará a verificar o servidor.

&lt;/details>

&lt;details>
&lt;summary>&lt;strong>Pilar 3️⃣: Iniciar a Interação&lt;/strong>&lt;/summary>

No terminal do servidor (Terminal 1), pressione Enter.
A mensagem ... Microfone ATIVADO... aparecerá.
Fale sua pergunta de astronomia claramente para o microfone do computador.
O robô NAO receberá e falará a resposta gerada pelo AstroNAOta!
Para fazer uma nova pergunta, basta pressionar Enter novamente no terminal do servidor.
&lt;/details>

📄 Artigo e Pesquisa
A fundamentação teórica, a metodologia detalhada e os resultados deste projeto estão consolidados em um artigo preparado para o VIII Congresso Nacional de Inovação e Tecnologia (INOVA 2025).


🌟 Contribuições
Este projeto oferece uma solução prática e inovadora para modernizar plataformas robóticas legadas, demonstrando a eficácia da engenharia de prompts para criar interações humano-robô ricas, seguras e personalizadas no contexto educacional.

Este projeto é desenvolvido no âmbito do Laboratório de Informática Industrial.