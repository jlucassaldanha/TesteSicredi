# Processador Automático de Solicitações de Cadastro

Esta aplicação é uma automação desenvolvida em Python para processar solicitações de cadastro diárias disponibilizadas em formato JSON. A solução realiza a leitura, validação, sanitização e filtragem dos registros, gerando um arquivo CSV apenas com as solicitações aprovadas e um log detalhado de toda a execução.


## 📁 Estrutura do Projeto

O projeto foi organizado de forma modular para garantir a separação de responsabilidades, facilitando a manutenção e a testabilidade:

```text
desafio_python/
│── main.py              # Ponto de entrada e orquestração do pipeline
│── core_processor.py    # Lógica de negócio e validação dos registros
│── file_processor.py    # Leitura de JSON e exportação de CSV (I/O)
│── logger_setup.py      # Configuração do sistema de logging
│── test_processor.py    # Suíte de testes unitários automatizados
│── solicitacoes.json    # Arquivo de entrada com os registros
└── README.md            # Documentação técnica da solução
```

## 🛠️ Pré-requisitos e Dependências

* **Python 3.8+** instalado.
* **Bibliotecas externas:** Nenhuma. Toda a solução foi desenvolvida utilizando exclusivamente as bibliotecas nativas do Python (`json`, `csv`, `logging`, `pathlib` e `unittest`), dispensando o uso de arquivo `requirements.txt`.


## 🚀 Como Executar o Projeto

### 1. Executando o Processamento Principal
Certifique-se de que o arquivo `solicitacoes.json` está na raiz do diretório e execute:
```bash
python main.py
```

Após a execução, os seguintes arquivos serão gerados na raiz do projeto:
* **`aprovados.csv`**: Arquivo final contendo apenas as solicitações válidas e aprovadas.
* **`processamento.log`**: Registros de execução com timestamps, avisos de registros ignorados e resumo de métricas.

### 2. Executando os Testes Automatizados
Para rodar a suíte de testes unitários e verificar o comportamento das regras de negócio e tratamento de exceções:
```bash
python -m unittest test_processor.py
```


## ⚙️ Premissas Adotadas e Decisões Relevantes

1. **Separador do CSV (`;`):** Optou-se pelo uso do ponto e vírgula (`;`) como delimitador. Essa decisão visa garantir a abertura direta e correta do arquivo CSV em editores de planilha (como Microsoft Excel) em sistemas operacionais configurados no padrão regional brasileiro/latino.
2. **Codificação UTF-8:** A leitura e escrita dos arquivos foram configuradas para `UTF-8` para assegurar a correta preservação de caracteres acentuados.
3. **Sanitização de CPF:** Além de verificar a presença do campo, a validação limpa o CPF removendo caracteres não numéricos (pontos e traços), garantindo a padronização do dado na saída.
4. **Resiliência e Tratamento de Erros:** Falhas de sintaxe em JSON, arquivos ausentes ou registros incompletos são devidamente capturados e registrados no arquivo de log sem interromper o fluxo de execução dos demais registros válidos.


## 🔄 Integração com Processos (BPM) e Arquitetura

*Pergunta do desafio: Como você adaptaria essa solução para um processo de BPM, no qual os registros fossem recebidos por um formulário e o arquivo CSV fosse gerado após uma etapa de aprovação?*

**Resposta:**

Para evoluir a solução de um modelo em lote (*batch*) estático para um processo dinâmico de BPM (ex.: Camunda, Bizagi, ServiceNow ou módulos de ERP como Protheus):

1. **Entrada de Dados via Formulário:**
   O formulário da plataforma de BPM substitui o arquivo `solicitacoes.json`. Cada envio cria uma nova instância de processo com status "PENDENTE", persistindo os dados no banco/engine do processo.

2. **Evento de Aprovação:**
   O registro aguarda a etapa de decisão (*User Task*). Assim que o aprovador conclui a tarefa, o sistema altera o estado do processo para "APROVADO".

3. **Integração Orientada a Eventos / APIs (Pós-Aprovação):**
   A geração do CSV deixa de ser um script isolado e passa a ser disparada após o evento de aprovação. Isso pode ser desenhado usando padrões de integração consagrados:
   * **Webhook / API REST (Síncrono):** O BPM faz uma chamada HTTP POST para uma API REST em Python enviando os dados do registro recém-aprovado para geração do CSV.
   * **Filas e Mensageria (Assíncrono):** A aprovação publica uma mensagem em uma fila (ex.: RabbitMQ, SQS, Kafka). Um *worker* em Python consome esse evento, valida o registro e alimenta o CSV ou banco de dados de destino de forma resiliente.
   * **Consumo Batch via API:** Um script Python agendado consulta periodicamente o endpoint REST do BPM/ERP recuperando apenas os registros aprovados no período.


## 🤖 Transparência no Uso de Ferramentas de IA

Em conformidade com as diretrizes do processo seletivo:
* **Ferramenta:** Gemini.
* **Contribuição:** Utilizado como assistente consultivo para suporte no desenvolvimento, revisão das boas práticas de logging/testes unitários e auxílio na formatação da documentação técnica.




