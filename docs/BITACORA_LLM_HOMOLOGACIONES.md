# Bitacora del fork: homologacion academica asistida por LLM

## Objetivo del fork

Construir una herramienta de linea de comandos que compare espacios academicos entre dos carreras, estime que materias son homologables y entregue:

- porcentaje general de compatibilidad entre carreras;
- porcentaje de compatibilidad por cada materia origen contra sus mejores candidatas destino;
- decision de homologacion por materia usando un umbral minimo del 40%;
- evidencia textual que explique por que una materia supera o no supera el umbral.

El enfoque del fork sera usar un LLM mediano, por ejemplo Qwen, para comparar contenidos academicos extraidos desde archivos Excel. El LLM no deberia reemplazar todo el flujo: primero se debe extraer informacion estructurada y luego pedirle al modelo una evaluacion controlada con salida JSON.

## Estado actual del proyecto

### Estructura encontrada

```text
src/
  entities/
    subject.py
    competency.py
    human_action_dimensions.py
  gateways/
    parsing_syllabus_gateway.py
  adapters/
    parsing_syllabus_gateway/
      xlsx/
        xlsx_parsing_syllabus_gateway.py
tests/
  entities/
  adapters/syllabus_gateways/
```

El proyecto ya esta orientado a una arquitectura simple de puertos y adaptadores:

- `entities`: modelos de dominio (`Subject`, `Competency`, `HumanActionDimensions`).
- `gateways`: contratos o interfaces, hoy con `ParsingSyllabusGateway`.
- `adapters`: implementaciones concretas, hoy pensadas para leer syllabus desde XLSX.
- `tests`: pruebas unitarias y de adaptadores.

### Estado de pruebas

Comando usado:

```bash
uv run pytest -q
```

Resultado actual:

- 1 prueba pasa: igualdad de `HumanActionDimensions`.
- 1 prueba falla: `test_marketing_syllabus`.

La falla ocurre porque `XLSXParsingSyllabusGateway.extract_subject_from_syllabus()` aun no retorna un `Subject`; el metodo solo tiene documentacion y no tiene implementacion.

### Observaciones de estilo y diseno

- Se usan `dataclass(frozen=True)`, buena base para datos de dominio inmutables.
- Se usa `Protocol`, buena base para mantener interfaces limpias.
- El adaptador XLSX todavia no existe funcionalmente.
- `HumanActionDimensions.__eq__` es redundante: `dataclass` ya genera igualdad por valor, pero no es urgente cambiarlo.
- Hay nombres en camelCase (`problemicCore`, `didacticStrategies`, `humanActionDimensions`) dentro de Python. Conviene no cambiarlos al inicio para evitar tocar archivos originales y romper pruebas, pero los nuevos modulos podrian usar `snake_case` y mapear al dominio existente.
- El contrato `ParsingSyllabusGateway.extract_subject_from_syllabus` deberia declarar `self` si se espera instancia; hoy el adaptador lo usa con `self`.
- La prueba de XLSX contiene un problema probable: `for want_competency, index in enumerate(want.competencies)` invierte los nombres. Lo correcto seria `for index, want_competency in enumerate(...)`. No se toca todavia para respetar la regla de no modificar originales.

## Regla de trabajo para este fork

1. No modificar entidades originales salvo que sea indispensable.
2. No reescribir el adaptador original hasta tener clara la forma real de los Excel.
3. Agregar funcionalidades nuevas en modulos nuevos.
4. Reutilizar las interfaces existentes cuando ayuden.
5. Mantener pruebas para cada paso funcional.
6. Separar extraccion, normalizacion, comparacion y reporte.

## Rama de trabajo

Rama creada:

```bash
feat/llm-homologation-roadmap
```

Cambios locales previos detectados y no tocados:

```text
.direnv/bin/nix-direnv-reload
.direnv/flake-profile-d2fb9f988e3626867595d62109c330e08a0fc244.rc
```

Estos archivos parecen pertenecer al entorno local y no a la funcionalidad.

## Flujo funcional propuesto

### Paso 1: Entrada

El usuario entrega dos carpetas o archivos Excel:

```bash
homologations analyze \
  --source "Ingenieria de Sistemas" ./data/sistemas/*.xlsx \
  --target "Ingenieria de Datos e Inteligencia Artificial" ./data/datos-ia/*.xlsx \
  --model qwen
```

Cada Excel representa un espacio academico o syllabus.

