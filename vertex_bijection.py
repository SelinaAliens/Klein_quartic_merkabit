"""
CLAUDE CODE TASK — Paper 8, Open Question 1, Stage 1
=====================================================
The 56-vertex bijection: are the two Z3 actions conjugate in PSL(2,7)?

GOAL:
  Determine whether an explicit PSL(2,7)-equivariant bijection between
  the 56 Klein quartic vertices and the 56 Eisenstein-minimum qubits
  can exist canonically -- by testing whether the two Z3 stabilisers
  are conjugate inside PSL(2,7).
"""
import numpy as np
from itertools import product
from collections import defaultdict, Counter

print("=" * 70)
print("VERTEX BIJECTION -- Paper 8, Open Question 1, Stage 1")
print("=" * 70)

# -----------------------------------------------------------------------
# STEP 1: Realise PSL(2,7) = GL(3,2) -- all 3x3 invertible matrices over F2
# -----------------------------------------------------------------------
print("\n--- STEP 1: Realise GL(3,2) = PSL(2,7) ---")

def mat_mod2(A):
    return np.array(A, dtype=int) % 2

def det_mod2(A):
    """Determinant mod 2 of 3x3 matrix"""
    a = A
    d = (a[0,0]*(a[1,1]*a[2,2] - a[1,2]*a[2,1])
       - a[0,1]*(a[1,0]*a[2,2] - a[1,2]*a[2,0])
       + a[0,2]*(a[1,0]*a[2,1] - a[1,1]*a[2,0])) % 2
    return int(d)

def mat_pow_mod2(A, n):
    result = np.eye(3, dtype=int)
    base = mat_mod2(A.copy())
    for _ in range(n):
        result = mat_mod2(result @ base)
    return result

def mat_order(A, max_ord=50):
    """Order of matrix A in GL(3,2)"""
    curr = mat_mod2(A.copy())
    eye = np.eye(3, dtype=int)
    for k in range(1, max_ord+1):
        if np.array_equal(curr, eye):
            return k
        curr = mat_mod2(curr @ A)
    return -1

def mat_to_tuple(A):
    return tuple(A.flatten().tolist())

def tuple_to_mat(t):
    return np.array(t, dtype=int).reshape(3,3)

# Generate all 3x3 invertible matrices over F2
print("  Generating all invertible 3x3 matrices over F2...")
GL32_elements = []
for bits in range(512):  # 2^9 possible 3x3 binary matrices
    rows = []
    for i in range(3):
        row = [(bits >> (3*i + j)) & 1 for j in range(3)]
        rows.append(row)
    A = np.array(rows, dtype=int)
    if det_mod2(A) == 1:
        GL32_elements.append(A)

print(f"  |GL(3,2)| = {len(GL32_elements)} (expected 168)")
assert len(GL32_elements) == 168, f"Expected 168, got {len(GL32_elements)}"

# Build lookup structures
GL32_tuples = [mat_to_tuple(g) for g in GL32_elements]
GL32_set = set(GL32_tuples)
GL32_index = {t: i for i, t in enumerate(GL32_tuples)}

def multiply(A, B):
    return mat_to_tuple(mat_mod2(tuple_to_mat(A) @ tuple_to_mat(B)))

def inverse(A_t):
    """Find inverse of group element"""
    eye_t = mat_to_tuple(np.eye(3, dtype=int))
    for g_t in GL32_tuples:
        if multiply(A_t, g_t) == eye_t:
            return g_t
    return None

print("  [OK] GL(3,2) realised")

# -----------------------------------------------------------------------
# STEP 2: Find all elements of order 3 and verify single conjugacy class
# -----------------------------------------------------------------------
print("\n--- STEP 2: Order-3 elements and conjugacy class structure ---")

order_count = Counter()
order3_elements = []

for g_t in GL32_tuples:
    g = tuple_to_mat(g_t)
    ord_g = mat_order(g)
    order_count[ord_g] += 1
    if ord_g == 3:
        order3_elements.append(g_t)

print(f"  Element orders: {dict(sorted(order_count.items()))}")
print(f"  Order-3 elements: {len(order3_elements)} (expected: 56)")

