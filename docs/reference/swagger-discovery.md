# Discovery API - Swagger UI

This page renders the REST/HTTP Discovery OpenAPI contract using Swagger UI.

Normative behavior remains defined in [Discovery and Well-Known](../protocol/discovery.md).

<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
<style>
  #swagger-ui {
    min-height: 75vh;
  }
  .swagger-ui .topbar {
    display: none;
  }
</style>

<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
  window.addEventListener('load', function () {
    SwaggerUIBundle({
      url: '../v2/rest-http-discovery.openapi.yaml',
      dom_id: '#swagger-ui',
      deepLinking: true,
      displayRequestDuration: true,
      docExpansion: 'list',
      defaultModelsExpandDepth: -1,
      filter: true,
      tryItOutEnabled: false
    });
  });
</script>
