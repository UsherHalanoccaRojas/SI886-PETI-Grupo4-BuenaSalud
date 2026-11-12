"""Construye el informe del taller (docx + pdf) sobre la plantilla SI886-PLANTILLA-TALLER.docx.
Uso:  python3 build_informe.py --grupo 4 --repo mi-org/mi-repo --autores "Apellidos, Nombres · 2021xxxxx;Otro, Nombre · 2021yyyyy"
Requiere: python-docx, pandas, LibreOffice (soffice)."""
import argparse, copy, re, subprocess, sys, os, shutil
import pandas as pd, docx, networkx, matplotlib
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ap = argparse.ArgumentParser()
ap.add_argument("--grupo", default="N"); ap.add_argument("--repo", default="<organizacion>/<repositorio>")
ap.add_argument("--autores", default="[APELLIDOS, NOMBRES · CÓDIGO];[APELLIDOS, NOMBRES · CÓDIGO];[APELLIDOS, NOMBRES · CÓDIGO]")
ap.add_argument("--plantilla", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),"SI886-PLANTILLA-TALLER.docx"))
a = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PF = os.path.join(ROOT,"07_portafolio")
BASE = f"https://github.com/{a.repo}/blob/taller-14/"; TREE = f"https://github.com/{a.repo}/tree/taller-14"
U = lambda p: BASE+p
OUT = f"SI886-S14-TALLER-Grupo{a.grupo}"
rd = lambda f: pd.read_csv(os.path.join(PF,f))

d = docx.Document(a.plantilla); body = d.element.body
find = lambda txt, style=None: next(p for p in d.paragraphs if p.text.strip().startswith(txt) and (style is None or p.style.name==style))
cur = None
def place(el):
    global cur; cur.addnext(el); cur = el
def runs(p, text, size=None, color=None, mono=False):
    for i,part in enumerate(re.split(r"\*\*", text)):
        if not part: continue
        r = p.add_run(part); r.bold = (i%2==1) or None
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor(*color)
        if mono: r.font.name = "Courier New"; r._element.rPr.rFonts.set(qn("w:eastAsia"),"Courier New")
def P(text, style="Body Text", size=None, align=None, hl=False, mono=False, indent=None, keep=False):
    p = d.add_paragraph(style=style); runs(p, text, size, mono=mono)
    if align=="c": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if indent: p.paragraph_format.left_indent = Cm(indent); p.paragraph_format.first_line_indent = Cm(-0.4)
    if keep: p.paragraph_format.keep_with_next = True
    if hl:
        for r in p.runs: r.font.highlight_color = 7
    place(p._p); return p
def B(text, **k): return P("– "+text, style="Compact", indent=0.8, **k)
def CODE(text):
    for ln in text.strip("\n").split("\n"):
        p = P(ln, style="Compact", size=8, mono=True)
        pPr = p._p.get_or_add_pPr(); sh = OxmlElement("w:shd"); sh.set(qn("w:val"),"clear"); sh.set(qn("w:fill"),"EEEEEE"); pPr.append(sh)
HEAD2 = copy.deepcopy(find("Paso A","Heading 2")._p)
def H2(text):
    h = copy.deepcopy(HEAD2); 
    for t in h.iter(qn("w:t")): t.text = ""
    list(h.iter(qn("w:t")))[0].text = text; place(h)
def T(rows, widths, size=7.5, header=True, bold_first_col=False):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = d.styles["Table"]; t.autofit = False
    tblPr = t._tbl.tblPr; lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"),"fixed"); tblPr.append(lay)
    for i,row in enumerate(rows):
        for j,v in enumerate(row):
            c = t.cell(i,j); c.width = Cm(widths[j]); c.text = ""
            p = c.paragraphs[0]; p.style = d.styles["Compact"]; runs(p, str(v), size)
            if header and i==0:
                for r in p.runs: r.bold = True
        if header and i==0:
            trPr = t.rows[0]._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:tblHeader"))
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"),str(int(sum(widths)*567))); tw.set(qn("w:type"),"dxa")
    for e in tblPr.findall(qn("w:tblW")): tblPr.remove(e)
    tblPr.append(tw)
    for gc,wd in zip(t._tbl.tblGrid.findall(qn("w:gridCol")),widths): gc.set(qn("w:w"),str(int(wd*567)))
    place(t._tbl); P("", style="Compact", size=4); return t
