## User

eu quero que vc remova a opção 'Editar essa Página' de toda a documentação.

## Assistant

Vou localizar onde a opção "Editar essa Página" é configurada na documentação (provavelmente no MkDocs).

## Tools

- Search: edit
- Search: edit_uri|edit this page|Editar essa|repo_url|content.action
- ListDir: .

## Assistant

Encontrei a configuração no `mkdocs.yml`: a feature `content.action.edit` e o `edit_uri`. Vou removê-las.

## Tools

- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (141-170)
- Edit: C:\OpenDelivery\opendelivery-v2\mkdocs.yml

## Assistant

Pronto. Removi a opção **“Editar esta página”** de toda a documentação no `mkdocs.yml`:

1. **`content.action.edit`** — feature do Material for MkDocs que exibe o botão de edição
2. **`edit_uri`** — caminho do GitHub usado por esse botão

O link do repositório no header (ícone do GitHub) continua ativo via `repo_url`. Só o botão de editar a página some.

No próximo build (`mkdocs build` / deploy), a alteração vale para todas as páginas (PT e EN).

## User

essa versão que estamos lançando será uma release candidate. A ideia é que ela passe por um periodo de validação, onde será revisada pelas empresas e também algumas empresas farão um piloto da documentação. somente após isso a documentação entrará em release mesmo. eu preciso ter isso na documentação, tanto no guia quanto no protocolo, quanto na api. pode colocar aonde vc achar mais valido e com o texto que preferir, passando essa ideia

## Assistant

Vou mapear a estrutura do guia, protocolo e OpenAPI para inserir o aviso de Release Candidate nos pontos mais visíveis e consistentes.

## Tools

- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (1-80)
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.en.md (1-80)
- Read: C:\OpenDelivery\opendelivery-v2\docs\overview.md (1-80)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md (1-60)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md (1-60)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md (1-38)
- Search: status|version|draft|beta|release|RC|candidate|experimental
- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (1-50)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.md (1-80)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml (1-80)
- Search: ^info:|version:|title:|description:|x-
- Search: od-badge|admonition|!!! warning|!!! info|rc
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.en.md (1-38)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.en.md (1-30)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md (2-21)
- Execute: Get-ChildItem docs\protocol\*.md | Select-Object -ExpandProperty Name; Get-ChildItem docs\protocol\*.en.md -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name; Get-ChildItem docs\reference\v2\*.openapi.yaml | Select-Object -ExpandProperty Name; Get-ChildItem docs\reference\*.md | Select-Object -ExpandProperty Name (List protocol, reference and openapi files)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.md (80-119)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.en.md (1-100)
- Search: ^info:|version:
- Search: od-version-banner|od-badge--rc|admonition
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (251-324)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\guidelines.md (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\evolution.md (1-50)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (1-50)
- Search: od-version|od-badge
- Execute: Get-ChildItem docs\protocol\*.en.md -ErrorAction SilentlyContinue | Select-Object Name; Get-ChildItem docs\guide\*.md | Select-Object Name; Get-ChildItem docs\documentation\*.md | Select-Object Name (List EN protocol and guide files)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\merchant.openapi.yaml (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\authentication.openapi.yaml (1-30)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\discovery.openapi.yaml (1-30)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (1176-1215)
- Read: C:\OpenDelivery\opendelivery-v2\docs\documentation\roadmap.md (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\evolution.md (51-68)

## Assistant

Vou inserir o aviso de Release Candidate nos pontos de entrada do Guia, do Protocolo e da API (OpenAPI), reaproveitando o que já existe de versão RC.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\evolution.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\guidelines.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css

## Assistant

Agora incluo o aviso de RC em todas as specs OpenAPI.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\merchant.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\authentication.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\discovery.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\customer.openapi.yaml
- Search: landing\.css|theme\.css|hero-wrapper|max-width
- Search: extra_css|stylesheets
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css (1-80)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Execute: python -m mkdocs build --strict 2>&1 (Strict MkDocs build to verify docs)
- Execute: if (Test-Path .venv\Scripts\python.exe) { .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 } elseif (Test-Path venv\Scripts\python.exe) { .\venv\Scripts\python.exe -m mkdocs build --strict 2>&1 } else { pip show mkdocs-material mkdocs-static-i18n 2>&1; Get-ChildItem -Directory | Select-Object Name } (Find venv and run mkdocs build)
- Search: Release Candidate|validação com o ecossistema|ecosystem validation|V2\.0\.0-rc
- Search: id=\"v200|Release Candidate status|validação com o ecossistema

## Assistant

Pronto. A mensagem de **Release Candidate em validação** ficou espalhada de forma coerente nas três camadas da documentação.

### Guia
| Onde | O que |
|------|--------|
| **Landing** (`index.md` / `index.en.md`) | Banner RC logo após o hero |
| **Primeiros Passos** (PT + EN) | Aviso em destaque no topo |
| **Changelog** (PT + EN) | Seção “Status: validação com o ecossistema” com as 4 etapas (revisão → piloto → feedback → release) |

### Protocolo
| Onde | O que |
|------|--------|
| **Princípios** | Aviso no topo (entrada do protocolo) |
| **Regras Gerais** | Aviso curto com link para Evolução |
| **Evolução** | Tabela da versão atual + seção “O que significa o RC atual” (normativa) |

### API
| Onde | O que |
|------|--------|
| **Referência** (`reference/index` PT + EN) | Aviso no topo da seção |
| **Todas as 7 OpenAPI** | Bloco `## Release Candidate status` em inglês no `info.description` (aparece no ReDoc) |

Também alinhei as versões das specs que ainda estavam como `draft` / `rc1` para **`2.0.0-rc`**.

### Ideia do texto (em todas as camadas)
1. Isto é **RC**, não release estável  
2. Há um período de **validação** com o ecossistema  
3. Inclui **revisão por empresas** e **pilotos**  
4. Ainda pode haver **ajustes** com base no feedback  
5. Só depois disso vem a **release estável**  
6. A **V1 permanece ativa** na transição  

Build (`mkdocs build`) concluiu com sucesso.

## User

pegando as tendencias de mercado de ui / ux, deixe o Hero da home mais atual e moderno

## Assistant

Vou analisar o Hero atual (HTML + CSS) e modernizá-lo com padrões de UI/UX mais atuais.

## Tools

- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (1-50)
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.en.md (1-50)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css (1-250)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (1-50)
- Search: hero|landing-page|od-badge
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css (621-646)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (671-750)
- Read: C:\OpenDelivery\opendelivery-v2\overrides\main.html (1-80)
- Search: md-content|hide|toc|landing

## Assistant

Vou redesenhar o Hero com layout em duas colunas, mesh gradient sutil, tipografia display e painel visual das três camadas — alinhado a padrões atuais de sites de produto/docs.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (1-120)

## Assistant

Corrigindo o HTML e reescrevendo o CSS do hero.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-Object -Last 30 (Build docs to verify hero changes)
- Search: class=\"hero|hero__title|hero-panel
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (331-370)

## Assistant

Hero redesenhado com padrões atuais de UI/UX (docs/product sites tipo Linear, Stripe, Vercel).

### O que mudou

**Layout**
- Hero em **duas colunas**: copy à esquerda + painel visual à direita
- Card com borda suave, mesh gradient e grid sutil de fundo
- Orbs com blur animado leve (`prefers-reduced-motion` respeitado)

**Tipografia e hierarquia**
- Headline display maior, tracking negativo
- “food service” com **gradient text** na marca
- Copy enxuta (lede único em vez de tagline + body)

**Componentes modernos**
- Pills de eyebrow (RC com **dot pulsante** + “Protocolo aberto”)
- CTAs em **pill**, primary com sombra e seta animada no hover
- **Micro-stats** (3 camadas · 7 capabilities · RC)
- Painel estilo “window” com stack Guia → Protocolo → API (clicável)
- Nodes OA · POS · LOG simbolizando o ecossistema
- Status RC integrado no rodapé do hero (glass strip)

**Responsivo**
- ≤960px: empilha e mostra o painel em cima  
- ≤480px: esconde o painel e prioriza copy + CTAs full-width  

Arquivos: `docs/index.md`, `docs/index.en.md`, `docs/stylesheets/landing.css`. Build ok.

Se quiser, no próximo passo dá para empurrar o hero para **full-bleed** (borda a borda da viewport) ou deixar um modo dark sutil só no hero.

## User

pode deixar full-bleed. na imagem pode tirar aquelas tags OA - POS - LOG. o botão o que mudou na v2 ta sem borda. pode tirar aquelas numeros 3 camadas de doc, etcc.

## Assistant

Vou aplicar full-bleed no hero, remover os nodes OA/POS/LOG e as micro-stats, e corrigir a borda do botão ghost.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css (2-31)
- Search: hero__stats|hero-nodes|hero-btn--ghost|landing-page|\.hero 
- Search: md-main|md-content|md-grid|padding|max-width
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Search: hero__stats|hero-nodes|hero-btn--ghost
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-Object -Last 15 (Rebuild docs after hero tweaks)

## Assistant

Ajustes feitos:

1. **Full-bleed** — o hero vai de borda a borda da viewport (sem card arredondado; só a linha inferior)
2. **Tags OA / POS / LOG** — removidas do painel
3. **Botão “O que mudou na V2”** — borda visível (mesmo estilo dos outros CTAs)
4. **Micro-stats** (3 camadas, 7 capabilities, etc.) — removidas

PT e EN atualizados.

## User

nao gostei do full-bleed. eu achei que ele ia ocupar a area toda mas iria manter o menu.

## Assistant

Entendi — você quer o hero preenchendo a área de conteúdo, sem invadir a viewport e sem “escapar” do layout (menu/header intactos). Vou reverter o full-bleed de viewport e ajustar o hero para ocupar só a coluna principal.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (341-370)
- Search: md-content|md-main|md-grid|md-sidebar|navigation
- Search: md-content|md-main|md-typeset|md-grid|sidebar
- Read: C:\OpenDelivery\opendelivery-v2\site\index.html (2421-2470)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Search: \.hero__status
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Search: ^  <(div|section|hr|ul)
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-Object -Last 12 (Rebuild docs after hero layout fix)

## Assistant

Faz sentido — eu tinha expandido o hero para a **viewport inteira** (por cima do layout), e não era isso.

### O que ficou agora
- **Sem breakout** para `100vw` — o hero não “vaza” da página
- Ocupa **100% da coluna de conteúdo** do MkDocs
- **Header, tabs e menu lateral** permanecem no lugar
- Fundo/mesh e layout em duas colunas continuam, dentro do card da área principal

Resumindo: o hero preenche a área de conteúdo disponível, mas continua **dentro** do layout do site, com o menu intacto.

## User

eu prefiro o estilo do warning do release candidate de antes (fora da hero). pode voltar. o texto também. estava melhor explicado

## Assistant

Vou restaurar o banner RC fora do hero, com o texto mais completo de antes.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\landing.css

## Assistant

Pronto. O aviso de **Release Candidate** voltou **fora do hero**, no estilo do banner anterior (`od-version-banner`), com o texto mais completo:

- validação com o ecossistema  
- revisão por empresas e pilotos  
- release estável só depois  
- V1 permanece ativa na transição  
- link “Saiba mais” / “Learn more”  

PT e EN atualizados.

## User

no inicio iamos ter um conceito de protocolo com regras e definições o transport binding, que seria o rest. no fim não iremos seguir com esse modelo, ficando as regras e definições na spec openapi e apenas teriamos um guia (sem normativas).
esse conceito inicial ainda está refletido em varias partes da documentação, e tem um pagina inteira dedicada a isso que (PROTOCOL_VS_BINDING). Retire da doc inteira todo esse conceito de transport binding. agora é só guia e spec. um ponto importante, a tab 'Protocolo', que seria a parte do PROTOCOL, ainda é valida. talvez possamos passar a parte mais normativa para a tab da API. (Regras Gerais e Tratamento de Erros, por exemplo. isso é só uma sugestão.) Analise tudo o que falei antes de mudar algo e me de sua opiniao

## Assistant

Vou mapear onde o modelo “protocolo vs binding” ainda aparece na doc e na navegação, e só depois te devolvo a análise e a recomendação — sem mudar nada ainda.

## Tools

- Search: binding|Protocolo vs|protocol vs|transport|normativ|OpenAPI|guia|protocol
- Search: PROTOCOL_VS_BINDING|transport-binding|binding|protocol first|protocolo vs
- Read: C:\OpenDelivery\opendelivery-v2\docs\PROTOCOL_VS_BINDING.md (1-120)
- Read: C:\OpenDelivery\opendelivery-v2\STRUCTURE.md (1-124)
- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (18-117)
- Search: od-api-callout|binding|normativ|MUST|DEVE|OpenAPI|contrato
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\error-handling.md (1-50)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\guidelines.md (1-50)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\orders.md (1-12)
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (31-80)
- Read: C:\OpenDelivery\opendelivery-v2\AGENTS.md

## Assistant

## Análise (sem mudanças ainda)

Você está certo: o site ainda carrega **dois modelos ao mesmo tempo**.

### Modelo antigo (o que ainda “vaza”)
```
Protocolo (WHAT, agnóstico de tecnologia, normativo)
    ↓
Transport Binding REST (HOW)
    ↓
Implementação
```

### Modelo que vocês querem (e que o `STRUCTURE.md` / `AGENTS.md` **já descrevem em parte**)
```
Guia (onboarding, não normativo)
Protocolo (explicativo: conceitos, papéis, fluxos — não é fonte de campos)
OpenAPI (única fonte normativa: endpoints, MUST/MAY, erros, exemplos)
```

Ou seja: a **intenção nova** já está escrita nas regras do repositório; o **conteúdo publicado** ainda vende o modelo velho em vários pontos.

---

## Onde o “binding” ainda aparece

| Área | Situação |
|------|----------|
| **`PROTOCOL_VS_BINDING` (+ EN)** | Página inteira do modelo abandonado; está na nav do Guia e no path “Novo aqui” da home |
| **`docs/transport-bindings/**`** | Já legado e fora do site (`exclude_docs`) — ok, mas reforça o fantasma no repo |
| **`protocol/principles.md`** | “Neutralidade de transporte”, “bindings PODEM ser definidos separadamente”, “protocolo em primeiro lugar ≠ API” |
| **`overview` / `core-concepts`** | Falam em transport bindings e REST como camada separada |
| **Landing (3 camadas)** | “Protocolo = regras normativas independentes de framework” + “API = contrato REST” — eco do split |
| **Algumas páginas de capability** | Callouts e frases do tipo “regras aqui / contrato no binding HTTP” |
| **`IMPLEMENTATION_GUIDE.md` / `STRUCTURE.md`** | Ainda misturam “protocol-first + binding” com “guia ↔ OpenAPI” |

Há um **descompasso interno**: o `AGENTS.md` já diz que o guia **não** é normativo de campos e que o OpenAPI se basta; a tab Protocolo e a home ainda soam como **segunda especificação normativa**.

---

## Sobre a tab **Protocolo**

Concordo: **continua válida** e eu **não** renomearia/removo a tab.

Motivo: o produto *é* o Open Delivery **Protocol**. O problema não é a palavra “Protocolo”; é a ideia de que existe um **protocolo agnóstico + bindings alternativos**.

Papel saudável da tab Protocolo no modelo novo:

| Tab | Função |
|-----|--------|
| **Guia** | Entrar no ecossistema: primeiros passos, papéis, migração, changelog |
| **Protocolo** | Entender o *domínio*: ciclos de vida, fluxos, papéis, o que é status vs evento, o que cada capability resolve — **narrativa, sem ser “a lei”** |
| **API** | Implementar e validar conformidade: **única fonte normativa** |

Se a tab Protocolo continuar com tabelas de campo + DEVE/MUST em paralelo à OpenAPI, vocês mantêm **duas fontes de verdade** — pior que o modelo binding, porque o implementador não sabe qual mandar.

---

## Sua sugestão: Regras Gerais e Erros → tab API

**Concordo em espírito, com um cuidado.**

### Tratamento de Erros → API: **sim**
A página já é bem “transporte”:
- schema de erro
- códigos HTTP  
Isso **não** deveria viver como “protocolo agnóstico”. Destino natural: **OpenAPI** (`components.schemas` de erro + descrições) e, se quiserem, uma página curta sob **Referência da API** apontando para a spec.

### Regras Gerais → API: **parcial**
- O que é **MUST de interoperabilidade** (campos obrigatórios, tolerar campos extras, idempotência) → deve estar **na OpenAPI** (texto de `info` / security / convenções compartilhadas), não só em Markdown solto.
- O que é **como documentamos / como lemos a spec** → pode sumir ou virar nota de contribuidores.
- O que é **mental model** (não inferir transição, eventos ≠ comandos) → pode ficar no **Protocolo** em tom de guia (“como pensar”), sem pretender ser o contrato.

**Evitem** só “mover o `.md` para a nav da API” sem embutir a regra na OpenAPI: isso cria uma terceira prateleira (“Markdown normativo na API”) em vez de fechar o modelo.

### Princípios / Evolução
- **Princípios**: reescrever (tirar multi-binding e “transporte é escolha”). Manter abertura, papéis, eventos, evolução — como **design intent**, não como contrato de campos.
- **Evolução / versionamento / RC**: pode ficar no Protocolo ou no Guia; não precisa ir para a API.

---

## Opinião objetiva

1. **Remover o conceito de transport binding da doc publicada** — correto e necessário. A página `PROTOCOL_VS_BINDING` deve sair; o resto é limpeza de linguagem + âncoras.

2. **Não colapsar tudo em “só Guia + API”** se isso significar matar a tab Protocolo. O que vocês querem, na prática, é:
   - **Guia** = onboarding  
   - **Protocolo** = *guia de domínio* (ainda chamado Protocolo)  
   - **API** = norma  

   Ou seja: “só guia e spec” no sentido de **não há binding layer**, não no sentido de “só duas tabs”.

3. **Fonte normativa única = OpenAPI.** Qualquer DEVE/MUST que importe para implementação deve estar (ou migrar para) a spec. Markdown do Protocolo deixa de competir.

4. **Mover Erros (e parte das Regras Gerais) para a órbita da API** — boa direção; o passo “certo” é **codificar na OpenAPI**, com página de apoio se fizer falta.

5. **Não fazer isso em um PR monstro de reescrita de todas as capabilities.** Ordem que eu faria:

| Fase | O quê |
|------|--------|
| **A – IA / estrutura** | Tirar `PROTOCOL_VS_BINDING` da nav e da home; limpar landing/STRUCTURE/AGENTS; language pass (“binding”, “agnóstico de transporte”, “protocol-first ≠ API”) |
| **B – Fundamentos** | Reescrever princípios; reposicionar Regras Gerais e Erros (API/OpenAPI vs guia) |
| **C – Capabilities** | Por capability: Protocolo vira visão + fluxos + checklist; schema/MUST só na OpenAPI (Indoor já é o piloto do `STRUCTURE.md`) |

---

## Risco a não subestimar

Hoje várias páginas de `protocol/*` **ainda são semi-normativas** (tabelas de campo, DEVE em fluxo). Se só apagarmos “binding” e mantivermos isso, o leitor continua com duas leis. A limpeza de binding e a **despromoção do Protocolo a guia de domínio** precisam andar juntas, senão a mensagem fica incoerente.

---

## Recomendação de posicionamento (uma frase)

> **Open Delivery é um protocolo de interoperabilidade expresso como contrato OpenAPI (REST/HTTP). O site explica o domínio (Guia + Protocolo) e define a conformidade na Referência da API — sem camada separada de transport binding.**

Se isso estiver alinhado com o que você quer, no próximo passo eu executo a **Fase A** (remoção da página e varredura de menções) e te proponho o diff concreto de nav + textos da home/princípios antes de mexer em Erros/Regras Gerais.

## User

pode implementar o A e B. as capabilities vamos revisar uma a uma

## Assistant

Implementando as fases A e B: mapeando todas as menções a binding e o estado atual dos fundamentos.

## Tools

- Search: PROTOCOL_VS_BINDING|transport.?binding|Transport Binding|protocol vs|Protocolo vs|bindings? de transporte|agnóstico|protocol-first|Neutralidade de Transporte|escolhas de implementação
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\error-handling.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\guidelines.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\documentation\core-concepts.md
- Search: guidelines|error-handling|PROTOCOL_VS_BINDING|protocol/principles|modelo híbrido|protocolo vs
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (89-148)
- Read: C:\OpenDelivery\opendelivery-v2\docs\overview.en.md (166-235)
- Read: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md (1-120)
- Read: C:\OpenDelivery\opendelivery-v2\README.md (71-120)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\flows.md (51-65)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\roles-and-responsibilities.md (1-40)
- Search: PROTOCOL_VS_BINDING|guidelines|error-handling|transport.binding|Protocolo vs
- Execute: Remove-Item -Force "docs\PROTOCOL_VS_BINDING.md","docs\PROTOCOL_VS_BINDING.en.md" -ErrorAction Stop; Write-Output "deleted" (Delete PROTOCOL_VS_BINDING pages)

## Assistant

Implementando as mudanças estruturais e o conteúdo das fases A e B.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\mkdocs.yml
- Edit: C:\OpenDelivery\opendelivery-v2\mkdocs.yml
- Edit: C:\OpenDelivery\opendelivery-v2\mkdocs.yml
- Edit: C:\OpenDelivery\opendelivery-v2\mkdocs.yml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md
- Execute: Remove-Item -Force "docs\protocol\guidelines.md","docs\protocol\error-handling.md" -ErrorAction Stop; Write-Output "deleted old protocol files" (Remove old protocol guidelines and errors)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\documentation\core-concepts.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\flows.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\extensions\reviews.md
- Edit: C:\OpenDelivery\opendelivery-v2\STRUCTURE.md
- Edit: C:\OpenDelivery\opendelivery-v2\AGENTS.md
- Edit: C:\OpenDelivery\opendelivery-v2\README.md
- Read: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md (101-150)
- Read: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md (301-360)
- Read: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md (341-360)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\roles-and-responsibilities.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Edit: C:\OpenDelivery\opendelivery-v2\IMPLEMENTATION_GUIDE.md
- Read: C:\OpenDelivery\opendelivery-v2\README_SPEC.md (1-80)
- Edit: C:\OpenDelivery\opendelivery-v2\README_SPEC.md
- Search: PROTOCOL_VS_BINDING|transport.?binding|protocol/guidelines|protocol/error-handling|Bindings de Transporte|Neutralidade de Transporte|Protocolo vs
- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (18-127)
- Read: C:\OpenDelivery\opendelivery-v2\README_SPEC.md (71-290)
- Edit: C:\OpenDelivery\opendelivery-v2\README_SPEC.md
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-Object -Last 40 (Strict MkDocs build to verify nav and pages)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\documentation\core-concepts.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "WARNING|ERROR|unrecognized|built|INFO    -  Doc" (Rebuild and filter warnings)

## Assistant

Fases **A** e **B** implementadas. Capabilities ficam para revisão uma a uma, como combinado.

### Fase A — remover o modelo binding
- **Removidos** `PROTOCOL_VS_BINDING.md` / `.en.md` e da nav
- **Home** (PT/EN): 3 camadas reescritas (Guia · Protocolo domínio · API normativa); link antigo trocado por “Contrato da API”
- **overview**, **core-concepts**, **flows**, **indoor**, **reviews**: sem “transport binding”
- **STRUCTURE.md**, **AGENTS.md**, **README**, **README_SPEC**, **IMPLEMENTATION_GUIDE**: modelo Guia · Protocolo · OpenAPI

### Fase B — fundamentos + API
- **Princípios** reescritos: sem multi-binding; deixa claro que **OpenAPI prevalece**
- **Regras Gerais** e **Tratamento de Erros** saíram de Protocolo e foram para **Referência da API → Convenções**
  - `reference/conventions.md` (+ EN)
  - `reference/error-handling.md` (+ EN)
  - Tom de resumo; norma = OpenAPI
- **Nav Protocolo / Fundamentos** agora: Princípios · Fluxos · Evolução
- Links em **getting-started** atualizados

### O que **não** mexemos (de propósito)
- Páginas de capability em `protocol/*` (Orders, Merchant, etc.) — ainda podem ter tabelas/MUST; revisão capability a capability
- Pasta legada `docs/transport-bindings/**` (continua excluída do site)

### Posicionamento vigente
| Tab | Papel |
|-----|--------|
| **Guia** | Onboarding |
| **Protocolo** | Domínio (explicativo) |
| **API** | Contrato normativo OpenAPI + convenções transversais |

Build `mkdocs` ok. Quando quiser, começamos a capability (sugestão: **Orders** ou **Indoor** como piloto).

## User

arrume a tab api do menu, deixe 3 colunas só, coloque convenções na primeira coluna

## Assistant

Vou localizar como o mega-menu da tab API monta as colunas e ajustar para 3 colunas, com Convenções na primeira.

## Tools

- Search: mega|dropdown|column|Referência|nav|tab|Conven
- ListDir: \overrides
- Read: C:\OpenDelivery\opendelivery-v2\overrides\main.html (241-460)

## Assistant

O mega-menu cria uma coluna por item de 1º nível; com “Visão Geral” solta ficavam 4. Vou reestruturar a nav da API em 3 grupos, com Convenções (incluindo Visão Geral) na primeira coluna.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\mkdocs.yml
- Edit: C:\OpenDelivery\opendelivery-v2\overrides\main.html
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "WARNING|ERROR|unrecognized|built|Translated" (Build site to verify API nav mega-menu)

## Assistant

Ajustado. O mega-menu da API fica com **3 colunas**:

1. **Convenções** — Visão Geral · Regras gerais · Tratamento de Erros  
2. **Infraestrutura** — Discovery · Autenticação  
3. **Capabilities** — Merchant · Pedidos (+ Indoor) · Logística · Customer  

A “Visão Geral” saiu de item solto no 1º nível (isso gerava a 4ª coluna) e entrou em **Convenções**. O JS do mega-menu também limita a no máximo **3** colunas.

## User

a parte de idempotencia não lembro de ter sido discutida nos comites, principalmente o x-request-id. vc pode verificar nas atas dos comites na pasta dos comites

## Assistant

Vou procurar nas atas dos comitês menções a idempotência e `X-Request-Id`.

## Tools

- ListDir: \docs\reference\v2\comites
- Search: idempot|X-Request-Id|request.?id|idempoten|X-Request
- Search: idempot|X-Request-Id|request.?id|idempoten

## Assistant

O grep não indexou bem os PDFs. Vou extrair e buscar o texto das atas.

## Tools

- Execute: .\.venv\Scripts\python.exe -c "import importlib; mods=['pypdf','PyPDF2','pdfminer','fitz'];
[print(m, bool(importlib.util.find_spec(m))) for m in mods]" (Check available PDF libraries)
- Execute: .\.venv\Scripts\python.exe -c "import importlib.util as u; mods=['pypdf','PyPDF2','pdfminer','fitz','pdfplumber'];
[print(m, bool(u.find_spec(m))) for m in mods]" (Check PDF Python packages in venv)
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
from pypdf import PdfReader
import re

root = Path(r'docs/reference/v2/comites')
patterns = re.compile(
    r'idempot|X-Request-Id|X-Request-ID|request[-_ ]?id|Idempot|identificador de requisi|request id|correlation',
    re.I
)
hits = []
empty = []
errors = []
for pdf in sorted(root.glob('*.pdf')):
    try:
        reader = PdfReader(str(pdf))
        text = '\n'.join((p.extract_text() or '') for p in reader.pages)
        if not text.strip():
            empty.append(pdf.name)
            continue
        for m in patterns.finditer(text):
            start = max(0, m.start() - 120)
            end = min(len(text), m.end() + 180)
            snippet = re.sub(r'\s+', ' ', text[start:end]).strip()
            hits.append((pdf.name, m.group(0), snippet))
    except Exception as e:
        errors.append((pdf.name, str(e)))

print('=== HITS', len(hits), '===')
for name, term, snip in hits:
    print('---')
    print('FILE:', name)
    print('TERM:', term)
    print('CTX:', snip)
print('=== EMPTY TEXT', len(empty), '===')
for n in empty[:15]:
    print(n)
if len(empty) > 15:
    print('... +', len(empty)-15)
print('=== ERRORS', len(errors), '===')
for n,e in errors:
    print(n, e)
"@
 (Search all committee PDFs for idempotency terms)
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
from pypdf import PdfReader
import re

pdf = Path(r'docs/reference/v2/comites') / '[Ata de Reunião] 26.03.2026 - Comitê Arquitetura - docx.pdf'
# find exact file
files = list(Path(r'docs/reference/v2/comites').glob('*26.03.2026*Arquitetura*'))
print('files', [f.name for f in files])
reader = PdfReader(str(files[0]))
text = '\n'.join((p.extract_text() or '') for p in reader.pages)
print(text)
"@
 (Extract full text of 26.03.2026 Architecture minutes)
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
from pypdf import PdfReader
import re

root = Path(r'docs/reference/v2/comites')
patterns = re.compile(
    r'duplic|retentat|retry|X-Request|header|cabeçal|202 Accepted|idempot|request[- ]id|correlation|rastreio de requisi',
    re.I
)
hits = []
for pdf in sorted(root.glob('*.pdf')):
    reader = PdfReader(str(pdf))
    text = '\n'.join((p.extract_text() or '') for p in reader.pages)
    for m in patterns.finditer(text):
        # only keep if near async/confirm/error/header context might be many - filter X-Request and idempot and request id tightly; for duplic keep if near chamad or evento
        term = m.group(0)
        start = max(0, m.start() - 80)
        end = min(len(text), m.end() + 120)
        snip = re.sub(r'\s+', ' ', text[start:end]).strip()
        if term.lower() in ('duplic',) or term.lower().startswith('duplic'):
            if not re.search(r'chamad|evento|pedido|confirm|requisi|post|retry|retent', snip, re.I):
                continue
        hits.append((pdf.name, term, snip))

# dedupe by file+term+approx
print('=== RELATED HITS', len(hits), '===')
seen=set()
for name, term, snip in hits:
    key=(name, term.lower(), snip[:60])
    if key in seen: continue
    seen.add(key)
    print('---')
    print('FILE:', name)
    print('TERM:', term)
    print('CTX:', snip)
"@
 (Broader search for retry/duplicate/header in minutes)

## Assistant

## Resultado da busca nas atas

Varri **todas as 57 atas PDF** em `docs/reference/v2/comites/` (texto extraído com `pypdf`).

### `X-Request-Id`
**Nenhuma menção** em nenhuma ata — nem como header, nem como “request id” de idempotência de cliente, nem “correlation id” com esse sentido.

Ou seja: o trecho das convenções sobre mutações + `X-Request-Id` **não tem base em comitê**. Entra no doc via material legado (`transport-bindings`, exemplos Indoor) e pela página de convenções, sem decisão registrada.

### Idempotência (em geral)
**Só aparece de forma substantiva em uma ata:**

**Comitê de Arquitetura — 26/03/2026**

Contexto: **duplicidade de chamadas** (ex.: `confirm` duas vezes), não um mecanismo de header.

| Ponto da ata | Conteúdo |
|---|---|
| Problema | PDV + Keeta confirmam ao mesmo tempo; **422** quebra fluxo |
| Debate | Desejável **202/200** se o pedido **já está confirmado**; reenvio de evento no polling |
| Encaminhamento | Async por padrão; **422 não é obrigatório**; implementação **pode** ser idempotente na duplicidade de chamada; lógica fecha por **eventos**, não pela resposta do endpoint |
| Opções para duplicidade | **202** + reenvio do evento **ou** manter **422** sem nova ação |

Não há acordo sobre:
- header `X-Request-Id`
- geração de id pelo cliente
- regra genérica de “mesmo id = mesmo resultado” para todas as mutações

### Outras menções (não são o mesmo assunto)
- **Eventos duplicados / ACK de polling** (Arquitetura 19/03) — consumo de eventos, não `X-Request-Id`
- **Unicidade de cliente no CRM** — dedupe de entidade
- **Headers** em webhooks / auth / merchant id — outro tema
- **Roadmap** (`docs/documentation/roadmap.md`) lista *“Idempotency rules consolidation”* como trabalho ativo — reforça que **não está consolidado**

---

## Conclusão

Sua intuição está certa:

1. **`X-Request-Id` como convenção transversal não foi decidido em comitê** → não deveria constar como regra/convenção “do protocolo” sem marcação clara de *não decidido* ou remoção.
2. **Idempotência discutida** = comportamento de **operação já no estado alvo** (ex. confirm repetido → 202/200), não o modelo de idempotency-key por header.
3. Alinha com `AGENTS.md` / atas: **não inventar norma sem base de comitê**.

---

## Onde a doc ainda afirma isso hoje
- `docs/reference/conventions.md` (+ EN) — seção **Idempotência** com `X-Request-Id`
- `docs/reference/error-handling.md` (+ EN) — retentativa ligada a `X-Request-Id`
- Legado `docs/transport-bindings/**` (fora do site)
- Roadmap: consolidação de regras de idempotência

Se quiser, no próximo passo eu **removo/suavizo** o `X-Request-Id` das convenções e de erros, e deixo no máximo um apontamento de que **duplicidade de mutações** (async / 202) foi encaminhada na ata de 26/03, sem header obrigatório.

## User

esqueça esse x-request-id. temos que tirar totalmente, pq isso provavelmente foi colocado por algum modelo de LLM. vamos pelo que o comite fala. Leia a regra da v1 @docs\reference\v1\openapi.yaml e adapte para o solicitado pela Keeta funcionar. se necessario podemos incluir um campo no discovery para ditar essa regra (só se vc achar necessário. se complicar muito a implementação, podemos adotar um default universal)

## Assistant

Vou remover o `X-Request-Id`, conferir a regra da V1 e alinhar o comportamento de duplicidade ao encaminhamento do comitê (caso Keeta).

## Tools

- Search: 422|idempot|confirm|duplicate|already|X-Request|Invalid state|INVALID_STATE
- Search: X-Request-Id|idempot
- Search: confirm|422|INVALID_STATE|already
- Search: confirm|422|idempot|duplicate
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v1\openapi.yaml (681-720)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v1\openapi.yaml (1591-1670)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml (2-51)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml (96-175)
- Search: parameters:|X-|headers|RequestId|Request-Id
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md

## Assistant

Removendo `X-Request-Id` e documentando o default universal do comitê: chamada duplicada em estado já atingido → `202` (não `422`).

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml (129-228)
- Search: X-Request-Id
- Edit: C:\OpenDelivery\opendelivery-v2\docs\documentation\roadmap.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Read: C:\OpenDelivery\opendelivery-v2\docs\transport-bindings\rest-http-orders.md (46-70)
- Read: C:\OpenDelivery\opendelivery-v2\docs\transport-bindings\rest-http-indoor.md (31-70)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (111-150)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\transport-bindings\rest-http-orders.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\transport-bindings\rest-http-indoor.md
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
p = Path('docs/transport-bindings/rest-http-indoor.md')
t = p.read_text(encoding='utf-8')
t2 = t.replace('X-Request-Id: req-001\n\n', '').replace('X-Request-Id: req-002\n\n', '').replace('X-Request-Id: req-003\n\n', '').replace('X-Request-Id: req-004\n\n', '').replace('X-Request-Id: req-005\n\n', '')
p.write_text(t2, encoding='utf-8')
print('done', 'X-Request-Id' in t2)
" (Strip X-Request-Id lines from indoor binding examples)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md
- Search: X-Request-Id
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "WARNING|ERROR|unrecognized|built" (Verify docs build after idempotency changes)
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
import re
p = Path('docs/transport-bindings/rest-http-indoor.md')
t = p.read_text(encoding='utf-8')
t2 = re.sub(r'^X-Request-Id:.*\r?\n', '', t, flags=re.M)
p.write_text(t2, encoding='utf-8')
print('remaining', 'X-Request-Id' in t2)
" (Remove remaining X-Request-Id example lines)

## Assistant

## O que foi feito

### `X-Request-Id` removido
- Convenções e erros (PT/EN)
- Legado `transport-bindings` (orders + indoor)
- Referências em getting-started / index da API

### Default universal (sem campo no Discovery)

Base: **V1** (async → reapresentar evento) + **comitê 26/03** + pedido **Keeta**.

| Situação | HTTP V2 |
|---|---|
| Transição válida, ainda não aplicada | `202` |
| **Mesma operação já aplicada** (ex.: confirm com pedido já `CONFIRMED`) | **`202`** (sem nova transição; **pode** reenviar o evento) |
| Transição **impossível** (ex.: confirm em `CANCELLED`) | `409` / erro de negócio |

**Não** se usa `422`/`409` só porque a operação “já foi feita”.

Não incluí flag no Discovery: um default único cobre o caso Keeta e evita complexidade de negociação.

### Onde está documentado
- `docs/reference/conventions.md` (+ EN) — seção **Duplicidade de operações de ciclo de vida**
- `docs/reference/error-handling.md` (+ EN) — retentativas e transição inválida
- `docs/reference/v2/orders.openapi.yaml` — seção normativa + `confirm` e demais progressões
- Nota em `docs/protocol/orders.md`

### Mantido de propósito
- Deduplicação de **eventos** por id (prática V1 / CRM) — isso não é `X-Request-Id` de cliente.

Se quiser, no próximo passo dá para espelhar o mesmo parágrafo de duplicidade na OpenAPI de Logistics/Indoor.

## User

pode fazer

## Assistant

Vou espelhar a regra de duplicidade de ciclo de vida nas OpenAPIs de Logistics e Indoor.

## Tools

- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml (1-80)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml (1-50)
- Search: ^  /|operationId:|responses:|'202'|'409'
- Search: ^  /|operationId:|post:|patch:|put:|delete:|'202'|'409'
- Search: Duplicate lifecycle|Async-first|202 Accepted
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml (106-325)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml (476-675)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml (245-294)
- Search: duplicate|Duplicate|async
- Search: 202|duplic|async
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\logistics.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml (296-335)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\orders.openapi.yaml
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\logistics.md (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.md (1-40)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\logistics.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.md
- Search: Duplicate lifecycle
- Execute: if (Test-Path docs\protocol\indoor.en.md) { Select-String -Path docs\protocol\indoor.en.md -Pattern "OpenAPI Indoor" | Select-Object -First 3 }; if (Test-Path docs\protocol\logistics.en.md) { "has logistics en" } else { "no logistics en" } (Check EN protocol files for logistics/indoor)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.en.md (2-36)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.en.md
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "WARNING|ERROR|unrecognized|built" (Build docs after logistics/indoor updates)

## Assistant

Pronto. A mesma regra de duplicidade está espelhada em **Logistics** e **Indoor**.

### OpenAPI
| Spec | O que entrou |
|------|----------------|
| **Logistics** | Seção *Duplicate lifecycle operations* + `create`, ready-for-pickup, collected, delivered, cancel |
| **Indoor** | Mesma seção + pre-close, unlock, close (já `IN_PAYMENT` / `CLOSED` → `202`) |
| **Orders** | Completado `delivered`, `cancel`, `conclude` (faltavam detalhe) |

### Guias de domínio
- `protocol/logistics.md` — nota de chamada repetida  
- `protocol/indoor.md` + `indoor.en.md` — idem  

**Default universal:** operação já aplicada no estado alvo → **`202`**; `409` só se a transição for **impossível**. Sem header de idempotência e sem flag no Discovery.

## User

tire qualquerm menção dos textos a palavra ou conceito Redoc. (o redoc é só onde o openapi é redenrizado). acho que também podemos trocar todos lugares que falam OpenApi, por especificação da API (no ingles use API Spec). coloque apenas em algum lugar que todas as specs são escritas em OpenAPI

## Assistant

Vou localizar todas as menções a “ReDoc” e “OpenAPI” nos textos e padronizar a linguagem.

## Tools

- Search: ReDoc|Redoc|redoc|OpenAPI|OpenApi|openapi
- Search: ReDoc|Redoc|OpenAPI
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
import re

root = Path('docs')
files = list(root.rglob('*.md'))
# also project meta
for p in [Path('STRUCTURE.md'), Path('AGENTS.md'), Path('README.md'), Path('README_SPEC.md'), Path('IMPLEMENTATION_GUIDE.md')]:
    if p.exists():
        files.append(p)

# skip transport-bindings? user said all text - include them for consistency
count_redoc = 0
count_openapi = 0
by_file = []
for f in files:
    t = f.read_text(encoding='utf-8')
    r = len(re.findall(r'(?i)redoc', t))
    o = len(re.findall(r'OpenAPI|OpenApi', t))
    if r or o:
        by_file.append((str(f), r, o))
        count_redoc += r
        count_openapi += o
print('files', len(by_file), 'redoc', count_redoc, 'OpenAPI', count_openapi)
for f,r,o in sorted(by_file):
    print(f'{r:2} {o:2} {f}')
"@
 (Count ReDoc/OpenAPI mentions in markdown files)
- Execute: .\.venv\Scripts\python.exe << 'PY'
from pathlib import Path
import re

files = list(Path('docs').rglob('*.md'))
for p in [Path('STRUCTURE.md'), Path('AGENTS.md'), Path('README.md'), Path('README_SPEC.md'), Path('IMPLEMENTATION_GUIDE.md')]:
    if p.exists():
        files.append(p)

# Paths/filenames to protect
PROTECT = [
    (re.compile(r'docs/reference/v2/\*\.openapi\.yaml'), '§PATH0§'),
    (re.compile(r'reference/v2/\*\.openapi\.yaml'), '§PATH1§'),
    (re.compile(r'[\w./-]+\.openapi\.yaml'), '§PATHFILE§'),
    (re.compile(r'\*\.openapi\.yaml'), '§PATHGLOB§'),
    (re.compile(r'openapi\.yaml'), '§PATHYAML§'),
    (re.compile(r'template:\s*redoc\.html'), '§REDOC_TMPL§'),
    (re.compile(r'redoc\.html'), '§REDOC_HTML§'),
]

# EN-specific replacements (apply to .en.md and EN-heavy root files)
EN_REPL = [
    (r'OpenAPI / ReDoc', 'API Spec'),
    (r'OpenAPI \+ ReDoc', 'API Spec'),
    (r'OpenAPI/ReDoc', 'API Spec'),
    (r'\(ReDoc\)', ''),
    (r'— ReDoc\.?', ''),
    (r'— rendered with ReDoc\.?', ''),
    (r', rendered with ReDoc', ''),
    (r'rendered with ReDoc', ''),
    (r'Documentation tooling \(e\.g\., Redoc\) is an implementation detail and may change without affecting the protocol\.',
     'Documentation presentation tooling is an implementation detail and may change without affecting the protocol.'),
    (r'pre-ReDoc', 'legacy'),
    (r'ReDoc shells', 'API reference shells'),
    (r'ReDoc shell notes', 'API reference shell notes'),
    (r'ReDoc narrative blocks', 'API Spec narrative blocks'),
    (r'ReDoc pages under', 'API reference pages under'),
    (r'Interactive OpenAPI specs', 'Interactive API Specs'),
    (r'Open OpenAPI reference', 'Open API Spec'),
    (r'OpenAPI Authentication \(EN\)', 'Authentication API Spec (EN)'),
    (r'Authentication OpenAPI', 'Authentication API Spec'),
    (r'Orders OpenAPI', 'Orders API Spec'),
    (r'Merchant OpenAPI', 'Merchant API Spec'),
    (r'Logistics OpenAPI', 'Logistics API Spec'),
    (r'Customer OpenAPI', 'Customer API Spec'),
    (r'Indoor OpenAPI', 'Indoor API Spec'),
    (r'Discovery OpenAPI', 'Discovery API Spec'),
    (r'OpenAPI Indoor', 'Indoor API Spec'),
    (r'OpenAPI Orders', 'Orders API Spec'),
    (r'OpenAPI Merchant', 'Merchant API Spec'),
    (r'OpenAPI Logistics', 'Logistics API Spec'),
    (r'OpenAPI Customer', 'Customer API Spec'),
    (r'OpenAPI Discovery', 'Discovery API Spec'),
    (r'OpenAPI Authentication', 'Authentication API Spec'),
    (r'Implement with Indoor OpenAPI', 'Implement with Indoor API Spec'),
    (r'OpenAPI always English', 'API Spec always English'),
    (r'OpenAPI is always English', 'API Spec is always English'),
    (r'OpenAPI contracts are \*\*always English\*\*', 'API Specs are **always English**'),
    (r'OpenAPI contracts', 'API Specs'),
    (r'OpenAPI contract', 'API Spec'),
    (r'OpenAPI specs', 'API Specs'),
    (r'OpenAPI Spec', 'API Spec'),
    (r'the OpenAPI\b', 'the API Spec'),
    (r'The OpenAPI\b', 'The API Spec'),
    (r'in OpenAPI\b', 'in the API Spec'),
    (r'via OpenAPI\b', 'via the API Spec'),
    (r'per OpenAPI\b', 'per the API Spec'),
    (r'Capability OpenAPI', 'capability API Spec'),
    (r'capability OpenAPI', 'capability API Spec'),
    (r'published OpenAPI', 'published API Spec'),
    (r'Implement OpenAPI', 'Implement the API Spec'),
    (r'OpenAPI over REST', 'API Spec over REST'),
    (r'Guide · Protocol · OpenAPI', 'Guide · Protocol · API Spec'),
    (r'Protocol · OpenAPI', 'Protocol · API Spec'),
    (r'live in \*\*OpenAPI\*\*', 'live in the **API Spec**'),
    (r'live in \*\*OpenAPI\b', 'live in the **API Spec'),
    (r'\bOpenAPI\b', 'API Spec'),  # catch-all EN
    (r'\bRedoc\b', ''),
    (r'\bReDoc\b', ''),
]

# PT replacements
PT_REPL = [
    (r'OpenAPI / ReDoc', 'especificação da API'),
    (r'OpenAPI \+ ReDoc', 'especificação da API'),
    (r'\(ReDoc\)', ''),
    (r'— ReDoc\.?', ''),
    (r', renderizado com ReDoc', ''),
    (r'renderizado com ReDoc', ''),
    (r'pre-ReDoc', 'legado'),
    (r'Abrir referência OpenAPI →', 'Abrir especificação da API →'),
    (r'Abrir referência OpenAPI', 'Abrir especificação da API'),
    (r'referência OpenAPI de Customer', 'especificação da API de Customer'),
    (r'referência OpenAPI', 'especificação da API'),
    (r'Referência OpenAPI', 'Especificação da API'),
    (r'contratos OpenAPI', 'especificações da API'),
    (r'Contratos OpenAPI', 'Especificações da API'),
    (r'contrato OpenAPI', 'especificação da API'),
    (r'Contrato OpenAPI', 'Especificação da API'),
    (r'Contrato da API \(OpenAPI\)', 'Especificação da API'),
    (r'OpenAPI specs interativas', 'Especificações da API interativas'),
    (r'OpenAPI Indoor', 'especificação Indoor'),
    (r'OpenAPI Orders', 'especificação Orders'),
    (r'OpenAPI Merchant', 'especificação Merchant'),
    (r'OpenAPI Logistics', 'especificação Logistics'),
    (r'OpenAPI Customer', 'especificação Customer'),
    (r'OpenAPI Discovery', 'especificação Discovery'),
    (r'OpenAPI de Discovery', 'especificação de Discovery'),
    (r'OpenAPI Authentication', 'especificação de Authentication'),
    (r'OpenAPI de Authentication', 'especificação de Authentication'),
    (r'\[OpenAPI ', '['),  # broken links fix later if any
    (r'prevalece a OpenAPI', 'prevalece a especificação da API'),
    (r'prevalece a \*\*OpenAPI\*\*', 'prevalece a **especificação da API**'),
    (r'na OpenAPI', 'na especificação da API'),
    (r'Na OpenAPI', 'Na especificação da API'),
    (r'da OpenAPI', 'da especificação da API'),
    (r'Da OpenAPI', 'Da especificação da API'),
    (r'à OpenAPI', 'à especificação da API'),
    (r'a OpenAPI', 'a especificação da API'),
    (r'A OpenAPI', 'A especificação da API'),
    (r'as specs \*\*OpenAPI\*\*', 'as **especificações da API**'),
    (r'specs \*\*OpenAPI\*\*', '**especificações da API**'),
    (r'\*\*OpenAPI\*\*', '**especificação da API**'),
    (r'## Contrato único: OpenAPI REST/HTTP', '## Contrato único: especificação da API (REST/HTTP)'),
    (r'## Contrato da API \(OpenAPI\)', '## Contrato da API'),
    (r'Guia · Protocolo · OpenAPI', 'Guia · Protocolo · especificação da API'),
    (r'Protocolo · OpenAPI', 'Protocolo · especificação da API'),
    (r'expresso como \*\*contrato OpenAPI \(REST/HTTP\)\*\*', 'expresso como **especificação da API (REST/HTTP)**'),
    (r'com contrato OpenAPI', 'com especificação da API'),
    (r'Contrato OpenAPI normativo', 'Especificação da API normativa'),
    (r'OpenAPI \(REST/HTTP\)', 'especificação da API (REST/HTTP)'),
    (r'\bOpenAPI\b', 'especificação da API'),
    (r'\bRedoc\b', ''),
    (r'\bReDoc\b', ''),
]

def protect(text):
    placeholders = []
    def store(m):
        placeholders.append(m.group(0))
        return f'§P{len(placeholders)-1}§'
    # protect openapi file refs
    text = re.sub(r'[\w./-]*\.openapi\.yaml', store, text)
    text = re.sub(r'\*\.openapi\.yaml', store, text)
    text = re.sub(r'template:\s*redoc\.html', store, text, flags=re.I)
    text = re.sub(r'redoc\.html', store, text, flags=re.I)
    return text, placeholders

def unprotect(text, placeholders):
    for i, val in enumerate(placeholders):
        text = text.replace(f'§P{i}§', val)
    return text

def is_en(path: Path) -> bool:
    name = path.name
    if name.endswith('.en.md'):
        return True
    if name in ('AGENTS.md', 'README.md', 'README_SPEC.md', 'IMPLEMENTATION_GUIDE.md', 'STRUCTURE.md'):
        # mixed; STRUCTURE is PT-leaning, AGENTS EN
        return name in ('AGENTS.md', 'README.md', 'README_SPEC.md', 'IMPLEMENTATION_GUIDE.md')
    # overview.md is English content without .en
    if name in ('overview.md', 'roadmap.md'):
        return True
    return False

changed = []
for f in files:
    raw = f.read_text(encoding='utf-8')
    text, ph = protect(raw)
    repls = EN_REPL if is_en(f) else PT_REPL
    # STRUCTURE is mostly PT
    if f.name == 'STRUCTURE.md':
        repls = PT_REPL
    new = text
    for pat, rep in repls:
        new = re.sub(pat, rep, new)
    # cleanup double spaces and empty parens
    new = re.sub(r'  +', ' ', new)
    new = re.sub(r'\(\s*\)', '', new)
    new = re.sub(r' +([,.;:])', r'\1', new)
    new = re.sub(r' +$', '', new, flags=re.M)
    new = unprotect(new, ph)
    if new != raw:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f))

print('changed', len(changed))
for c in changed:
    print(c)
# remaining OpenAPI/ReDoc in md (excluding protected paths)
print('--- remaining ---')
for f in files:
    t = f.read_text(encoding='utf-8')
    # ignore file path occurrences
    t2 = re.sub(r'[\w./-]*\.openapi\.yaml', '', t)
    t2 = re.sub(r'redoc\.html', '', t2, flags=re.I)
    if re.search(r'OpenAPI|ReDoc|Redoc', t2, re.I):
        for m in re.finditer(r'.{0,40}(OpenAPI|ReDoc|Redoc).{0,40}', t2, re.I):
            print(f, ':', m.group(0).replace('\n',' '))
PY
 (Bulk replace OpenAPI/ReDoc wording in markdown)
- Edit: C:\OpenDelivery\opendelivery-v2\tools\_rename_openapi_wording.py
- Execute: .\.venv\Scripts\python.exe tools\_rename_openapi_wording.py (Run OpenAPI/ReDoc wording rewrite script)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.en.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\orders.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (66-120)
- Search: ReDoc|Redoc|OpenAPI|especificação da API da|API Spec Spec|especificação da especificação
- Search: ReDoc|Redoc|OpenAPI

## Assistant

Corrigindo artefatos da substituição em massa e limpando menções restantes nos YAMLs.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\index.en.md
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
import re

fixes = [
    (r'Os especificações', 'As especificações'),
    (r'Os especificação', 'A especificação'),
    (r'O especificação', 'A especificação'),
    (r'com \*\*\*\*', ''),
    (r'with \*\*\*\*', ''),
    (r' com \*\*\*\*', ''),
    (r' with \*\*\*\*', ''),
    (r'\*\*\*\* —', '—'),
    (r'with \*\*\*\* —', '—'),
    (r'com \*\*\*\* —', '—'),
    (r'As specs especificação da API', 'As especificações da API'),
    (r'As specs especificação', 'As especificações'),
    (r'Especificação da API normativo', 'Especificação da API normativa'),
    (r'especificação da API normativo', 'especificação da API normativa'),
    (r'API Spec specs', 'API Specs'),
    (r'\*\*API Spec\*\* specs', '**API Specs**'),
    (r'API Spec Spec', 'API Spec'),
    (r'especificação da API da capability', 'especificação da capability'),
    (r'API Spec of the capability', 'capability API Spec'),
    (r'the API Spec of', 'the API Spec for'),
    (r'  +', ' '),
]

# shell note pages
shell_pt = '!!! note \"Idioma do contrato\"\n    A especificação da API desta página está **somente em inglês**.\n'
shell_en = '!!! note \"Contract language\"\n    The API Spec on this page is **English only**.\n'

for f in Path('docs/reference').glob('*.md'):
    if f.name.startswith('index') or f.name in ('conventions.md','error-handling.md','conventions.en.md','error-handling.en.md'):
        continue
    t = f.read_text(encoding='utf-8')
    if 'template: redoc.html' in t or 'openapi_spec:' in t:
        # rewrite language note only if present
        if f.name.endswith('.en.md'):
            t2 = re.sub(r'!!! note \"[^\"]+\"\n.*', shell_en.rstrip(), t, count=1, flags=re.S)
            # if multiline note at end
            if '!!! note' in t:
                parts = t.split('---', 2)
                if len(parts) >= 3:
                    front = '---' + parts[1] + '---\n\n'
                    t = front + shell_en
            else:
                t = t
        else:
            if '!!! note' in t:
                parts = t.split('---', 2)
                if len(parts) >= 3:
                    front = '---' + parts[1] + '---\n\n'
                    t = front + shell_pt
        f.write_text(t, encoding='utf-8')
        print('shell', f)

for f in Path('docs').rglob('*.md'):
    t = f.read_text(encoding='utf-8')
    orig = t
    for a,b in fixes:
        t = re.sub(a,b,t)
    # clean empty with leftover
    t = re.sub(r' with —', ' —', t)
    t = re.sub(r' com —', ' —', t)
    t = re.sub(r'  +', ' ', t)
    if t != orig:
        f.write_text(t, encoding='utf-8')
        print('fix', f)

# openapi yaml user-facing descriptions
for f in Path('docs/reference/v2').glob('*.openapi.yaml'):
    t = f.read_text(encoding='utf-8')
    orig = t
    t = t.replace('(ReDoc). ', '')
    t = t.replace('ReDoc', '')
    t = t.replace('Orders OpenAPI', 'Orders API Spec')
    t = t.replace('Authentication OpenAPI', 'Authentication API Spec')
    t = t.replace('Discovery OpenAPI', 'Discovery API Spec')
    t = t.replace('Merchant OpenAPI', 'Merchant API Spec')
    t = t.replace('Logistics OpenAPI', 'Logistics API Spec')
    t = t.replace('Customer OpenAPI', 'Customer API Spec')
    t = t.replace('Indoor OpenAPI', 'Indoor API Spec')
    t = t.replace('The OpenAPI on this page', 'The API Spec on this page')
    t = t.replace('OpenAPI', 'API Spec')  # remaining in descriptions - careful with openapi: version?
    # restore yaml key
    t = t.replace('API Spec: 3.', 'openapi: 3.')
    t = re.sub(r'^API Spec:', 'openapi:', t, flags=re.M)
    if t != orig:
        f.write_text(t, encoding='utf-8')
        print('yaml', f.name)
"@
 (Fix grammar leftovers and OpenAPI YAML wording)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\orders.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\orders.en.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml (1-30)
- Search: OpenAPI|ReDoc|Redoc|\*\*\*\*|Os espec|O espec|API Spec Spec|normativo
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.md (109-118)
- Read: C:\OpenDelivery\opendelivery-v2\docs\index.en.md (109-118)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\v2\indoor.openapi.yaml
- Search: OpenAPI|ReDoc|Redoc
- Search: OpenAPI|ReDoc|Redoc
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md (1-40)
- Read: C:\OpenDelivery\opendelivery-v2\AGENTS.md (1-37)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\indoor.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\indoor.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\indoor.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\indoor.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\AGENTS.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\index.en.md
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
import re
# fix o/Os especificação
for f in Path('docs').rglob('*.md'):
    t = f.read_text(encoding='utf-8')
    o = t
    t = re.sub(r'\bo especificação\b', 'a especificação', t)
    t = re.sub(r'\bO especificação\b', 'A especificação', t)
    t = re.sub(r'\bé o \*\*especificação', 'é a **especificação', t)
    t = re.sub(r'é o \*\*especificação', 'é a **especificação', t)
    t = re.sub(r'  +\n', '\n', t)
    if t != o:
        f.write_text(t, encoding='utf-8')
        print('fixed', f)
"
 (Fix PT article agreement for especificação)
- Execute: Remove-Item tools\_rename_openapi_wording.py -Force; .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "WARNING|ERROR|unrecognized|built|Doc file" (Delete temp script and build docs)
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
for f, a, b in [
    (Path('docs/index.md'), 'Especificação da API normativa (REST/HTTP): endpoints, schemas e exemplos ', 'Especificação da API (REST/HTTP): endpoints, schemas e exemplos.'),
    (Path('docs/index.en.md'), 'Normative API Spec (REST/HTTP): endpoints, schemas, and examples ', 'API Spec (REST/HTTP): endpoints, schemas, and examples.'),
]:
    t = f.read_text(encoding='utf-8')
    if a in t:
        f.write_text(t.replace(a,b), encoding='utf-8')
        print('ok', f)
    else:
        # show line
        for i,line in enumerate(t.splitlines(),1):
            if 'REST/HTTP' in line and 'schemas' in line:
                print(f, i, repr(line))
"
 (Fix index layer card text exactly)
- Search: OpenAPI|ReDoc|Redoc|\*\*\*\*|o especificação|O especificação|Os espec
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md (1-25)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\menu.md
- Search: OpenAPI|ReDoc|Redoc
- Search: OpenAPI|ReDoc|Redoc
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "ERROR|WARNING –|unrecognized relative|built" (Final strict docs build)

## Assistant

Pronto. Padronizei a linguagem em toda a documentação.

### Regras aplicadas
| Antes | Depois |
|--------|--------|
| **ReDoc** (em textos) | removido |
| **OpenAPI** (em textos de produto) | **especificação da API** (PT) / **API Spec** (EN) |
| Formato técnico | **só** em **Referência da API** (e no `AGENTS.md` para quem edita o repo) |

### Onde o formato OpenAPI ainda aparece (de propósito)
- `docs/reference/index.md` / `index.en.md` — nota **“Formato das especificações”**: todas as specs são escritas em OpenAPI (YAML)
- Nomes de arquivo `*.openapi.yaml` e front matter `openapi_spec` / `template: redoc.html` (técnico, não texto de usuário)

### Também ajustado
- Callouts “Abrir referência OpenAPI” → “Abrir especificação da API”
- Landing, princípios, guias, protocol, convenções, shells ReDoc
- YAML Indoor (textos internos sem ReDoc/OpenAPI no sentido de produto)

Build ok.

## User

vc mudou algumas partes de estilo que nao era pra mudar, por exemplo os textos que ficam dentro de tips ou warnigns

## Assistant

Vou comparar o estado atual dos admonitions (`!!! tip` / `!!! warning`) com o que o git mostra e corrigir o estilo que quebrou.

## Tools

- Execute: git diff --stat HEAD -- docs/ ; git diff HEAD -- docs/ | Select-String -Pattern "!!! (tip|warning|note|important)" -Context 0,5 | Select-Object -First 80 (Diff admonition blocks vs HEAD)
- Search: ^!!!

## Assistant

A substituição em massa colapsou a indentação (4 espaços → 1) dos admonitions. Vou restaurar o formato correto do Material/MkDocs.

## Tools

- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
import re

ADMON_RE = re.compile(r'^!!!\s+\w+')

def fix_admonitions(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        raw = line.rstrip('\r\n')
        ending = line[len(raw):]
        if ADMON_RE.match(raw):
            out.append(line)
            i += 1
            # body until non-empty line with no leading whitespace
            while i < len(lines):
                body = lines[i]
                braw = body.rstrip('\r\n')
                bending = body[len(braw):]
                if braw.strip() == '':
                    # peek ahead: if next non-empty has leading ws, keep blank inside block
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == '':
                        j += 1
                    if j < len(lines):
                        nxt = lines[j].rstrip('\r\n')
                        if nxt.startswith(' ') or nxt.startswith('\t'):
                            out.append(bending if bending else '\n')
                            i += 1
                            continue
                        # next structural content - blank ends block only if next has no indent
                        # keep one blank and end
                        out.append(bending if bending else '\n')
                        i += 1
                        break
                    out.append(bending if bending else '\n')
                    i += 1
                    break
                # non-empty
                if braw.startswith(' ') or braw.startswith('\t'):
                    content = braw.lstrip(' \t')
                    out.append('    ' + content + bending)
                    i += 1
                    continue
                # non-empty no indent -> end of admonition
                break
            continue
        out.append(line)
        i += 1
    return ''.join(out)

changed = []
for f in Path('docs').rglob('*.md'):
    raw = f.read_text(encoding='utf-8')
    if '!!!' not in raw:
        continue
    new = fix_admonitions(raw)
    if new != raw:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f))

print('fixed', len(changed), 'files')
for c in sorted(changed):
    print(c)

# sample check
samples = [
    'docs/extensions/loyalty.md',
    'docs/guide/getting-started.md',
    'docs/reference/index.md',
    'docs/protocol/orders.md',
]
for s in samples:
    t = Path(s).read_text(encoding='utf-8')
    # find first !!! and next 6 lines
    for m in re.finditer(r'^!!!.*$', t, re.M):
        start = m.start()
        chunk = t[start:start+400]
        print('---', s)
        print(chunk.split('\n\n')[0][:350])
        print()
        break
"@
 (Restore 4-space indent in MkDocs admonitions)
- Read: C:\OpenDelivery\opendelivery-v2\docs\extensions\loyalty.md (24-38)
- Read: C:\OpenDelivery\opendelivery-v2\docs\extensions\loyalty.md (249-268)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md (2-26)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md (1-30)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.md (18-37)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\indoor.md
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
import re
# find !!! followed by line that is not empty and not 4-space indented
bad = []
for f in Path('docs').rglob('*.md'):
    lines = f.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^!!!\s+\w+', line):
            j = i+1
            while j < len(lines):
                L = lines[j]
                if L.strip() == '':
                    # look ahead
                    k = j+1
                    while k < len(lines) and lines[k].strip()=='':
                        k += 1
                    if k >= len(lines):
                        break
                    if not (lines[k].startswith('    ') or lines[k].startswith('\t')):
                        break
                    j += 1
                    continue
                if L.startswith('    ') or L.startswith('\t'):
                    j += 1
                    continue
                # non-indented non-empty right after admonition without blank - BAD if previous was admonition body expected
                # if first body line is non-indented, bad
                if j == i+1:
                    bad.append((str(f), i+1, line, L[:80]))
                break
print('bad first-body', len(bad))
for b in bad[:20]:
    print(b)
"
 (Validate admonition body indentation)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (129-153)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.en.md (264-288)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md (1-25)
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "ERROR|WARNING –|built|Doc file" (Verify build after admonition fix)

## Assistant

Corrigindo também glitches de texto residual da mesma substituição.

## Tools

- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
import re
subs = [
    (r'spec especificação da API', 'especificação da API'),
    (r'specs especificação da API', 'especificações da API'),
    (r'Nas specs especificação da API', 'Nas especificações da API'),
    (r'cada spec especificação', 'cada especificação'),
    (r'API Spec Spec', 'API Spec'),
    (r'the API Spec Spec', 'the API Spec'),
]
for f in Path('docs').rglob('*.md'):
    t = f.read_text(encoding='utf-8')
    o = t
    for a,b in subs:
        t = t.replace(a,b)
    if t != o:
        f.write_text(t, encoding='utf-8')
        print('fixed', f)
"@
 (Fix residual wording glitches from bulk replace)
- Search: spec especificação|specs especificação|API Spec Spec
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.md
- Search: spec especificação|specs especificação|mesmo especificação
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
import re
# remaining broken admonitions: body line with only 1 space
bad=[]
for f in Path('docs').rglob('*.md'):
    lines=f.read_text(encoding='utf-8').splitlines()
    for i,l in enumerate(lines):
        if re.match(r'^!!!\s', l):
            if i+1 < len(lines) and re.match(r'^ [^\s]', lines[i+1]):
                bad.append((str(f), i+2, lines[i+1][:60]))
print('still broken', len(bad))
for b in bad: print(b)
"
 (Confirm no single-space admonition bodies remain)

## Assistant

Você tinha razão.

### O que aconteceu
Na troca em massa de “OpenAPI/ReDoc”, o script colapsou espaços (`  +` → um espaço). Nos admonitions do Material/MkDocs o corpo precisa de **4 espaços** de indentação; isso virou **1 espaço** e o estilo de tip/warning/note quebrou.

### O que foi corrigido
- Indentação restaurada em **39 arquivos** (`!!! tip`, `!!! warning`, `!!! note`, `!!! info`, `!!! important`)
- Checklists e blocos multiparágrafo voltam ao formato correto
- Também limpei restos de texto do tipo `spec especificação da API`

Desculpa pelo efeito colateral — a intenção era só renomear termos, não alterar o layout dos callouts.

## User

não sei pq mas eu to achando que esses blocos que levam a outras paginas, por exemplo na visao geral da api, tem esse bloco: Convenções transversais (datas, paginação, erros) antes das capabilities.

Regras gerais e erros →

quebram o flow da leitura. eu acho que isso talvez ficasse melhor no final das paginas não? ou isso é padrao de docs?

## Assistant

Vou checar como esses callouts estão posicionados hoje para te dar uma recomendação objetiva.

## Tools

- Search: od-api-callout
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (745-784)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (781-830)
- Search: od-next-step|od-api-callout

## Assistant

Sua leitura faz sentido — e o projeto **já tem o padrão certo** para isso: a classe `od-next-step` (“Próximo passo”), pensada para o **fim** da página. Os `od-api-callout` no topo viraram um atalho que compete com o conteúdo.

### O que docs costumam fazer

| Posição | Uso típico |
|--------|------------|
| **Topo** | Contexto mínimo: status (RC), idioma, “esta página é X, não Y” — sem pedir que você saia dali |
| **Meio** | Links inline no texto, quando o assunto aparece de verdade |
| **Fim** | “Próximo passo / Continue” — Stripe, MDN, AWS, etc. |

Callout no topo do tipo *“antes de ler, vá para outra página”* é o que mais **quebra o fluxo**. Quem abriu “Visão geral da API” quer o mapa da seção; convenções já estão na própria página (tabela **Convenções**).

### Recomendação

1. **Não usar** `od-api-callout` no topo como “vá para lá primeiro”.
2. **Mover** esse tipo de link para o **final**, no bloco `od-next-step` (já existe e algumas páginas já usam: loyalty, reviews, by-role).
3. No topo, manter só o que é **orientação in-place** (ex.: warning RC, nota de idioma/formato OpenAPI).
4. Na visão geral da API, o callout de convenções é **redundante** com a seção Convenções logo abaixo — pode sumir do topo; no fim, algo como “Próximo passo → Regras gerais · Discovery · Pedidos” encaixa melhor.

### Resumo

Não é “padrão de docs” empurrar o leitor para fora no começo. Padrão bom é: **ler a página → no fim, próximo destino**.

Se quiser, no próximo passo eu padronizo isso: callouts de navegação só no rodapé (`od-next-step`) e limpo os do topo em Guia / Protocolo / API.

## User

quero. tbm quero aproveitar e tirar aquela navegação do rodapé. não acho que esse é uma documentação tão linear assim, pra poder ir seguintes passos ou lições. se vc concorda pode fazer, senão me de as ajustificava para manter

## Assistant

Concordo: docs de protocolo/API não são linear como um curso — o “Anterior/Próximo” do rodapé e os callouts de “continue a jornada” no topo atrapalham mais do que ajudam. Vou remover o footer de navegação e limpar esses blocos de desvio.

## Tools

- Search: od-api-callout|navigation\.footer|od-next-step
- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (131-160)
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
import re

# 1) mkdocs footer
mk = Path('mkdocs.yml')
t = mk.read_text(encoding='utf-8')
t2 = re.sub(r'\n\s*- navigation\.footer\n', '\n', t)
if t2 != t:
    mk.write_text(t2, encoding='utf-8')
    print('mkdocs: removed navigation.footer')
else:
    print('mkdocs: footer not found or already gone')

# 2) remove od-api-callout and od-next-step blocks from markdown
# Match <div class=\"od-api-callout\">...</div> and od-next-step
block_re = re.compile(
    r'\n?<div class=\"od-(?:api-callout|next-step)\">.*?</div>\s*\n?',
    re.S
)

changed = []
for f in Path('docs').rglob('*.md'):
    raw = f.read_text(encoding='utf-8')
    new = block_re.sub('\n', raw)
    # collapse triple+ newlines
    new = re.sub(r'\n{3,}', '\n\n', new)
    if new != raw:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f))

