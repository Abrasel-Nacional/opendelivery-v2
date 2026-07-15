# Guia para próximas mudanças na documentação

Consolidado a partir de 3 sessões de trabalho (reescrita de Orders/Merchant/Customer,
reestruturação do site, piloto Indoor Guia↔API Spec). Objetivo: não perder decisões já
fechadas nem repetir os mesmos erros técnicos. Regras estruturais completas continuam em
**`AGENTS.md`** (idioma) e **`STRUCTURE.md`** (modelo Guia · Protocolo · API Spec, checklist
por capability) — este arquivo é o resumo operacional + o que ainda falta.

## 1. Status por capability

| Capability | Reescrita padrão Orders/Indoor | Piloto Guia↔API Spec (auto-suficiente + exemplos) | Pendências |
|---|---|---|---|
| **Orders** | ✅ | Não | Backlog em `artifacts/orders-v2-backlog.md` (itens 1, 3–7) |
| **Indoor** | ✅ | ✅ (é o piloto/template) | Nenhuma conhecida; serve de modelo para replicar |
| **Merchant** | ✅ | Não | Aplicar o padrão do piloto Indoor (exemplos JSON, call-flow cards, External docs) |
| **Customer** (+ Reviews/Loyalty) | ✅ | Não | Idem; revisar nomenclatura (nunca "CRM") ao expandir exemplos |
| **Logistics** | Parcial (regra de duplicidade replicada) | Não | Não passou pela reescrita completa no padrão Orders |
| **Discovery / Authentication** | — | Não | Já têm admonition de topo + Relacionado; não passaram pelo piloto de exemplos |

**Ordem de trabalho combinada:** Orders → Merchant → Logistics → Customer (ver `STRUCTURE.md`).
O próximo passo natural é aplicar o **piloto Indoor** (exemplos JSON completos, call-flow
cards, tag External docs) em **Orders**, depois Merchant/Logistics/Customer.

## 2. Decisões fechadas — não reabrir sem motivo novo

Coisas que já foram debatidas e decididas; se surgir de novo, tratar como confirmado, não
como pergunta em aberto:

- **Sem `POST /orders`**: entrada de pedido é só via evento `CREATED` + `GET`.
- **Orders é obrigatória só para Indoor.** Merchant, Logistics e Customer funcionam sozinhas.
- **Customer nunca é "CRM"** no nome da capability (PT descritivo: "dados do cliente"). CRM é
  tipo de software que consome a capability. Reviews e Loyalty são **módulos** de Customer,
  não extensões — dá para implementar só um dos dois.
- **Cancelamento (Orders)**: dois fluxos distintos, não um só.
  - **Merchant → OA**: handshake via `POST /requestCancellation` (mantido da v1). `202` ≠
    cancelado. Aceito → `CANCELLATION_REQUEST_ACCEPTED` (status inalterado) → depois
    `CANCELLED`. Recusado → `CANCELLATION_REQUEST_DENIED`.
  - **OA → Merchant**: só **mandatório**, sem handshake — evento/status `CANCELLED` direto.
- **`DISPATCHED`**: não foi removido (ata de comitê não fechou isso). Fica como `MAY` em
  DELIVERY, `MUST NOT` em TAKEOUT/INDOOR, com nota de possível depreciação futura. Não
  remover sem nova decisão de comitê.
- **`X-Request-Id` / idempotência por header: não existe.** Foi removido de propósito (não
  tinha base em ata — provável invenção de sessão de IA anterior). Regra vigente: chamada
  duplicada em estado já atingido → **`202`** (não 422/409); só usar 409 se a transição for
  **impossível**. Sem flag no Discovery para isso.
- **Sem "transport binding"**: não reintroduzir a ideia de protocolo agnóstico + binding REST
  separado. Modelo é Guia (onboarding) · Protocolo (narrativa de domínio) · API Spec (única
  fonte normativa).
- **Terminologia**: no texto de produto, nunca "ReDoc" (é só o renderizador) e nunca
  "OpenAPI" solto — usar "especificação da API" / "API Spec". "OpenAPI" como formato técnico
  só aparece em `docs/reference/index.md` (nota de formato) e em arquivos técnicos
  (`*.openapi.yaml`, `AGENTS.md`).
- **Navegação não é linear**: sem rodapé Anterior/Próximo do MkDocs, sem blocos de "próximo
  passo" empurrando para outra página no topo. Padrão único: bloco **"Relacionado"**
  (`.od-related`) no fim da página, e um admonition no topo das capabilities/Discovery/Auth
  apontando para a spec.
