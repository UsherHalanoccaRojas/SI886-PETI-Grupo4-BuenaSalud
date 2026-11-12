"""PR04 - Niveles de dependencia (networkx), propuesta de olas y verificacion de PR05_hoja_ruta.csv.
Lee PR03_priorizado.csv, PR01_portafolio_marcado.csv, PF02_tco.csv y PR05_hoja_ruta.csv."""
import pandas as pd, networkx as nx, sys

MAX_SIMULTANEOS, MAX_JEFE = 3, 2   # fijados en PR02_pesos.md
hr = pd.read_csv("PR05_hoja_ruta.csv"); hr["Depende de"] = hr["Depende de"].fillna("")
pf = pd.read_csv("PR01_portafolio_marcado.csv").set_index("id")
pr = pd.read_csv("PR03_priorizado.csv").set_index("id")

G = nx.DiGraph()
for _,r in hr.iterrows():
    G.add_node(r.Proyecto)
    for d in filter(None, r["Depende de"].split(";")): G.add_edge(d, r.Proyecto)
assert nx.is_directed_acyclic_graph(G), "Hay un ciclo de dependencias"
niveles = {n:i for i,g in enumerate(nx.topological_generations(G)) for n in g}
print("NIVELES DE DEPENDENCIA (0 = sin predecesores)")
for n in sorted(niveles, key=lambda k:(niveles[k],k)):
    pred = list(G.predecessors(n)); sc = pr.loc[n,"puntaje"] if n in pr.index else "NN"
    print(f" nivel {niveles[n]}  {n}  puntaje={sc}  depende de {pred or '-'}")

ini = lambda s: pd.Period(s,"M").start_time
fin = lambda s: pd.Period(s,"M").end_time
errores = 0
print("\nVERIFICACION 1 - dependencias fin-inicio")
for _,r in hr.iterrows():
    for d in filter(None, r["Depende de"].split(";")):
        fd = hr.set_index("Proyecto").loc[d,"Fin"]
        ok = ini(r.Inicio) > fin(fd)
        errores += (not ok)
        print(f" {d} (fin {fd}) -> {r.Proyecto} (inicio {r.Inicio}): {'OK' if ok else 'ROTA'}")
print(f" Dependencias rotas: {errores}")

print("\nVERIFICACION 2 - capacidad simultanea por trimestre")
trims = pd.period_range("2027Q1","2029Q4",freq="Q"); exceso = 0
for q in trims:
    act = [r.Proyecto for _,r in hr.iterrows() if ini(r.Inicio)<=q.end_time and fin(r.Fin)>=q.start_time]
    jefe = [p for p in act if pf.loc[p,"requiere_jefe"]==1]
    ok = len(act)<=MAX_SIMULTANEOS and len(jefe)<=MAX_JEFE; exceso += (not ok)
    print(f" {q}: {len(act)} proyectos {act} | con Jefe de Sistemas: {len(jefe)} -> {'OK' if ok else 'EXCEDE'}")
print(f" Trimestres que exceden la capacidad: {exceso}")

print("\nPROPUESTA DE OLAS A PARTIR DE LOS NIVELES (referencia; la hoja de ruta final es PR05)")
for lvl in sorted(set(niveles.values())): print(f" nivel {lvl}: {sorted(n for n,v in niveles.items() if v==lvl)}")
print("\nRESULTADO:", "CORRECTO" if errores==0 and exceso==0 else "REVISAR")
sys.exit(0 if errores==0 and exceso==0 else 1)