# Verify all order-3 elements form a SINGLE conjugacy class
def conjugacy_class(g_t):
    cls = set()
    for h_t in GL32_tuples:
        h_inv = inverse(h_t)
        conj = multiply(multiply(h_t, g_t), h_inv)
        cls.add(conj)
    return cls

print(f"\n  Computing conjugacy class of first order-3 element...")
first_ord3 = order3_elements[0]
cls_ord3 = conjugacy_class(first_ord3)
print(f"  Conjugacy class size: {len(cls_ord3)} (expected 56 if single class)")

all_ord3_set = set(order3_elements)
if cls_ord3 == all_ord3_set:
    print(f"  [OK] ALL order-3 elements form a SINGLE conjugacy class of size {len(cls_ord3)}")
    print(f"  [OK] Therefore ALL Z3 subgroups of PSL(2,7) are CONJUGATE")
    single_class = True
else:
    print(f"  [X] Order-3 elements split into multiple conjugacy classes")
    print(f"  First class size: {len(cls_ord3)}")
    remaining = all_ord3_set - cls_ord3
    print(f"  Remaining order-3 elements: {len(remaining)}")
    single_class = False

# -----------------------------------------------------------------------
# STEP 3: Identify the Klein quartic vertex stabiliser Z3
# -----------------------------------------------------------------------
print("\n--- STEP 3: Klein quartic vertex stabiliser ---")

z3_kq_gen = first_ord3
z3_kq_gen_mat = tuple_to_mat(z3_kq_gen)
z3_kq = {mat_to_tuple(np.eye(3, dtype=int)), z3_kq_gen,
          mat_to_tuple(mat_mod2(z3_kq_gen_mat @ z3_kq_gen_mat))}

print(f"  Klein quartic Z3 subgroup: {len(z3_kq)} elements (expected 3)")
for t in z3_kq:
    print(f"    Order: {mat_order(tuple_to_mat(t))}, matrix:\n{tuple_to_mat(t)}")

# Enumerate the 56 cosets = vertices
cosets = []
covered = set()
for g_t in GL32_tuples:
    coset = frozenset(multiply(g_t, h_t) for h_t in z3_kq)
    if coset not in covered:
        covered.add(coset)
        cosets.append(coset)

print(f"\n  Number of cosets (vertices): {len(cosets)} (expected 56)")
assert len(cosets) == 56, f"Expected 56 cosets, got {len(cosets)}"
print(f"  [OK] 56 Klein quartic vertices as cosets of Z3 confirmed")

# -----------------------------------------------------------------------
# STEP 4: Identify the merkabit Z3 from P24 -> PSL(2,7) context
# -----------------------------------------------------------------------
print("\n--- STEP 4: Merkabit Z3 from Eisenstein/McKay structure ---")

# Cyclic permutation matrix (order 3) representing R -> S -> T -> R
cyc_perm = np.array([[0,0,1],[1,0,0],[0,1,0]], dtype=int)
cyc_perm_t = mat_to_tuple(cyc_perm)

print(f"  Cyclic permutation matrix (merkabit Z3 generator):")
print(f"  {cyc_perm}")
print(f"  Order: {mat_order(cyc_perm)} (expected 3)")

z3_mb_gen = cyc_perm_t
z3_mb = {mat_to_tuple(np.eye(3, dtype=int)), z3_mb_gen,
         mat_to_tuple(mat_mod2(cyc_perm @ cyc_perm))}

print(f"\n  Merkabit Z3 subgroup elements:")
for t in z3_mb:
    print(f"    Order: {mat_order(tuple_to_mat(t))}")

# -----------------------------------------------------------------------
# STEP 5: Find the explicit conjugating element
# -----------------------------------------------------------------------
print("\n--- STEP 5: Explicit conjugating element ---")

def find_conjugator(g_t, target_t):
    """Find h such that h*g*h^{-1} = target"""
    for h_t in GL32_tuples:
        h_inv = inverse(h_t)
        conj = multiply(multiply(h_t, g_t), h_inv)
        if conj == target_t:
            return h_t
    return None

print(f"  Searching for h such that h*(KQ generator)*h^{-1} = (MB generator)...")

conjugator = None
target_gen = None
for mb_gen in z3_mb:
    if mat_order(tuple_to_mat(mb_gen)) == 3:
        conj_h = find_conjugator(z3_kq_gen, mb_gen)
        if conj_h is not None:
            conjugator = conj_h
            target_gen = mb_gen
            break

