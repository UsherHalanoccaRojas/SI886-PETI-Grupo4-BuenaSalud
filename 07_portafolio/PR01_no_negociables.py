"""PR01 - Separa los proyectos no negociables del modelo multicriterio.
Lee PF01_portafolio_candidatos.csv y produce PR01_portafolio_marcado.csv."""
import pandas as pd

df = pd.read_csv("PF01_portafolio_candidatos.csv")
df["no_negociable"] = df["no_negociable"].str.upper().eq("SI")
df["entra_al_modelo"] = ~df["no_negociable"]
df.to_csv("PR01_portafolio_marcado.csv", index=False)

nn = df[df.no_negociable]
print("PROYECTOS NO NEGOCIABLES (fuera del modelo)")
for _, r in nn.iterrows():
    print(f" {r.id} {r.proyecto}\n    norma: {r.norma}\n    plazo: {r.plazo_norma}")
print(f"\nCandidatos totales: {len(df)} | no negociables: {len(nn)} | compiten en el modelo: {int(df.entra_al_modelo.sum())}")