def FIG(path, caption, w=15.5):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(path, width=Cm(w)); p.paragraph_format.keep_with_next = True; place(p._p)
    P(caption, style="Image Caption", align="c")

# ---------- carátula ----------
for _p in [d.paragraphs[i] for i in (22,23,24)]: _p._p.getparent().remove(_p._p)
_t = find("“…………………………………………….”")
for r in _t.runs[1:]: r.text = ""
_t.runs[0].text = "“Priorización, hoja de ruta y presupuesto · Semana 14”"
_c = find("“………………………….”")
for r in _c.runs[1:]: r.text = ""
_c.runs[0].text = "“SI-886 Planeamiento Estratégico de TI”"
t17 = find("APELLIDOS Y NOMBRES"); autores = a.autores.split(";")
for r in t17.runs[1:]: r.text = ""
t17.runs[0].text = f"Grupo {a.grupo}"
prev = t17._p
for au in autores:
    np_ = copy.deepcopy(t17._p)
    for r in list(np_.iter(qn("w:t"))): r.text = ""
    list(np_.iter(qn("w:t")))[0].text = au.strip(); prev.addnext(np_); prev = np_
    if au.startswith("["):
        for r in np_.iter(qn("w:rPr")):
            hl = OxmlElement("w:highlight"); hl.set(qn("w:val"),"yellow"); r.append(hl)

# ---------- quitar "Cómo se usa esta plantilla" ----------
start = find("Cómo se usa esta plantilla","Heading 1"); sec1 = find("1. Información sobre el evento práctico","Heading 1")
el = start._p; kill = []
while el is not sec1._p: kill.append(el); el = el.getnext()
# conservar un salto de página antes de la sección 1 si el elemento previo lo traía
for e in kill: e.getparent().remove(e)
for p in d.paragraphs:
    if p.style.name=="toc 1" and p.text.startswith("Cómo se usa"): p._p.getparent().remove(p._p)


# ---------- 1. Información ----------
cur = find("1.1 Título del evento práctico","Heading 2")._p
P("Semana 14 · Priorización multicriterio, hoja de ruta y presupuesto plurianual del PETI de **CADENA DE FARMACIAS BUENA SALUD E.I.R.L.** (Empresa 10 del banco de casos, retail farmacéutico, 23 locales). El taller redacta las secciones 7.2, 7.3 y 7.4 del PETI.")
cur = find("1.2 Objetivos","Heading 2")._p
P("Son los de la guía `3-TALLER.md` de la Semana 14, sección 1.1. La guía indica no copiarlos en el informe.".replace("`",""))
cur = find("1.3 Tiempo de duración","Heading 2")._p
P("Sesión 2 en laboratorio, según la guía de la Semana 14. La guía indica no copiar la duración en el informe.")
cur = find("1.4 Resultados de aprendizaje","Heading 2")._p
P("Son los del sílabo y de la guía de la Semana 14. La guía indica no copiarlos en el informe.")
vers = {"Python":sys.version.split()[0],"pandas":pd.__version__,"networkx":networkx.__version__,"matplotlib":matplotlib.__version__,"python-docx":docx.__version__ if hasattr(docx,"__version__") else ""}
tab = d.tables[0]; tab._tbl.getparent().remove(tab._tbl)
cur = find("1.5 Recursos","Heading 2")._p
T([["Recurso","Versión","Para qué se usó"],
   ["Python",vers["Python"],"Ejecutar los programas PR01, PR03, PR04, PR05 (generador del .gan) y PR06"],
   ["pandas",vers["pandas"],"Separar los no negociables, calcular el modelo multicriterio, el presupuesto y la curva de OPEX"],
   ["networkx",vers["networkx"],"Niveles de dependencia y verificación de que no hay dependencias rotas"],
   ["matplotlib",vers["matplotlib"],"Matriz esfuerzo-impacto, vista de la hoja de ruta y curva de OPEX acumulado"],
   ["GanttProject","formato 3.2","Archivo .gan de la hoja de ruta con dependencias fin-inicio e hitos (captura pendiente, ver sección 3)"],
   ["Git y GitHub","—","Versionado, Pull Request, etiquetas `taller-14` y `v0.14`".replace("`","")],
   ["Documentos del caso","Entrega del 12-jun-2026","Ficha de la organización, presupuesto de TI e inversiones cerradas con sus expedientes"]],
  [3.2,2.8,10.5])