print('md cleaned', len(changed))
for c in sorted(changed):
    print(' ', c)

# verify remaining
rem = []
for f in Path('docs').rglob('*.md'):
    t = f.read_text(encoding='utf-8')
    if 'od-api-callout' in t or 'od-next-step' in t:
        rem.append(str(f))
print('remaining', rem)
"@
 (Remove footer nav, api-callouts, and next-step blocks)
- Search: od-api-callout|od-next-step
- Search: od-api-callout|od-next-step
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path
import re

# leftover fragments from nested next-step
patterns = [
    re.compile(r'\n?<div class=\"od-next-step__label\">.*?</div>\s*', re.S),
    re.compile(r'\n?<div class=\"od-next-step__links\">.*?</div>\s*</div>\s*', re.S),
    re.compile(r'\n?<div class=\"od-next-step__links\">.*?</div>\s*', re.S),
    re.compile(r'\n?</div>\s*(?=\n---|\n##|\n\*\*|\Z)', re.S),  # careful - too broad
]

# safer: remove complete orphaned structures
orphan = re.compile(
    r'(?:\n*<div class=\"od-next-step__label\">[^<]*</div>\s*)?'
    r'<div class=\"od-next-step__links\">.*?</div>\s*'
    r'</div>\s*',
    re.S
)