### Paso 2: Extraccion estructurada

Responsabilidad:

- leer XLSX;
- encontrar campos academicos relevantes;
- construir objetos tipo `Subject`;
- conservar texto crudo util para auditoria.

Campos minimos recomendados:

- nombre del espacio academico;
- programa;
- proposito u objetivo;
- nucleo problemico;
- estrategias didacticas;
- competencias;
- resultados de aprendizaje;
- contenidos;
- tiempos o creditos si existen;
- mecanismos de evaluacion;
- recursos didacticos.

### Paso 3: Normalizacion

Crear una representacion interna para comparacion, sin cambiar las entidades originales:

```text
src/use_cases/
src/services/
src/adapters/llm/
src/reports/
```

Propuesta de modelos nuevos:

- `ComparableSubject`: texto normalizado para comparar.
- `SubjectMatch`: resultado de una comparacion materia contra materia.
- `CareerHomologationReport`: resultado agregado de carrera contra carrera.

### Paso 4: Comparacion con LLM

El LLM debe recibir dos materias a la vez y devolver JSON estricto:

```json
{
  "source_subject": "Programacion I",
  "target_subject": "Fundamentos de programacion",
  "score": 0.72,
  "homologable": true,
  "threshold": 0.40,
  "criteria": {
    "contents": 0.75,
    "learning_results": 0.70,
    "competencies": 0.80,
    "evaluation": 0.50,
    "workload": 0.60
  },
  "evidence": [
    "Ambas materias cubren estructuras de control y programacion basica.",
    "Los resultados de aprendizaje comparten aplicacion practica de algoritmos."
  ],
  "risks": [
    "No se encontro equivalencia explicita en intensidad horaria."
  ]
}
```

Regla principal:

- si `score >= 0.40`, la materia es candidata homologable;
- si `score < 0.40`, no debe recomendarse como homologacion;
- el reporte puede mostrar candidatas por debajo del umbral, pero marcadas como no homologables.

### Paso 5: Seleccion de mejores equivalencias

Para cada materia origen:

1. Comparar contra todas las materias destino o contra un subconjunto prefiltrado.
2. Ordenar por `score` descendente.
3. Elegir la mejor candidata.
4. Marcar homologable si supera 40%.
5. Guardar tambien segunda y tercera candidata para revision humana.

### Paso 6: Porcentaje general

Calculo inicial recomendado:

```text
porcentaje_general = materias_homologables / total_materias_origen
```

Ejemplo:

```text
18 materias homologables / 42 materias origen = 42.86%
```

Mas adelante se puede ponderar por creditos o intensidad horaria si los Excel lo contienen de forma confiable.

### Paso 7: Reporte

Formatos recomendados:

- consola: resumen corto;
- CSV: tabla de resultados;
- JSON: salida completa para auditoria;
- HTML opcional: vista navegable usando futuras interfaces.

Columnas minimas:

- programa origen;
- materia origen;
- programa destino;
- mejor materia destino;
- porcentaje;
- homologable;
- justificacion;
- riesgos;
- candidatas alternativas.

## Diseno tecnico recomendado

### Capas

```text
src/
  entities/                         # existente
  gateways/                         # existente
  adapters/
    parsing_syllabus_gateway/       # existente
    llm/                            # nuevo
    reports/                        # nuevo
  use_cases/                        # nuevo
  services/                         # nuevo
  cli/                              # nuevo
```

### Puertos nuevos

```python
class SubjectComparatorGateway(Protocol):
    def compare(self, source: Subject, target: Subject) -> SubjectMatch:
        ...
```

```python
class CareerReportGateway(Protocol):
    def write(self, report: CareerHomologationReport, output_path: Path) -> None:
        ...
```

### Adaptadores nuevos

- `QwenSubjectComparatorGateway`: llama a Qwen local o remoto.
- `JsonReportGateway`: escribe resultados completos.
- `CsvReportGateway`: escribe tabla resumida.

### Caso de uso principal

```python
class AnalyzeCareerHomologation:
    def execute(self, source_paths: list[Path], target_paths: list[Path]) -> CareerHomologationReport:
        ...
```

Este caso de uso debe orquestar:

1. parseo XLSX;
2. normalizacion;
3. comparacion;
4. seleccion de mejores matches;
5. calculo de porcentaje general;
6. generacion de reporte.

## Estrategia con Qwen

### Opcion local