sec16 = find("Reglas de uso del laboratorio")
sec16.text = ""; cur = find("1.6 Seguridad","Heading 2")._p
cur.getnext().getparent().remove(cur.getnext())
P("Reglas que se respetaron durante el trabajo:", keep=True)
B("El presupuesto de TI se trató como información **Confidencial**: el repositorio del equipo debe ser privado.")
B("El criterio «Impacto social y ambiental» está en el modelo con peso 0.10, el mínimo exigido, y se fijó antes de calcular.")
B("Los pesos se escribieron en `PR02_pesos.md` antes de ejecutar `PR03_priorizacion.py`; no se ajustaron mirando el resultado.".replace("`",""))
B("Los proyectos descartados y los riesgos asumidos se declaran en `PR07_no_se_hara.csv` para comunicarlos a la gerencia.".replace("`",""))
B("Todas las cifras se presentan con su rango de incertidumbre (escenarios bajo, medio y alto).")

# ---------- 2. Procedimiento ----------
cur = find("Cada paso lleva su título")._p
pa, pb_, pc = find("Paso A","Heading 2"), find("Paso B","Heading 2"), find("Paso C","Heading 2")
pa.runs[0].text = "Paso A — Separar los no negociables y fijar los pesos"
for r in pa.runs[1:]: r.text = ""
cur = pa._p
P("**Qué se buscaba.** Sacar del modelo los proyectos que no se priorizan porque la norma o la exposición vigente los obliga, y fijar los pesos con su justificación antes de calcular.")
P("**Acción.** Se armó `PF01_portafolio_candidatos.csv` con 15 candidatos derivados de los riesgos conocidos, el incidente del periodo, los hechos verificados y los expedientes de inversión; luego se ejecutó:".replace("`",""))
CODE("cd 07_portafolio && python3 PR01_no_negociables.py")
P("Resultado: 15 candidatos, **2 no negociables** (P01 trazabilidad de productos controlados ante DIGEMID y P02 adecuación a la Ley 29733 con DS 016-2024-JUS) y 13 que compiten. Los plazos son metas internas al 30-jun-2027 porque el caso no trae una fecha normativa expresa.")
P("Pesos fijados en `PR02_pesos.md`, cada uno con su justificación en el diagnóstico (suman 1.00):".replace("`",""), keep=True)
w = [["Criterio","Peso","Justificación derivada del diagnóstico"],
 ["Contribución a los objetivos","0.25","Objetivos de TI: eliminar la dependencia de una sola persona y cumplir la trazabilidad de DIGEMID"],
 ["Riesgo de no hacerlo","0.20","Tres riesgos conocidos sin tratar y un incidente de 214 unidades con posible sanción"],
 ["Urgencia","0.10","Consolidación con fallas dos veces por semana; el POS solo conserva 90 días"],
 ["Habilitación","0.10","Cadena de dependencias: conocimiento → consolidación → compras"],
 ["Beneficio económico","0.10","TI es 1.11 % de la facturación; compras de más por stock desactualizado"],
 ["Impacto social y ambiental","0.10","Datos de salud de clientes, medicamentos disponibles en 3 regiones, menos papel"],
 ["Facilidad de ejecución","0.10","3 personas en TI y un único conocedor del POS"],
 ["Aceptación organizacional","0.05","Comité sin reunirse en un año; cambios formalizados después de aplicarse"]]