# also lone leftover closing divs after links removed
changed=[]
for f in Path('docs').rglob('*.md'):
    raw = f.read_text(encoding='utf-8')
    new = orphan.sub('\n', raw)
    # remove any remaining od-next-step / od-api-callout markers
    if 'od-next-step' in new or 'od-api-callout' in new:
        # line-based cleanup of leftover tags
        lines = new.splitlines(keepends=True)
        out=[]
        skip_until_close = 0
        i=0
        while i < len(lines):
            L = lines[i]
            if re.search(r'class=\"od-(?:next-step|api-callout)', L):
                # skip until matching closing - simple: skip until line with only </div>
                depth = L.count('<div') - L.count('</div>')
                i += 1
                while i < len(lines) and depth > 0:
                    depth += lines[i].count('<div') - lines[i].count('</div>')
                    i += 1
                continue
            if re.match(r'^\s*</div>\s*$', L) and i>0 and 'od-next' in ''.join(out[-5:]):
                i += 1
                continue
            out.append(L)
            i += 1
        new = ''.join(out)
    new = re.sub(r'\n{3,}', '\n\n', new)
    if new != raw:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f))

print('changed', len(changed))
rem=[]
for f in Path('docs').rglob('*.md'):
    t=f.read_text(encoding='utf-8')
    if 'od-api-callout' in t or 'od-next-step' in t:
        rem.append(str(f))
        # show context
        for i,l in enumerate(t.splitlines(),1):
            if 'od-' in l:
                print(f, i, l)
