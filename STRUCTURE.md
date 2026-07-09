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

## i18n (PT + EN)

Plugin: **mkdocs-static-i18n** (`docs_structure: suffix`).

| Locale | Arquivos | URL |
|--------|----------|-----|
| **pt** (default) | `page.md` | `/…` |
| **en** | `page.en.md` | `/en/…` |

- `fallback_to_default: true` — se faltar `.en.md`, o EN reutiliza o PT (temporário).
- **OpenAPI / ReDoc:** sempre **inglês**; YAML compartilhado em `docs/reference/v2/`.
- **Não traduzir** nomes de schemas, campos, enums, eventos, paths nem exemplos JSON (iguais à spec).
- Nav EN via `nav_translations` no `mkdocs.yml`.
- `navigation.instant` desativado (incompatível com language switcher).

### Como adicionar uma página bilingue

1. Criar/editar `docs/path/page.md` (PT).
2. Criar `docs/path/page.en.md` (EN) com a mesma estrutura de âncoras/links relativos.
3. Manter identificadores técnicos em inglês nos dois arquivos.
4. Incluir na `nav` (título PT); traduzir título em `nav_translations` se necessário.
5. `python -m mkdocs build --strict`.
