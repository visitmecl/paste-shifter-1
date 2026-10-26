# Indexación y metadatos sociales

El sitio estático se publica desde `Store/Site` mediante `vercel.json`.

- `robots.txt`: permite rastrear el sitio e indica el sitemap; no es un mecanismo de autorización.
- `sitemap.xml`: portada, ficha del producto, soporte y privacidad. Añadir futuras páginas públicas aquí.
- `product.html`: ficha factual, accesible por enlaces HTML desde las páginas públicas.
- `llms.txt`: índice opcional de documentación; no garantiza indexación o respuestas de IA. Google Search no lo utiliza para mejorar visibilidad.
- Metadatos por página: canonical, descripción, Open Graph, Twitter Cards y JSON-LD.
- `SoftwareApplication` describe capacidades y requisitos confirmados. No se inventan ofertas, precios o valoraciones; no se promete elegibilidad para resultados enriquecidos de Google.
- `assets/social-card.png`: imagen social opaca de 1200 × 630 px, con texto alternativo y URL absoluta. Al sustituirla, versionar el nombre si las plataformas conservan una vista previa antigua.

## Validación

Desde la raíz: `python3 scripts/check_site_metadata.py`.

La comprobación revisa coherencia entre sitemap, canonical, enlaces y archivos locales, metadatos completos, JSON-LD parseable y dimensiones reales de la imagen. No sustituye una comprobación de indexación en Search Console ni un validador externo de resultados enriquecidos.

Después de publicar: comprobar respuesta 200 de las cuatro páginas, robots, sitemap, llms e imagen social. El envío del sitemap y la inspección de URLs en Search Console son pasos independientes; no se realizan automáticamente desde este PR.

Referencias: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide y https://developers.google.com/search/docs/appearance/structured-data/software-app.

## Imagen social

Generada con imagegen integrado a partir del icono original y del producto aprobado. Exportada con sips a 1200 × 630 px.

Prompt:

Create a polished Open Graph social sharing image for Paste Shifter. Landscape ratio 1200:630, opaque pale lavender/off-white background. Reference 1 is exact brand icon, preserve its two asymmetric white shapes and purple glitter rounded square, NO circular dot. Reference 2 is product visual, preserve MacBook, clipboard cards and Android phone as supporting right-hand composition. On left, small logo + brand name 'Paste Shifter', then huge bold black sans-serif exact headline 'Tu portapapeles. Siempre a mano.' Below, modest violet text 'Mac + Android · Conexión Orbital'. High-end minimalist editorial design, subtle violet orbit curve and soft shadows, all content 60px from edges, highly legible as link thumbnail. Keep headline as dominant content with no clipping. Product group occupies right 48%, no overlap with text. No ratings, prices, store badges or extra copy. Produce single finished social card, not a mockup around it, not transparent.
