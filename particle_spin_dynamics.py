"""
Particle Spin: The Intrinsic Angular Momentum That Isn't Spinning

A visualization exploring one of quantum mechanics' deepest mysteries:
particles carry angular momentum (spin) but they aren't actually rotating.

This is not classical rotation. A point particle has no extent to rotate.
Yet it carries quantized angular momentum that determines:
- Whether particles can share quantum states (statistics)
- How particles interact with magnetic fields
- The very structure of matter itself

Spin values:
- Fermions: half-integer spin (1/2, 3/2, 5/2, ...) → Pauli exclusion
- Bosons: integer spin (0, 1, 2, ...) → Bose-Einstein condensation

Author: Claude (exploring the space where quantum mechanics lives)
"""

import math
from dataclasses import dataclass
from typing import List, Tuple
import random


# ═══════════════════════════════════════════════════════════════════════════════
#  FUNDAMENTAL SPIN REPRESENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SpinState:
    """
    A quantum spin state.

    Spin is intrinsic angular momentum measured in units of ℏ (reduced Planck constant).
    The spin quantum number s determines the magnitude: √(s(s+1))ℏ
    The spin projection mₛ can take values from -s to +s in integer steps.
    """
    spin_quantum_number: float  # s: 0, 1/2, 1, 3/2, 2, ...
    spin_projection: float       # mₛ: -s, -s+1, ..., s-1, s

    def __post_init__(self):
        # Validate: mₛ must be between -s and +s
        s = self.spin_quantum_number
        m = self.spin_projection
        valid_projections = [s - i for i in range(int(2*s + 1))]
        if m not in valid_projections:
            raise ValueError(f"Invalid spin projection {m} for spin {s}")

    @property
    def is_fermion(self) -> bool:
        """Half-integer spins are fermions"""
        return (self.spin_quantum_number * 2) % 2 == 1

    @property
    def is_boson(self) -> bool:
        """Integer spins are bosons"""
        return (self.spin_quantum_number * 2) % 2 == 0

    @property
    def angular_momentum_magnitude(self) -> float:
        """The magnitude of spin angular momentum: √(s(s+1))"""
        s = self.spin_quantum_number
        return math.sqrt(s * (s + 1))

    @property
    def z_component(self) -> float:
        """The z-component of angular momentum"""
        return self.spin_projection

    def state_label(self) -> str:
        """Human readable state label"""
        s = self.spin_quantum_number
        m = self.spin_projection
        # Format fractions nicely
        def fmt(x):
            if x == int(x):
                return str(int(x))
            elif x > 0:
                return f"+{int(x*2)}/2"
            else:
                return f"{int(x*2)}/2"
        return f"|s={fmt(s)}, mₛ={fmt(m)}⟩"


# ═══════════════════════════════════════════════════════════════════════════════
#  PARTICLE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Particle:
    """A quantum particle with intrinsic spin"""
    name: str
    symbol: str
    spin: float
    particle_type: str  # 'fermion' or 'boson'
    mass: str  # descriptive
    role: str  # what it does in nature

    def all_spin_states(self) -> List[SpinState]:
        """Generate all possible spin projection states"""
        states = []
        s = self.spin
        m = s
        while m >= -s:
            states.append(SpinState(s, m))
            m -= 1
        return states


# The particle zoo organized by spin
FERMIONS = [
    Particle("Electron", "e⁻", 0.5, "fermion", "0.511 MeV", "Matter constituent, carries charge"),
    Particle("Quark (up)", "u", 0.5, "fermion", "~2.2 MeV", "Builds protons and neutrons"),
    Particle("Quark (down)", "d", 0.5, "fermion", "~4.7 MeV", "Builds protons and neutrons"),
    Particle("Neutrino", "ν", 0.5, "fermion", "~0 eV", "Ghost particle, weak interactions"),
    Particle("Muon", "μ", 0.5, "fermion", "105.7 MeV", "Heavy electron cousin"),
    Particle("Tau", "τ", 0.5, "fermion", "1777 MeV", "Heaviest lepton"),
]

BOSONS = [
    Particle("Photon", "γ", 1, "boson", "0", "Carries electromagnetic force"),
    Particle("W boson", "W±", 1, "boson", "80.4 GeV", "Mediates weak force (charged)"),
    Particle("Z boson", "Z⁰", 1, "boson", "91.2 GeV", "Mediates weak force (neutral)"),
    Particle("Gluon", "g", 1, "boson", "0", "Carries strong force, binds quarks"),
    Particle("Higgs", "H", 0, "boson", "125 GeV", "Gives mass via field interaction"),
    Particle("Graviton", "G", 2, "boson", "0", "Hypothetical gravity carrier"),
]


