# Open Delivery Protocol v2 — Documentation Structure

## Hierarchy (published site)

```
Open Delivery Protocol v2
├── 1. GUIA
│ ├── Início (landing)
│ ├── Primeiros Passos
│ ├── Trilhas por papel
│ ├── Conceitos
│ ├── Visão Geral do Protocolo
│ ├── Papéis e Responsabilidades
│ └── Migração e Histórico (Changelog, V1→V2, Roadmap)
│
├── 2. PROTOCOLO
│ ├── Fundamentos (princípios, fluxos, evolução)
│ ├── Infraestrutura (Discovery, Autenticação) — narrativa de domínio
│ ├── Capabilities
│ │ ├── Merchant
│ │ │ ├── Visão geral
│ │ │ ├── Dados da Loja
│ │ │ └── Menus
│ │ ├── Orders / Pedidos
│ │ │ └── Indoor / Salão (extensão)
│ │ ├── Logística
│ │ └── Customer
│ │ ├── Reviews (módulo)
│ │ └── Loyalty (módulo)
│
└── 3. REFERÊNCIA DA API (especificação da API) — fonte normativa
 ├── Convenções (regras gerais, tratamento de erros)
 ├── Infraestrutura (Discovery, Autenticação)
 └── Capabilities (Merchant, Orders, Logistics, Customer, Indoor)
```

## Notes

- **Sem transport binding:** não há camada “protocolo agnóstico + binding REST”. O contrato implementável é a **especificação da API**.
- **Camadas:** Guia = onboarding; Protocolo = domínio (explicativo); API = norma de implementação.
- **Header:** mega-menu em colunas no Protocolo (Fundamentos · Infra · Capabilities); subpáginas (Menus, Indoor…) só na **sidebar**.
- **Extensões** (ex.: Indoor) dependem da capability pai e são declaradas no Discovery. **Reviews** e **Loyalty** são módulos de Customer, não extensões.
- **`docs/transport-bindings/**`** é legado pré- e **não** entra no site (`exclude_docs`).
- Atas de comitê em `docs/reference/v2/comites/` ficam no repositório mas **não** entram no site.

## Modelo Guia ↔ especificação da API (capabilities)

Padrão híbrido (piloto: **Indoor**; replicar nas demais capabilities):

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| **Guia de domínio** | `docs/protocol/{capability}.md` | Visão geral, papéis, conceitos, fluxos Mermaid, checklists, mapa ops → especificação da API, fora do MVP — **não** é fonte normativa de campos |
| **especificação da API** | `docs/reference/v2/{capability}.openapi.yaml` | Normativa auto-suficiente **em inglês**: endpoints, campos, MUST/MAY, erros, **exemplos JSON**, webhooks |
| **Casca ** | `docs/reference/{capability}.md` (+ `.en.md`) | Front matter `template: redoc.html` + callout ligando ao guia (nota de idioma) |

### Regras

1. **especificação da API se basta** — quem só abre o consegue implementar (exemplos em request/response/schemas). Em divergência com o Markdown de Protocolo, **prevalece a especificação da API**.
2. **Protocolo é auxiliar** — não é fonte normativa de campos; evita tabelas de schema longas (linka para a spec).
3. **Cruzamento obrigatório**
 - Protocolo → callout + tabela “objetivo → operationId” + próximo passo para.
 - especificação da API → `info.externalDocs` / tags External docs para o guia e specs irmãs (Orders, Auth, Discovery).
4. **Fora do MVP** — temas em debate no comitê ficam explícitos (não se tornam normativos “por acaso”).
5. **Atas** em `docs/reference/v2/comites/` orientam decisões; não inventar regras sem base.

### Call flow card (endpoints)

 **escapes raw HTML** in descriptions. Use a fenced block processed by JS in `overrides/redoc.html`:

````markdown
```od-call-flow
method: GET
from: Ordering Application
fromLabel: Client
fromParty: oa
to: Software Service
toLabel: Host
toParty: ss
```
````

- **OA → SS** (normal): Client = Ordering Application, Host = Software Service
- **SS → OA** (webhook): reverse parties (adds `od-call-flow--webhook` styling)

### Checklist ao editar uma capability

- [ ] Guia de domínio **PT + EN** (`page.md` e `page.en.md`): callout de camadas, Discovery, mapa ops, fora do MVP
- [ ] especificação da API **somente EN**: exemplos em todas as operações e schemas-chave
- [ ] especificação da API: tag **External docs** no grupo Overview (não `info.externalDocs` solto)
- [ ] especificação da API: `.od-call-flow` em cada operação (hosts/calls + method)
- [ ] especificação da API: eventos com obrigatoriedade MUST/MAY alinhada ao guia de domínio
- [ ] `reference/{capability}.md` + `.en.md`: callout para o guia + “especificação da API always English”
- [ ] Sem linguagem de “transport binding” / protocolo agnóstico de transporte
- [ ] `python -m mkdocs build --strict`

### Ordem de capabilities (nav, landing, indexes)

**Orders sempre em primeiro** entre as capabilities de domínio (antes de Merchant, Logistics, Customer). Indoor permanece sob Orders como extensão.

Ordem de trabalho de documentação: Orders → Merchant → Logistics → Customer (e extensões Reviews/Loyalty).

## i18n (PT + EN)

Plugin: **mkdocs-static-i18n** (`docs_structure: suffix`).

| Locale | Arquivos | URL |
|--------|----------|-----|
| **pt** (default) | `page.md` | `/…` |
| **en** | `page.en.md` | `/en/…` |

- `fallback_to_default: true` — se faltar `.en.md`, o EN reutiliza o PT (temporário).
- **especificação da API contracts:** **always English** (`docs/reference/v2/*.openapi.yaml`). No exceptions per capability.
- **Guides / protocol pages:** **bilingual** — PT default (`page.md`) + EN (`page.en.md`).
- **Não traduzir** nomes de schemas, campos, enums, eventos, paths nem tokens de protocolo nos exemplos JSON.
- Nav EN via `nav_translations` no `mkdocs.yml`.
- `navigation.instant` desativado (incompatível com language switcher).
- Full language rules: see **`AGENTS.md`**.

### Como adicionar uma página bilingue

1. Criar/editar `docs/path/page.md` (PT).
2. Criar `docs/path/page.en.md` (EN) com a mesma estrutura de âncoras/links relativos.
3. Manter identificadores técnicos em inglês nos dois arquivos.
4. Incluir na `nav` (título PT); traduzir título em `nav_translations` se necessário.
5. `python -m mkdocs build --strict`.