T(w,[4.3,1.3,10.9])
P("**Evidencia.** "+U("07_portafolio/PR01_portafolio_marcado.csv")+" · "+U("07_portafolio/PR02_pesos.md")+" · "+U("evidencias/S14/salidas/PR01_salida.txt"), size=8, style="Compact")
P("**Reserva.** Los pesos son una propuesta del equipo y deben confirmarse en la Entrevista 3 simulada con el docente; si cambian, se corrige `PR02_pesos.md` y se recalcula.".replace("`",""))

pb_.runs[0].text = "Paso B — Calcular la priorización"
for r in pb_.runs[1:]: r.text = ""
cur = pb_._p
P("**Qué se buscaba.** Un puntaje por proyecto y la matriz esfuerzo-impacto. Puntaje = suma de pesos por puntajes de 1 a 5, llevada a base 100. Impacto = promedio ponderado de los seis criterios de valor; esfuerzo = mitad de (6 − facilidad) y mitad de la banda de costo a 3 años.")
CODE("cd 07_portafolio && python3 PR03_priorizacion.py")
pr = rd("PR03_priorizado.csv"); q = {"1":"①","2":"②","3":"③","4":"④"}
rows = [["#","Proyecto","Puntaje","Impacto","Esfuerzo","Cuad.","Decisión"]]
for _,r in pr.iterrows(): rows.append([r.ranking,f"{r.id} {r.proyecto}",f"{r.puntaje:.0f}",f"{r.impacto:.2f}",f"{r.esfuerzo:.1f}",q[r.cuadrante[0]],r.decision.replace("NO EJECUTAR","**No ejecutar**")])
T(rows,[0.8,7.0,1.4,1.4,1.5,1.2,3.2])
FIG(os.path.join(PF,"graficos/PR_esfuerzo_impacto.png"),"Figura 1. Matriz esfuerzo-impacto con los cuatro cuadrantes poblados.",12.5)
P("Candidatos del cuadrante ④ (no ejecutar): **P13, P14 y P15**. P12 queda en el cuadrante ② y en el tercer puesto, pero se descarta porque su costo a 3 años supera la capacidad libre trianual. P06 y P07 están justo en el umbral de impacto (3.00) y P15 en el de esfuerzo (3.00).")
P("**Evidencia.** "+U("07_portafolio/PR03_priorizado.csv")+" · "+U("07_portafolio/graficos/PR_esfuerzo_impacto.png")+" · "+U("evidencias/S14/salidas/PR03_salida.txt"), size=8, style="Compact")

pc.runs[0].text = "Paso C — Construir la hoja de ruta"
for r in pc.runs[1:]: r.text = ""
cur = pc._p
P("**Qué se buscaba.** Ordenar las olas sin romper precedencias y sin superar la capacidad simultánea (3 proyectos por trimestre y 2 que necesiten al Jefe de Sistemas).")
CODE("cd 07_portafolio && python3 PR04_hoja_ruta.py\npython3 PR05_generar_gan.py   # genera PR05_hoja_ruta.gan")
P("`PR04_hoja_ruta.py` calculó tres niveles: nivel 0 (P01, P02, P04, P05, P07, P08, P10), nivel 1 (P03, P06, P11) y nivel 2 (P09). La hoja de ruta se registró a mano en `PR05_hoja_ruta.csv` con tres olas y se verificó: **0 dependencias rotas** y **0 trimestres que excedan la capacidad**.".replace("`",""))
hr = rd("PR05_hoja_ruta.csv"); rows=[["Proy.","Ola","Inicio","Fin","Meses","Depende de","Hito de decisión"]]
for _,r in hr.iterrows(): rows.append([r.Proyecto,r.Ola,r.Inicio,r.Fin,r["Duración (meses)"],"" if pd.isna(r["Depende de"]) else r["Depende de"],r["Hito de decisión"]])
T(rows,[1.1,0.9,1.7,1.7,1.5,2.0,7.6])
P("**Fundamento de las olas.** Ola 1 (2027, cumplir y estabilizar): P01, P02, P05, P04, P08. Ola 2 (2028, ordenar y proteger): P10, P07, P03, P11, P06. Ola 3 (2029, automatizar): P09. P03, primero del ranking, no está en la Ola 1 porque depende de P04. Los trimestres 2027-T4 y 2028-T4 quedan sin proyectos nuevos para absorber el cambio y decidir en los hitos H1 y H2.")
FIG(os.path.join(PF,"graficos/PR_gantt.png"),"Figura 2. Hoja de ruta 2027-2029 (vista equivalente generada con matplotlib; la captura de GanttProject va en el anexo C).",15)
P("**Evidencia.** "+U("07_portafolio/PR05_hoja_ruta.csv")+" · "+U("07_portafolio/PR05_hoja_ruta.gan")+" · "+U("evidencias/S14/salidas/PR04_salida.txt"), size=8, style="Compact")