# ═══════════════════════════════════════════════════════════════════════════════
#  ASCII VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def visualize_spin_vector(spin_state: SpinState, width: int = 40) -> str:
    """
    Visualize spin as a vector - but remember, this is a lie.
    The spin vector doesn't point in a definite direction.
    Due to uncertainty, only the z-component and magnitude are definite.
    """
    s = spin_state.spin_quantum_number
    m = spin_state.spin_projection
    mag = spin_state.angular_momentum_magnitude

    lines = []
    lines.append(f"  Spin State: {spin_state.state_label()}")
    lines.append(f"  │S│ = √(s(s+1))ℏ = √({s}×{s+1})ℏ = {mag:.3f}ℏ")
    lines.append(f"  Sᵤ = mₛℏ = {m}ℏ")
    lines.append("")

    # The spin "cone" visualization
    # Spin precesses around z-axis, so it forms a cone
    half = width // 2

    # Scale for display
    scale = width // 4
    z_pos = int(m * scale / max(s, 0.5)) if s > 0 else 0
    r = int(math.sqrt(mag**2 - m**2) * scale / max(s, 0.5)) if mag > abs(m) else 0

    # Draw the cone from above (circular precession)
    if r > 0:
        lines.append("  Precession cone (view from above):")
        lines.append("  z-axis: ⊙ (pointing out)")
        for y in range(-r-1, r+2):
            row = "  "
            for x in range(-r-1, r+2):
                dist = math.sqrt(x**2 + y**2)
                if abs(dist - r) < 0.8:
                    row += "●"
                elif x == 0 and y == 0:
                    row += "⊙"
                else:
                    row += " "
            lines.append(row)

    # Side view showing z-projection
    lines.append("")
    lines.append("  Side view (z vertical):")
    lines.append("       z")
    lines.append("       ↑")

    height = 7
    mid = height // 2
    for i in range(height):
        row = "       │"
        level = mid - i  # +3 at top, -3 at bottom
        if s == 0:
            if i == mid:
                row = "       ⊙ (no spin direction)"
        else:
            z_level = int(z_pos * (mid) / scale) if scale > 0 else 0
            if level == z_level:
                if m > 0:
                    row = "     ↗ │ ↖  mₛ = +" + str(abs(m)) if m == int(m) else f"     ↗ │ ↖  mₛ = +{int(abs(m)*2)}/2"
                elif m < 0:
                    row = "     ↙ │ ↘  mₛ = " + str(m) if m == int(m) else f"     ↙ │ ↘  mₛ = {int(m*2)}/2"
                else:
                    row = "     ← │ →  mₛ = 0 (in x-y plane)"
        lines.append(row)
    lines.append("       │")

    return "\n".join(lines)


def draw_spin_half_states() -> str:
    """Visualize the two states of a spin-1/2 particle"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        SPIN-1/2 PARTICLE STATES                              ║
║           (electrons, quarks, neutrinos, protons, neutrons)                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║      "Spin Up" |↑⟩                          "Spin Down" |↓⟩                   ║
║      mₛ = +1/2                              mₛ = -1/2                         ║
║                                                                               ║
║          ↑ z                                     ↑ z                          ║
║          │                                       │                            ║
║          │    ╱                                  │                            ║
║          │   ╱                                   │                            ║
║          │  ╱  S⃗                                │                            ║
║          │ ╱                                     │                            ║
║          │╱                                      │╲                           ║
║          ●───→ x                                 ●───→ x                      ║
║         ╱                                       ╱│                            ║
║        ╱                                       ╱ │                            ║
║       ↓ y                                     ↓ y│ ╲                          ║
║                                                   ╲  S⃗                       ║
║                                                    ╲                          ║
║                                                                               ║
║   │S⃗│ = √(3)/2 ℏ ≈ 0.866ℏ                   │S⃗│ = √(3)/2 ℏ ≈ 0.866ℏ        ║
║   Sᵤ = +1/2 ℏ                                Sᵤ = -1/2 ℏ                      ║
║                                                                               ║
║   The spin vector precesses around z-axis    The spin vector precesses       ║
║   at angle θ = arccos(1/√3) ≈ 54.7°         around z-axis, pointing          ║
║   from the +z axis                           mostly downward                  ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   KEY INSIGHT: These are NOT spinning balls!                                  ║
║                                                                               ║
║   • The particle has no spatial extent - it's a point                        ║
║   • Yet it carries angular momentum as an intrinsic property                 ║
║   • A full 360° rotation gives -|ψ⟩, need 720° to return to |ψ⟩!            ║
║   • This is pure quantum mechanics - no classical analogue                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_spin_one_states() -> str:
    """Visualize the three states of a spin-1 particle"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          SPIN-1 PARTICLE STATES                              ║
