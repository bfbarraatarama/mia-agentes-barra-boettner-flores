# Trabajo integrador - Agentes Autónomos y Sistemas de decisión - MIA - UdeSA

Integrantes del grupo:
- Barra Atarama, Bruno F.
- Boettner, María Luisa
- Flores, Jorge Federico

## Descripción general
En este repositorio se desarrolla el trabajo integrador de la materia **Agentes Autónomos y Sistemas de decisión** de la **Maestría en Inteligencia Artificial** de la **Universidad de San Andrés**.

El desarrollo se realizará en tres "milestones", `M1`, `M2` y `M3`.

Estado actual: `M2 abordada`.

## Informes 
La documentación de cada etapa completada se complementará con un informe en `informes/m*.md`

Informes actuales
- [m1.md](informes/m1.md)
- [m2.md](informes/m2.md)

## Resultados experimentales y Git LFS

La evidencia primaria de cada corrida experimental se versiona bajo `eval/results/`.
Los raw runs conservan los traces completos de todos los trials y pueden superar los
90 MB, por lo que se almacenan mediante **Git LFS**. La política está expresada por
path en `.gitattributes` y se aplica automáticamente a los runs futuros:

| Artefacto | Almacenamiento |
|---|---|
| `eval/results/runs/<run_id>.json` | Git LFS |
| `eval/results/runs/<run_id>.manifest.json` | Git convencional |
| `eval/results/evaluations/<eval_id>/results.json` | Git convencional |
| `eval/results/evaluations/<eval_id>/*.md`, `*.png` | Git convencional |

### Requisito para trabajar con los resultados

Git LFS debe estar instalado **antes** de clonar el repositorio:

```bash
sudo apt install git-lfs   # o: brew install git-lfs
git lfs install
```

Si ya clonaste sin tenerlo, los raw runs aparecen como archivos de ~130 bytes con un
pointer en lugar del JSON. Se materializan con:

```bash
git lfs install
git lfs pull
```

Para verificar qué archivos administra LFS:

```bash
git lfs ls-files
```
