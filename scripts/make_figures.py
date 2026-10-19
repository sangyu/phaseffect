"""Redraw the two derived figures of the phaseffect site from the cohort-level tables in tables/.

F1_cohort_shifts.png   : phase shifts in native units (tables/cohort_phenovector.csv)
F2_repeatability.png   : within- vs between-person distances and per-feature ICC (tables/repeatability_summary.json, tables/feature_icc.csv)
F3_published_vs_this_site.png : published luteal − late-follicular contrasts beside this site's estimates (tables/cohort_phenovector.csv + transcribed values)

Every input is a cohort aggregate over at least five participants; nothing participant-level is read or drawn.
"""
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES, FIGURES = ROOT / 'tables', ROOT / 'figures'
INK, INK2, PAPER, GRID = '#1a1a1a', '#666666', '#fcfcfa', '#dddddd'
CONTRASTS = ['Menstrual − Follicular', 'Fertility − Follicular', 'Luteal − Follicular']
SHORT = {c: c.split(' ')[0] for c in CONTRASTS}
MARK = {'Menstrual − Follicular': 's', 'Fertility − Follicular': '^', 'Luteal − Follicular': 'o'}
NICE = {'sorebreasts': 'sore breasts', 'moodswing': 'mood swings', 'foodcravings': 'food cravings', 'sleepissue': 'sleep issues'}

plt.rcParams.update({
    'axes.edgecolor': INK2, 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.facecolor': PAPER, 'figure.facecolor': PAPER,
})


def excludes_zero(lo, hi):
    return lo > 0 or hi < 0


def nice(label):
    return NICE.get(label, label)


