"""
KAM Theory — Harmonic Accumulation at Criticality

Numerical computations and terminal visualization for the core mathematical
structures connecting KAM theory, harmonic series, and dynamical criticality.

The central result: at the critical Diophantine exponent τ_c = n, the
resonance accumulation sum becomes the harmonic series, the Lyapunov
exponent is zero, and the system lives at the unique boundary between
order and chaos compatible with sustained non-equilibrium dynamics.

    S(τ, n) = Σ_{j=1}^∞ j^{n-1-τ}

    τ < n  →  diverges (chaotic, λ > 0)
    τ = n  →  harmonic series (critical, λ = 0)
    τ > n  →  converges (ordered, λ ≤ 0)
"""

import math

EULER_MASCHERONI = 0.5772156649015329
PHI = (1 + math.sqrt(5)) / 2


# ─────────────────────────────────────────────
# Core computations
# ─────────────────────────────────────────────

def harmonic_partial_sum(K):
    """H_K = Σ_{j=1}^{K} 1/j"""
    return sum(1.0 / j for j in range(1, K + 1))


def resonance_sum(K, tau, n):
    """S_K(τ, n) = Σ_{j=1}^{K} j^{n-1-τ}"""
    exp = n - 1 - tau
    return sum(math.pow(j, exp) for j in range(1, K + 1))


def entropy_production_rate(t, alpha):
    """σ(t) = 1/t^α"""
    if t <= 0:
        return float('inf')
    return math.pow(t, -alpha)


def cumulative_entropy(T, alpha, steps=1000):
    """∫₁ᵀ t^{-α} dt"""
    if alpha == 1.0:
        return math.log(T)
    return (math.pow(T, 1 - alpha) - 1) / (1 - alpha)


def diophantine_quality(omega, K):
    """
    Measure how well ω resists rational approximation.
    Returns min_{1≤|k|≤K} |kω - round(kω)| · |k|^n for n=1.
    Higher values = more irrational = more robust torus.
    """
    worst = float('inf')
    for k in range(1, K + 1):
        residue = abs(k * omega - round(k * omega))
        quality = residue * k
        worst = min(worst, quality)
    return worst


def golden_ratio_convergents(n):
    """
    Return first n convergents p_k/q_k of the golden ratio φ.
    These are ratios of consecutive Fibonacci numbers.
    """
    fibs = [1, 1]
    for _ in range(n):
        fibs.append(fibs[-1] + fibs[-2])
    return [(fibs[i + 1], fibs[i]) for i in range(n)]


def riemann_zero_density(t):
    """Approximate density of ζ zeros near height t: ln(t/(2π)) / (2π)"""
    if t <= 2 * math.pi:
        return 0
    return math.log(t / (2 * math.pi)) / (2 * math.pi)


def prime_density(x):
    """Approximate density of primes near x: 1/ln(x)"""
    if x <= 1:
        return 0
    return 1.0 / math.log(x)


def collatz_lyapunov(n, max_iter=10000):
    """
    Estimate the Lyapunov exponent of the Collatz trajectory starting at n.
    λ = lim (1/K) Σ ln|C'(n_k)|
    Even step: |C'| = 1/2. Odd step (3n+1 then /2): |C'| = 3/2.
    """
    x = n
    total = 0.0
    steps = 0
    for _ in range(max_iter):
        if x == 1:
            break
        if x % 2 == 0:
            total += math.log(0.5)
            x = x // 2
        else:
            total += math.log(1.5)
            x = (3 * x + 1) // 2
        steps += 1
    return total / steps if steps > 0 else 0


# ─────────────────────────────────────────────
# Terminal visualization
# ─────────────────────────────────────────────

def _bar(value, max_val, width=50):
    filled = int((value / max_val) * width) if max_val > 0 else 0
    filled = max(0, min(width, filled))
    return '█' * filled + '░' * (width - filled)


def show_resonance_regimes(n=2, K=100):
    """Display the three regimes of the resonance sum."""
    print(f"\n  KAM Resonance Sum  S_K(τ, n={n})  —  K = {K}")
    print(f"  {'─' * 58}")

    cases = [
        (n - 0.5, "τ < n  (chaotic)   "),
        (n,       "τ = n  (critical)  "),
        (n + 1,   "τ > n  (ordered)   "),
    ]

    values = [(label, resonance_sum(K, tau, n)) for tau, label in cases]
    max_val = max(v for _, v in values)

    for label, val in values:
        bar = _bar(val, max_val, 35)
        print(f"  {label} {bar}  {val:.4f}")

    print(f"\n  At τ = n, the sum is the harmonic series:")
    print(f"  H_{K} = {harmonic_partial_sum(K):.6f}")
    print(f"  ln({K}) + γ = {math.log(K) + EULER_MASCHERONI:.6f}")
    print(f"  gap = {harmonic_partial_sum(K) - math.log(K):.6f}  (γ = {EULER_MASCHERONI:.6f})")


