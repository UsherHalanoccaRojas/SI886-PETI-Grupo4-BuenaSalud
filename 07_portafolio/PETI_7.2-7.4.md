# PETI · Cadena de Farmacias Buena Salud E.I.R.L.
## Secciones 7.2 a 7.4 · versión v0.14

> Las cifras son estimaciones sin cotización formal y se presentan con su rango. Los pesos y el techo de gasto son supuestos de trabajo pendientes de confirmar en la Entrevista 3 con la gerencia.

## 7.2 Priorización del portafolio

### 7.2.1 Proyectos no negociables y su plazo

Se identificaron 15 proyectos candidatos a partir de los riesgos conocidos (sección H de la ficha), el incidente del periodo (sección G), los hechos verificados (sección F) y los expedientes de inversión. Dos son no negociables y **salen del modelo**, porque no se priorizan: se ejecutan y se ubican por su plazo (`PR01_portafolio_marcado.csv`).

| Proyecto | Norma | Plazo |
|---|---|---|
| P01 Trazabilidad de productos controlados | DIGEMID (Ley 29459 y DS 023-2001-SA, a confirmar con asesor legal) | La exposición ya existe: 214 unidades de diferencia en 4 locales en 2025. Meta interna: 30-jun-2027 |
| P02 Adecuación a la Ley 29733 | Ley 29733 y su Reglamento (DS 016-2024-JUS, vigente desde el 30-mar-2025) | El plazo de adecuación para designar al Oficial de Datos Personales habría vencido el 30-jun-2026 según una fuente secundaria (verificar). Meta interna: 30-jun-2027 |

Los 13 proyectos restantes compiten en el modelo.

### 7.2.2 Modelo multicriterio · criterios, pesos y su justificación acordada

Ocho criterios con pesos fijados **antes** de calcular (`PR02_pesos.md`). Suman 1.00 y el criterio de impacto social y ambiental pesa 0.10, el mínimo obligatorio.

| Criterio | Peso | Justificación (diagnóstico) |
|---|---|---|
| Contribución a los objetivos | 0.25 | Objetivos de TI: eliminar la dependencia de una sola persona y cumplir la trazabilidad de DIGEMID |
| Riesgo de no hacerlo | 0.20 | Tres riesgos conocidos sin tratar y un incidente con posible sanción |
| Urgencia | 0.10 | Consolidación con fallas dos veces por semana; detalle del POS solo 90 días |
| Habilitación | 0.10 | Cadena de dependencias entre proyectos |
| Beneficio económico | 0.10 | TI es 1.11 % de la facturación; compras de más por stock desactualizado |
| Impacto social y ambiental | 0.10 | Datos de salud de clientes, disponibilidad de medicamentos en 3 regiones, menos papel |
| Facilidad de ejecución | 0.10 | 3 personas en TI; una es el único conocedor del POS |
| Aceptación organizacional | 0.05 | Comité sin reunirse en un año; cambios formalizados después de aplicarse |

El estado del acuerdo con la gerencia es **propuesta del equipo, pendiente de confirmar en la Entrevista 3**.

### 7.2.3 Resultados de la priorización

| # | Proyecto | Puntaje (0-100) | Impacto | Esfuerzo | Cuadrante | Decisión |
|---|---|---|---|---|---|---|
| 1 | P03 Rediseño de la consolidación nocturna | 87 | 4.53 | 2.5 | ① | Ejecutar |
| 2 | P04 Continuidad del conocimiento del POS | 82 | 4.18 | 2.0 | ① | Ejecutar |
| 3 | P12 Reemplazo del POS por solución en la nube | 71 | 3.94 | 5.0 | ② | **No ejecutar** (excede la capacidad) |
| 4 | P05 Respaldos completos y prueba de restauración | 69 | 3.24 | 1.0 | ① | Ejecutar |
| 5 | P08 Gobierno de inversiones de TI | 65 | 3.24 | 1.5 | ① | Ejecutar |
| 6 | P07 Seguridad básica: MFA, política y capacitación | 62 | 3.00 | 1.5 | ① | Ejecutar |
| 7 | P09 Compras y distribución en el módulo del POS | 61 | 3.18 | 3.5 | ② | Ejecutar |
| 8 | P06 BIA completo y plan de continuidad | 60 | 3.00 | 2.0 | ① | Ejecutar |
| 9 | P11 Inventario de activos y control de contratos | 52 | 2.24 | 1.0 | ③ | Ejecutar |
| 10 | P10 Mesa de servicios ligera | 51 | 2.35 | 1.5 | ③ | Ejecutar |
| 11 | P15 Analítica BI de ventas e inventario | 39 | 1.76 | 3.0 | ④ | **No ejecutar** |
| 12 | P14 App móvil y comercio electrónico | 37 | 1.76 | 4.0 | ④ | **No ejecutar** |
| 13 | P13 Videovigilancia fase 2 | 30 | 1.35 | 4.0 | ④ | **No ejecutar** |

P06 y P07 quedan exactamente en el umbral de impacto (3.00) y P15 en el umbral de esfuerzo (3.00); un cambio de un punto en un solo puntaje los movería de cuadrante.