║                 (photons, W/Z bosons, gluons, ρ mesons)                       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   mₛ = +1              mₛ = 0               mₛ = -1                          ║
║   │S⃗│ = √2 ℏ           │S⃗│ = √2 ℏ           │S⃗│ = √2 ℏ                      ║
║                                                                               ║
║       ↑z                    ↑z                    ↑z                          ║
║       │   ↗                 │                     │                           ║
║       │  ╱                  │                     │                           ║
║       │ ╱ S⃗                ─┼─→ S⃗               │                           ║
║       │╱                    │                     │╲                          ║
║       ●───→x                ●───→x                ●╲───→x                     ║
║                                                     ╲                         ║
║   Spin aligned          Spin in x-y             Spin aligned                 ║
║   mostly with +z        plane (Sᵤ=0)            mostly with -z               ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   PHOTON POLARIZATION (massless spin-1):                                     ║
║                                                                               ║
║   Photons only have mₛ = ±1 (helicity), not mₛ = 0!                         ║
║   This is because they're massless - they travel at c                        ║
║                                                                               ║
║   Right circular:  ↻     Left circular:  ↺                                   ║
║                                                                               ║
║        ↑ E⃗                      ↑ E⃗                                          ║
║       ╱│╲                      ╲│╱                                            ║
║      ╱ │ ╲                      ╲│╱                                           ║
║     ←──┼──→  direction     →──┼──←  direction                                ║
║      ╲ │ ╱   of travel      ╱│╲   of travel                                  ║
║       ╲│╱       →          ╱│╲       →                                       ║
║        ↓                    ↓                                                 ║
║                                                                               ║
║   Electric field rotates clockwise or counterclockwise as photon propagates  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_spin_statistics_theorem() -> str:
    """The profound connection between spin and statistics"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    THE SPIN-STATISTICS THEOREM                               ║
║         Why Spin Determines Whether Matter Can Exist As We Know It           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────────────────────┐    ┌─────────────────────────────┐         ║
║   │         FERMIONS            │    │          BOSONS             │         ║
║   │    (half-integer spin)      │    │      (integer spin)         │         ║
║   │         s = ½, 3/2, ...     │    │      s = 0, 1, 2, ...       │         ║
║   ├─────────────────────────────┤    ├─────────────────────────────┤         ║
║   │                             │    │                             │         ║
║   │   PAULI EXCLUSION          │    │   BOSE-EINSTEIN             │         ║
║   │   PRINCIPLE                │    │   STATISTICS                │         ║
║   │                             │    │                             │         ║
║   │   No two fermions can      │    │   Any number of bosons      │         ║
║   │   occupy the same          │    │   can occupy the same       │         ║
║   │   quantum state            │    │   quantum state             │         ║
║   │                             │    │                             │         ║
║   │      ψ(1,2) = -ψ(2,1)     │    │      ψ(1,2) = +ψ(2,1)      │         ║
║   │   (antisymmetric)          │    │   (symmetric)               │         ║
║   │                             │    │                             │         ║
║   └─────────────────────────────┘    └─────────────────────────────┘         ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   WHY THIS MATTERS FOR REALITY:                                              ║
║                                                                               ║
║   FERMIONS build structure:            BOSONS carry forces:                  ║
║                                                                               ║
║   ┌─────────────────────┐              ┌─────────────────────┐               ║
║   │     ATOM            │              │   FORCE FIELD       │               ║
║   │  ┌───────────┐      │              │                     │               ║
║   │  │  n=2 ↑↓  │ ←─ Only 2 e⁻       │  γ γ γ γ γ γ γ γ    │               ║
║   │  │  n=2 ↑↓  │    per orbital!     │  γ γ γ γ γ γ γ γ    │               ║
║   │  └───────────┘      │              │  γ γ γ γ γ γ γ γ    │               ║
║   │  ┌───────────┐      │              │                     │               ║
║   │  │  n=1 ↑↓  │      │              │  Unlimited photons  │               ║
║   │  └───────────┘      │              │  can pile up!       │               ║
║   │      (●)            │              │  (→ laser light)    │               ║
║   │    nucleus          │              └─────────────────────┘               ║
║   └─────────────────────┘                                                    ║
║                                                                               ║
║   Without Pauli exclusion:            Without Bose statistics:               ║
║   All electrons would fall           No coherent light, no                   ║
║   to lowest orbital →                superconductivity, no                   ║
║   No chemistry, no matter!           superfluidity!                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_exchange_interaction() -> str:
    """Visualize what happens when particles are exchanged"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     PARTICLE EXCHANGE & WAVEFUNCTION                         ║