print('remaining files', rem)
"@
 (Remove leftover next-step fragment divs)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\by-role.md (36-85)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (281-289)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\index.md (1-35)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md (1-25)
- Search: navigation\.footer|md-footer__link|Previous|Next|Anterior|Próximo
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "ERROR|WARNING –|built|footer" (Build site without navigation footer)

## Assistant

Concordo com a sua leitura — e apliquei.

### Por que não manter (e não “justificar” o contrário)
Documentação de **protocolo + API de referência** é **não linear**: a pessoa entra por papel, capability ou busca.  
“Anterior / Próximo” e “próximo passo / lição” servem a tutoriais em sequência; aqui o menu, a busca e os links no texto bastam.

### O que foi feito

1. **Rodapé Material desligado** — removido `navigation.footer` do `mkdocs.yml` (some o Anterior/Próximo entre páginas).

2. **Callouts de desvio removidos** (`od-api-callout`) — inclusive o da visão geral da API (“Convenções transversais…”).

3. **Blocos “Próximo passo” removidos** (`od-next-step`) — o fluxo linear artificial some.

4. **Mantido o que ainda faz sentido**
   - Tabelas **Leituras** em *Trilhas por papel* (índice por papel, não sequência de lições)
   - Links inline no fim de algumas páginas de capability (ex.: “Referência completa…”)
   - Notas in-page (RC, idioma, formato OpenAPI)

