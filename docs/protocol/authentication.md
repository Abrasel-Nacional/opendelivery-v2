# Autenticação

Autenticação não é um domínio de capability.

É um mecanismo transversal ao protocolo que governa como os participantes obtêm e apresentam credenciais para acessar operações protegidas. A autenticação se aplica uniformemente a todas as capabilities do ODP — Merchant, Orders, Logistics e outras.

## Modelos de Autenticação Suportados

O ODP v2 suporta três modelos de autenticação OAuth 2.0. O protocolo não impõe um único modelo para todos os ecossistemas. Cada plataforma DEVE declarar qual(is) modelo(s) suporta, e essa declaração DEVE ser explicitada no endpoint de Discovery e durante o onboarding.

| modelo | identificador | status |
|---|---|---|
| Client Credentials por Estabelecimento | `client_credentials_merchant` | Suportado — compatibilidade legada |
| Client Credentials por Aplicação | `client_credentials_application` | Suportado — recomendado para novas integrações |
| Authorization Code | `authorization_code` | Suportado — opcional, casos de uso avançados |

## Requisitos Comuns

Independentemente do modelo de autenticação selecionado, toda implementação DEVE seguir estas regras:

1. O modelo de autenticação selecionado DEVE ser declarado no endpoint de Discovery.
2. O modelo de autenticação usado em produção DEVE ser alinhado explicitamente durante o onboarding.
3. Os escopos suportados DEVEM ser declarados e consistentes com as capabilities do protocolo utilizadas.
4. As regras de autorização de estabelecimentos DEVEM ser explícitas e descobríveis.
5. A assinatura de mensagens, quando suportada, DEVE ser declarada independentemente do fluxo OAuth 2.0.
6. Os payloads de eventos e requisições DEVEM preservar a identificação do estabelecimento sempre que exigido pelo modelo de integração.
7. O material de autenticação DEVE ser protegido em trânsito e em repouso.

## Modelo 1 — Client Credentials por Estabelecimento

Um par `client_id`/`client_secret` separado é emitido para cada estabelecimento.

Este é o modelo utilizado no ODP v1. É suportado na v2 para cenários de compatibilidade e migração.

A **Ordering Application** ou o **Logistics Service** DEVE fornecer um `client_id` e `client_secret` para cada estabelecimento individual com o qual trabalha, mesmo que esses estabelecimentos usem o mesmo **Software Service**.

**Aquisição de credenciais:** O **Software Service** do estabelecimento recupera o `client_id` e o `client_secret` da **Ordering Application** ou do **Logistics Service** e os utiliza para obter um token de acesso via endpoint de token.

**Uso do token:** O `accessToken` obtido deve ser incluído no header `Authorization` de toda requisição protegida:

```
Authorization: Bearer <accessToken>
```

O campo `expiresIn` indica o tempo de vida do token de acesso em segundos. O token DEVE ser armazenado em cache e reutilizado entre requisições até a expiração — NÃO DEVE ser regenerado por requisição.

!!! note
    Refresh Token não é suportado neste modelo.

**Mapeamento de escopo por capability na v1:**

| capability | responsável pelas credenciais |
|---|---|
| Orders, Merchant | Ordering Application |
| Logistics | Logistics Service |

**Quando usar:**

- Migrações legadas da v1
- Ecossistemas onde as credenciais são provisionadas por estabelecimento
- Cenários onde alterar o modelo de credenciais operacionais produziria custo excessivo de migração

**Trade-offs:**

- Requer provisionamento repetido de credenciais para cada estabelecimento
- Maior sobrecarga operacional para provedores de software que gerenciam muitos estabelecimentos
- Menor escalabilidade para integrações multi-estabelecimento

## Modelo 2 — Client Credentials por Aplicação

Um único par `client_id`/`client_secret` é emitido para o software ou aplicação. O acesso ao estabelecimento é determinado separadamente por meio de regras de autorização, fora do token em si.

Este é o modelo recomendado para novas integrações no ODP v2.

**Capabilities complementares recomendadas ao usar este modelo:**

- Um endpoint para listar os estabelecimentos autorizados para a aplicação (ex.: `GET /merchants`)
- Mecanismos de notificação de autorização e desautorização
- Filtragem opcional por estabelecimento nos fluxos de recuperação assíncrona de eventos

**Trade-offs:**

- Requer uma estratégia explícita de autorização de estabelecimentos separada da credencial
- Estabelecimentos NÃO DEVEM ser incorporados no token de acesso em si

## Modelo 3 — Authorization Code

O Authorization Code é um modelo OAuth 2.0 opcional destinado a cenários onde um **proprietário ou administrador de estabelecimento** deve conceder explicitamente acesso a uma aplicação externa aos seus dados.