### 7.2.4 Matriz esfuerzo-impacto

Ver `graficos/PR_esfuerzo_impacto.png`. Los cuatro cuadrantes están poblados: ① P03, P04, P05, P06, P07, P08; ② P09 y P12; ③ P10 y P11; ④ P13, P14 y P15.

### 7.2.5 Proyectos que NO se ejecutarán y el riesgo que la organización asume

Detalle en `PR07_no_se_hara.csv`. Se descartan P13, P14 y P15 (cuadrante ④) y se descarta P12 aunque ocupa el tercer puesto, porque su costo a 3 años (S/ 328 800) supera toda la capacidad libre del periodo (S/ 324 272). Quien acepta el riesgo es la Gerencia General; la revisión se programa en los hitos H2 y H3.

## 7.3 Hoja de ruta

### 7.3.1 Restricciones · dependencias, plazos, capacidad y absorción del cambio

- **Dependencias:** P04 → P03; P05 → P06; P10 → P11; P03 y P08 → P09.
- **Plazos:** P01 y P02 con meta al 30-jun-2027.
- **Capacidad:** máximo 3 proyectos simultáneos por trimestre y 2 que necesiten al Jefe de Sistemas, porque TI son 3 personas.
- **Absorción del cambio:** los trimestres 2027-T4 y 2028-T4 quedan sin proyectos nuevos para consolidar y decidir.

### 7.3.2 Olas de implantación y su fundamento

| Ola | Año | Proyectos | Fundamento |
|---|---|---|---|
| 1 · Cumplir y estabilizar | 2027 | P01, P02, P05, P04, P08 | Cierra la exposición regulatoria, cubre los respaldos y documenta el conocimiento crítico |
| 2 · Ordenar y proteger | 2028 | P10, P07, P03, P11, P06 | P03 espera a P04; se instalan controles básicos y continuidad |
| 3 · Automatizar compras y distribución | 2029 | P09 | Necesita datos de stock fiables (P03) y gobierno de inversiones (P08) |

P03 es el primero del ranking pero no está en la Ola 1: depende de P04.

### 7.3.3 Cronograma plurianual con hitos de decisión

Ver `PR05_hoja_ruta.csv`, `PR05_hoja_ruta.gan` y `graficos/PR_gantt.png`. Hitos de decisión: H1 (31-dic-2027), H2 (31-dic-2028) y H3 (31-dic-2029); hitos normativos en rojo el 30-jun-2027.

### 7.3.4 Verificación · dependencias respetadas y capacidad no excedida

`PR04_hoja_ruta.py`: **0 dependencias rotas** y **0 trimestres** que excedan la capacidad (salida en `evidencias/S14/salidas/PR04_salida.txt`).

## 7.4 Presupuesto

### 7.4.1 Estructura · CAPEX, OPEX, gestión del cambio y contingencia

CAPEX por proyecto, gestión del cambio entre 5 % y 15 % del CAPEX, contingencia de 20 % y OPEX anual desde el mes siguiente al cierre de cada proyecto. La contingencia se calibra con las tres inversiones cerradas, que se desviaron +44.8 % en conjunto.

### 7.4.2 Presupuesto por año

| Año | CAPEX | Gestión del cambio | Contingencia | OPEX | Total | Capacidad | Uso | Rango (bajo - alto) |
|---|---|---|---|---|---|---|---|---|
| 2027 | 72 000 | 6 520 | 15 704 | 11 100 | 105 324 | 108 091 | 97.4 % | 88 510 - 126 477 |
| 2028 | 56 000 | 6 280 | 12 456 | 32 400 | 107 136 | 108 091 | 99.1 % | 91 440 - 127 453 |
| 2029 | 45 000 | 6 750 | 10 350 | 40 500 | 102 600 | 108 091 | 94.9 % | 88 200 - 121 519 |

La capacidad es el techo de TI (S/ 468 000) menos la base operativa ejecutada en 2025 (S/ 359 909). **En el escenario alto el plan excede la capacidad en S/ 13 400 a S/ 19 400 por año.**

### 7.4.3 Curva de gasto operativo acumulado y su interpretación

Ver `graficos/PR_presupuesto.png`. El OPEX acumulado llega a S/ 84 000 a diciembre de 2029 (rango 75 600 - 96 600) y el gasto recurrente anual queda en S/ 48 600, el 10.4 % del techo de TI. La curva nunca baja: cada proyecto entregado deja un gasto que la gerencia compromete para siempre.

### 7.4.4 Supuestos y rangos de incertidumbre

- Costos estimados sin cotización. Escenario bajo: sin contingencia y OPEX -10 %. Escenario alto: contingencia de 44.8 % y OPEX +15 %.
- Techo de TI constante en S/ 468 000. Si la base operativa volviera a su nivel planificado (S/ 430 560), la capacidad sería de solo S/ 37 440 y el plan no cabría en ningún año.
- Los tres expedientes cerrados suman S/ 708 158 ejecutados, más que todo el gasto de TI de 2025 (S/ 402 215). Se debe aclarar con la gerencia de qué partida salieron.