def f1():
    t = pd.read_csv(TABLES / 'cohort_phenovector.csv')
    t = t[~t.suppressed]
    phys, sym = t[t.family == 'physiology'], t[t.family == 'symptom']
    def order(fam, by):
        # same rule as the source run: rows follow each family's strongest contrast, by Hedges' g
        g = fam[fam.contrast == by].set_index('feature').hedges_g
        return list(g.sort_values(ascending=False).index)

    phys_feats, sym_feats = order(phys, 'Luteal − Follicular'), order(sym, 'Menstrual − Follicular')

    fig = plt.figure(figsize=(12, 10))
    gs = fig.add_gridspec(2, 6, height_ratios=[1, 1.8], hspace=0.5, wspace=0.5)

    for j, f in enumerate(phys_feats):
        ax = fig.add_subplot(gs[0, j])
        r = phys[phys.feature == f].set_index('contrast')
        for i, c in enumerate(CONTRASTS):
            if c not in r.index:
                continue
            row, y = r.loc[c], len(CONTRASTS) - 1 - i
            ax.plot([row.mean_diff_lo, row.mean_diff_hi], [y, y], color=INK, lw=1.6, solid_capstyle='round')
            filled = excludes_zero(row.mean_diff_lo, row.mean_diff_hi)
            ax.scatter([row.mean_diff], [y], s=44, marker=MARK[c], color=INK if filled else PAPER, edgecolor=INK, lw=1.2, zorder=3)
        ax.axvline(0, color=INK2, lw=0.8)
        ax.set_yticks(range(len(CONTRASTS)))
        ax.set_yticklabels([SHORT[c] for c in CONTRASTS[::-1]] if j == 0 else [], fontsize=8.5)
        ax.set_ylim(-0.6, len(CONTRASTS) - 0.4)
        ax.set_xlabel(str(r.unit.iloc[0]), fontsize=8.5)
        n_lo, n_hi = int(r.n_participants.min()), int(r.n_participants.max())
        n_txt = f'n = {n_hi}' if n_lo == n_hi else f'n = {n_lo}–{n_hi}'
        ax.set_title(f'{textwrap.fill(str(r.label.iloc[0]), 16)}\n{n_txt}', fontsize=9, loc='left', color=INK)
        ax.grid(axis='x', color=GRID, lw=0.5)
        ax.tick_params(labelsize=8)

    ax = fig.add_subplot(gs[1, 1:5])
    off = {'Menstrual − Follicular': -0.24, 'Fertility − Follicular': 0.0, 'Luteal − Follicular': 0.24}
    for k, f in enumerate(sym_feats):
        r = sym[sym.feature == f].set_index('contrast')
        for c in CONTRASTS:
            if c not in r.index:
                continue
            row, y = r.loc[c], k + off[c]
            ax.plot([row.mean_diff_lo, row.mean_diff_hi], [y, y], color=INK, lw=1.3, solid_capstyle='round')
            filled = excludes_zero(row.mean_diff_lo, row.mean_diff_hi)
            ax.scatter([row.mean_diff], [y], s=36, marker=MARK[c], color=INK if filled else PAPER, edgecolor=INK, lw=1.1, zorder=3)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_yticks(range(len(sym_feats)))
    ax.set_yticklabels([nice(sym[sym.feature == f].label.iloc[0]) for f in sym_feats], fontsize=9)
    ax.set_ylim(len(sym_feats) - 0.5, -0.5)
    ax.set_xlabel('points on the 0–5 scale', fontsize=9)
    n_lo, n_hi = int(sym.n_participants.min()), int(sym.n_participants.max())
    ax.set_title(f'Diary symptoms, n = {n_lo}–{n_hi}', fontsize=9.5, loc='left', color=INK)
    ax.grid(axis='x', color=GRID, lw=0.5)
    handles = [Line2D([], [], marker=MARK[c], color=INK, markerfacecolor=INK, markeredgecolor=INK, lw=0, markersize=7, label=f'{c}') for c in CONTRASTS]
    handles.append(Line2D([], [], marker='o', color=INK, markerfacecolor=PAPER, markeredgecolor=INK, lw=0, markersize=7, label='open: interval includes 0'))
    ax.legend(handles=handles, frameon=False, fontsize=8.5, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

    fig.suptitle("Shifts relative to each participant's own follicular days, mcPHASES interval 2022.  "
                 "Paired mean difference, 95 % BCa over participants; filled: interval excludes 0",
                 x=0.01, y=0.985, ha='left', fontsize=11, color=INK)
    fig.text(0.01, 0.005, 'Cohort aggregates over 37–42 participants per cell; no participant-level value, identifier or date appears.',
             fontsize=8, color=INK2)
    out = FIGURES / 'F1_cohort_shifts.png'
    fig.savefig(out, dpi=170, bbox_inches='tight', facecolor=PAPER)
    plt.close(fig)
    return out


def f2():
    s = json.loads((TABLES / 'repeatability_summary.json').read_text())
    icc = pd.read_csv(TABLES / 'feature_icc.csv')
    icc = icc[~icc.suppressed].sort_values('icc', ascending=False).reset_index(drop=True)

    fig = plt.figure(figsize=(12, 5.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.6], wspace=0.5)

    ax = fig.add_subplot(gs[0, 0])
    for x, key in ((0, 'within'), (1, 'between')):
        v = s[key]
        ax.plot([x, x], [v['lo'], v['hi']], color=INK, lw=2, solid_capstyle='round')
        ax.scatter([x], [v['point']], s=80, color=PAPER, edgecolor=INK, lw=1.6, zorder=3)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, max(s['within']['hi'], s['between']['hi']) * 1.18)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['within person', 'between people'], fontsize=9.5)
    ax.set_ylabel('mean distance between cycle vectors (pooled-SD units)', fontsize=9)
    r = s['ratio']
    ax.text(0.98, 0.04, f"within / between = {r['point']:.2f}  [{r['lo']:.2f}, {r['hi']:.2f}]",
            transform=ax.transAxes, ha='right', va='bottom', fontsize=10, color=INK)
    ax.set_title(f"A  Luteal − follicular cycle vectors, {s['n_features']} features\n"
                 f"{s['n_participants_within']} participants with ≥ 2 closed cycles, {s['n_cycles_in_within_set']} cycles",
                 fontsize=9.5, loc='left', color=INK)
    ax.grid(axis='y', color=GRID, lw=0.5)

    ax = fig.add_subplot(gs[0, 1])
    for y, row in icc.iterrows():
        phys = row.family == 'physiology'
        ax.plot([row.icc_lo, row.icc_hi], [y, y], color=INK if phys else INK2, lw=1.6, solid_capstyle='round')
        ax.scatter([row.icc], [y], s=40, color=INK if phys else PAPER, edgecolor=INK if phys else INK2, lw=1.2, zorder=3)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_yticks(range(len(icc)))
    ax.set_yticklabels([nice(l) for l in icc.label], fontsize=8.5)
    ax.set_ylim(len(icc) - 0.5, -0.5)
    ax.set_xlim(-0.85, 1.0)
    ax.set_xlabel("ICC(1) of the luteal − follicular shift across a person's cycles, 95 % BCa", fontsize=9)
    ax.grid(axis='x', color=GRID, lw=0.5)
    n_lo, n_hi = int(icc.n_participants.min()), int(icc.n_participants.max())
    ax.set_title(f'B  Per feature, {n_lo}–{n_hi} participants (filled: device signals)', fontsize=9.5, loc='left', color=INK)

    fig.suptitle("Does a person's luteal − follicular shift repeat across her cycles?  mcPHASES interval 2022, closed cycles",
                 x=0.01, y=0.99, ha='left', fontsize=11, color=INK)
    fig.text(0.01, 0.005, f"Cohort aggregates over {n_lo}–{s['n_participants_within']} participants; no participant-level value, identifier or date appears.",
             fontsize=8, color=INK2)
    out = FIGURES / 'F2_repeatability.png'
    fig.savefig(out, dpi=170, bbox_inches='tight', facecolor=PAPER)
    plt.close(fig)
    return out


