# CLI Career Homologations

Herramienta de linea de comandos para analizar compatibilidad de homologacion entre programas academicos usando syllabus en Excel, planes de estudio en PDF y comparadores deterministico/LLM local.

## Requisitos

- Nix + direnv habilitado para este proyecto.
- Python/uv provistos por el dev shell.
- Los archivos reales deben estar en `data/raw/`.

Recargar entorno:

```bash
direnv allow
direnv reload
```

Validar:

```bash
uv run pytest -q
```

## Inventario y extraccion XLSX

Generar inventario:

```bash
uv run homologations inventory \
  data/raw \
  --output data/processed/inventory.json
```

Extraer syllabus legibles a JSON:

```bash
uv run homologations extract-xlsx \
  data/raw \
  --output data/processed/syllabus.json
```

## Analisis por planes de estudio PDF

Este flujo usa el plan de estudios para comparar espacios academicos por nombre y creditos.

Reglas actuales:

- Nombre equivalente + creditos origen >= creditos destino: homologacion 100%.
- Nombre equivalente + creditos origen < creditos destino: no homologable por deficit de creditos.
- Niveles distintos no son equivalencia directa, por ejemplo `Lengua extranjera I` no homologa directamente con `Lengua extranjera V`.

Ejemplo: Sistemas vs Marketing

```bash
uv run homologations analyze-plans \
  data/raw/SYLLABUS_INGENIERIA_DE_SISTEMAS/plan-de-estudios-ingenieria-de-sistemas-hibrida-santo-tomas-tunja-boyaca-2026.pdf \
  data/raw/SYLLABUS_MARKETING_Y_TRANSOFRMACION_DIGITAL/plan-de-estudios-Marketing-y-Transformacion-Digital-santoto-tunja-boyaca-2026-1.pdf \
  --source-program "Ingenieria de Sistemas" \
  --target-program "Marketing y Transformacion Digital" \
  --output-json data/reports/sistemas_vs_marketing_plan.json \
  --output-csv data/reports/sistemas_vs_marketing_plan.csv
```

## Analisis deterministico desde JSON procesado

Este flujo evita reabrir los Excel y compara desde `data/processed/syllabus.json`.

```bash
uv run homologations analyze-processed \
  data/processed/syllabus.json \
  SYLLABUS_INGENIERIA_DE_SISTEMAS \
  SYLLABUS_Diseño_De_Interaccion \
  --comparator deterministic \
  --output-json data/reports/sistemas_vs_diseno_processed.json \
  --output-csv data/reports/sistemas_vs_diseno_processed.csv
```

## Analisis con llama.cpp local

Primero levantar el servidor local en una terminal:

```bash
direnv exec . llama-server \
  --hf-repo Qwen/Qwen3-4B-GGUF:Q4_K_M \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 4096 \
  --threads 4
```

Notas:

- La primera ejecucion descarga el modelo GGUF en cache local de llama.cpp.
- En CPU puede tardar bastante.
- Para pruebas iniciales usar `--candidate-limit 1`.

En otra terminal ejecutar:

```bash
uv run homologations analyze-processed \
  data/processed/syllabus.json \
  SYLLABUS_INGENIERIA_DE_SISTEMAS \
  SYLLABUS_Diseño_De_Interaccion \
  --comparator llamacpp \
  --model Qwen/Qwen3-4B-GGUF:Q4_K_M \
  --candidate-limit 1 \
  --llamacpp-timeout 900 \
  --llamacpp-max-tokens 320 \
  --output-json data/reports/sistemas_vs_diseno_llamacpp.json \
  --output-csv data/reports/sistemas_vs_diseno_llamacpp.csv
```

Si llama.cpp devuelve JSON invalido, el analisis no se detiene: ese par usa fallback deterministico y deja evidencia en el reporte.

## Salidas

Los reportes se generan en:

```text
data/reports/
```

Los archivos reales y reportes locales estan ignorados por Git:

```text
data/raw/
data/processed/
data/reports/
```