Usar Qwen mediante Ollama, llama.cpp, vLLM o Transformers, segun recursos disponibles.

Ventajas:

- privacidad de archivos academicos;
- costo bajo por ejecucion;
- facil repetir analisis.

Riesgos:

- variabilidad de salida;
- consumo de memoria;
- necesidad de validar JSON.

### Reglas para prompts

- Pedir salida JSON estricta.
- Incluir rubrica de evaluacion.
- Prohibir inventar campos ausentes.
- Obligar a citar evidencia desde textos recibidos.
- Usar temperatura baja.
- Reintentar si la respuesta no es JSON valido.

### Rubrica inicial

Ponderacion sugerida:

- contenidos: 35%;
- resultados de aprendizaje: 25%;
- competencias: 25%;
- evaluacion y metodologia: 10%;
- intensidad horaria o creditos: 5%.

El puntaje final debe estar entre `0.0` y `1.0`.

## Bitacora paso a paso

### Fase 0: Orden del repositorio

- Crear rama de trabajo.
- Documentar diagnostico inicial.
- No tocar archivos originales.
- Confirmar pruebas actuales.

Estado: completado parcialmente en esta rama.

### Fase 1: Entender los Excel reales

- Recolectar al menos 2 syllabus de Sistemas y 2 de Datos e IA.
- Revisar si todos usan la misma plantilla.
- Definir campos obligatorios y opcionales.
- Documentar celdas, titulos y variaciones.

Salida esperada:

- fixtures de prueba;
- mapa de plantilla XLSX;
- decision sobre libreria de lectura (`openpyxl` probablemente).

Avance:

- Se agrego inventario automatico sobre `data/raw`.
- Se detectaron 274 archivos totales.
- Se detectaron 81 archivos `.xlsx` no vacios y soportados.
- Se detectaron 189 archivos vacios.
- Se detectaron 3 archivos no soportados por ahora (`.xlsb`/`.ods`).
- Se ignoro `desktop.ini`.
- Los `.xlsx` no vacios procesados actualmente pertenecen a `SYLLABUS_Diseño_De_Interaccion` e `SYLLABUS_INGENIERIA_DE_SISTEMAS`.

### Fase 2: Implementar extraccion XLSX sin LLM

- Agregar dependencia de lectura XLSX.
- Implementar adaptador o crear uno nuevo para no tocar el original.
- Crear pruebas con fixtures pequenos.
- Validar que cada Excel produzca un `Subject`.

Salida esperada:

- parser confiable;
- pruebas verdes para extraccion.

Avance:

- Se agrego `openpyxl`.
- Se implemento extraccion base desde `.xlsx`.
- Se extraen nombre de programa, nombre de espacio academico, proposito, nucleo problemico, estrategias didacticas y competencias.
- Se agrego soporte para variaciones de plantilla en ingles y syllabus repartidos en varias hojas.
- Se agrego CLI inicial:
  - `homologations inventory data/raw --output data/processed/inventory.json`
  - `homologations extract-xlsx data/raw --output data/processed/syllabus.json`
- Extraccion actual: 81 syllabus procesados, 0 errores de lectura.
- Cobertura actual: 0 registros sin nombre, 0 sin objetivo y 0 sin competencias.
- Competencias extraidas: 234.
- Pendiente tecnico menor: agregar progreso por archivo en la CLI porque algunos libros de ingles tardan varios segundos.

### Fase 3: Modelos de resultado

- Crear modelos nuevos para `SubjectMatch` y `CareerHomologationReport`.
- Agregar calculo del umbral de 40%.
- Probar reglas sin LLM usando comparador falso.

Salida esperada:

- logica de homologacion independiente del modelo.

Avance:

- Se agregaron modelos de resultado:
  - `SubjectMatch`
  - `SubjectHomologationResult`
  - `CareerHomologationReport`
- Se agrego un comparador deterministico temporal basado en similitud textual.
- Se agrego la regla de homologacion `score >= 0.40`.
- Se agrego generacion de reportes JSON y CSV.
- Se agrego comando:
  - `homologations analyze <programa_origen> <programa_destino> --output-json ... --output-csv ...`
- Se agrego comando rapido desde JSON procesado:
  - `homologations analyze-processed data/processed/syllabus.json <prefijo_origen> <prefijo_destino> --output-json ... --output-csv ...`