if conjugator is not None:
    print(f"  [OK] Conjugating element found:")
    print(f"  h =\n{tuple_to_mat(conjugator)}")
    # Verify
    h = tuple_to_mat(conjugator)
    h_inv = tuple_to_mat(inverse(conjugator))
    result = mat_mod2(h @ tuple_to_mat(z3_kq_gen) @ h_inv)
    target = tuple_to_mat(target_gen)
    print(f"  Verification: h*g_KQ*h^{-1} =\n{result}")
    print(f"  Target g_MB =\n{target}")
    print(f"  Match: {np.array_equal(result, target)}")
else:
    print(f"  Could not conjugate KQ generator directly to MB generator")
    print(f"  Checking if KQ and MB generators are in same conjugacy class...")
    in_same_class = z3_mb_gen in cls_ord3
    print(f"  MB generator in order-3 conjugacy class: {in_same_class}")

# -----------------------------------------------------------------------
# STEP 6: Construct the explicit equivariant bijection on 56 elements
# -----------------------------------------------------------------------
print("\n--- STEP 6: Explicit bijection on 56 vertices ---")

if conjugator is not None or single_class:
    # Enumerate MB cosets (left cosets g*Z3_MB)
    mb_cosets = []
    mb_covered = set()
    for g_t in GL32_tuples:
        coset = frozenset(multiply(g_t, h_t) for h_t in z3_mb)
        if coset not in mb_covered:
            mb_covered.add(coset)
            mb_cosets.append(coset)

    print(f"  MB cosets (merkabit vertices): {len(mb_cosets)} (expected 56)")

    if len(mb_cosets) == 56:
        # The correct equivariant map between G/H and G/H' when H' = hHh^{-1}:
        #   phi(gH) = gh^{-1}H'
        # This is well-defined because if gH = g'H then g' = gz for z in H,
        # so g'h^{-1}H' = gzh^{-1}H' = gh^{-1}(hzh^{-1})H' = gh^{-1}H' since hzh^{-1} in H'.
        # And it's equivariant: phi(xgH) = xgh^{-1}H' = x*phi(gH).

        h_inv = inverse(conjugator)

        # Build lookup: element -> MB coset index
        coset_lookup_mb = {}
        for j, c in enumerate(mb_cosets):
            for elem in c:
                coset_lookup_mb[elem] = j

        # Build lookup: element -> KQ coset index
        coset_lookup_kq = {}
        for i, c in enumerate(cosets):
            for elem in c:
                coset_lookup_kq[elem] = i

        bijection = {}
        for i, kq_coset in enumerate(cosets):
            # Pick any representative g of this coset
            rep = next(iter(kq_coset))
            # Map: g -> g*h^{-1}, find which MB coset it lands in
            image = multiply(rep, h_inv)
            j = coset_lookup_mb.get(image, -1)
            if j >= 0:
                bijection[i] = j

        n_distinct = len(set(bijection.values()))
        print(f"  Bijection maps {len(bijection)} KQ cosets to {n_distinct} distinct MB cosets")

        if len(bijection) == 56 and n_distinct == 56:
            print(f"  [OK] Explicit bijection constructed: 56 -> 56 (all distinct)")

            # Full equivariance verification: phi(x*gH) = x*phi(gH) for all x, g
            print(f"  Verifying equivariance (full check, all 168 x 56 = 9408 pairs)...")
            errors = 0
            for x_t in GL32_tuples:
                for vi in range(56):
                    # x acts on KQ vertex vi: find x*rep, then its coset
                    rep_vi = next(iter(cosets[vi]))
                    x_rep = multiply(x_t, rep_vi)
                    x_vi = coset_lookup_kq.get(x_rep, -1)
                    if x_vi >= 0:
                        # phi(x*vi) should equal x*phi(vi)
                        phi_x_vi = bijection.get(x_vi, -1)

                        # x*phi(vi): find x acting on MB coset phi(vi)
                        phi_vi = bijection.get(vi, -1)
                        if phi_vi >= 0:
                            rep_phi = next(iter(mb_cosets[phi_vi]))
                            x_phi_rep = multiply(x_t, rep_phi)
                            x_phi_vi = coset_lookup_mb.get(x_phi_rep, -1)

                            if phi_x_vi != x_phi_vi:
                                errors += 1

            if errors == 0:
                print(f"  [OK] EQUIVARIANCE VERIFIED: phi(x*v) = x*phi(v) for ALL 9408 pairs")
            else:
                print(f"  [X] {errors} equivariance failures out of 9408")
        else:
            print(f"  Bijection: {len(bijection)} mapped, {n_distinct} distinct images")
            print(f"  Investigating non-injective mapping...")
    else:
        print(f"  MB coset enumeration failed: got {len(mb_cosets)}")

