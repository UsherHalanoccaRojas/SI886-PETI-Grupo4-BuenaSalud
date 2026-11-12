"""Genera PR05_hoja_ruta.gan (GanttProject) y graficos/PR_gantt.png desde PR05_hoja_ruta.csv."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xml.sax.saxutils import quoteattr as q

hr = pd.read_csv("PR05_hoja_ruta.csv"); hr["Depende de"]=hr["Depende de"].fillna("")
nom = pd.read_csv("PF01_portafolio_candidatos.csv").set_index("id")["proyecto"]
def d_ini(s):
    d=np.datetime64(pd.Period(s,"M").start_time.date()); return np.busday_offset(d,0,roll="forward")
def d_fin(s): return np.datetime64(pd.Period(s,"M").end_time.date())
ids = {}; n = 0
for ola in (1,2,3): n+=1; ids[f"ola{ola}"]=n
for p in hr.Proyecto: n+=1; ids[p]=n
colores = {1:"#8cb6ce",2:"#a8d5a2",3:"#f2c78d"}
xml=['<?xml version="1.0" encoding="UTF-8"?>','<project name="PETI Buena Salud - Hoja de ruta 2027-2029" company="Cadena de Farmacias Buena Salud E.I.R.L." webLink="" view-date="2027-01-04" view-index="0" gantt-divider-location="400" resource-divider-location="300" version="3.2" locale="es">',' <description/>',' <view zooming-state="default:5" id="gantt-chart"/>',' <view id="resource-table"/>',' <tasks empty-milestones="true">']
for ola in (1,2,3):
    sub = hr[hr.Ola==ola]; a=min(d_ini(s) for s in sub.Inicio); b=max(d_fin(s) for s in sub.Fin)
    xml.append(f'  <task id="{ids[f"ola{ola}"]}" name={q(f"Ola {ola}")} color="{colores[ola]}" meeting="false" start="{a}" duration="{int(np.busday_count(a,b+1))}" complete="0" expand="true">')
    for _,r in sub.iterrows():
        a2=d_ini(r.Inicio); b2=d_fin(r.Fin); dur=int(np.busday_count(a2,b2+1))
        deps="".join(f'<depend id="{ids[d]}" type="2" difference="0" hardness="Strong"/>' for d in filter(None,r["Depende de"].split(";")))
        xml.append(f'   <task id="{ids[r.Proyecto]}" name={q(r.Proyecto+" "+nom[r.Proyecto])} color="{colores[ola]}" meeting="false" start="{a2}" duration="{dur}" complete="0" expand="true">{deps}</task>')
    xml.append("  </task>")
hitos=[("PLAZO NORMATIVO DIGEMID - trazabilidad (P01)","2027-06-30","#ff0000"),("PLAZO NORMATIVO Ley 29733 (P02)","2027-06-30","#ff0000"),
       ("HITO H1 - Decision: medir beneficios de Ola 1 y liberar Ola 2","2027-12-31","#000000"),("HITO H2 - Decision: cierre de Ola 2 y revision de P12","2028-12-30","#000000"),("HITO H3 - Cierre del plan y revision de P13 a P15","2029-12-31","#000000")]
for t,f,c in hitos:
    n+=1; f=np.busday_offset(np.datetime64(f),0,roll="backward")
    xml.append(f'  <task id="{n}" name={q(t)} color="{c}" meeting="true" start="{f}" duration="0" complete="0" expand="true"/>')
xml+=[" </tasks>",' <resources/>',' <allocations/>',' <vacations/>',' <previous/>',' <roles roleset-name="Default"/>',"</project>"]
open("PR05_hoja_ruta.gan","w",encoding="utf-8").write("\n".join(xml))

fig,ax=plt.subplots(figsize=(12,5.5)); orden=list(hr.Proyecto)[::-1]
for i,p in enumerate(orden):
    r=hr[hr.Proyecto==p].iloc[0]; a=pd.Period(r.Inicio,"M").start_time; b=pd.Period(r.Fin,"M").end_time
    ax.barh(i,(b-a).days,left=a,color=colores[r.Ola],edgecolor="k"); 
    for d in filter(None,r["Depende de"].split(";")):
        pr=hr[hr.Proyecto==d].iloc[0]; ax.annotate("",xy=(a,i),xytext=(pd.Period(pr.Fin,"M").end_time,orden.index(d)),arrowprops=dict(arrowstyle="->",color="gray",lw=1))
ax.set_yticks(range(len(orden))); ax.set_yticklabels([f"{p} {nom[p][:32]}" for p in orden],fontsize=8)
for f,c,l in [("2027-06-30","red","Plazos DIGEMID y Ley 29733"),("2027-12-31","k","H1"),("2028-12-31","k","H2"),("2029-12-31","k","H3")]:
    ax.axvline(pd.Timestamp(f),color=c,ls="--" if c=="k" else "-",lw=1.2); ax.text(pd.Timestamp(f),len(orden)-.3,l,fontsize=8,ha="right",color=c)
ax.set_title("Hoja de ruta 2027-2029 en tres olas (dependencias fin-inicio)"); plt.tight_layout(); plt.savefig("graficos/PR_gantt.png",dpi=160)
print("PR05_hoja_ruta.gan generado con", len(hr), "proyectos y", len(hitos), "hitos")
