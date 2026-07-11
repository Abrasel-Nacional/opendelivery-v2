# Open Delivery Protocol v2 — Documentation Structure

## Hierarchy (published site)

```
Open Delivery Protocol v2
├── 1. GUIA
│   ├── Início (landing)
│   ├── Primeiros Passos
│   ├── Trilhas por papel
│   ├── Conceitos
│   ├── Visão Geral do Protocolo
│   ├── Protocolo vs Binding
│   ├── Papéis e Responsabilidades
│   └── Migração e Histórico (Changelog, V1→V2, Roadmap)
│
├── 2. PROTOCOLO
│   ├── Fundamentos (princípios, regras, erros, fluxos, evolução)
│   ├── Infraestrutura (Discovery, Autenticação)
│   ├── Capabilities
│   │   ├── Merchant
│   │   │   ├── Visão geral
│   │   │   ├── Dados da Loja
│   │   │   └── Menus
│   │   ├── Orders / Pedidos
│   │   │   └── Indoor / Salão (extensão)
│   │   ├── Logística
│   │   └── Customer / CRM
│   │       ├── Reviews (extensão)
│   │       └── Loyalty / Fidelidade (extensão)
│
└── 3. REFERÊNCIA DA API (OpenAPI + ReDoc)
    ├── Infraestrutura (Discovery, Autenticação)
    └── Capabilities (Merchant, Orders, Logistics, Customer, Indoor)
```

## Notes

- **Protocol-first:** regras e papéis vivem em Protocolo; contrato HTTP em **Referência** (ReDoc).
- **Header:** mega-menu em colunas no Protocolo (Fundamentos · Infra · Capabilities); subpáginas (Menus, Indoor…) só na **sidebar**.
- **Extensões** dependem da capability pai e são declaradas no Discovery.
- **Bindings REST** (`docs/transport-bindings/`) são legado pré-ReDoc e **não** entram no site (`exclude_docs`).
- Atas de comitê em `docs/reference/v2/comites/` ficam no repositório mas **não** entram no site.

## Modelo Guia ↔ OpenAPI (capabilities)

Padrão híbrido (piloto: **Indoor**; replicar nas demais capabilities):

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| **Guia** | `docs/protocol/{capability}.md` | Visão geral, papéis, conceitos, fluxos Mermaid, checklists, Discovery, mapa ops → OpenAPI, fora do MVP |
| **OpenAPI** | `docs/reference/v2/{capability}.openapi.yaml` | Normativa auto-suficiente **em inglês**: endpoints, campos, MUST/MAY, erros, **exemplos JSON**, webhooks |
| **Casca ReDoc** | `docs/reference/{capability}.md` (+ `.en.md`) | Front matter `template: redoc.html` + callout ligando ao guia (nota de idioma) |

### Regras

1. **OpenAPI se basta** — quem só abre o ReDoc consegue implementar (exemplos em request/response/schemas).
2. **Guia é auxiliar** — não é fonte normativa de campos; evita tabelas de schema longas (linka para a spec).
3. **Cruzamento obrigatório**
   - Guia → callout + tabela “objetivo → operationId” + próximo passo para ReDoc.
   - OpenAPI → `info.externalDocs` + links no `info.description` / tags para o guia e specs irmãs (Orders, Auth, Discovery).
4. **Fora do MVP** — temas em debate no comitê ficam explícitos (não se tornam normativos “por acaso”).
5. **Atas** em `docs/reference/v2/comites/` orientam decisões; não inventar regras sem base.

### Call flow card (endpoints)

ReDoc **escapes raw HTML** in descriptions. Use a fenced block processed by JS in `overrides/redoc.html`:

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

Same idea as the old Hosted/Called table; reusable for all capabilities.

### Checklist ao editar uma capability

- [ ] Guia **PT + EN** (`page.md` e `page.en.md`): callout de camadas, Discovery, mapa ops, fora do MVP
- [ ] OpenAPI **somente EN**: exemplos em todas as operações e schemas-chave
- [ ] OpenAPI: tag **External docs** no grupo Overview (não `info.externalDocs` solto)
- [ ] OpenAPI: `.od-call-flow` em cada operação (hosts/calls + method)
- [ ] OpenAPI: eventos com obrigatoriedade MUST/MAY alinhada ao guia
- [ ] `reference/{capability}.md` + `.en.md`: callout para o guia + “OpenAPI always English”
- [ ] `python -m mkdocs build --strict`

### Ordem sugerida (pós-Indoor)

Orders → Merchant → Logistics → Customer (e extensões Reviews/Loyalty).

## i18n (PT + EN)

Plugin: **mkdocs-static-i18n** (`docs_structure: suffix`).

| Locale | Arquivos | URL |
|--------|----------|-----|
| **pt** (default) | `page.md` | `/…` |
| **en** | `page.en.md` | `/en/…` |

- `fallback_to_default: true` — se faltar `.en.md`, o EN reutiliza o PT (temporário).
- **OpenAPI / ReDoc contracts:** **always English** (`docs/reference/v2/*.openapi.yaml`). No exceptions per capability.
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