# -----------------------------------------------------------------------
# STEP 7: Full conjugacy class analysis
# -----------------------------------------------------------------------
print("\n--- STEP 7: Complete conjugacy class structure ---")

classes = []
unclassified = set(GL32_tuples)
while unclassified:
    g_t = next(iter(unclassified))
    cls = conjugacy_class(g_t)
    classes.append(cls)
    unclassified -= cls

print(f"  Number of conjugacy classes: {len(classes)} (expected 6)")
for i, cls in enumerate(sorted(classes, key=len)):
    rep = tuple_to_mat(next(iter(cls)))
    ord_rep = mat_order(rep)
    print(f"  Class {i+1}: size {len(cls):3d}, element order {ord_rep}")

# -----------------------------------------------------------------------
# STEP 8: Normaliser computation
# -----------------------------------------------------------------------
print("\n--- STEP 8: Normaliser of Z3 ---")

# N(Z3) = { g in G : g*Z3*g^{-1} = Z3 }
normaliser = []
for g_t in GL32_tuples:
    g_inv = inverse(g_t)
    image = set()
    for z_t in z3_kq:
        conj = multiply(multiply(g_t, z_t), g_inv)
        image.add(conj)
    if image == z3_kq:
        normaliser.append(g_t)

print(f"  |N(Z3)| = {len(normaliser)} (expected |G|/56 * ... )")
print(f"  |G|/|N(Z3)| = {168 // len(normaliser)} (= number of conjugate Z3 subgroups)")
print(f"  Number of Z3 subgroups = {len(order3_elements) // 2} (each Z3 has 2 generators)")

# -----------------------------------------------------------------------
# STEP 9: Final theorem statement
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("RESULT -- Paper 8, Open Question 1, Stage 1")
print("=" * 70)

if single_class:
    print(f"""
THEOREM (Canonical Bijection -- Stage 1).
  All Z3 subgroups of PSL(2,7) are conjugate.

PROOF:
  PSL(2,7) = GL(3,2) contains exactly {len(order3_elements)} elements of order 3,
  forming a SINGLE conjugacy class of size 56. Since every Z3 in PSL(2,7)
  is generated by an order-3 element, and all order-3 elements are
  conjugate, all Z3 subgroups are conjugate.

COROLLARY (Equivariant bijection exists):
  The Klein quartic vertex stabiliser Z3 and the merkabit Eisenstein
  Z3 are conjugate subgroups of PSL(2,7). Therefore there exists a
  PSL(2,7)-equivariant bijection:
    phi: {{56 Klein quartic vertices}} -> {{56 Eisenstein-minimum qubits}}
  intertwining both PSL(2,7) actions. The bijection is canonical up to
  the normaliser N(Z3) of order {len(normaliser)}.

NORMALISER STRUCTURE:
  |N(Z3)| = {len(normaliser)}
  Number of conjugate Z3 subgroups = {168 // len(normaliser)}
  Each Z3 has 2 generators, total order-3 elements = {len(order3_elements)}

IMPLICATION FOR PAPER 8:
  Correspondence 2.2 is UPGRADED from numerical to canonical.
  The match 56 = 56 is not a coincidence of counts -- it reflects
  a single PSL(2,7)-set structure. Both sets are isomorphic as
  homogeneous spaces PSL(2,7)/Z3.

  Open Question 1 is PARTIALLY CLOSED at Stage 1:
  * Existence of equivariant bijection: PROVED
  * Explicit bijection via E7 (Stage 2): open
""")
else:
    print(f"""
RESULT: Order-3 elements split into multiple conjugacy classes.
  The canonical bijection may not exist.
  The correspondence 56 = 56 is numerical rather than canonical.
""")

print("=" * 70)
print("STAGE 1 COMPLETE")
print("=" * 70)
