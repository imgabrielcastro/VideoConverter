Transcrição e Análise de Ligações do Treinamento Inicial

Este repositório contém um código em Python desenvolvido para a empresa NextFit com o objetivo de facilitar o processo dos times. O projeto transcreve ligações do "Treinamento Inicial" realizadas com clientes da plataforma Next Fit. Além de transcrever, o código organiza as informações em relatórios de fácil leitura para auxiliar na análise e melhoria do atendimento.

Funcionalidades

Transcrição de áudio: Converte o áudio das ligações em texto utilizando o serviço de Speech-to-Text da Azure.

Template de Análise: Gera relatórios padronizados com os principais pontos abordados na ligação.

Organização de arquivos: Cria automaticamente uma pasta na área de trabalho para armazenar os relatórios de todas as ligações transcritas.

Exemplo de Relatório Gerado

Treinamento Inicial realizado com Jonas

TREINAMENTO@COMPUTADOR

Modelo de Negócio do cliente:
Jonas identifica seu negócio como um estúdio de cross training, também chamado de funcional. Durante o processo diário, ele programa as aulas e gerencia o pagamento dos alunos manualmente, utilizando o WhatsApp para agendar aulas e comunicar-se com os alunos (0:02:58, 0:16:00).

Configurações Realizadas por o Cliente:

Cadastro de novos usuários para funcionários (0:01:01).

Configuração e exclusão de modalidades desatualizadas (0:03:46).

Ajuste e atualização de planos semestrais (0:06:54).

Itens abordados durante o treinamento:

Introdução ao sistema web e suas funcionalidades gerais (0:00:30).

Criação e edição de usuários dentro do sistema, com atenção às permissões (0:01:57).

Configuração de modalidades e planos de treino, incluindo edição de planos desatualizados (0:03:46, 0:06:54).

Detalhamento sobre a venda de contratos e suas funcionalidades financeiras (0:08:09).

Explanação sobre o uso do aplicativo Next Fit Pay e suas vantagens (0:09:30).

Demonstração de como criar e gerenciar grades de horário e agendamentos (0:19:28).

Comportamento do cliente durante o treinamento:
Jonas mostrou-se atento e colaborativo durante o treinamento, participando ativamente das demonstrações. Ele expressou suas dúvidas principalmente em relação ao Next Fit Pay e seu funcionamento (0:12:13, 0:16:52). Ao longo das explicações sobre o cadastramento de usuários e modalidades, ele foi receptivo às sugestões e demonstrou iniciativa ao planejar a aplicação das funcionalidades discutidas (0:01:57, 0:04:11). Em momentos de esclarecimento sobre o uso do aplicativo mobile pelos alunos, Jonas parecia satisfeito com a proposta de uma gestão mais simplificada e interativa (0:32:44).

Alinhamento final:

Jonas se comprometeu a revisar e ajustar os contratos atuais, observando nomes e preços desatualizados (0:35:03).

Iniciar o cadastro de todos os alunos ativos e potenciais no sistema (0:35:07).

Incorporar gradualmente o sistema Next Fit Pay (0:13:48).

Enviar ao consultor a arte com a identidade visual do estúdio para personalização do aplicativo (0:37:11).

Requisitos para Execução

Python 3.8 ou superior.

Bibliotecas:

ffmpeg

tkinter

azure-cognitiveservices-speech

openai

Configuração e Execução

Clone o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

Instale as dependências:

pip install -r requirements.txt

Certifique-se de ter o ffmpeg instalado:

Guia de instalação do ffmpeg

Configure as chaves de acesso:

Adicione suas chaves da API da Azure e do OpenAI em um arquivo .env no formato:

AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=your_azure_region
OPENAI_API_KEY=your_openai_key

Execute o programa:

python main.py

Licença

Este projeto está licenciado sob a MIT License.

Contato

Para dúvidas ou sugestões, entre em contato:

Email: josegabrielsouzacastro@gmail.com

LinkedIn: [José Gabriel Souza de Castro](https://www.linkedin.com/in/josé-gabriel-souza-de-castro/)
