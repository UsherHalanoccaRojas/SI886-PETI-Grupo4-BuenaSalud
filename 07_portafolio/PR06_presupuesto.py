"""PR06 - Presupuesto plurianual (CAPEX, OPEX, gestion del cambio, contingencia) y curva de OPEX acumulado.
Lee PF02_tco.csv, PR05_hoja_ruta.csv, caso/presupuesto_ti.csv y caso/inversiones_cerradas.csv.
Produce PR06_presupuesto.csv, PR06_detalle_proyecto.csv y graficos/PR_presupuesto.png."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TECHO = 468000.0
CONT = 0.20
meses = pd.period_range("2027-01","2029-12",freq="M")
tco = pd.read_csv("PF02_tco.csv").set_index("id")
hr  = pd.read_csv("PR05_hoja_ruta.csv")
pt  = pd.read_csv("caso/presupuesto_ti.csv")
inv = pd.read_csv("caso/inversiones_cerradas.csv")

base_ej  = pt.loc[pt.tipo=="Operación","ejecutado"].sum()
base_pl  = pt.loc[pt.tipo=="Operación","planificado"].sum()
desv_hist = inv.ejecutado.sum()/inv.presupuesto.sum()-1       # promedio ponderado de las 3 inversiones cerradas
CAP_EJ, CAP_PL = TECHO-base_ej, TECHO-base_pl
print(f"Techo de TI: S/ {TECHO:,.0f} | base operativa ejecutada 2025: S/ {base_ej:,.2f} | planificada: S/ {base_pl:,.2f}")
print(f"Capacidad real para proyectos: S/ {CAP_EJ:,.2f} (base ejecutada) o S/ {CAP_PL:,.2f} (base planificada)")
print(f"Desviacion historica ponderada de inversiones cerradas: {desv_hist*100:.1f} %")

ESC = {"bajo":(0.0,0.90),"medio":(CONT,1.00),"alto":(desv_hist,1.15)}   # (contingencia, factor OPEX)
def calcular(cont, fop):
    f = {m:{"capex":0,"cambio":0,"conting":0,"opex":0} for m in meses}; det=[]
    for _,r in hr.iterrows():
        t = tco.loc[r.Proyecto]; ms = pd.period_range(r.Inicio,r.Fin,freq="M"); n=len(ms)
        for m in ms:
            f[m]["capex"]   += t.capex/n
            f[m]["cambio"]  += t.capex*t.gestion_cambio_pct/n
            f[m]["conting"] += t.capex*(1+t.gestion_cambio_pct)*cont/n
        for m in pd.period_range(pd.Period(r.Fin,"M")+1,"2029-12",freq="M"): f[m]["opex"] += t.opex_anual*fop/12
    return pd.DataFrame(f).T
res = {k:calcular(*v) for k,v in ESC.items()}

med = res["medio"]; med["anio"]=med.index.year
anual = med.groupby("anio")[["capex","cambio","conting","opex"]].sum()
anual["total"] = anual.sum(axis=1)
anual["capacidad"] = CAP_EJ
anual["uso_%"] = anual.total/CAP_EJ*100
anual["holgura"] = CAP_EJ-anual.total
anual["opex_acumulado"] = anual.opex.cumsum()
for k in ("bajo","alto"):
    r = res[k]; a = r.groupby(r.index.year).sum().sum(axis=1)
    anual[f"total_{k}"] = a
anual["techo_total_ti"] = TECHO
anual["gasto_ti_total_medio"] = base_ej + anual.total
anual.round(2).to_csv("PR06_presupuesto.csv", index_label="anio")

det=[]
for _,r in hr.iterrows():
    t = tco.loc[r.Proyecto]; ms = pd.period_range(r.Inicio,r.Fin,freq="M"); n=len(ms)
    for a in sorted({m.year for m in ms}):
        k = sum(1 for m in ms if m.year==a)/n
        det.append((r.Proyecto,a,t.capex*k,t.capex*t.gestion_cambio_pct*k,t.capex*(1+t.gestion_cambio_pct)*CONT*k))
pd.DataFrame(det,columns=["proyecto","anio","capex","gestion_cambio","contingencia"]).round(2).to_csv("PR06_detalle_proyecto.csv",index=False)

pd.set_option("display.width",200)
print("\nPRESUPUESTO PLURIANUAL - ESCENARIO MEDIO (S/)"); print(anual[["capex","cambio","conting","opex","total","capacidad","uso_%","holgura","opex_acumulado"]].round(0).to_string())
print("\nRANGO DE INCERTIDUMBRE (total anual de proyectos, S/)"); print(anual[["total_bajo","total","total_alto"]].round(0).to_string())
print("\nVERIFICACION 3 - cuadra con la capacidad real de gasto")
for a,r in anual.iterrows():
    print(f" {a}: medio {r.total:,.0f} vs capacidad {CAP_EJ:,.0f} -> {'CUADRA' if r.total<=CAP_EJ else 'EXCEDE'} | alto {r.total_alto:,.0f} -> {'cuadra' if r.total_alto<=CAP_EJ else 'EXCEDE en '+format(r.total_alto-CAP_EJ,',.0f')}")
    print(f"      gasto de TI total medio {r.gasto_ti_total_medio:,.0f} vs techo {TECHO:,.0f} ({r.gasto_ti_total_medio/TECHO*100:.1f} %)")
print(f" Con base operativa PLANIFICADA la capacidad seria S/ {CAP_PL:,.0f}: el plan excederia el techo en todos los anios.")
print(f"\nOPEX recurrente anual al cierre de 2029 (run-rate): S/ {tco.loc[hr.Proyecto,'opex_anual'].sum():,.0f}")

fig,(a1,a2)=plt.subplots(1,2,figsize=(13,5.2))
x=anual.index.astype(str); b=0
for c,l,col in [("capex","CAPEX","#1565c0"),("cambio","Gestión del cambio","#6a1b9a"),("conting","Contingencia","#f9a825"),("opex","OPEX","#2e7d32")]:
    a1.bar(x,anual[c],bottom=b,label=l,color=col); b=b+anual[c]
a1.axhline(CAP_EJ,color="#c62828",ls="--",label=f"Capacidad real S/ {CAP_EJ:,.0f}")
for i,v in enumerate(anual.total_alto): a1.plot(i,v,"v",color="k",label="Escenario alto" if i==0 else None)
a1.set_title("Gasto anual de proyectos y capacidad real"); a1.set_ylabel("Soles"); a1.set_ylim(0,165000); a1.legend(fontsize=7,ncol=3,loc="upper center")
for k,col,ls in [("bajo","#81c784","--"),("medio","#2e7d32","-"),("alto","#c62828","--")]:
    a2.plot([str(m) for m in meses],res[k].opex.cumsum().values,color=col,ls=ls,label=f"OPEX acumulado {k}")
a2.set_xticks(range(0,36,6)); a2.set_xticklabels([str(m) for m in meses][::6],rotation=45)
a2.set_title("Curva de OPEX acumulado 2027-2029 (nunca baja)"); a2.set_ylabel("Soles acumulados"); a2.legend(fontsize=8)
plt.tight_layout(); plt.savefig("graficos/PR_presupuesto.png",dpi=160)
print("\nOPEX acumulado a dic-2029 (bajo / medio / alto):", *(f"{res[k].opex.sum():,.0f}" for k in ("bajo","medio","alto")))
