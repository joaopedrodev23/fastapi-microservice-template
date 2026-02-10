📄 CONTRATO CANÔNICO – MICROSSERVIÇO IPIRANGA (v1)
1. Objetivo

Este documento define o contrato canônico de um microserviço Ipiranga, servindo como base padrão para a geração automática de microserviços REST em Python utilizando FastAPI.

O objetivo do microserviço é:

Receber eventos via API REST no padrão Ipiranga (DME), validar e transformar os dados, e encaminhá-los para um sistema backend (REST, inicialmente mockado).

Este contrato é agnóstico de negócio, focado exclusivamente em estrutura, fluxo e padronização técnica.

2. Responsabilidade do Microserviço

Todo microserviço Ipiranga deve:

Expor uma API REST

Receber um payload no padrão DME

Validar o payload recebido

Realizar data mapping para o formato esperado pelo backend

Realizar uma chamada REST outbound

Retornar uma resposta padronizada

O microserviço não:

Contém regra de negócio complexa

Persiste dados (na versão inicial)

Orquestra múltiplos sistemas

3. Interface REST (Entrada)
3.1 Método e Endpoint

Método: POST

Endpoint: definido por serviço
Exemplo:

POST /{service-name}


Cada microserviço possui um endpoint principal.

4. DME – Data Message Envelope (Input Canônico)
4.1 Estrutura Base do DME

Todo microserviço deve aceitar um DME com a seguinte estrutura mínima:

{
  "header": {
    "eventId": "uuid",
    "source": "string",
    "timestamp": "ISO-8601"
  },
  "payload": {
    "data": {}
  }
}

4.2 Regras do DME

header é obrigatório e padronizado

payload.data é variável e específica por microserviço

O microserviço não altera o header

O eventId deve ser propagado para logs e resposta

5. Pipeline de Processamento (Fluxo Padrão)

Todo microserviço deve seguir exatamente o pipeline abaixo:

Recebimento REST
        ↓
Validação do DME
        ↓
Extração do payload.data
        ↓
Mapping DME → Backend Payload
        ↓
Chamada REST Outbound
        ↓
Resposta Padronizada


Esse pipeline não deve ser quebrado ou reordenado.

6. Data Mapping
6.1 Conceito

O microserviço deve realizar a transformação de dados do formato:

DME.payload.data → Backend Payload

6.2 Regras de Mapping

Mapping deve ser explícito e legível

Nenhum campo deve ser transformado implicitamente

Campos inexistentes devem ser tratados com erro controlado

O mapping deve ser facilmente substituível/configurável

7. Integração Outbound (REST)
7.1 Comportamento

Realizar chamada REST para backend configurado

Backend inicialmente pode ser mockado

URL, headers e timeout devem ser configuráveis

7.2 Responsabilidade

O microserviço apenas encaminha dados

Não interpreta resposta do backend (versão inicial)

8. Resposta da API (Output Canônico)

Toda resposta deve seguir o padrão:

{
  "status": "SUCCESS | ERROR",
  "message": "string",
  "eventId": "uuid"
}

Regras:

eventId deve ser o mesmo recebido no DME

Mensagens devem ser claras e não técnicas

Erros devem retornar HTTP status adequado (4xx / 5xx)

9. Configuração por Ambiente

Todo microserviço deve suportar múltiplos ambientes:

dev

hml

prod

Configurações incluem:

URL do backend

Timeout

Headers outbound

Flags de mock

10. Observações Importantes

Este contrato é a fonte da verdade

Templates, geradores e automações devem respeitá-lo

Mudanças futuras devem ser feitas primeiro neste documento

O contrato deve evoluir versionado (v1, v2, etc.)

11. Próximos Passos Planejados

Criar template FastAPI baseado neste contrato

Criar gerador de microserviços a partir do template

Usar GitHub Copilot para escalar geração de serviços

Evoluir suporte a database e Kafka