# Published luteal − late-follicular contrasts, transcribed from the papers listed on prior-findings.qmd
PUBLISHED = [
    ('glucose', 'Lin 2023, mixed-model β\n49 participants, 149 cycles', 0.15, 0.09, 0.20),
    ('temp', 'Lin 2024, difference of group means\n45 participants, no interval', 0.30, None, None),
    ('rhr', 'Lin 2026 descriptor, ANOVA only\nsize not published', None, None, None),
]


def f3():
    t = pd.read_csv(TABLES / 'cohort_phenovector.csv')
    lut = t[t.contrast == 'Luteal − Follicular'].set_index('feature')
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), gridspec_kw={'wspace': 1.1})
    for ax, (f, lab, pt, lo, hi) in zip(axes, PUBLISHED):
        r = lut.loc[f]
        ax.plot([r.mean_diff_lo, r.mean_diff_hi], [0, 0], color=INK, lw=2, solid_capstyle='round')
        ax.scatter([r.mean_diff], [0], s=60, color=INK, zorder=3)
        xs = [0, r.mean_diff_lo, r.mean_diff_hi]
        if pt is not None:
            if lo is not None:
                ax.plot([lo, hi], [1, 1], color=INK2, lw=2, solid_capstyle='round')
                xs += [lo, hi]
            ax.scatter([pt], [1], s=60, marker='o' if lo is not None else 'D', color=INK2, zorder=3)
            xs.append(pt)
        else:
            ax.text(0.5, 1, 'size not published', transform=ax.get_yaxis_transform(), ha='center', va='center', fontsize=9, color=INK2)
        ax.axvline(0, color=INK2, lw=0.8)
        ax.set_yticks([0, 1])
        ax.set_yticklabels([f'This site, luteal − follicular\n{int(r.n_participants)} participants', lab], fontsize=8.5)
        ax.set_ylim(-0.7, 1.7)
        span = max(xs) - min(xs)
        ax.set_xlim(min(xs) - 0.15 * span, max(xs) + 0.15 * span)
        ax.set_title(f'{r.label} ({r.unit})', fontsize=10, loc='left', color=INK)
        ax.grid(axis='x', color=GRID, lw=0.5)
        ax.tick_params(labelsize=8.5)
    fig.suptitle("Published luteal − late-follicular contrasts (grey) beside this site's luteal − follicular estimates (black).  "
                 "Diamond: point estimate without an interval", x=0.01, y=1.02, ha='left', fontsize=10.5, color=INK)
    out = FIGURES / 'F3_published_vs_this_site.png'
    fig.savefig(out, dpi=170, bbox_inches='tight', facecolor=PAPER)
    plt.close(fig)
    return out


if __name__ == '__main__':
    for p in (f1(), f2(), f3()):
        print('wrote', p.relative_to(ROOT))