Build ok. Se em alguma página o final ficar “seco” demais e você quiser um link só para a spec irmã, dá para colocar **uma linha de texto**, sem caixa de “próximo passo”.

## User

eu gostei do relacionado, que tem na pagina de tratamento de erros. talvez podemos fazer ela ser padrão, com uma identidadae visual padronizada e colocar em todas as paginas do guia. oq acha?

## Tools

- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md (91-100)
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md (91-100)
- Search: ^## Relacionado|^## Related|^\*\*Referência
- ListDir: \docs\guide
- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (18-37)
- Read: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css (781-820)
- Read: C:\OpenDelivery\opendelivery-v2\mkdocs.yml (156-188)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\by-role.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\documentation\core-concepts.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\documentation\roadmap.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\roles-and-responsibilities.md

## Assistant

Concordo: “Relacionado” é melhor que “próximo passo” — é mapa, não lição. Vou criar um bloco visual padrão e colocar no fim de todas as páginas do Guia.

## Tools

- Edit: C:\OpenDelivery\opendelivery-v2\docs\stylesheets\theme.css
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\error-handling.en.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\reference\conventions.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.en.md (121-138)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\getting-started.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\by-role.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\documentation\core-concepts.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\overview.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\roles-and-responsibilities.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.en.md (126-139)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.md (186-190)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.en.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.md (176-190)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\changelog.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\documentation\roadmap.md
- Execute: .\.venv\Scripts\python.exe -c "
from pathlib import Path
p = Path('docs/guide/migration-v1-v2.md')
t = p.read_text(encoding='utf-8').rstrip() + '''

<div class=\"od-related\">
  <p class=\"od-related__label\">Relacionado</p>
  <ul class=\"od-related__list\">
    <li><a href=\"changelog.md\">Changelog</a> — histórico completo de versões</li>
    <li><a href=\"getting-started.md\">Primeiros Passos</a> — caminho mínimo V2</li>
    <li><a href=\"../protocol/discovery.md\">Discovery</a> · <a href=\"../protocol/authentication.md\">Autenticação</a></li>
    <li><a href=\"../reference/index.md\">Referência da API</a></li>
  </ul>
</div>
'''
p.write_text(t, encoding='utf-8')
print('ok migration pt')
"
 (Append Related block to migration PT page)