- Prueba real ejecutada:
  - origen: `data/raw/SYLLABUS_INGENIERIA_DE_SISTEMAS`
  - destino: `data/raw/SYLLABUS_Diseño_De_Interaccion`
  - resultado baseline: 25 materias origen, 56 materias destino, 1 homologable, 4% general.
- La misma prueba desde `data/processed/syllabus.json` mantiene el resultado y evita reabrir Excel.
- Nota: este comparador es solo una base deterministica para validar la tuberia. La decision academica debe venir despues con LLM y revision humana.

### Fase 4: Comparador LLM

- Crear interfaz `SubjectComparatorGateway`.
- Implementar adaptador Qwen.
- Validar JSON con esquema o dataclasses.
- Agregar cache por hash de materias para no recalcular.

Salida esperada:

- comparaciones reproducibles;
- errores controlados cuando el modelo responde mal.

Avance:

- Se agrego el contrato `SubjectComparatorGateway`.
- Se adapto el comparador deterministico al contrato.
- Se agrego `LlamaCppSubjectComparator`, que llama a un endpoint OpenAI-compatible de `llama-server`.
- Se agrego `llama-cpp` al shell Nix.
- La CLI ahora acepta:
  - `--comparator deterministic`
  - `--comparator llamacpp`
  - `--llamacpp-url`
  - `--model`
  - `--candidate-limit`
- Para evitar demasiadas llamadas al modelo, el modo `llamacpp` preselecciona candidatos con el comparador deterministico. Por defecto usa 3 candidatos destino por materia origen.

Arrancar modelo local con llama.cpp:

```bash
direnv exec . llama-server \
  --hf-repo Qwen/Qwen3-4B-GGUF:Q4_K_M \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 8192
```

Ejecutar analisis con llama.cpp:

```bash
uv run homologations analyze-processed \
  data/processed/syllabus.json \
  SYLLABUS_INGENIERIA_DE_SISTEMAS \
  SYLLABUS_Diseño_De_Interaccion \
  --comparator llamacpp \
  --model Qwen/Qwen3-4B-GGUF:Q4_K_M \
  --candidate-limit 3 \
  --output-json data/reports/sistemas_vs_diseno_llamacpp.json \
  --output-csv data/reports/sistemas_vs_diseno_llamacpp.csv
```

Nota: en CPU puede ser lento. Para primeras pruebas se recomienda usar `--candidate-limit 1` o filtrar pocos syllabus. Si aparece `TimeoutError`, usar:

```bash
--llamacpp-timeout 900 --llamacpp-max-tokens 320 --candidate-limit 1
```

Tambien se recomienda arrancar `llama-server` con `--ctx-size 4096` en CPU si `8192` queda lento o consume demasiada RAM.

Si llama.cpp devuelve JSON incompleto o invalido, el analisis ya no se detiene: ese par usa fallback deterministico y deja evidencia en el reporte.

### Fase 5: CLI

- Crear comando `homologations analyze`.
- Recibir rutas origen y destino.
- Permitir elegir modelo y umbral.
- Exportar JSON y CSV.

Salida esperada:

- herramienta usable desde terminal.

### Fase 6: Reporte y revision humana

- Mostrar ranking por materia.
- Resaltar homologables y no homologables.
- Mostrar justificacion y riesgos.
- Permitir revisar casos cercanos al umbral, por ejemplo 35%-45%.

Salida esperada:

- reporte util para una decision academica, no solo un numero.

## Proximos cambios recomendados

1. Agregar archivos Excel reales de prueba en una carpeta no versionada o en fixtures anonimizados.
2. Crear modelos de reporte nuevos sin modificar `Subject`.
3. Implementar un comparador falso primero para probar calculos.
4. Despues conectar Qwen cuando el flujo deterministico ya funcione.

## Comandos utiles

Ejecutar pruebas:

```bash
uv run pytest -q
```

Ver estado de Git:

```bash
git status --short --branch
```

Ver rama actual:

```bash
git branch --show-current
```

Crear una rama futura de implementacion:

```bash
git switch -c feat/llm-homologation-core
```

## Criterios de aceptacion iniciales

- La herramienta puede leer dos conjuntos de Excel.
- Cada materia origen recibe al menos una candidata destino.
- Toda materia con compatibilidad menor a 40% queda marcada como no homologable.
- El porcentaje general se calcula y se muestra.
- El reporte incluye evidencia textual y riesgos.
- Las decisiones del LLM quedan guardadas en JSON para auditoria.