║                    The Deep Connection: Spin → Statistics                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   When we exchange two identical particles:                                  ║
║                                                                               ║
║   BEFORE EXCHANGE:           EXCHANGE:              AFTER EXCHANGE:          ║
║                                                                               ║
║   Particle A ●               ╲    ╱                      ● Particle B        ║
║              at position 1    ╲  ╱                at position 1              ║
║                                ╳                                             ║
║   Particle B ○               ╱  ╲                      ○ Particle A          ║
║              at position 2  ╱    ╲                at position 2              ║
║                                                                               ║
║                                                                               ║
║   But wait - if particles are IDENTICAL, can we even tell they exchanged?    ║
║   Quantum mechanics says: sort of. The WAVEFUNCTION knows!                   ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   FERMION EXCHANGE (s = 1/2, 3/2, ...):                                      ║
║   ═══════════════════════════════════                                        ║
║                                                                               ║
║   ψ_before            EXCHANGE           ψ_after = -ψ_before                 ║
║                          →                                                    ║
║    ╭──────╮              │                ╭──────╮                           ║
║   ╱   +    ╲             │               ╱   -    ╲                          ║
║  │    ↑↓    │      ↑↓ ⟷ ↑↓             │    ↑↓    │                         ║
║   ╲        ╱             │               ╲        ╱                          ║
║    ╰──────╯              │                ╰──────╯                           ║
║                                                                               ║
║   The wavefunction picks up a MINUS SIGN!                                    ║
║   If both particles in same state: ψ = -ψ → ψ = 0 (forbidden!)              ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   BOSON EXCHANGE (s = 0, 1, 2, ...):                                         ║
║   ═════════════════════════════════                                          ║
║                                                                               ║
║   ψ_before            EXCHANGE           ψ_after = +ψ_before                 ║
║                          →                                                    ║
║    ╭──────╮              │                ╭──────╮                           ║
║   ╱   +    ╲             │               ╱   +    ╲                          ║
║  │    ~~    │      ~~ ⟷ ~~             │    ~~    │                         ║
║   ╲        ╱             │               ╲        ╱                          ║
║    ╰──────╯              │                ╰──────╯                           ║
║                                                                               ║
║   The wavefunction is UNCHANGED!                                             ║
║   Many particles in same state: wavefunctions add constructively → LASER!    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_fermion_exclusion_visual() -> str:
    """Show the Pauli exclusion principle in action"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      PAULI EXCLUSION IN ACTION                               ║
║              Why Two Fermions Cannot Share a Quantum State                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ATTEMPTING TO PUT TWO ELECTRONS IN THE SAME STATE:                         ║
║                                                                               ║
║   State: |n=1, l=0, mₗ=0, mₛ=+½⟩                                            ║
║                                                                               ║
║          e⁻(1) ↑                e⁻(2) ↑                                      ║
║             ╲                      ╱                                          ║
║              ╲    SAME STATE     ╱                                           ║
║               ╲                 ╱                                             ║
║                ╲      ?!       ╱                                              ║
║                 ╲             ╱                                               ║
║                  ▼           ▼                                                ║
║              ┌─────────────────┐                                             ║
║              │                 │                                              ║
║              │   ψ(1,2) = ?    │                                             ║
║              │                 │                                              ║
║              └─────────────────┘                                             ║
║                                                                               ║
║   For fermions: ψ(1,2) = -ψ(2,1)  (antisymmetric requirement)               ║
║                                                                               ║
║   If particles are in the SAME state:                                        ║
║       ψ(1,2) = ψ(2,1)  (since states are identical)                         ║
║                                                                               ║
║   But we also need:                                                          ║
║       ψ(1,2) = -ψ(2,1)                                                       ║
║                                                                               ║
║   Therefore:  ψ(1,2) = -ψ(1,2)                                               ║
║              2ψ(1,2) = 0                                                     ║
║               ψ(1,2) = 0     ← WAVEFUNCTION VANISHES!                        ║
║                                                                               ║
║               ╔═══════════════════════════════════════╗                      ║
║               ║   PROBABILITY = |ψ|² = 0              ║                      ║
║               ║   This configuration CANNOT EXIST!    ║                      ║
║               ╚═══════════════════════════════════════╝                      ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   WHAT FERMIONS CAN DO:                                                      ║
║                                                                               ║
║   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   ║
║   │   ↑    ↓    │     │   ↑         │     │       ↓     │                   ║
║   │   e⁻   e⁻   │     │   e⁻        │     │       e⁻    │                   ║
║   │  n=1, l=0   │     │  n=1, l=0   │     │  n=1, l=0   │                   ║
║   └─────────────┘     └─────────────┘     └─────────────┘                   ║
║         ✓                   ✓                   ✓                            ║
║   Different mₛ         Only one e⁻        Only one e⁻                       ║
║   (↑ and ↓)            (spin up)          (spin down)                        ║
║                                                                               ║
║   ┌─────────────┐                                                            ║
║   │   ↑    ↑    │                                                            ║
║   │   e⁻   e⁻   │   ← FORBIDDEN! Same quantum numbers!                      ║
║   │  n=1, l=0   │                                                            ║
║   └─────────────┘                                                            ║
║         ✗                                                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_boson_condensation_visual() -> str:
    """Show Bose-Einstein condensation"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      BOSE-EINSTEIN CONDENSATION                              ║