- Execute: .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "ERROR|WARNING –|built|unrecognized" (Build docs after Related blocks)
- Read: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.md (186-190)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\guide\migration-v1-v2.md
- Execute: .\.venv\Scripts\python.exe -c "from pathlib import Path; print('od-related count', sum(1 for f in Path('docs').rglob('*.md') if 'od-related' in f.read_text(encoding='utf-8')))" (Count pages with od-related block)

## Assistant

Concordo — e já deixei padrão.

### Por que “Relacionado” funciona aqui
- Não impõe ordem de leitura (diferente de “próximo passo / lição”)
- Fecha a página com **saídas úteis** sem roubar o topo
- Combina com doc de referência/protocolo (mapa, não curso)

### O que foi feito

**Identidade visual** (`.od-related` no `theme.css`):
- bloco discreto no fim da página  
- label em caixa alta (`Relacionado` / `Related`)  
- lista de links com descrição curta  
- borda esquerda na cor da marca  

**Páginas do Guia** (nav Guia):
| Página | PT | EN |
|--------|----|----|
| Primeiros Passos | ✓ | ✓ |
| Trilhas por papel | ✓ | — |
| Conceitos | ✓ | — |
| Visão geral | ✓ | ✓ |
| Papéis e responsabilidades | ✓ | — |
| Changelog | ✓ | ✓ |
| Migração V1→V2 | ✓ | ✓ |
| Roadmap | ✓ | — |

