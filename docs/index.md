---
hide:
  - toc
title: Open Delivery Protocol
description: The common language for ordering applications, software services, and logistics providers.
---

<div class="landing-page">

  <!-- ── HERO ──────────────────────────────────────────────── -->
  <div class="hero-wrapper">
    <div class="hero-content">
      <h1>Open Delivery<br>Protocol</h1>
      <p class="hero-subheading">
        The common language for ordering, fulfillment, and delivery.
      </p>
      <p class="hero-description">
        Open Delivery defines building blocks for food and retail delivery coordination—from
        merchant catalog discovery to order placement and last-mile logistics—allowing
        the ecosystem to interoperate through one standard, without custom bilateral integrations.
      </p>
      <a href="documentation/core-concepts/" class="promo-button">Get started</a>
    </div>
    <div class="hero-image">
      <img src="assets/images/opendelivery-logo.png" alt="Open Delivery Protocol logo" class="hero-logo-crisp">
    </div>
  </div>

  <!-- ── PROMO CARDS ───────────────────────────────────────── -->
  <div class="promo-card-wrapper">
    <div class="promo-card">
      <h3>Learn</h3>
      <p>Protocol overview, core concepts, and design principles</p>
      <a href="documentation/core-concepts/" class="promo-button">Read the docs</a>
    </div>
    <div class="promo-card">
      <h3>Implement</h3>
      <p>GitHub repo, technical spec, and capability reference</p>
      <a href="https://github.com/Abrasel-Nacional/opendelivery-v2" class="promo-button" target="_blank">View on GitHub</a>
    </div>
    <div class="promo-card">
      <h3>Contribute</h3>
      <p>Feedback, issues, and pull requests welcome</p>
      <a href="https://github.com/Abrasel-Nacional/opendelivery-v2/issues" class="promo-button" target="_blank">Open an issue</a>
    </div>
  </div>

  <hr class="od-divider">

  <!-- ── CORE CAPABILITIES ─────────────────────────────────── -->
  <div class="section-intro">
    <h2>Core capabilities</h2>
    <p>
      The protocol is organized into independent capabilities. Each capability specifies
      information model, supported operations, interaction roles, and interoperability obligations.
    </p>
    <p>
      Before any capability is used, participants discover each other through the mandatory
      well-known document defined by the protocol.
    </p>
  </div>

  <div class="domain-grid">
    <div class="domain-card">
      <div class="domain-card-icon">🏢</div>
      <h3>Merchant</h3>
      <p>Merchant entity structure and operational rules. Menus, categories, items, availability.</p>
      <br><a href="specification/merchant/" class="promo-button">Learn more</a>
    </div>
    <div class="domain-card">
      <div class="domain-card-icon">📋</div>
      <h3>Orders</h3>
      <p>Order lifecycle, state management, and coordination. Idempotency, events, cancellation.</p>
      <br><a href="specification/orders/" class="promo-button">Learn more</a>
    </div>
    <div class="domain-card">
      <div class="domain-card-icon">👤</div>
      <h3>Customer</h3>
      <p>Customer, lead, and customer-linked order interoperability for CRM, loyalty, and marketing use cases.</p>
      <br><a href="specification/customer/" class="promo-button">Learn more</a>
    </div>
    <div class="domain-card">
      <div class="domain-card-icon">📍</div>
      <h3>Logistics</h3>
      <p>Delivery coordination and tracking. Address resolution, delivery states, and updates.</p>
      <br><a href="specification/logistics/" class="promo-button">Learn more</a>
    </div>
  </div>

  <hr class="od-divider">

  <!-- ── FEATURES ──────────────────────────────────────────── -->
  <div class="section-intro">
    <h2>Built for flexibility, neutrality, and scale</h2>
    <p>
      Delivery coordination demands interoperability. Open Delivery is built on
      transport-agnostic protocol semantics—REST, MCP, or any other binding—so
      different systems work together without custom integration per pair.
    </p>
  </div>

  <div class="features-section">
    <div class="features-list">
      <div class="feature-item">
        <div class="feature-item-icon">🔄</div>
        <div>
          <h3>Transport-agnostic</h3>
          <p>Protocol semantics define conformance. Transport binding (REST, MCP, queues) is a separate layer. The same protocol works over any data interchange mechanism.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-item-icon">🏪</div>
        <div>
          <h3>Merchants at the center</h3>
          <p>Built to facilitate commerce while ensuring merchants retain control of their catalog, pricing, and operational rules. Merchant context is the single source of truth.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-item-icon">📐</div>
        <div>
          <h3>Normative and unambiguous</h3>
          <p>Uses RFC 2119 keywords (MUST, MUST NOT, SHOULD, MAY) throughout. No implicit behavior—if it is not normatively stated, it is not required.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-item-icon">🔗</div>
        <div>
          <h3>Autonomous peers</h3>
          <p>Ordering Application, Software Service, and Logistics Service are independent peers. There is no central orchestrator—each party decides autonomously.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-item-icon">🔒</div>
        <div>
          <h3>Secure and merchant-scoped</h3>
          <p>Credentials are merchant-scoped. Implementations MUST NOT share a single credential set across merchants. Security contracts are first-class protocol citizens.</p>
        </div>
      </div>
    </div>
  </div>

  <hr class="od-divider">

  <!-- ── GET STARTED ───────────────────────────────────────── -->
  <div class="get-started-container">
    <div class="get-started-container-intro">
      <h2>Get started today</h2>
      <p>
        Open Delivery is an open standard designed to let ordering apps, merchant software,
        and logistics providers interact seamlessly—without needing custom, one-off
        integrations for every connection. We actively seek your feedback and contributions.
      </p>
    </div>
    <div class="get-started-container-steps">
      <div class="get-started-container-step">
        <div class="get-started-container-step-icon">📖</div>
        <div>
          <h3><a href="documentation/core-concepts/">Read the concepts</a></h3>
          <p>Understand parties, capabilities, and coordination model</p>
        </div>
      </div>
      <div class="get-started-container-step">
        <div class="get-started-container-step-icon">📐</div>
        <div>
          <h3><a href="protocol/guidelines/">Follow the rules</a></h3>
          <p>Cross-cutting normative rules and RFC 2119 language</p>
        </div>
      </div>
      <div class="get-started-container-step">
        <div class="get-started-container-step-icon">🏗️</div>
        <div>
          <h3><a href="protocol/authentication/">Set up access</a></h3>
          <p>Understand the shared authentication flow before protected capability operations</p>
        </div>
      </div>
    </div>
  </div>

</div>
