---
hide:
  - toc
title: Open Delivery Protocol
description: A linguagem de interoperabilidade do delivery de alimentos no Brasil.
---

<div class="landing-page">

  <!-- ── HERO ─────────────────────────────────────────────────── -->
  <div class="hero-wrapper">
    <div class="hero-content">
      <div class="hero-badges">
        <span class="od-badge od-badge--rc">V2.0.0-rc</span>
        <span class="od-badge">Protocolo de interoperabilidade</span>
      </div>
      <h1>Open Delivery Protocol</h1>
      <p class="hero-tagline">A linguagem universal do food service.</p>
      <p class="hero-body">
        Open Delivery define como plataformas de pedido, sistemas de gestão e operações logísticas se comunicam — do pedido ao salão — permitindo que qualquer participante do ecossistema opere sob um único padrão, sem integrações customizadas ponto-a-ponto.
      </p>
      <div class="hero-actions">
        <a href="guide/getting-started/" class="hero-btn hero-btn--primary">Começar integração</a>
        <a href="guide/migration-v1-v2/" class="hero-btn hero-btn--secondary">Migrar da V1</a>
        <a href="guide/changelog/" class="hero-btn hero-btn--ghost">O que mudou na V2</a>
      </div>
    </div>
  </div>

  <hr class="od-divider">

  <!-- ── 3 CAMADAS ────────────────────────────────────────────── -->
  <div class="section-intro">
    <h2>Como a documentação se organiza</h2>
    <p>O Open Delivery é um <strong>protocolo</strong>, não um produto. A documentação separa entendimento, regras e contrato de implementação.</p>
  </div>

  <div class="layers-grid">
    <a href="documentation/core-concepts/" class="layer-card">
      <span class="layer-card__step">1</span>
      <h3>Guia</h3>
      <p>Conceitos, papéis, primeiros passos e migração. Entenda o ecossistema antes de codar.</p>
    </a>
    <a href="protocol/principles/" class="layer-card">
      <span class="layer-card__step">2</span>
      <h3>Protocolo</h3>
      <p>Regras normativas, fluxos, status e eventos por capability — independente de framework.</p>
    </a>
    <a href="reference/" class="layer-card">
      <span class="layer-card__step">3</span>
      <h3>Referência da API</h3>
      <p>Contrato OpenAPI (REST/HTTP) com endpoints, schemas e exemplos — renderizado com ReDoc.</p>
    </a>
  </div>

  <hr class="od-divider">

  <!-- ── POR ONDE COMEÇAR ──────────────────────────────────────── -->
  <div class="section-intro">
    <h2>Por onde você quer começar?</h2>
    <p>Escolha o caminho que melhor descreve o que você precisa agora.</p>
  </div>

  <div class="path-grid">

    <!-- PATH 1: Novo aqui -->
    <div class="path-card path-card--new">
      <div class="path-label path-label--new">Novo aqui</div>
      <h3>Não conheço o projeto</h3>
      <p>Entenda o que é o Open Delivery, como o ecossistema funciona e quais problemas o protocolo resolve antes de qualquer implementação.</p>
      <ul class="path-links">
        <li><a href="documentation/core-concepts/">O que é o Open Delivery?</a></li>
        <li><a href="protocol/principles/">Princípios do protocolo</a></li>
        <li><a href="protocol/roles-and-responsibilities/">Papéis no ecossistema</a></li>
        <li><a href="PROTOCOL_VS_BINDING/">Protocolo vs Binding</a></li>
      </ul>
    </div>

    <!-- PATH 2: Vou implementar -->
    <div class="path-card path-card--implement">
      <div class="path-label path-label--implement">Quero implementar</div>
      <h3>Conheço o projeto, vou implementar o protocolo V2</h3>
      <p>Você já sabe o que é o Open Delivery — ou conhecia a V1 — e quer iniciar ou aprofundar sua implementação do protocolo V2.</p>
      <ul class="path-links">
        <li><a href="guide/getting-started/">Primeiros Passos</a></li>
        <li><a href="protocol/discovery/">Configurar o Discovery</a></li>
        <li><a href="protocol/authentication/">Autenticar minha aplicação</a></li>
        <li><a href="reference/">Referência da API</a></li>
      </ul>
    </div>

    <!-- PATH 3: Migrar da V1 -->
    <div class="path-card path-card--migrate">
      <div class="path-label path-label--migrate">Migrando da V1</div>
      <h3>Tenho uma implementação V1 e quero migrar para V2</h3>
      <p>Você já implementou o protocolo V1 e precisa entender o que mudou, o que quebra e como planejar a migração.</p>
      <ul class="path-links">
        <li><a href="guide/changelog/">O que mudou na V2?</a></li>
        <li><a href="guide/migration-v1-v2/">Guia de Migração V1→V2</a></li>
        <li><a href="guide/getting-started/">Primeiros Passos na V2</a></li>
      </ul>
    </div>

  </div>

  <hr class="od-divider">

  <!-- ── POR PAPEL ─────────────────────────────────────────────── -->
  <div class="section-intro">
    <h2>Quem é você no ecossistema?</h2>
    <p>Trilhas de implementação por papel — o Open Delivery não exige todas as capabilities de uma vez.</p>
  </div>

  <div class="role-grid">
    <a href="guide/by-role/#originador" class="role-card">
      <span class="role-card__label">Originador</span>
      <h3>App, marketplace, totem</h3>
      <p>Cria pedidos, consome cardápio e acompanha o ciclo de vida.</p>
      <span class="role-card__caps">Orders · Merchant · Discovery</span>
    </a>
    <a href="guide/by-role/#pdv" class="role-card">
      <span class="role-card__label">PDV / Software</span>
      <h3>Gestão do restaurante</h3>
      <p>Confirma pedidos, publica catálogo e é autoridade da conta em salão.</p>
      <span class="role-card__caps">Merchant · Orders · Indoor</span>
    </a>
    <a href="guide/by-role/#logistica" class="role-card">
      <span class="role-card__label">Logística</span>
      <h3>Entrega e tracking</h3>
      <p>Cotação, despacho e eventos de entrega sem redefinir o status do pedido.</p>
      <span class="role-card__caps">Logistics · Orders</span>
    </a>
    <a href="guide/by-role/#crm" class="role-card">
      <span class="role-card__label">CRM</span>
      <h3>Cliente, reviews, fidelidade</h3>
      <p>Relacionamento e inteligência — sem alterar o fluxo operacional da cozinha.</p>
      <span class="role-card__caps">Customer · Reviews · Loyalty</span>
    </a>
  </div>

  <p class="role-grid-more"><a href="guide/by-role/">Ver trilhas completas por papel →</a></p>

  <hr class="od-divider">

  <!-- ── CAPABILITIES ──────────────────────────────────────────── -->
  <div class="section-intro">
    <h2>Capabilities do protocolo</h2>
    <p>Capabilities são as áreas funcionais do protocolo. Elas são <strong>independentes</strong>: cada participante implementa apenas o que faz sentido para o seu papel.</p>
  </div>

  <div class="cap-strip">

    <!-- Merchant -->
    <div class="cap-group">
      <a href="protocol/merchant/" class="cap-item cap-item--parent">
        <div class="cap-item-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="4" y="3" width="11" height="18" rx="1"/>
            <path d="M9 21v-4h2v4"/>
            <path d="M7 7h2M11 7h2M7 11h2M11 11h2M7 15h2M11 15h2"/>
            <path d="M15 9h4a1 1 0 0 1 1 1v11h-5"/>
          </svg>
        </div>
        <span class="cap-item-name">Merchant</span>
      </a>
      <div class="cap-group__children">
        <a href="protocol/merchant-store/" class="cap-item cap-item--child">
          <div class="cap-item-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l1.5-4.5h15L21 9"/>
              <path d="M4 9v10a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9"/>
              <path d="M10 20v-6h4v6"/>
            </svg>
          </div>
          <span class="cap-item-name">Dados da Loja</span>
        </a>
        <a href="protocol/menu/" class="cap-item cap-item--child">
          <div class="cap-item-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 6h16M4 12h16M4 18h10"/>
            </svg>
          </div>
          <span class="cap-item-name">Menus</span>
        </a>
      </div>
    </div>

    <!-- Orders + Indoor -->
    <div class="cap-group">
      <a href="protocol/orders/" class="cap-item cap-item--parent">
        <div class="cap-item-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="6" y="4" width="12" height="17" rx="2"/>
            <path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/>
            <path d="M9 11h6M9 14h6M9 17h4"/>
          </svg>
        </div>
        <span class="cap-item-name">Orders</span>
      </a>
      <div class="cap-group__children">
        <a href="protocol/indoor/" class="cap-item cap-item--child">
          <div class="cap-item-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="6" width="20" height="14" rx="2"/>
              <path d="M2 10h20"/>
              <circle cx="7" cy="15" r="1.5"/>
              <circle cx="12" cy="15" r="1.5"/>
              <circle cx="17" cy="15" r="1.5"/>
            </svg>
          </div>
          <span class="cap-item-name">Indoor</span>
          <span class="cap-item-new">Novo</span>
        </a>
      </div>
    </div>

    <!-- Logistics -->
    <div class="cap-group">
      <a href="protocol/logistics/" class="cap-item cap-item--parent">
        <div class="cap-item-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 21s7-7.21 7-12a7 7 0 1 0-14 0c0 4.79 7 12 7 12Z"/>
            <circle cx="12" cy="9" r="2.5"/>
          </svg>
        </div>
        <span class="cap-item-name">Logistics</span>
      </a>
    </div>

    <!-- Customer + Reviews + Loyalty -->
    <div class="cap-group">
      <a href="protocol/customer/" class="cap-item cap-item--parent">
        <div class="cap-item-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="8" r="3.5"/>
            <path d="M5 20c0-3.866 3.134-7 7-7s7 3.134 7 7"/>
          </svg>
        </div>
        <span class="cap-item-name">Customer</span>
        <span class="cap-item-new">Novo</span>
      </a>
      <div class="cap-group__children">
        <a href="extensions/reviews/" class="cap-item cap-item--child">
          <div class="cap-item-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
          </div>
          <span class="cap-item-name">Reviews</span>
          <span class="cap-item-new">Novo</span>
        </a>
        <a href="extensions/loyalty/" class="cap-item cap-item--child">
          <div class="cap-item-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 21.593c-5.63-5.539-11-10.297-11-14.402C1 3.518 3.8 1 7.4 1c1.8 0 3.4.754 4.6 1.965C13.2 1.754 14.8 1 16.6 1 20.2 1 23 3.518 23 7.19c0 4.106-5.37 8.863-11 14.403z"/>
            </svg>
          </div>
          <span class="cap-item-name">Loyalty</span>
          <span class="cap-item-new">Novo</span>
        </a>
      </div>
    </div>

  </div>

  <hr class="od-divider">

  <!-- ── O QUE MUDOU ───────────────────────────────────────────── -->
  <div class="section-intro">
    <h2>O que mudou na V2</h2>
    <p>Principais mudanças da Release Candidate. Detalhes e tabelas no changelog.</p>
  </div>

  <div class="wn-strip">
    <a href="guide/changelog/" class="wn-pill wn-pill--break">Auth por aplicação</a>
    <a href="guide/changelog/" class="wn-pill wn-pill--break">Merchant ID do originador</a>
    <a href="guide/changelog/" class="wn-pill wn-pill--break">Cardápio com CRUD</a>
    <a href="protocol/customer/" class="wn-pill wn-pill--new">Customer / CRM</a>
    <a href="protocol/indoor/" class="wn-pill wn-pill--new">Indoor / Salão</a>
    <a href="protocol/discovery/" class="wn-pill wn-pill--improve">Discovery obrigatório</a>
    <a href="guide/changelog/" class="wn-pill wn-pill--more">Ver changelog completo →</a>
  </div>

  <hr class="od-divider">

  <!-- ── ECOSYSTEM ─────────────────────────────────────────────── -->
  <div class="eco-strip">
    <span class="eco-strip-label">Links do ecossistema:</span>

    <a href="https://github.com/Abrasel-Nacional/opendelivery-v2" class="eco-link" target="_blank">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2z"/>
      </svg>
      GitHub
    </a>

    <a href="guide/changelog/" class="eco-link">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 8v4l3 3"/>
        <circle cx="12" cy="12" r="9"/>
      </svg>
      Changelog
    </a>

    <a href="documentation/roadmap/" class="eco-link">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12h18M3 6l4-3 4 3 4-3 4 3M3 18l4 3 4-3 4 3 4-3"/>
      </svg>
      Roadmap
    </a>

    <a href="https://github.com/Abrasel-Nacional/opendelivery-v2/issues" class="eco-link" target="_blank">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      Reportar Issue
    </a>

  </div>

</div>