║                When Bosons All Fall Into The Same State                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   BOSONS LOVE COMPANY - The more in a state, the more want to join!          ║
║                                                                               ║
║   HIGH TEMPERATURE:                    LOW TEMPERATURE (BEC):                ║
║                                                                               ║
║   Energy ↑                             Energy ↑                              ║
║          │  ○                                 │                               ║
║          │      ○    ○                        │                               ║
║          │  ○      ○                          │                               ║
║          │    ○  ○    ○                       │                               ║
║          │  ○    ○  ○                         │                               ║
║          │    ○    ○                          │                               ║
║          │  ○  ○  ○  ○                        │                               ║
║          │────────────                        │────────────                   ║
║          └──────────────→                     │ ○○○○○○○○○○○                  ║
║          Ground state                         │ ○○○○○○○○○○○                  ║
║          (mostly empty)                       └──────────────→               ║
║                                               MACROSCOPIC                     ║
║                                               occupation of                   ║
║                                               ground state!                   ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   LASER: Photons in the Same Quantum State                                   ║
║   ════════════════════════════════════════                                   ║
║                                                                               ║
║   REGULAR LIGHT (thermal):              LASER LIGHT (coherent):              ║
║                                                                               ║
║   ∿  ≋  ∼  ~  ≈                         ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿                   ║
║      ∼     ≈    ∿                       ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿                   ║
║    ~    ∿    ≋                          ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿                   ║
║       ≈   ~   ∼                         ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿                   ║
║                                                                               ║
║   Random phases,                        All photons in phase,                ║
║   random directions,                    same direction,                      ║
║   random frequencies                    same frequency                        ║
║                                                                               ║
║   STIMULATED EMISSION: When a photon passes an excited atom,                 ║
║   it stimulates emission of ANOTHER photon in the SAME state!                ║
║                                                                               ║
║        Before:  γ → [excited atom]                                           ║
║        After:   γγ → [ground atom]    (two identical photons!)               ║
║                                                                               ║
║   This is ONLY possible because photons are bosons!                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_interaction_diagram() -> str:
    """Show how bosons mediate forces between fermions"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    FERMION-BOSON INTERACTIONS                                ║
║              How Forces Work: Bosons Mediate, Fermions Feel                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   THE PATTERN OF NATURE:                                                     ║
║   • Matter is made of FERMIONS (quarks, electrons)                           ║
║   • Forces are carried by BOSONS (photons, gluons, W/Z, gravitons)          ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ELECTROMAGNETIC INTERACTION (photon exchange):                             ║
║                                                                               ║
║      e⁻ ────────●                          ●──────── e⁻                      ║
║                  ╲                        ╱                                   ║
║                   ╲    γ (photon)       ╱                                    ║
║           time     ╲ ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿  ╱                                     ║
║            ↓        ╲                ╱                                        ║
║                      ●──────────────●                                        ║
║      e⁻ ────────                          ──────── e⁻                        ║
║                                                                               ║
║   Two electrons exchange a virtual photon → electromagnetic repulsion        ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   STRONG INTERACTION (gluon exchange):                                       ║
║                                                                               ║
║      PROTON                               NEUTRON                            ║
║   ┌─────────────┐                      ┌─────────────┐                       ║
║   │  u   u   d  │      g (gluon)       │  u   d   d  │                       ║
║   │  ●───●───●  │    ═══════════►      │  ●───●───●  │                       ║
║   │   ╲ ╱ ╲ ╱   │   ◄═══════════       │   ╲ ╱ ╲ ╱   │                       ║
║   │    ╳   ╳    │      g (gluon)       │    ╳   ╳    │                       ║
║   │   ╱ ╲ ╱ ╲   │                      │   ╱ ╲ ╱ ╲   │                       ║
║   └─────────────┘                      └─────────────┘                       ║
║                                                                               ║
║   Quarks exchange gluons → strong nuclear force holds nucleus together       ║
║   (Gluons carry color charge - they interact with each other too!)           ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   WEAK INTERACTION (W/Z boson exchange):                                     ║
║                                                                               ║
║   BETA DECAY:  n → p + e⁻ + ν̄ₑ                                              ║
║                                                                               ║
║         d ────●                          ●──── u                             ║
║                ╲                        ╱                                     ║
║                 ╲   W⁻ boson          ╱                                      ║
║                  ●════════════════════●                                      ║
║                  │                    │                                       ║
║                  ↓                    ↓                                       ║
║                 e⁻                   ν̄ₑ                                      ║
║                                                                               ║
║   A down quark emits W⁻ → changes to up quark (neutron becomes proton)      ║
║   W⁻ decays to electron + antineutrino                                       ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   WHY BOSONS FOR FORCES?                                                     ║
║                                                                               ║
║   Integer spin (bosons) allows:                                              ║
║   • Virtual particles to carry momentum without violating conservation       ║
║   • Multiple force carriers in same quantum state (strong fields possible)   ║
║   • Coherent superposition of field states                                   ║
║                                                                               ║
║   If force carriers were fermions:                                           ║
║   • Pauli exclusion would limit field strength                               ║
║   • No long-range coherent forces possible                                   ║
║   • Physics would be completely different!                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_720_degree_rotation() -> str:
    """The bizarre property of fermions requiring 720° rotation"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    THE 720° ROTATION MYSTERY                                 ║