def show_entropy_regimes(T=100):
    """Display the three entropy accumulation regimes."""
    print(f"\n  Cumulative Entropy Production  ∫₁ᵀ t⁻ᵅ dt  —  T = {T}")
    print(f"  {'─' * 58}")

    cases = [
        (0.6, f"α = 0.6  (burns gradient)  "),
        (1.0, f"α = 1.0  (critical)        "),
        (1.5, f"α = 1.5  (motion ceases)   "),
    ]

    values = [(label, cumulative_entropy(T, a)) for a, label in cases]
    max_val = max(v for _, v in values)

    for label, val in values:
        bar = _bar(val, max_val, 30)
        print(f"  {label} {bar}  {val:.4f}")

    print(f"\n  Only α = 1 gives ln(T) = {math.log(T):.4f}")
    print(f"  — diverges (motion persists) but slowly (gradient persists)")


def show_golden_ratio_robustness(K=15):
    """Show why φ is the most robust frequency."""
    print(f"\n  Diophantine Quality  —  Resistance to Rational Approximation")
    print(f"  {'─' * 58}")

    frequencies = [
        (PHI, "φ = (1+√5)/2       "),
        (math.sqrt(2), "√2                  "),
        (math.pi, "π                   "),
        (math.e, "e                   "),
        (math.sqrt(3), "√3                  "),
    ]

    values = [(label, diophantine_quality(omega, 200)) for omega, label in frequencies]
    max_val = max(v for _, v in values)

    for label, val in values:
        bar = _bar(val, max_val, 30)
        print(f"  {label} {bar}  {val:.6f}")

    print(f"\n  φ has the highest quality — worst rational approximation")
    print(f"  → last KAM torus to break under perturbation")

    print(f"\n  Golden ratio convergents (Fibonacci ratios):")
    for p, q in golden_ratio_convergents(10):
        approx = p / q
        err = abs(approx - PHI)
        print(f"    {p:>5}/{q:<5} = {approx:.10f}   error = {err:.2e}")


def show_harmonic_partial_sums(K=50):
    """Display harmonic partial sums vs ln(K) + γ."""
    print(f"\n  Harmonic Partial Sums  H_K = Σ 1/j")
    print(f"  {'─' * 58}")
    print(f"  {'K':>6}  {'H_K':>10}  {'ln(K)+γ':>10}  {'gap':>10}")
    print(f"  {'─' * 6}  {'─' * 10}  {'─' * 10}  {'─' * 10}")

    for k in [1, 2, 5, 10, 20, 50, 100, 500, 1000]:
        if k > K and k > 1000:
            break
        Hk = harmonic_partial_sum(k)
        lnk = math.log(k) + EULER_MASCHERONI
        gap = Hk - lnk
        print(f"  {k:>6}  {Hk:>10.6f}  {lnk:>10.6f}  {gap:>10.6f}")

    print(f"\n  The gap converges to 0 as O(1/2K)")
    print(f"  γ = {EULER_MASCHERONI:.10f} (Euler-Mascheroni)")


def show_dual_densities():
    """Show the dual logarithmic processes: zeros thicken, primes thin."""
    print(f"\n  Dual Logarithmic Processes")
    print(f"  {'─' * 58}")
    print(f"  {'x/t':>8}  {'prime density':>14}  {'zero density':>14}  {'product':>10}")
    print(f"  {'─' * 8}  {'─' * 14}  {'─' * 14}  {'─' * 10}")

    for x in [10, 50, 100, 500, 1000, 5000, 10000]:
        pd = prime_density(x)
        zd = riemann_zero_density(x)
        prod = pd * zd
        print(f"  {x:>8}  {pd:>14.6f}  {zd:>14.6f}  {prod:>10.6f}")

    print(f"\n  Primes thin as 1/ln(x)  ·  Zeros thicken as ln(t)/2π")
    print(f"  Product ≈ 1/2π = {1/(2*math.pi):.6f} (dual processes)")


def show_collatz_criticality(samples=20):
    """Show Collatz trajectories near the critical Lyapunov exponent."""
    print(f"\n  Collatz Lyapunov Exponents")
    print(f"  {'─' * 58}")
    print(f"  Critical frequency: p_c = ln(2)/ln(3) = {math.log(2)/math.log(3):.6f}")
    print(f"  Trajectories with λ < 0 contract → reach 1")
    print()

    import random
    random.seed(42)
    test_nums = sorted(random.sample(range(100, 100000), samples))

    for n in test_nums:
        lam = collatz_lyapunov(n)
        bar_len = int(abs(lam) * 30)
        if lam < 0:
            bar = '◄' + '─' * min(bar_len, 25)
            print(f"  n={n:>6}  λ = {lam:>8.4f}  {bar}")
        else:
            bar = '─' * min(bar_len, 25) + '►'
            print(f"  n={n:>6}  λ = {lam:>8.4f}  {bar}")


def show_all():
    """Display all visualizations."""
    print("=" * 62)
    print("  KAM THEORY — HARMONIC ACCUMULATION AT CRITICALITY")
    print("=" * 62)

    show_resonance_regimes()
    show_entropy_regimes()
    show_harmonic_partial_sums()
    show_golden_ratio_robustness()
    show_dual_densities()
    show_collatz_criticality()

    print(f"\n{'=' * 62}")
    print("  The harmonic rate 1/t is the unique fixed point:")
    print("  motion persists (∫σ diverges) AND gradient persists (σ decays)")
    print("  Realized in KAM theory at τ_c = n, where λ = 0")
    print(f"{'=' * 62}\n")


if __name__ == '__main__':
    show_all()