**Mesmo padrão** também em **Convenções** e **Tratamento de Erros** (onde o padrão nasceu).

Landing (`index`) ficou de fora de propósito — já tem CTAs e trilhas próprias.

Se quiser, no próximo passo replicamos o mesmo bloco no **fim das páginas de Protocolo** (por capability).

## User

sim. e sempre que tiver a spec relacionada, precisamos levar a pessoa a spec. acho que isso pode estar no inicio das paginas de capabilities (alem do discovery e autenticação) com um adnotation.

## Assistant

Vou mapear as páginas de Protocolo, adicionar o bloco Relacionado no fim e um admonition no topo das capabilities (e Discovery/Auth) apontando para a spec.

## Tools

- Search: ^# |reference/|especificação|API Spec|od-related
- ListDir: \docs\protocol
- ListDir: \docs\extensions
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (1-25)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (276-289)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.md (1-25)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\authentication.md (1-25)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Execute: .\.venv\Scripts\python.exe -c @"
from pathlib import Path

# show last 8 lines of each protocol/extension page
for f in sorted(Path('docs/protocol').glob('*.md')) + sorted(Path('docs/extensions').glob('*.md')):
    lines = f.read_text(encoding='utf-8').splitlines()
    print('===', f, 'lines', len(lines))
    for L in lines[-6:]:
        print(repr(L)[:100])
    print()
"@
 (Inspect ends of protocol and extension pages)
- Edit: C:\OpenDelivery\opendelivery-v2\tools\_add_protocol_related.py
- Execute: .\.venv\Scripts\python.exe tools\_add_protocol_related.py (Add API Spec notes and Related blocks to Protocol)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md (1-30)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\orders.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.md (1-25)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.md (1-45)
- Read: C:\OpenDelivery\opendelivery-v2\docs\extensions\loyalty.md (1-35)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\authentication.en.md (1-25)
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\principles.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.en.md (1-20)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.md
- Read: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.en.md (1-35)
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\discovery.en.md
- Edit: C:\OpenDelivery\opendelivery-v2\docs\protocol\indoor.en.md
- Execute: Remove-Item tools\_add_protocol_related.py -Force -ErrorAction SilentlyContinue; .\.venv\Scripts\python.exe -m mkdocs build --strict 2>&1 | Select-String -Pattern "ERROR|WARNING –|built|unrecognized" (Remove temp script and build docs)

## Assistant

Concordo e já está aplicado.

### Padrão

**1. Topo (capabilities + Discovery + Auth + extensões)**  
Admonition fixo:

> **Especificação da API** / **API Spec**  
> Contrato implementável em **[link da spec]** — somente em inglês.

**2. Fim da página**  
Bloco **Relacionado** (`.od-related`), com a **spec em primeiro** quando existir.

### Onde entrou

| Página | Note no topo → Spec | Relacionado |
|--------|---------------------|-------------|
| Discovery, Auth | ✓ | ✓ |
| Orders, Logistics, Merchant, Dados da Loja, Menus | ✓ | ✓ |
| Customer, Indoor, Reviews, Loyalty | ✓ | ✓ |
| Princípios, Fluxos, Evolução, Papéis | — (sem spec 1:1) | ✓ (com API geral quando faz sentido) |

Removi rodapés antigos do tipo “Referência completa…” que competiam com o bloco novo, e enxuguei textos duplicados em Discovery/Indoor.

Build ok.