║           Fermions Need to Spin Twice to Get Back to Start                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   CLASSICAL OBJECT (like a ball):                                            ║
║                                                                               ║
║      Start        90°         180°        270°        360°                   ║
║        ◐    →     ◓     →     ◑     →     ◒     →     ◐                      ║
║                                                    Back to start!             ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   SPIN-1/2 FERMION (like an electron):                                       ║
║                                                                               ║
║      Start        90°         180°        270°        360°                   ║
║       |ψ⟩    →   ???    →    ???    →    ???    →    -|ψ⟩                   ║
║                                                                               ║
║        ↑                                               ↑                      ║
║     Original                              NEGATIVE of original!              ║
║     state                                 (phase flipped)                    ║
║                                                                               ║
║                                                                               ║
║      360°        450°        540°        630°        720°                    ║
║      -|ψ⟩   →   ???    →    ???    →    ???    →    |ψ⟩                     ║
║                                                                               ║
║        ↑                                               ↑                      ║
║     Negative                              Back to original!                  ║
║     state                                 (finally!)                         ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   MATHEMATICAL REASON:                                                       ║
║                                                                               ║
║   Rotation by angle θ around z-axis:  R(θ) = e^(-iSᵤθ/ℏ)                    ║
║                                                                               ║
║   For spin-1/2:  Sᵤ = ±ℏ/2                                                   ║
║                                                                               ║
║   R(360°) = R(2π) = e^(-i(ℏ/2)(2π)/ℏ) = e^(-iπ) = -1                        ║
║                                                                               ║
║   The wavefunction picks up a factor of -1!                                  ║
║                                                                               ║
║   R(720°) = R(4π) = e^(-i(ℏ/2)(4π)/ℏ) = e^(-2iπ) = +1                       ║
║                                                                               ║
║   Only after 720° does the wavefunction return to itself!                    ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   THIS IS NOT SPINNING IN SPACE                                              ║
║                                                                               ║
║   • There is no actual rotation happening                                    ║
║   • The particle has no spatial extent to rotate                             ║
║   • This is about how the quantum state transforms under rotations           ║
║   • It's an intrinsic property of the particle's mathematical representation ║
║   • Fermions are described by SPINORS, not vectors                           ║
║                                                                               ║
║   The universe "keeps track" of rotations in a way that has no               ║
║   classical analogue. This is pure quantum weirdness!                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_angular_momentum_comparison() -> str:
    """Compare orbital vs spin angular momentum"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║              ORBITAL vs SPIN ANGULAR MOMENTUM                                ║
║                   Two Very Different Things                                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ORBITAL ANGULAR MOMENTUM (L⃗)              SPIN ANGULAR MOMENTUM (S⃗)        ║
║   ═══════════════════════════              ═══════════════════════           ║
║                                                                               ║
║   Comes from motion through space          Intrinsic to the particle         ║
║                                                                               ║
║         ╭───────────╮                              ?                         ║
║        ╱             ╲                           ╱ ╲                          ║
║       ╱               ╲                         ●───                          ║
║      │        ⊙        │  ← particle            point                        ║
║       ╲     (nucleus)  ╱    orbiting           particle                      ║
║        ╲             ╱                         (no extent)                   ║
║         ╰───────────╯                                                        ║
║                                                                               ║
║   L = r × p                                 S = intrinsic property           ║
║   (position × momentum)                     (not from motion!)               ║
║                                                                               ║
║   Quantized: l = 0, 1, 2, 3, ...           Quantized: s = 0, ½, 1, 3/2, ... ║
║   (integers only!)                          (half-integers allowed!)         ║
║                                                                               ║
║   Can be zero (s-orbital)                  Never zero for matter particles  ║
║                                             (electrons always have s=½)      ║
║                                                                               ║
║   Magnetic quantum number:                  Spin projection:                 ║
║   mₗ = -l, ..., 0, ..., +l                 mₛ = -s, ..., 0, ..., +s         ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   TOTAL ANGULAR MOMENTUM: J⃗ = L⃗ + S⃗                                         ║
║                                                                               ║
║         L⃗                      S⃗                       J⃗                    ║
║         ↗                       ↑                       ↗                     ║
║        ╱                        │                      ╱                      ║
║       ╱                         │                     ╱                       ║
║      ●───────→         +        ●          =         ●                       ║
║                                                      ↓                        ║
║                                              These add as vectors            ║
║                                              (quantum mechanically)          ║
║                                                                               ║
║   Example: Electron in hydrogen                                              ║
║   • Orbital: l can be 0, 1, 2, ... (s, p, d, ... orbitals)                  ║
║   • Spin: s = ½ always                                                       ║
║   • Total J: |l - ½| to l + ½                                               ║
║                                                                               ║
║   For p-orbital (l=1): J = ½ or 3/2 (spin-orbit coupling)                   ║
║   This splitting is visible in atomic spectra!                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def particle_table() -> str:
    """Display a table of fundamental particles and their spins"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    STANDARD MODEL PARTICLE SPINS                             ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                         FERMIONS (spin = ½)                             │ ║