# Pasos D-G
last = cur
def newstep(txt):
    global cur
    cur = last if False else cur
    H2(txt)
cur = cur  # continúa tras Paso C
H2("Paso D — Presupuesto plurianual y curva de OPEX")
P("**Qué se buscaba.** CAPEX, gestión del cambio, contingencia y OPEX por año, cuadrados con la capacidad real de gasto. Capacidad = techo de TI S/ 468 000 menos la base operativa ejecutada en 2025 (S/ 359 909) = **S/ 108 091 por año**. Contingencia de 20 % sobre el CAPEX con gestión del cambio; las tres inversiones cerradas se desviaron +44.8 % en conjunto.")
CODE("cd 07_portafolio && python3 PR06_presupuesto.py")
bp = rd("PR06_presupuesto.csv"); f = lambda v: f"{v:,.0f}".replace(","," ")
rows=[["Año","CAPEX","Cambio","Contingencia","OPEX","Total","Capacidad","Uso","Rango bajo - alto"]]
for _,r in bp.iterrows(): rows.append([int(r.anio),f(r.capex),f(r.cambio),f(r.conting),f(r.opex),f(r.total),f(r.capacidad),f"{r['uso_%']:.1f} %",f"{f(r.total_bajo)} - {f(r.total_alto)}"])
T(rows,[1.1,1.6,1.5,1.9,1.5,1.7,1.9,1.3,3.9])
FIG(os.path.join(PF,"graficos/PR_presupuesto.png"),"Figura 3. Gasto anual frente a la capacidad real (izquierda) y curva de OPEX acumulado (derecha).",16)
P("**Interpretación.** El OPEX acumulado llega a S/ 84 000 en diciembre de 2029 (rango 75 600 a 96 600) y deja un gasto recurrente de S/ 48 600 al año, el 10.4 % del techo de TI. La curva nunca baja. El plan usa entre 95 % y 99 % de la capacidad, de modo que **cuadra en el escenario medio y falla en el alto** (excede entre S/ 13 400 y S/ 19 400 por año).")
P("**Evidencia.** "+U("07_portafolio/PR06_presupuesto.csv")+" · "+U("07_portafolio/graficos/PR_presupuesto.png")+" · "+U("evidencias/S14/salidas/PR06_salida.txt"), size=8, style="Compact")

H2("Paso E — Declarar lo que no se hará y redactar")
P("Se declararon cuatro proyectos que no se ejecutan, cada uno con el objetivo que queda sin cumplir, el riesgo asumido, quién lo acepta y cuándo se revisa (`PR07_no_se_hara.csv`):".replace("`",""), keep=True)
ns = rd("PR07_no_se_hara.csv"); rows=[["Proyecto","Punt.","Objetivo sin cumplir","Riesgo asumido","Acepta","Revisión"]]
for _,r in ns.iterrows(): rows.append([r.Proyecto,r.Puntaje,r["Objetivo que queda sin cumplir"],r["Riesgo que la organización asume"],r["Responsable de aceptar el riesgo"],r["Fecha de revisión"]])
T(rows,[2.6,0.9,3.6,5.2,2.2,2.0],size=7)
P("Las secciones 7.2, 7.3 y 7.4 del PETI están redactadas en "+U("07_portafolio/PETI_7.2-7.4.md")+" con los títulos que pide la guía.")