- **Orders sempre em primeiro** nos menus, landing e índices de referência.

## 3. Processo para reescrever/atualizar uma capability

Sequência que funcionou nas 3 capabilities já feitas (Orders, Merchant, Customer):

1. Ler o estado atual: guia + spec da capability + a capability já feita mais parecida
   (Indoor é o template canônico).
2. Ler `docs/reference/v1/openapi.yaml` na área equivalente (fonte de comportamento legado).
3. Buscar nas atas (`docs/reference/v2/comites/*.pdf`) menções ao tema — **não inventar
   regra normativa sem base de ata**. Se não achar nada, dizer isso explicitamente em vez de
   assumir.
4. Montar plano (modo Plan) e pedir aprovação antes de editar em massa.
5. Implementar: primeiro a API Spec (fonte normativa), depois o guia (PT+EN), depois cascas
   de referência (`docs/reference/{cap}.md` + `.en.md`), depois nav/landing/migration/changelog.
6. `python -m mkdocs build --strict` antes de reportar como concluído.
7. Se o usuário aprovar mudança de regra de negócio no meio (ex.: cancelamento), reabrir só o
   trecho afetado — não refazer a capability inteira.

Para levar uma capability ao nível do piloto **Indoor** (auto-suficiência + exemplos), seguir
o checklist já escrito em `STRUCTURE.md` → "Checklist ao editar uma capability".

## 4. Gotchas técnicos recorrentes (ReDoc / mkdocs)

Coisas que já custaram várias idas e vindas — verificar antes de "consertar de novo":

- **`overrides/**` não tem hot-reload.** `mkdocs serve` só observa `docs/` e `mkdocs.yml`.
  Qualquer mudança em `overrides/redoc.html`, `overrides/main.html` etc. exige **reiniciar o
  serve**, senão parece que "não fez efeito".
- **ReDoc escapa HTML dentro de `description`.** Não dá pra injetar `<div>` direto num campo
  de descrição OpenAPI esperando que renderize. Usar fence customizado (estilo Mermaid, ex.
  \`\`\`od-call-flow\`\`\`) processado por JS depois do render — é o padrão já implementado em
  `overrides/redoc.html` para os cards Client/Host.
- **Exemplos que não aparecem no painel JSON:** verificar se o `value:` do `examples:` não
  ficou `null` com os campos "vazados" para fora dele (bug comum de scripts de edição em
  massa via `yaml.dump`). O ReDoc só lê o que está dentro de `example.value`.
- **YAML EN da spec resolvido errado sob `/en/`:** o front matter `openapi_spec: ../v2/x.yaml`
  é relativo à URL da página; sem normalização, a versão `/en/reference/x/` tentava carregar
  `/en/reference/v2/x.yaml` (404), porque o i18n não duplica os `.openapi.yaml` por locale. Já
  corrigido no `redoc.html` removendo `/en` do path antes de resolver — não reintroduzir o
  problema ao mexer nesse trecho.
- **Sync do menu lateral do ReDoc é frágil.** Forçar `top`/`height`/`overflow` no
  `.menu-content`, ou somar `scroll-margin-top` no conteúdo **junto** com o `scrollYOffset` do
  ReDoc, causa dessincronia (clique expande o item errado, ou highlight fica atrasado). O
  ReDoc já cuida de posição/scroll-spy sozinho — só estilizar (cor, fonte, borda), não
  reimplementar o scroll.
- **Bulk find-replace em `.md` pode quebrar admonitions.** Colapsar espaços múltiplos
  (`  +` → um espaço) destrói a indentação de 4 espaços exigida pelo corpo de `!!! tip` /
  `!!! warning` do Material. Depois de qualquer substituição em massa por regex, checar
  admonitions especificamente.

## 5. Backlog aberto

- **Orders** (`artifacts/orders-v2-backlog.md`): itens 1 (matriz eventos/status), 3
  (descrição de campos), 4 (payload V2), 5 (tracking vs Logistics), 6 (remover `conclude`?),
  7 (diff normativo V1↔V2). Ordem sugerida: 1 → 6 → 5 → 3+4 → 7.
- **Aplicar o piloto Indoor** (exemplos JSON completos, call-flow cards, tag External docs,
  auto-suficiência) em **Merchant**, **Logistics** e **Customer**.
- **`DISPATCHED`**: aguardando confirmação final do comitê sobre depreciação (não decidir
  sozinho na doc).