Neste fluxo, a autorização não é implícita na credencial — ela requer uma etapa interativa. O fluxo típico é:

1. Um **Software Service** inicia uma solicitação de autorização para um estabelecimento específico.
2. O estabelecimento é redirecionado para uma interface de autorização hospedada pela plataforma.
3. O estabelecimento se autentica e aprova ou nega explicitamente o acesso para aquela aplicação.
4. Após a aprovação, a plataforma emite um código de autorização que a aplicação troca por um token de acesso.
5. O token resultante tem escopo para aquele estabelecimento e aquela aplicação.

Este modelo fornece governança mais forte sobre quais aplicações podem acessar os dados de um estabelecimento, tornando-o adequado para ecossistemas onde o consentimento do estabelecimento deve ser auditável e revogável.

Não é obrigatório para todas as integrações. Quando suportado, DEVE ser declarado no Discovery.

## API Key

Alguns endpoints podem exigir autenticação via API Key em vez de OAuth 2.0. Quando utilizada, a chave DEVE ser passada no header da requisição:

| header | tipo | descrição |
|---|---|---|
| `X-API-KEY` | string | Chave de API emitida pelo host do endpoint para seus clientes |

A criação e gestão da API Key é responsabilidade do host do endpoint. Cada cliente pode ter sua própria chave. As operações que exigem autenticação via API Key declaram isso explicitamente em sua definição.

## Autenticação de Webhooks

Webhooks não usam OAuth 2.0. Utilizam um mecanismo de **assinatura de mensagens** para permitir que o receptor verifique a autenticidade do remetente.

Quando uma **Ordering Application** envia um evento de webhook para um **Software Service**, a requisição DEVE carregar informações de identidade assinadas — incluindo a identidade da aplicação, o estabelecimento envolvido e uma assinatura criptográfica do payload derivada do `client_secret` compartilhado.

O **Software Service** é responsável por verificar a assinatura em cada webhook recebido para confirmar que a requisição origina de uma **Ordering Application** conhecida e autorizada.

## Escopos

Os escopos no ODP v2 são organizados por domínio de capability. Toda operação protegida declara qual escopo é necessário.

| escopo | domínio |
|---|---|
| `od.orders` | Orders |
| `od.menu` | Merchant / Catálogo |
| `od.logistics` | Logistics |
| `od.crm` | CRM e Loyalty |
| `od.all` | Todas as capabilities (acesso total) |

!!! note
    No ODP v1, um único escopo `od.all` era usado para todos os endpoints. Tokens com escopo por domínio são uma introdução da v2 e permitem controle de acesso mais granular.

As implementações DEVEM declarar os escopos que suportam no Discovery.

## Assinatura de Mensagens

A assinatura de mensagens é uma capability de segurança independente do modelo de autenticação OAuth 2.0. Pode ser aplicada a requisições e respostas em ambas as direções.

- A assinatura de mensagens **não é obrigatória** para o transporte REST fora de webhooks.
- O suporte à assinatura de mensagens DEVE ser declarado no Discovery.
- Quando declarado, o mecanismo de assinatura e as operações aplicáveis DEVEM ser especificados explicitamente.

## Declaração no Discovery

Toda implementação ODP v2 DEVE expor um [endpoint de Discovery](discovery.md) que declare sua configuração de autenticação. Os seguintes campos são obrigatórios para a declaração de autenticação:

| campo | tipo | obrigatório | descrição |
|---|---|---|---|
| `authentication.supportedGrantTypes` | array[string] | SIM | Grant types OAuth 2.0 aceitos: `client_credentials`, `authorization_code` |
| `authentication.clientIdGeneration` | array[string] | SIM | Como os client IDs são emitidos: `by_app` (recomendado) ou `by_merchant` (legado V1) |

**Exemplo de bloco de autenticação no Discovery:**

```yaml
authentication:
  supportedGrantTypes:
    - client_credentials
    - authorization_code
  clientIdGeneration:
    - by_app
```

## Declaração por Operação

Cada operação de capability DEVE documentar explicitamente:

- Se a operação é pública ou protegida
- Qual escopo é necessário quando a operação é protegida
- Qual participante deve apresentar a credencial

Essa declaração aparece na definição da operação, com referência a esta seção.

## Relação com as Capabilities

A autenticação protege recursos e operações expostos pelas capabilities como Merchant, Orders e Logistics. Algumas operações do protocolo (como o próprio endpoint de Discovery) são públicas. A maioria das interações produtivas requer autenticação.

A autenticação não define lógica de coordenação de negócio. É um pré-requisito para acesso às capabilities.
