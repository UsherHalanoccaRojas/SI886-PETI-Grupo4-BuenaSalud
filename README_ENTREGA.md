# SI-886 · Semana 14 · Taller (Cadena de Farmacias Buena Salud)

Estructura para copiar a la raíz del repositorio del equipo:

```
07_portafolio/   PF01, PF02 (entradas) · PR01–PR07 · programas .py · PETI_7.2-7.4.md · graficos/ · caso/
evidencias/S14/salidas/   salida de cada programa (.txt)
anexos/          anexos A–F del informe
docs/            informe (.docx y .pdf), plantilla y build_informe.py
```

## Antes de subir (el equipo debe completar)
1. Reemplazar en el informe: número de grupo, integrantes con código y `<organizacion>/<repositorio>`:
   `python3 docs/build_informe.py --grupo 4 --repo MI-ORG/MI-REPO --autores "Apellidos, Nombres · código;Otro, Nombre · código"`
   `python3 docs/export_pdf.py docs/SI886-S14-TALLER-Grupo4.docx`
2. Confirmar pesos, techo de gasto y base operativa en la Entrevista 3 simulada; si cambian, editar `PR02_pesos.md` y los programas, y volver a correrlos.
3. Abrir `07_portafolio/PR05_hoja_ruta.gan` en GanttProject, tomar la captura y guardarla en `evidencias/S14/`.
4. Comparar PF01/PF02 y los programas con los de `RECURSOS-TALLER/` del curso (aquí se construyeron desde los documentos del caso).

## Regenerar resultados
```bash
pip install -r requirements.txt
cd 07_portafolio
python3 PR01_no_negociables.py && python3 PR03_priorizacion.py && python3 PR04_hoja_ruta.py
python3 PR05_generar_gan.py && python3 PR06_presupuesto.py
```

## Git (en este orden, para que el historial pruebe que los pesos se fijaron antes de calcular)
```bash
git switch -c taller/s14
git add 07_portafolio/PF0*.csv 07_portafolio/PR02_pesos.md && git commit -m "S14: pesos fijados antes de calcular"
git add . && git commit -m "S14: priorizacion, hoja de ruta y presupuesto - secciones 7.2 a 7.4"
git push -u origin taller/s14        # Pull Request hacia develop
# tras fusionar el PR:
git tag -a v0.14 -m "PETI v0.14 - plan ejecutable"
git tag -a taller-14 -m "Taller 14 · SI886"
git push origin v0.14 taller-14
```
