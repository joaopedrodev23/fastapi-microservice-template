# FastAPI Microservice Template - Ipiranga

Template base de microservico REST em FastAPI seguindo o contrato canonico `docs/CONTRATO_MICROSERVICO_IPIRANGA.md`.
O objetivo e acelerar a criacao de novos servicos, padronizando estrutura, validacao, mapping e integracao outbound.

## Como rodar

1. Instale dependencias (exemplo):

```bash
pip install fastapi uvicorn pydantic httpx pyyaml
```

2. Defina o ambiente e execute:

```bash
# Windows (PowerShell)
$env:APP_ENV = "dev"
uvicorn app.main:app --reload
```

O endpoint sera exposto em `POST /{service-name}` conforme definido em `settings.<env>.yml`.

## Exemplo de payload DME

```json
{
  "header": {
    "eventId": "00000000-0000-0000-0000-000000000000",
    "source": "sistema-origem",
    "timestamp": "2026-02-10T12:00:00Z"
  },
  "payload": {
    "data": {
      "example_field_1": "valor1",
      "example_field_2": "valor2"
    }
  }
}
```

## Onde adaptar campos e regras

- Schema de entrada (DME): `app/domain/dme_input.py`
- Schema do payload de saida (backend): `app/domain/backend_payload.py`
- Mapping explicito (DME -> Backend): `app/services/mapper.py`
- Integracao outbound (REST): `app/integrations/outbound_rest.py`
- Configuracao por ambiente: `settings.dev.yml`, `settings.hml.yml`, `settings.prod.yml`

## Como evoluir o template

- Criar novos endpoints: adicionar rotas em `app/api/inbound.py` seguindo o pipeline padrao.
- Ajustar validacoes do DME: expandir os modelos em `app/domain/dme_input.py`.
- Alterar o mapping: atualizar `required_fields` e o retorno em `app/services/mapper.py`.
- Trocar mock por chamada real: ajustar `mock_enabled` em `settings.<env>.yml` e configurar `base_url`/`endpoint_path`.

## Observacoes importantes

- Nao ha persistencia de dados.
- Nao ha integracao com database ou Kafka no MVP.
- O header do DME nao deve ser alterado.
- O `eventId` e propagado para logs e resposta.
