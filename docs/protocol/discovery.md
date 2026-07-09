# Discovery

<p class="od-meta">
  <span class="od-badge od-badge--code">discovery</span>
  <span class="od-badge od-badge--must">Obrigatório</span>
</p>

<div class="od-api-callout">
  <p>Primeiro passo de qualquer integração V2. O contrato HTTP (OpenAPI) está em inglês.</p>
  <a href="../reference/discovery/">Abrir referência OpenAPI →</a>
</div>

Antes de qualquer operação de capability, cada participante publica um documento público, legível por máquina, que declara o que ele suporta. Esse documento é o **manifesto de discovery**, servido em uma URL well-known.

Esta página explica para que serve o discovery, como cada lado o usa e como ler/publicar um manifesto. Regras normativas e a referência completa de campos estão na [spec OpenAPI de Discovery](../reference/discovery.md) (**somente em inglês**).

---

## O problema que o Discovery resolve

Na V1 não havia forma padrão de saber o que a contraparte suportava antes de chamar. Integradores descobriam por tentativa e erro: chamavam um endpoint, recebiam `404` ou erro inesperado, e voltavam a negociar bilateralmente. Isso era lento, caro e gerava implementações divergentes.

O Discovery elimina isso. Em vez de descobrir capabilities por falhas, cada participante declara o que implementa em um documento sempre disponível.

---

## Como funciona

O manifesto é servido com `GET` HTTP em uma URL que termina com `/.well-known/opendelivery`:

```
GET https://example.com/.well-known/opendelivery
```

O endpoint é **público** — sem autenticação. A resposta é JSON com o que a contraparte precisa antes de enviar qualquer requisição de capability: capabilities ativas, operações, eventos, webhook ou polling, limites operacionais.

- **Publisher** — quem implementa e serve o manifesto.
- **Consumer** — quem lê o manifesto antes de integrar.

Na prática ambos os lados costumam ser publisher e consumer.

---

## Fluxo de integração

Discovery é sempre o passo zero:

```
Consumer                                 Publisher
   |                                         |
   |  GET /.well-known/opendelivery          |
   |---------------------------------------->|
   |  200 OK  { manifest }                   |
   |<----------------------------------------|
   |  [lê capabilities, limites, eventos]    |
   |  POST /orders   (ou webhook, etc.)      |
   |---------------------------------------->|
```

A URL completa de discovery é trocada **fora de banda** (onboarding/configuração). O manifesto não é o lugar para “descobrir a URL”.

---

## Conteúdo do manifesto

### Identidade e versão do protocolo

```json
{
  "appId": "550e8400-e29b-41d4-a716-446655440000",
  "openDelivery": {
    "currentVersion": "2.0",
    "supportedVersions": ["2.0"]
  },
  "discovery": {
    "version": "1.0.0"
  }
}
```

`appId` identifica a aplicação. `openDelivery.supportedVersions` indica interoperabilidade de versão. Sem overlap de versões, a integração não pode prosseguir.

### Autenticação e capabilities

O manifesto declara modelos OAuth suportados (`client_credentials`, `authorization_code`, geração `by_app` / `by_merchant`) e o mapa de **capabilities** (`merchant`, `orders`, `logistics`, `customer`, extensões como `indoor` / `loyalty`) com endpoints e modos de interação.

Detalhes de campos e schemas: [OpenAPI Discovery](../reference/discovery.md) (EN).

---

## Regras

- Participantes que expõem qualquer capability **DEVEM** publicar Discovery.
- O manifesto **DEVE** ser consistente com o comportamento real (capabilities, eventos, auth).
- Consumidores **DEVEM** ler o manifesto antes de operações de capability.
- Mudanças que afetam integração **DEVEM** ser refletidas no manifesto.

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="../reference/discovery/">OpenAPI Discovery (EN)</a>
    <a href="authentication/">Autenticação</a>
    <a href="../guide/getting-started/">Primeiros Passos</a>
  </div>
</div>