H2("Paso F — Validar y corregir")
T([["Comprobación","Resultado","Acción"],
 ["1. Pesos suman 1 y cada uno tiene su justificación","Suman 1.00; el social pesa 0.10; los ocho tienen justificación en `PR02_pesos.md`".replace("`",""),"Ninguna"],
 ["2. Ningún proyecto antes de aquel del que depende","0 dependencias rotas (5 enlaces fin-inicio revisados)","Ninguna"],
 ["3. El presupuesto cuadra con la capacidad real","Escenario medio cuadra (95 % a 99 %); escenario alto excede entre S/ 13 400 y S/ 19 400 por año","El borrador inicial ponía P10 en 2027-T3 y superaba la capacidad (estimado S/ 110 800 contra S/ 108 091); se movió a 2028-T1 y P11 lo siguió. El exceso del escenario alto no se corrige: se documenta en Problemas y mejoras"]],
 [5.0,5.5,6.0])
H2("Paso G — Registrar la evidencia y cerrar")
P("Comandos para versionar y etiquetar (se ejecutan desde la raíz del repositorio del equipo):", keep=True)
CODE('git switch -c taller/s14\ngit add 07_portafolio/PF0* 07_portafolio/PR02_pesos.md && git commit -m "S14: pesos acordados antes de calcular"\ngit add . && git commit -m "S14: priorizacion, hoja de ruta y presupuesto - secciones 7.2 a 7.4"\ngit push -u origin taller/s14   # abrir Pull Request hacia develop\ngit tag -a v0.14 -m "PETI v0.14 - plan ejecutable"\ngit tag -a taller-14 -m "Taller 14 · SI886"\ngit push origin v0.14 taller-14')
P("URL de entrega: "+TREE+" (etiqueta `taller-14`). URL del Pull Request: [pegar aquí].".replace("`",""), hl=True)
P("**Pregunta de transferencia.** Se responde en la sección 5.")

# ---------- 3. Resultados ----------
old = d.tables[0] if d.tables else None
for t_ in list(d.tables): 
    if t_.rows[0].cells[0].text.strip()=="#": t_._tbl.getparent().remove(t_._tbl)
cur = find("3. Resultados","Heading 1")._p
S = "07_portafolio/"
res = [
 ["1","Proyectos no negociables separados del modelo, con norma y plazo","Sí",U(S+"PR01_portafolio_marcado.csv")],
 ["2","Pesos con justificación acordada con la gerencia, sumando 1","Parcial",U(S+"PR02_pesos.md")],
 ["3","Priorización calculada para todos los proyectos que compiten","Sí",U(S+"PR03_priorizado.csv")],
 ["4","Matriz esfuerzo-impacto con los cuatro cuadrantes poblados","Sí",U(S+"graficos/PR_esfuerzo_impacto.png")],
 ["5","Proyectos del cuadrante ④ identificados","Sí",U("evidencias/S14/salidas/PR03_salida.txt")],
 ["6","Niveles de dependencia; cero dependencias rotas","Sí",U("evidencias/S14/salidas/PR04_salida.txt")],
 ["7","Hoja de ruta en tres olas con su fundamento","Sí",U(S+"PR05_hoja_ruta.csv")],
 ["8","Capacidad simultánea respetada en todos los trimestres","Sí",U("evidencias/S14/salidas/PR04_salida.txt")],
 ["9","Cronograma en GanttProject con dependencias, hitos y plazos normativos","Parcial",U(S+"PR05_hoja_ruta.gan")],
 ["10","Presupuesto plurianual con CAPEX, OPEX, gestión del cambio y contingencia","Sí",U(S+"PR06_presupuesto.csv")],
 ["11","Curva de OPEX acumulado graficada e interpretada","Sí",U(S+"graficos/PR_presupuesto.png")],
 ["12","Tabla de lo que no se hará con riesgo y responsable","Sí",U(S+"PR07_no_se_hara.csv")],
 ["13","Secciones 7.2 a 7.4 redactadas y etiqueta v0.14","Parcial",U(S+"PETI_7.2-7.4.md")+" · etiqueta v0.14 pendiente de crear"]]
