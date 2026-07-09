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
│   └── Bindings REST (documentação de transporte complementar)
│
└── 3. REFERÊNCIA DA API (OpenAPI + ReDoc)
    ├── Infraestrutura (Discovery, Autenticação)
    └── Capabilities (Merchant, Orders, Logistics, Customer, Indoor)
```

## Notes

- **Protocol-first:** regras e papéis vivem em Protocolo; HTTP/OpenAPI em Referência.
- **Extensões** dependem da capability pai e são declaradas no Discovery.
- **ReDoc** é o renderer da referência OpenAPI (Scalar não é usado no site).
- Atas de comitê em `docs/reference/v2/comites/` ficam no repositório mas **não** entram no site (`exclude_docs`).
