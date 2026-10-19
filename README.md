# phaseffect

How much does the menstrual phase move wearable signals and symptoms, and does a person's own shift repeat across her cycles? Effect sizes with 95 % intervals from interval 2022 of the [mcPHASES](https://physionet.org/content/mcphases/1.0.0/) dataset: 42 participants, Fitbit Sense, Dexcom CGM, Mira urine hormones, daily diary. Every contrast is within the same participants against their own follicular days.

**Site:** https://sangyu.github.io/phaseffect · Cohort aggregates only; no participant-level value, identifier or date appears anywhere in this repository.

## Cohort shifts by phase

Luteal − follicular, same participants: resting heart rate **+3.0 bpm** [2.2, 3.8], wrist temperature **+0.23 °C** [0.12, 0.31], glucose **+0.16 mmol/L** [0.06, 0.27], breathing rate +0.48 /min, HRV −3.9 ms. Menses is the symptom phase: cramps +1.1 points, 41 of 42 participants higher. [Page →](https://sangyu.github.io/phaseffect/cohort-shifts.html)

![Phase shifts in native units: six device signals and eleven diary symptoms, three contrasts each, 95 % BCa intervals](figures/F1_cohort_shifts.png)

<img src="figures/P2_phenovector_heatmap.png" alt="Hedges' g by phase, for comparison across signals" width="55%">

## Does a person's shift repeat?

Not detectably with two or three closed cycles per person: the distance between one person's own luteal − follicular vectors equals the distance to other people's, ratio **1.00** [0.92, 1.08]. Resting heart rate is the one signal with a repeatable personal shift (ICC 0.61 [0.09, 0.86]); the wrist-temperature rise does not repeat (ICC −0.02 [−0.34, 0.31]). [Page →](https://sangyu.github.io/phaseffect/repeatability.html)

![Within- vs between-person distances and per-feature ICC](figures/F2_repeatability.png)

## Context

[Prior findings](https://sangyu.github.io/phaseffect/prior-findings.html): the 17 works that have used this dataset, what each established, and the data hazards they report. No published work gives a within-person effect with its uncertainty. [Methods](https://sangyu.github.io/phaseffect/methods.html) in one screen.

## What is here

| Path | Content |
|---|---|
| `*.qmd`, `_quarto.yml`, `styles.css` | The site. Render with `quarto render` (Quarto ≥ 1.4) |
| `docs/` | Rendered site, served by GitHub Pages |
| `tables/` | Cohort-level tables: effect sizes for 51 cells, per-feature ICCs, the repeatability summary |
| `figures/` | Figures. `F1` and `F2` are redrawn from `tables/` by `scripts/make_figures.py` (pandas, matplotlib) |

## Data and licences

The dataset is restricted-access on PhysioNet. Cite the dataset record ([Lin et al. 2025, PhysioNet, doi:10.13026/zx6a-2c81](https://doi.org/10.13026/zx6a-2c81)), the platform ([Pollard et al. 2026, *Nature Health*](https://doi.org/10.1038/s44360-026-00096-z)) and the descriptor ([Lin et al. 2026, *Scientific Data*](https://doi.org/10.1038/s41597-026-06805-3)). The analysis code that reads it is released separately. Code here: see `LICENSE`. Text and figures made here: © Sangyu Xu 2026. Reproduced published figures keep their own licences, stated in their captions.