T([["#","Resultado esperado","¿Se logró?","Evidencia (URL)"]]+res,[0.7,5.3,1.6,8.9],size=7)
# reemplazar el párrafo de la plantilla
exp = find("Si algo no se logró")
exp._p.getparent().remove(exp._p)
P("**Lo que no se logró del todo y por qué (Problemas y mejoras).**", keep=True)
B("**Resultado 2.** Los pesos están fijados antes de calcular y suman 1, pero la Entrevista 3 con la gerencia es simulada con el docente y su confirmación está pendiente. Lo mismo vale para el techo de gasto y la base operativa usados como capacidad.")
B("**Resultado 9.** El archivo `.gan` se generó por script y su XML es válido, pero falta abrirlo en GanttProject y tomar la captura real; la figura 2 es una vista equivalente. Los hitos normativos se dibujaron sin enlace de dependencia para que la herramienta no los desplace.".replace("`",""))
B("**Resultado 13.** Las secciones están redactadas; las etiquetas `v0.14` y `taller-14` y el Pull Request los crea el equipo con los comandos del Paso G.".replace("`",""))
B("**Costos.** Son estimaciones del equipo sin cotización; por eso se reportan con rango. En el escenario alto el plan excede la capacidad de cada año; mitigación propuesta: reserva de gestión fuera del techo y congelar P09 en el hito H2 si la Ola 1 y la Ola 2 se desvían.")
B("**Capacidad.** El plan cabe porque la base operativa de 2025 se ejecutó por debajo de lo planificado (−29 % en licencias y −37.6 % en infraestructura). Si esa base volviera al nivel planificado, solo quedarían S/ 37 440 por año y el plan no cabría.")
B("**Datos por aclarar.** Los tres expedientes cerrados suman S/ 708 158 ejecutados, más que todo el gasto de TI de 2025 (S/ 402 215); hay que confirmar de qué partida salieron. La norma de P01 debe confirmarse con asesor legal y el plazo de P02 proviene de una fuente secundaria.")
B("**Umbrales.** P06 y P07 (impacto 3.00) y P15 (esfuerzo 3.00) están exactamente en el umbral de su cuadrante.")

# ---------- 4. Conclusiones ----------
exp = find("Mínimo tres."); exp._p.getparent().remove(exp._p); cur = find("4. Conclusiones","Heading 1")._p
for i,tx in enumerate([
 "Priorizar es decidir qué no se hará. La capacidad real es S/ 108 091 al año, apenas el 23 % del techo de TI, y por eso cuatro de los 13 proyectos que competían quedan fuera. P12 ocupó el tercer puesto con 71 puntos y aun así no se ejecuta, porque su costo a tres años (S/ 328 800) supera toda la capacidad del periodo; el puntaje ordena, pero la capacidad decide (resultados 3, 4 y 12).",
 "La secuencia la fijan las dependencias y no el puntaje. P03 tiene el puntaje más alto (87), pero no puede empezar hasta que P04 documente el conocimiento del POS, de modo que arranca en enero de 2028; y P09 solo entra en 2029 porque necesita datos de stock fiables y gobierno de inversiones (resultados 6, 7 y 8).",
 "El gasto operativo no baja y deja el plan sin margen. El OPEX acumulado llega a S/ 84 000 en 2029 y queda un gasto recurrente de S/ 48 600 al año, el 10.4 % del techo; con un uso de la capacidad de 95 % a 99 %, una desviación como la histórica de +44.8 % rompe el plan. Por eso P08 va en la Ola 1 y los hitos de decisión H1 y H2 pueden frenar P09 (resultados 10 y 11)."],1):
    P(f"{i}. "+tx, style="Body Text")