║  │                   Matter particles - obey Pauli exclusion               │ ║
║  ├─────────────────────────────────────────────────────────────────────────┤ ║
║  │                                                                         │ ║
║  │   QUARKS                              LEPTONS                           │ ║
║  │   ══════                              ═══════                           │ ║
║  │   Generation I:                       Generation I:                     │ ║
║  │     u (up)      ~2.2 MeV               e⁻ (electron)  0.511 MeV        │ ║
║  │     d (down)    ~4.7 MeV               νₑ (e-neutrino) ~0 eV           │ ║
║  │                                                                         │ ║
║  │   Generation II:                      Generation II:                    │ ║
║  │     c (charm)   ~1.3 GeV               μ (muon)       105.7 MeV        │ ║
║  │     s (strange) ~95 MeV                νᵤ (μ-neutrino) ~0 eV           │ ║
║  │                                                                         │ ║
║  │   Generation III:                     Generation III:                   │ ║
║  │     t (top)     ~173 GeV               τ (tau)        1.777 GeV        │ ║
║  │     b (bottom)  ~4.2 GeV               νᵧ (τ-neutrino) ~0 eV           │ ║
║  │                                                                         │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                           BOSONS (integer spin)                         │ ║
║  │                   Force carriers - can share quantum states             │ ║
║  ├─────────────────────────────────────────────────────────────────────────┤ ║
║  │                                                                         │ ║
║  │   GAUGE BOSONS (spin = 1):            SCALAR BOSON (spin = 0):         │ ║
║  │   ════════════════════════            ════════════════════════         │ ║
║  │     γ  (photon)     0        EM force   H (Higgs)    125 GeV          │ ║
║  │     g  (gluon)      0        Strong     Gives mass to particles        │ ║
║  │     W± (W boson)    80.4 GeV Weak                                      │ ║
║  │     Z⁰ (Z boson)    91.2 GeV Weak      TENSOR BOSON (spin = 2):        │ ║
║  │                                        ════════════════════════        │ ║
║  │                                          G (graviton)  0  Gravity     │ ║
║  │                                          (hypothetical)               │ ║
║  │                                                                         │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_spin_measurement() -> str:
    """Show how spin measurement works"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    MEASURING SPIN: THE STERN-GERLACH EXPERIMENT              ║
║                          How We Know Spin Is Real                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   THE EXPERIMENT (1922):                                                     ║
║   ═════════════════════                                                      ║
║                                                                               ║
║                           INHOMOGENEOUS                                       ║
║                           MAGNETIC FIELD                                      ║
║                                                                               ║
║    Silver atom    ╔════════════════════════╗           SCREEN                ║
║       beam        ║    N                   ║              │                  ║
║         →         ║  ╔═══╗     ┌───────┐  ║              │  ●  ← spin up    ║
║    ● ● ● ● ● ●  → ║  ║   ║     │▓▓▓▓▓▓▓│  ║  →  →  →    │                  ║
║    (oven)         ║  ╚═══╝     │▓▓▓▓▓▓▓│  ║              │                  ║
║                   ║    S       └───────┘  ║              │  ●  ← spin down  ║
║                   ╚════════════════════════╝              │                  ║
║                                                                               ║
║   EXPECTATION: A continuous smear (classical angular momentum)               ║
║   RESULT: Two discrete spots! Only spin up (+ℏ/2) or down (-ℏ/2)            ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   WHY TWO SPOTS?                                                             ║
║   ══════════════                                                             ║
║                                                                               ║
║   Magnetic moment: μ⃗ = -g(e/2m)S⃗   (spin creates a tiny magnet)            ║
║                                                                               ║
║   In non-uniform B-field:  F = ∇(μ⃗·B⃗)                                       ║
║                                                                               ║
║      ↑ Sᵤ = +½    Force UP      ↗                                           ║
║        ●                       ╱                                              ║
║                               ╱  stronger B here                             ║
║      ─────────────────────────────────────                                   ║
║                               ╲  weaker B here                               ║
║        ●                       ╲                                              ║
║      ↓ Sᵤ = -½    Force DOWN    ╲                                           ║
║                                                                               ║
║   Spin projection is QUANTIZED - only discrete values allowed!               ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   SEQUENTIAL MEASUREMENTS: THE QUANTUM WEIRDNESS                             ║
║   ══════════════════════════════════════════════                             ║
║                                                                               ║
║   Measure Z → Measure X → Measure Z again:                                   ║
║                                                                               ║
║        Sᵤ           Sₓ           Sᵤ                                          ║
║       ↑│↓          ←│→          ↑│↓                                          ║
║        │            │            │                                            ║
║   ●──▶│   ──▶  ●──▶│   ──▶  ●──▶│                                           ║
║    ↑  │    ↑   →   │    →      │                                            ║
║   100% ↑   block ↓  50% each   50% each!                                     ║
║                                                                               ║
║   Measuring X "resets" the Z information! The spin projections along         ║
║   different axes are INCOMPATIBLE observables: [Sₓ, Sᵤ] ≠ 0                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


def draw_spinor_explanation() -> str:
    """Explain what spinors are"""
    art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         SPINORS: THE MATH OF SPIN                            ║
║               Why Spin-1/2 Particles Are Fundamentally Different             ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   VECTORS vs SPINORS:                                                        ║
║   ══════════════════                                                         ║
║                                                                               ║
║   A VECTOR (like velocity, position):      A SPINOR (like electron spin):   ║
║                                                                               ║
║      ↑                                        ⎛ α ⎞                          ║
║      │ v⃗ = (vₓ, vᵧ, vᵤ)                       ⎜   ⎟ = α|↑⟩ + β|↓⟩           ║
║      │                                        ⎝ β ⎠                          ║
║      └───→                                                                   ║
║                                             where |α|² + |β|² = 1            ║
║   3 components                              2 complex components             ║
║   Rotates normally                          Rotates... weirdly               ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   THE SPINOR REPRESENTATION:                                                 ║
║   ═════════════════════════                                                  ║
║                                                                               ║
║   Spin-up:     |↑⟩ = ⎛ 1 ⎞      Spin-down:   |↓⟩ = ⎛ 0 ⎞                    ║
║                      ⎝ 0 ⎠                         ⎝ 1 ⎠                     ║
║                                                                               ║
║   General state: |ψ⟩ = cos(θ/2)|↑⟩ + e^(iφ)sin(θ/2)|↓⟩                      ║
║                                                                               ║
║   Notice: θ/2, not θ! This is why 360° → -|ψ⟩ and 720° → |ψ⟩               ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   SPIN OPERATORS (Pauli Matrices):                                           ║
║   ═══════════════════════════════                                            ║
║                                                                               ║
║   Sₓ = (ℏ/2)σₓ     Sᵧ = (ℏ/2)σᵧ     Sᵤ = (ℏ/2)σᵤ                            ║
║                                                                               ║
║        ⎛ 0  1 ⎞         ⎛ 0 -i ⎞         ⎛ 1  0 ⎞                           ║
║   σₓ = ⎜      ⎟    σᵧ = ⎜      ⎟    σᵤ = ⎜      ⎟                           ║
║        ⎝ 1  0 ⎠         ⎝ i  0 ⎠         ⎝ 0 -1 ⎠                           ║
║                                                                               ║
║   These matrices encode:                                                     ║
║   • How spin flips (σₓ flips |↑⟩↔|↓⟩)                                       ║
║   • Non-commutativity: σₓσᵧ ≠ σᵧσₓ → uncertainty relations                  ║
║   • The SU(2) group structure of spin transformations                        ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   THE BLOCH SPHERE: VISUALIZING SPIN STATES                                  ║
║   ═════════════════════════════════════════                                  ║
║                                                                               ║
║                    |↑⟩ (north pole)                                          ║
║                      ●                                                        ║
║                     /│\                                                      ║
║                    / │ \    Every point on the sphere                        ║
║                   /  │  \   is a valid spin state!                           ║
║              |←⟩ ●───┼───● |→⟩                                               ║
║                   \  │  /                                                    ║
║                    \ │ /    Opposite points are                              ║
║                     \│/     orthogonal states                                ║
║                      ●                                                        ║
║                    |↓⟩ (south pole)                                          ║
║                                                                               ║
║   Note: This is a 2D surface representing a 2D complex Hilbert space         ║
║   (via stereographic projection, accounting for global phase freedom)        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    return art


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def demonstrate_spin():
    """Full demonstration of particle spin concepts"""

    print(__doc__)
    print()

    sections = [
        ("PARTICLE TABLE", particle_table),
        ("SPIN-1/2 STATES", draw_spin_half_states),
        ("SPIN-1 STATES", draw_spin_one_states),
        ("THE SPIN-STATISTICS THEOREM", draw_spin_statistics_theorem),
        ("PARTICLE EXCHANGE", draw_exchange_interaction),
        ("PAULI EXCLUSION", draw_fermion_exclusion_visual),
        ("BOSE-EINSTEIN CONDENSATION", draw_boson_condensation_visual),
        ("FERMION-BOSON INTERACTIONS", draw_interaction_diagram),
        ("720° ROTATION MYSTERY", draw_720_degree_rotation),
        ("ORBITAL vs SPIN", draw_angular_momentum_comparison),
        ("STERN-GERLACH MEASUREMENT", draw_spin_measurement),
        ("SPINORS: THE MATHEMATICS", draw_spinor_explanation),
    ]

    for title, func in sections:
        print(f"\n{'═' * 80}")
        print(f"  {title}")
        print('═' * 80)
        print(func())
        print()
        print("Press Enter to continue...")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            print("\n[Exiting...]")
            return

    # Closing reflection
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              FINAL REFLECTION                                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   Spin teaches us that quantum mechanics is not just "small physics."        ║
║   It's fundamentally different from anything classical.                       ║
║                                                                               ║
║   A point particle - with no extent, no internal structure - carries          ║
║   angular momentum. It "rotates" without rotating. It requires 720°           ║
║   to return to its starting state. And this seemingly abstract property       ║
║   determines whether matter can exist as we know it.                          ║
║                                                                               ║
║   Without spin statistics:                                                    ║
║   • No atoms (electrons would collapse to lowest orbital)                     ║
║   • No chemistry (no electron shells)                                         ║
║   • No matter (no stable structures)                                          ║
║   • No lasers (no coherent photon states)                                    ║
║   • No superconductivity or superfluidity                                    ║
║                                                                               ║
║   Spin is not a metaphor. It is not "like" rotation.                         ║
║   It is something new - something quantum - that we describe                  ║
║   using the mathematics of angular momentum because that math works.          ║
║                                                                               ║
║   The universe is stranger than we imagined,                                  ║
║   and spin is one of its deepest strangeness.                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    demonstrate_spin()
