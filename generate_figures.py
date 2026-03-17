"""
Generate figures for Paper 8: The Merkabit Architecture and the Klein Quartic
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from itertools import combinations
from collections import Counter
import os

outdir = os.path.dirname(os.path.abspath(__file__))

# Use consistent style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'figure.dpi': 300,
})

# =========================================================================
# FIGURE 1: The Azygetic Graph T(8) on 28 bitangents
# =========================================================================
print("Generating Figure 1: Azygetic graph / T(8)...")

# Recompute the azygetic graph
all_chars = []
for i in range(64):
    vec = np.array([(i >> j) & 1 for j in range(6)], dtype=int)
    all_chars.append(vec)

def arf(v):
    return int(np.dot(v[:3], v[3:]) % 2)

odd_chars = [v for v in all_chars if arf(v) == 1]

def symplectic_pairing(u, v):
    a, b = u[:3], u[3:]
    c, d = v[:3], v[3:]
    return int((np.dot(a, d) + np.dot(b, c)) % 2)

n = 28
adj = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symplectic_pairing(odd_chars[i], odd_chars[j]) == 1:
            adj[i, j] = 1
            adj[j, i] = 1

# Find max cliques using Bron-Kerbosch
def bron_kerbosch(R, P, X, adj, cliques):
    if not P and not X:
        if len(R) >= 3:
            cliques.append(sorted(R))
        return
    pivot = max(P | X, key=lambda v: len([u for u in P if adj[v,u]]))
    for v in list(P - set([u for u in P if adj[pivot,u]])):
        bron_kerbosch(R | {v}, {u for u in P if adj[v,u]},
                      {u for u in X if adj[v,u]}, adj, cliques)
        P.remove(v)
        X.add(v)

cliques = []
bron_kerbosch(set(), set(range(28)), set(), adj, cliques)
max_cliques = [c for c in cliques if len(c) == 7]

# Assign colors based on clique membership
colors_8 = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
            '#ff7f00', '#a65628', '#f781bf', '#999999']
node_colors = ['#cccccc'] * 28
clique_of = {}
for ci, clique in enumerate(max_cliques):
    for v in clique:
        if v not in clique_of:
            clique_of[v] = ci
            node_colors[v] = colors_8[ci]

# Layout: arrange by clique membership in a circle
angles = np.linspace(0, 2*np.pi, 28, endpoint=False)
# Group nodes by their primary clique
ordered = []
for ci in range(8):
    members = [v for v in range(28) if clique_of.get(v) == ci]
    ordered.extend(members)

pos = {}
for idx, v in enumerate(ordered):
    a = angles[idx]
    pos[v] = (2.5 * np.cos(a), 2.5 * np.sin(a))

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Draw edges (light gray)
for i in range(n):
    for j in range(i+1, n):
        if adj[i, j]:
            ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]],
                    '-', color='#cccccc', linewidth=0.3, zorder=1)

# Draw nodes
for v in range(28):
    circle = plt.Circle(pos[v], 0.15, color=node_colors[v],
                        ec='black', linewidth=0.8, zorder=3)
    ax.add_patch(circle)
    ax.text(pos[v][0], pos[v][1], str(v), ha='center', va='center',
            fontsize=6, fontweight='bold', zorder=4)

# Legend for cliques
legend_patches = [mpatches.Patch(color=colors_8[i], label=f'Clique {i+1} (size 7)')
                  for i in range(8)]
ax.legend(handles=legend_patches, loc='upper left', fontsize=7,
          title='8 Maximum Cliques', title_fontsize=8, framealpha=0.9)

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('The Azygetic Graph on 28 Bitangents\nsrg(28, 12, 6, 4) $\\cong$ T(8) = L(K$_8$)',
             fontsize=13, fontweight='bold', pad=15)

fig.tight_layout()
fig.savefig(os.path.join(outdir, 'fig1_azygetic_graph.png'), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved fig1_azygetic_graph.png")

# =========================================================================
# FIGURE 2: Adjacency matrix heatmap showing srg structure
# =========================================================================
print("Generating Figure 2: Adjacency matrix heatmap...")

# Reorder by clique for visual clarity
reorder = ordered
adj_reord = adj[np.ix_(reorder, reorder)]

fig, ax = plt.subplots(1, 1, figsize=(7, 6))
cmap = plt.cm.colors.ListedColormap(['white', '#2166ac'])
ax.imshow(adj_reord, cmap=cmap, interpolation='none', aspect='equal')

# Draw clique boundaries
cum = 0
for ci in range(8):
    sz = sum(1 for v in range(28) if clique_of.get(v) == ci)
    if cum > 0:
        ax.axhline(cum - 0.5, color='red', linewidth=1.0, alpha=0.7)
        ax.axvline(cum - 0.5, color='red', linewidth=1.0, alpha=0.7)
    cum += sz

ax.set_xlabel('Bitangent index (reordered by T(8) clique)', fontsize=10)
ax.set_ylabel('Bitangent index (reordered by T(8) clique)', fontsize=10)
ax.set_title('Adjacency Matrix of the Azygetic Graph\n(blue = azygetic, white = syzygetic; red lines = T(8) clique boundaries)',
             fontsize=11, fontweight='bold')

fig.tight_layout()
fig.savefig(os.path.join(outdir, 'fig2_adjacency_matrix.png'), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved fig2_adjacency_matrix.png")

# =========================================================================
# FIGURE 3: Subfield lattice of Q(zeta_21)
# =========================================================================
print("Generating Figure 3: Cyclotomic subfield lattice...")

fig, ax = plt.subplots(1, 1, figsize=(8, 6))

# Positions for field nodes
fields = {
    'Q':           (0.5, 0.0),
    'Q(sqrt(-3))': (0.15, 0.25),
    'Q(sqrt(-7))': (0.85, 0.25),
    'Q(zeta_3)':   (0.15, 0.5),
    'Q(zeta_7)+':  (0.85, 0.5),
    'Q(zeta_7)':   (0.85, 0.75),
    'Q(zeta_21)':  (0.5, 1.0),
}

labels = {
    'Q':           '$\\mathbb{Q}$',
    'Q(sqrt(-3))': '$\\mathbb{Q}(\\sqrt{-3})$',
    'Q(sqrt(-7))': '$\\mathbb{Q}(\\sqrt{-7})$',
    'Q(zeta_3)':   '$\\mathbb{Q}(\\zeta_3)$\nEisenstein lattice',
    'Q(zeta_7)+':  '$\\mathbb{Q}(\\zeta_7)^+$\nCM totally real',
    'Q(zeta_7)':   '$\\mathbb{Q}(\\zeta_7)$\nKlein quartic CM',
    'Q(zeta_21)':  '$\\mathbb{Q}(\\zeta_{21})$\ndegree $\\varphi(21) = 12 = h(E_6)$',
}

# Degree labels on edges
edges = [
    ('Q', 'Q(sqrt(-3))', '2'),
    ('Q', 'Q(sqrt(-7))', '2'),
    ('Q(sqrt(-3))', 'Q(zeta_3)', '1'),
    ('Q(sqrt(-7))', 'Q(zeta_7)+', '3/2'),
    ('Q', 'Q(zeta_7)+', '3'),
    ('Q(zeta_3)', 'Q(zeta_21)', '6'),
    ('Q(zeta_7)', 'Q(zeta_21)', '2'),
    ('Q(zeta_7)+', 'Q(zeta_7)', '2'),
]

# Draw edges
for src, dst, deg in edges:
    x0, y0 = fields[src]
    x1, y1 = fields[dst]
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-', color='#666666', linewidth=1.5))
    mx, my = (x0+x1)/2, (y0+y1)/2
    # offset label slightly
    dx, dy = x1-x0, y1-y0
    nx, ny = -dy, dx  # normal
    norm = (nx**2 + ny**2)**0.5
    if norm > 0:
        nx, ny = nx/norm*0.04, ny/norm*0.04

# Draw field nodes
for name, (x, y) in fields.items():
    bbox_color = '#e8f4e8' if name in ['Q(zeta_3)', 'Q(zeta_21)'] else \
                 '#e8e8f4' if name in ['Q(zeta_7)', 'Q(zeta_7)+'] else '#f4f4f4'
    if name == 'Q(zeta_21)':
        bbox_color = '#fff2cc'
    ax.text(x, y, labels[name], ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=bbox_color,
                      edgecolor='black', linewidth=1.2),
            zorder=5)

# Add annotations
ax.text(0.08, 0.37, 'deg 2', fontsize=8, color='#444444', ha='center')
ax.text(0.92, 0.37, 'deg 2', fontsize=8, color='#444444', ha='center')
ax.text(0.25, 0.78, 'deg 6', fontsize=8, color='#444444', ha='center')
ax.text(0.75, 0.88, 'deg 2', fontsize=8, color='#444444', ha='center')

# Title annotation
ax.text(0.5, -0.08, 'Linearly disjoint: $\\mathbb{Q}(\\zeta_3) \\cap \\mathbb{Q}(\\zeta_7) = \\mathbb{Q}$',
        ha='center', fontsize=10, style='italic')
ax.text(0.5, -0.15, '$\\zeta_3 = \\zeta_{21}^7$,   $\\zeta_7 = \\zeta_{21}^3$',
        ha='center', fontsize=10)

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.22, 1.15)
ax.axis('off')
ax.set_title('Subfield Lattice of $\\mathbb{Q}(\\zeta_{21})$\nCyclotomic Unification of Merkabit and Klein Quartic',
             fontsize=13, fontweight='bold', pad=15)

fig.tight_layout()
fig.savefig(os.path.join(outdir, 'fig3_subfield_lattice.png'), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved fig3_subfield_lattice.png")

# =========================================================================
# FIGURE 4: The forcing chain diagram
# =========================================================================
print("Generating Figure 4: Route B forcing chain...")

fig, ax = plt.subplots(1, 1, figsize=(10, 5))

# Chain: alpha^{-1} = 137 -> 137-28=109 -> N(12+5w) -> (12,5) forced
steps = [
    ('$\\alpha^{-1} = 137$\n(experimental)', 0.05),
    ('$\\dim(D_4) = 28$\n(triality)', 0.22),
    ('$109 = 137 - 28$\n(forced norm)', 0.39),
    ('$a = h(E_6) = 12$\n(Coxeter number)', 0.56),
    ('$b^2 - 12b + 35 = 0$\n$b = 5$ or $b = 7$', 0.73),
    ('$b = 5$\n(Weyl chamber)', 0.90),
]

y = 0.55
for label, x in steps:
    bbox_color = '#fff2cc' if x == 0.90 else '#e8f0ff'
    ax.text(x, y, label, ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=bbox_color,
                      edgecolor='black', linewidth=1.2),
            zorder=5)

# Arrows between steps
for i in range(len(steps)-1):
    x0 = steps[i][1] + 0.06
    x1 = steps[i+1][1] - 0.06
    ax.annotate('', xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='->', color='#333333',
                                linewidth=1.5, shrinkA=2, shrinkB=2))

# Bottom: the result
ax.text(0.5, 0.15,
        '$\\alpha^{-1} = N(h(E_6) + e_3 \\cdot \\omega) + \\dim(D_4) = N(12 + 5\\omega) + 28 = 109 + 28 = 137$',
        ha='center', va='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#d4edda',
                  edgecolor='#155724', linewidth=2))

# Labels for what forces each step
force_labels = [
    (0.05, 0.85, 'Input', '#999999'),
    (0.22, 0.85, 'McKay + P$_{24}$', '#999999'),
    (0.39, 0.85, 'Subtraction', '#999999'),
    (0.56, 0.85, '$|P_{24}| = 2h$', '#999999'),
    (0.73, 0.85, 'Quadratic', '#999999'),
    (0.90, 0.85, '$\\mathrm{Im}(\\zeta_{12}^5) > 0$', '#999999'),
]
for x, fy, label, color in force_labels:
    ax.text(x, fy, label, ha='center', va='center', fontsize=7.5,
            color=color, style='italic')

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(0.0, 1.0)
ax.axis('off')
ax.set_title('Route B Forcing Chain: Zero Free Parameters',
             fontsize=14, fontweight='bold', pad=10)

fig.tight_layout()
fig.savefig(os.path.join(outdir, 'fig4_forcing_chain.png'), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved fig4_forcing_chain.png")

# =========================================================================
# FIGURE 5: Conjugacy class structure of PSL(2,7)
# =========================================================================
print("Generating Figure 5: PSL(2,7) conjugacy classes...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# Left: pie chart of conjugacy classes
class_data = [
    (1, 1, '#f7f7f7'),
    (21, 2, '#92c5de'),
    (56, 3, '#d73027'),
    (42, 4, '#fc8d59'),
    (24, 7, '#4575b4'),
    (24, 7, '#313695'),
]
sizes = [d[0] for d in class_data]
labels_pie = [f'Order {d[1]}\n({d[0]} elts)' for d in class_data]
colors_pie = [d[2] for d in class_data]

wedges, texts, autotexts = ax1.pie(sizes, labels=labels_pie, colors=colors_pie,
                                     autopct='%1.0f%%', startangle=90,
                                     textprops={'fontsize': 8})
for at in autotexts:
    at.set_fontsize(7)
ax1.set_title('Conjugacy Classes of PSL(2,7)\n|G| = 168', fontsize=11, fontweight='bold')

# Highlight the order-3 class
# Add annotation arrow pointing to the order-3 wedge
ax1.annotate('Single class of size 56\n= Klein quartic vertices\n= Eisenstein qubits',
             xy=(0.3, 0.45), fontsize=8, ha='center',
             bbox=dict(boxstyle='round', facecolor='#ffeeee', edgecolor='#d73027'),
             arrowprops=dict(arrowstyle='->', color='#d73027'))

# Right: bar chart of element orders
orders = {1: 1, 2: 21, 3: 56, 4: 42, 7: 48}
bars = ax2.bar(list(orders.keys()), list(orders.values()),
               color=['#f7f7f7', '#92c5de', '#d73027', '#fc8d59', '#4575b4'],
               edgecolor='black', linewidth=0.8)
ax2.set_xlabel('Element Order')
ax2.set_ylabel('Count')
ax2.set_title('Element Order Distribution\nin PSL(2,7) = GL(3,$\\mathbb{F}_2$)',
              fontsize=11, fontweight='bold')
ax2.set_xticks([1, 2, 3, 4, 7])

# Annotate the order-3 bar
ax2.annotate('ALL conjugate\n(single class)', xy=(3, 56), xytext=(4.5, 60),
             fontsize=8, ha='center',
             bbox=dict(boxstyle='round', facecolor='#ffeeee', edgecolor='#d73027'),
             arrowprops=dict(arrowstyle='->', color='#d73027'))

# Annotate order-7 bars
ax2.annotate('Two classes\nof size 24', xy=(7, 48), xytext=(6.0, 55),
             fontsize=8, ha='center',
             bbox=dict(boxstyle='round', facecolor='#eeeeff', edgecolor='#4575b4'),
             arrowprops=dict(arrowstyle='->', color='#4575b4'))

for bar, count in zip(bars, orders.values()):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             str(count), ha='center', va='bottom', fontsize=9, fontweight='bold')

fig.tight_layout(pad=2)
fig.savefig(os.path.join(outdir, 'fig5_conjugacy_classes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved fig5_conjugacy_classes.png")

# =========================================================================
# FIGURE 6: Spectrum comparison (azygetic vs T(8))
# =========================================================================
print("Generating Figure 6: Spectral comparison...")

# T(8) adjacency
pairs_8 = list(combinations(range(8), 2))
T8_adj = np.zeros((28, 28), dtype=int)
for i, p in enumerate(pairs_8):
    for j, q in enumerate(pairs_8):
        if i != j and len(set(p) & set(q)) == 1:
            T8_adj[i, j] = 1

spec_az = sorted(np.linalg.eigvalsh(adj.astype(float)))
spec_T8 = sorted(np.linalg.eigvalsh(T8_adj.astype(float)))

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ax.plot(range(28), spec_az, 'o', color='#d73027', markersize=8, label='Azygetic graph', zorder=3)
ax.plot(range(28), spec_T8, 'x', color='#4575b4', markersize=10, markeredgewidth=2,
        label='T(8) = L(K$_8$)', zorder=4)

ax.axhline(y=12, color='#999999', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axhline(y=4, color='#999999', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axhline(y=-2, color='#999999', linestyle='--', linewidth=0.5, alpha=0.5)

ax.text(27.5, 12, '12 (mult. 1)', fontsize=8, va='bottom', ha='right', color='#666666')
ax.text(27.5, 4, '4 (mult. 7)', fontsize=8, va='bottom', ha='right', color='#666666')
ax.text(27.5, -2, '$-$2 (mult. 20)', fontsize=8, va='top', ha='right', color='#666666')

ax.set_xlabel('Eigenvalue index')
ax.set_ylabel('Eigenvalue')
ax.set_title('Spectral Identity: Azygetic Graph $\\cong$ T(8)\nAll 28 eigenvalues match exactly',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10, loc='center right')
ax.grid(True, alpha=0.2)

fig.tight_layout()
fig.savefig(os.path.join(outdir, 'fig6_spectral_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved fig6_spectral_comparison.png")

print("\nAll 6 figures generated successfully.")