# ---------- 5. Cuestionario ----------
exp = find("Copia cada pregunta"); exp._p.getparent().remove(exp._p); cur = find("5. Cuestionario","Heading 1")._p
P("**¿Qué riesgo correría una organización real si esto se hiciera mal?**", keep=True)
P("Aprobaría un plan que parece financiado pero no lo está: con pesos ajustados después de ver el resultado, un proyecto habilitador programado después del que lo necesita o un presupuesto sin la curva de OPEX, la gerencia descubriría en el segundo o tercer año que no puede pagar lo que ya empezó. En esta organización, además, un orden mal hecho dejaría sin atender la exposición ante DIGEMID y la Ley 29733 mientras se gasta en proyectos de bajo impacto.")

# ---------- 6. Referencias ----------
exp = find("Normas técnicas, marcos"); exp._p.getparent().remove(exp._p); cur = find("6. Referencias bibliográficas","Heading 1")._p
refs = ["Project Management Institute. *The Standard for Portfolio Management*. https://www.pmi.org/",
 "ISO 21500:2021. *Project, programme and portfolio management*. https://www.iso.org/standard/75704.html",
 "ISACA. (2018). *COBIT 2019*, APO05 Managed Portfolio y APO06 Managed Budget and Costs. https://www.isaca.org/resources/cobit",
 "ISACA. *Val IT Framework*. https://www.isaca.org/resources/frameworks-standards-and-models",
 "Resolución de Secretaría de Gobierno Digital 005-2018-PCM/SEGDI, Anexo I. https://cdn.www.gob.pe/uploads/document/file/356863/Anexo_I_Lineamientos_PGD.pdf",
 "Rodríguez Bermúdez, J. R. (2015). *Planificación y dirección estratégica de sistemas de información*. Editorial UOC. https://elibro.net/es/lc/bibliotecaupt/titulos/57875",
 "González Millán, J. (2020). *Manual práctico de planeación estratégica*. Ediciones Díaz de Santos. https://elibro.net/es/lc/bibliotecaupt/titulos/129291",
 "Kotter, J. P. (2012). *Leading Change*. Harvard Business Review Press.",
 "GanttProject. *User Guide*. https://www.ganttproject.biz/",
 "Ministerio de Justicia y Derechos Humanos. (2024). *Decreto Supremo N.º 016-2024-JUS, que aprueba el Reglamento de la Ley N.º 29733, Ley de Protección de Datos Personales*. Diario Oficial El Peruano, 30 de noviembre de 2024. https://www.congreso.gob.pe/Docs/DGP/DIDP/files/ds_016-2024-jus.pdf"]
for r_ in refs: P(r_.replace("*",""), style="Compact", size=9)

# ---------- 7. Anexos ----------
exp = find("Capturas completas"); exp._p.getparent().remove(exp._p); cur = find("7. Anexos","Heading 1")._p
P("Los anexos están en la carpeta anexos/ del repositorio ("+TREE+"/anexos) y se mencionan en las secciones 2 y 3:", keep=True)
for t_ in ["**Anexo A.** Priorización completa (`anexo_A_priorizacion.xlsx`).","**Anexo B.** Matriz esfuerzo-impacto (`anexo_B_esfuerzo_impacto.png`).","**Anexo C.** Hoja de ruta: `anexo_C_hoja_ruta.gan` y su exportación en `anexo_C_hoja_ruta.pdf`.","**Anexo D.** Presupuesto plurianual y supuestos de costo (`anexo_D_presupuesto.xlsx`).","**Anexo E.** Curva de OPEX acumulado (`anexo_E_curva_opex.png`).","**Anexo F.** Lo que no se hará (`anexo_F_no_se_hara.pdf`).","**Anexo G.** Secciones 7.2 a 7.4 del PETI (`07_portafolio/PETI_7.2-7.4.md`)."]:
    B(t_.replace("`",""))

# actualizar campos al abrir en Word
st = d.settings.element; uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"),"true"); st.append(uf)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT+".docx"); d.save(out); print("docx:", out)
