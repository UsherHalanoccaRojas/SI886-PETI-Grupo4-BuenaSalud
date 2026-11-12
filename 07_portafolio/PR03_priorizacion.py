"""PR03 - Priorizacion multicriterio y matriz esfuerzo-impacto.
Lee PR01_portafolio_marcado.csv y PF02_tco.csv. Produce PR03_priorizado.csv y
graficos/PR_esfuerzo_impacto.png. Los pesos son los de PR02_pesos.md."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Pesos fijados en PR02_pesos.md (se validan antes de calcular) ---
PESOS = {"contribucion":.25,"riesgo_no_hacerlo":.20,"urgencia":.10,"habilitacion":.10,
         "beneficio_economico":.10,"impacto_social_ambiental":.10,"facilidad":.10,"aceptacion":.05}
assert abs(sum(PESOS.values())-1)<1e-9, "Los pesos deben sumar 1"
assert PESOS["impacto_social_ambiental"]>=.10, "El criterio social y ambiental pesa al menos 10 %"
CRITERIOS_VALOR = ["contribucion","riesgo_no_hacerlo","urgencia","habilitacion","beneficio_economico","impacto_social_ambiental"]
CONT, UMBRAL = 0.20, 3.0
CAPACIDAD_LIBRE_ANUAL = 108091  # 468 000 - base operativa ejecutada 2025 (359 909)

# --- Puntajes 1-5 (contribucion, riesgo, urgencia, habilitacion, beneficio, social, facilidad, aceptacion) ---
P = {
 "P03":(5,5,4,5,4,3,3,4),  # falla 2 veces por semana; habilita compras
 "P04":(5,5,4,5,2,2,4,3),  # ataca directamente la dependencia de una persona
 "P05":(3,4,4,3,2,3,5,4),  # tres sistemas sin respaldo; solucion simple
 "P06":(3,4,3,2,2,3,3,3),  # no existe plan de continuidad
 "P07":(3,4,3,2,2,3,4,3),  # MFA solo en correo; politica sin aprobar
 "P08":(3,4,3,5,3,1,4,2),  # inversiones sin medicion y +44.8 % de desviacion
 "P09":(4,3,2,2,4,3,2,3),  # compras en hojas de calculo y correo
 "P10":(2,3,2,4,2,1,4,3),  # incidentes no registrados
 "P11":(2,3,2,3,2,1,5,4),  # inventario desactualizado
 "P12":(5,4,3,3,4,3,1,2),  # reemplazo del POS
 "P13":(1,2,1,1,1,2,2,3),  # ampliar videovigilancia
 "P14":(2,1,1,1,3,3,2,3),  # app y comercio electronico
 "P15":(2,1,2,1,3,2,3,3),  # BI
}
cols = list(PESOS)
df = pd.read_csv("PR01_portafolio_marcado.csv"); df = df[df.entra_al_modelo].copy()
tco = pd.read_csv("PF02_tco.csv").set_index("id")
for i,c in enumerate(cols): df[c] = df["id"].map(lambda k: P[k][i])
df["puntaje"] = sum(df[c]*w for c,w in PESOS.items())/5*100
df["impacto"] = sum(df[c]*PESOS[c] for c in CRITERIOS_VALOR)/sum(PESOS[c] for c in CRITERIOS_VALOR)
df["tco_3a"] = df["id"].map(lambda k: tco.loc[k,"capex"]*(1+tco.loc[k,"gestion_cambio_pct"])*(1+CONT)+3*tco.loc[k,"opex_anual"])
banda = lambda v: 1 if v<30000 else 2 if v<60000 else 3 if v<120000 else 4 if v<250000 else 5
df["banda_costo"] = df["tco_3a"].map(banda)
df["esfuerzo"] = .5*(6-df["facilidad"]) + .5*df["banda_costo"]
def cuad(r):
    if r.impacto>=UMBRAL: return "1 Alto impacto / bajo esfuerzo" if r.esfuerzo<UMBRAL else "2 Alto impacto / alto esfuerzo"
    return "3 Bajo impacto / bajo esfuerzo" if r.esfuerzo<UMBRAL else "4 Bajo impacto / alto esfuerzo"
df["cuadrante"] = df.apply(cuad, axis=1)
def decision(r):
    if r.cuadrante.startswith("4"): return "NO EJECUTAR (cuadrante 4)"
    if r.tco_3a > 3*CAPACIDAD_LIBRE_ANUAL: return "NO EJECUTAR (excede la capacidad trianual)"
    return "Ejecutar"
df["decision"] = df.apply(decision, axis=1)
df = df.sort_values("puntaje", ascending=False).reset_index(drop=True); df.insert(0,"ranking",df.index+1)
out = ["ranking","id","proyecto","puntaje","impacto","esfuerzo","cuadrante","tco_3a","decision"]+cols
df[out].round(2).to_csv("PR03_priorizado.csv", index=False)

print("PESOS:", PESOS, "| suma =", round(sum(PESOS.values()),2))
print(df[["ranking","id","proyecto","puntaje","impacto","esfuerzo","cuadrante","decision"]].round(2).to_string(index=False))
print("\nPROYECTOS DEL CUADRANTE 4 (candidatos a no ejecutar):")
for _,r in df[df.cuadrante.str.startswith("4")].iterrows(): print(f" {r.id} {r.proyecto} | impacto {r.impacto:.2f} esfuerzo {r.esfuerzo:.2f}")
print("Cuadrantes poblados:", sorted(df.cuadrante.str[0].unique()))

fig, ax = plt.subplots(figsize=(8.5,6.5))
ax.axhline(UMBRAL,color="gray",ls="--"); ax.axvline(UMBRAL,color="gray",ls="--")
col = {"1":"#2e7d32","2":"#1565c0","3":"#f9a825","4":"#c62828"}
for _,r in df.iterrows():
    ax.scatter(r.esfuerzo,r.impacto,s=170,color=col[r.cuadrante[0]],edgecolor="k",zorder=3)
    ax.annotate(r.id,(r.esfuerzo,r.impacto),xytext=(6,6),textcoords="offset points",fontsize=9)
ax.set_xlim(.8,5.2); ax.set_ylim(1,4.9)
for t,x,y in [("1 Hacer primero",.9,4.75),("2 Planificar",3.1,4.75),("3 Hacer si sobra capacidad",.9,1.1),("4 Candidatos a no ejecutar",3.1,1.1)]:
    ax.text(x,y,t,fontsize=10,fontweight="bold",color="#444")
ax.set_xlabel("Esfuerzo (1 bajo - 5 alto)"); ax.set_ylabel("Impacto (1 bajo - 5 alto)")
ax.set_title("Matriz esfuerzo-impacto - Cadena de Farmacias Buena Salud")
plt.tight_layout(); plt.savefig("graficos/PR_esfuerzo_impacto.png",dpi=160)
