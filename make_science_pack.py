#!/usr/bin/env python3
"""
make_science_pack.py — create packs/science/ for modular-ai-packs.

Run this from inside ~/modular-ai-packs. It does NOT guess your pack.json
schema: it reads an existing pack manifest, clones its exact structure, and
swaps in the science values. Same trick for the registry entry.

Usage:
  cd ~/modular-ai-packs
  python make_science_pack.py
  python build_vectors.py            # fills in the real embeddings
  git add . && git commit -m "Add science pack" && git push

Safe to re-run: it overwrites packs/science/ and replaces (not duplicates)
the science entry in the registry.
"""

import os
import sys
import json
import glob
import copy

PACK_ID = "science"
PACK_NAME = "Science"
PACK_DESC = ("Physics, chemistry, and biology fundamentals — units and dimensional "
             "analysis, mechanics, energy, stoichiometry, cell biology, and genetics.")
ROUTER_DESC = ("Questions about the physical and natural world: forces, motion, energy, "
               "heat, electricity, atoms, molecules, chemical reactions and balancing "
               "equations, moles and concentration, cells, DNA, evolution, ecology, "
               "unit conversion and scientific notation.")
KEYWORDS = [
    "physics", "chemistry", "biology", "science", "force", "velocity",
    "acceleration", "momentum", "energy", "joule", "newton", "gravity",
    "thermodynamics", "entropy", "voltage", "current", "atom", "molecule",
    "element", "compound", "reaction", "mole", "stoichiometry", "molar",
    "ph", "acid", "base", "periodic table", "cell", "mitosis", "dna",
    "rna", "protein", "enzyme", "gene", "chromosome", "evolution",
    "photosynthesis", "ecosystem", "unit conversion", "significant figures",
]
TAGS = ["science", "physics", "chemistry", "biology", "stem"]


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

PROMPT_MD = """\
# Science

You answer questions in physics, chemistry, and biology.

## How you work

1. **Name the principle first.** Before any arithmetic, say which law or
   relationship applies (conservation of energy, ideal gas law, Mendelian
   inheritance) and why it fits this situation.
2. **Carry units through every step.** Units are the error check. If the units
   of your answer are wrong, the answer is wrong — say so and redo it.
3. **Show the substitution.** Write the symbolic form, then the same equation
   with numbers in it, then the result. Don't jump to a number.
4. **Respect significant figures.** Match the least precise input. State the
   figure count when it matters.
5. **Sanity-check the magnitude.** Compare the result to something familiar. A
   falling apple does not carry a megajoule.

## Boundaries

- Distinguish settled science from open questions. Say plainly when a question
  is at the edge of current understanding.
- For medical, pharmacological, or dosage questions, give the underlying
  science and direct the person to a qualified professional for anything
  affecting a real patient.
- For any procedure involving hazardous reagents, energetic reactions, or
  pressure vessels, describe the chemistry conceptually and do not give
  step-by-step preparation instructions.
- If a question is really mathematics or programming wearing a lab coat, say so
  — another domain handles it better.

## Style

Plain language. Define a term the first time you use it. An analogy is worth
using when it genuinely maps onto the mechanism, and worth skipping when it
doesn't.
"""

EXAMPLES_MD = """\
# Examples

---

**Q:** A 2 kg block slides down a frictionless ramp from a height of 3 m. How
fast is it moving at the bottom?

**A:** Conservation of energy. The ramp is frictionless, so all gravitational
potential energy converts to kinetic energy.

    mgh = ½mv²

Mass cancels — the answer is independent of how heavy the block is.

    v = √(2gh) = √(2 × 9.81 m/s² × 3 m) = √(58.9 m²/s²) ≈ 7.7 m/s

Units check: √(m/s² × m) = √(m²/s²) = m/s. ✓

7.7 m/s is about 28 km/h, which is a reasonable speed for a 3 m drop.

---

**Q:** Balance: Fe + O₂ → Fe₂O₃

**A:** Atoms are conserved, so each element must appear in equal numbers on both
sides.

Start with iron. The product has 2 Fe, so put 2 in front of Fe on the left.
Oxygen: the product has 3 O, but O₂ supplies them in pairs — 3 is odd. Double
everything to clear it.

    4 Fe + 3 O₂ → 2 Fe₂O₃

Check: Fe → 4 left, 4 right ✓. O → 6 left (3 × 2), 6 right (2 × 3) ✓.

---

**Q:** Why do cells divide by mitosis instead of just growing bigger?

**A:** Surface area scales with the square of the radius; volume scales with the
cube. Double a cell's radius and its volume grows eightfold while its membrane
grows only fourfold.

The membrane is where nutrients enter and waste leaves. The volume is what needs
feeding. So as a cell grows, demand outruns supply — the surface-area-to-volume
ratio falls, and diffusion can no longer service the interior fast enough.

Dividing resets that ratio. Two small cells have the same total volume as one
large one but considerably more membrane.

---

**Q:** How many grams of NaCl are in 250 mL of a 0.50 M solution?

**A:** Molarity is moles per litre, so convert volume to litres first.

    moles = M × V = 0.50 mol/L × 0.250 L = 0.125 mol

Molar mass of NaCl: Na = 22.99 + Cl = 35.45 = 58.44 g/mol.

    mass = 0.125 mol × 58.44 g/mol = 7.3 g

Two significant figures, matching the 0.50 M input.
"""

KNOWLEDGE = {
"units-and-measurement.md": """\
# Units and Measurement

## SI base units

Seven base units define all others: metre (length), kilogram (mass), second
(time), ampere (electric current), kelvin (temperature), mole (amount of
substance), candela (luminous intensity). Every other SI unit is a combination
of these. A newton is kg·m/s². A joule is a newton-metre, so kg·m²/s². A watt is
a joule per second.

Knowing the composition of a derived unit is often enough to reconstruct a
forgotten formula. Since a joule is kg·m²/s², any expression for energy must
reduce to mass times velocity squared in its dimensions — which is why both
½mv² and mgh work, and why mv would not.

## Dimensional analysis

Every term in a valid equation must carry the same dimensions. This is the
cheapest error check in physics: if one side reduces to metres per second and
the other to metres, the equation is wrong regardless of how the algebra looked.

Dimensional analysis also constrains unknown relationships. If a pendulum's
period can depend only on length L, mass m, and gravity g, then the only
combination yielding units of time is √(L/g) — which correctly predicts that
period does not depend on mass.

Arguments of transcendental functions must be dimensionless. You can take the
sine of an angle or the logarithm of a ratio, never of three metres.

## Significant figures

The precision of a result is limited by the least precise input. For
multiplication and division, the result carries as many significant figures as
the input with the fewest. For addition and subtraction, match the fewest
decimal places instead.

Leading zeros are never significant; 0.0042 has two. Trailing zeros after a
decimal point are significant; 4.200 has four. Trailing zeros in a whole number
are ambiguous, which is one reason scientific notation exists: 4.2 × 10³ says
two figures, 4.200 × 10³ says four.

Carry extra digits through intermediate steps and round only at the end.
Rounding early compounds error.

## Scientific notation and prefixes

A number in scientific notation is written as a coefficient between 1 and 10
times a power of ten. Multiplying adds exponents, dividing subtracts them.

Common prefixes step by factors of a thousand: kilo (10³), mega (10⁶), giga
(10⁹), tera (10¹²) going up; milli (10⁻³), micro (10⁻⁶), nano (10⁻⁹), pico
(10⁻¹²) going down. Centi (10⁻²) is the notable exception to the thousand-step
pattern and survives mainly in the centimetre.
""",

"mechanics-and-energy.md": """\
# Mechanics and Energy

## Newton's laws

An object at rest stays at rest, and an object in motion continues at constant
velocity, unless acted on by a net external force. "Net" is the operative word:
a book resting on a table has gravity and the normal force acting on it, but
they cancel.

The second law states that net force equals mass times acceleration, F = ma.
More precisely, force is the rate of change of momentum, which matters when mass
itself changes — a rocket burning fuel, for instance.

The third law states that forces come in pairs: if A pushes B, then B pushes A
with equal magnitude in the opposite direction. The paired forces act on
different objects, which is why they never cancel each other out. A horse can
pull a cart because the reaction force acts on the horse, not the cart.

## Kinematics

For constant acceleration in one dimension, three relations cover most problems:
v = v₀ + at, x = x₀ + v₀t + ½at², and v² = v₀² + 2a(x − x₀).

The third is useful precisely because it contains no time — reach for it when a
problem gives distances and speeds but never mentions duration.

Projectile motion decomposes into two independent problems. Horizontal velocity
is constant when air resistance is neglected; vertical motion is free fall under
gravity. The two share only the clock. This is why a bullet fired horizontally
and one dropped from the same height land at the same moment.

## Energy and its conservation

Kinetic energy is ½mv². Gravitational potential energy near Earth's surface is
mgh. Energy is neither created nor destroyed, only converted — the total in a
closed system stays constant.

Working with energy instead of forces sidesteps the details of the path. A block
sliding down a curved frictionless ramp arrives at the bottom with exactly the
speed a straight ramp of the same height would give, because only the height
difference enters the calculation.

Friction does not destroy energy; it converts mechanical energy to thermal
energy. Energy is conserved either way, but the thermal portion is no longer
available to do useful work.

## Momentum

Momentum is mass times velocity, and total momentum is conserved in any
collision with no external forces. This holds whether the collision is elastic
or not.

In an elastic collision, kinetic energy is conserved as well. In an inelastic
collision, momentum is still conserved but some kinetic energy becomes heat,
sound, and deformation. When two objects stick together, the collision is
perfectly inelastic and loses the maximum kinetic energy compatible with
conserving momentum.
""",

"chemistry-fundamentals.md": """\
# Chemistry Fundamentals

## Atoms and the periodic table

An atom's identity is set by its proton count — the atomic number. Neutrons vary
within an element, producing isotopes with the same chemistry but different
masses. Electrons determine essentially all chemical behaviour.

Rows of the periodic table are periods, corresponding to electron shells.
Columns are groups, and elements within a group share valence electron counts,
which is why they behave alike. Group 1 metals are all violently reactive with
water; group 18 noble gases have full shells and barely react at all.

Two trends explain much of descriptive chemistry. Atomic radius decreases across
a period as nuclear charge pulls electrons inward, and increases down a group as
shells are added. Electronegativity, the pull an atom exerts on shared
electrons, does the reverse: it rises across a period and falls down a group.

## Bonding

Ionic bonds form when electronegativity differs enough that an electron
transfers outright, leaving oppositely charged ions held by electrostatic
attraction. The resulting solids have high melting points and conduct when
molten or dissolved.

Covalent bonds form when atoms share electrons. Equal sharing gives a nonpolar
bond; unequal sharing gives a polar one, with partial charges at each end.

Molecular shape follows from electron pair repulsion: pairs around a central
atom arrange themselves as far apart as possible. Four pairs give a tetrahedron,
three give a trigonal plane, two give a line. Lone pairs occupy space too, which
is why water is bent rather than linear — and that bend is what makes water
polar, which in turn explains its high boiling point and its power as a solvent.

## The mole and stoichiometry

A mole is 6.022 × 10²³ particles, chosen so that an element's atomic mass in
grams contains exactly one mole of atoms. The mole is the bridge between the
gram scale of the laboratory and the atom scale of the reaction.

A balanced equation is a recipe in moles, not grams. Converting a mass problem
means going grams → moles → moles (via the equation's coefficients) → grams.

The limiting reagent is the reactant that runs out first, and it caps the yield.
Identify it by converting each reactant to moles and dividing by its coefficient
— the smallest ratio wins. Percent yield is actual mass over theoretical mass,
times 100.

## Solutions, acids, and bases

Molarity is moles of solute per litre of solution. Diluting conserves the amount
of solute, giving M₁V₁ = M₂V₂.

An acid donates protons; a base accepts them. pH is the negative logarithm of
hydrogen ion concentration, so each pH unit is a tenfold change — pH 3 is a
hundred times more acidic than pH 5. Neutral water sits at pH 7 at 25 °C.

Strength and concentration are independent properties. A strong acid dissociates
completely, a weak one only partially, but a dilute strong acid can easily be
less hazardous than a concentrated weak one.
""",

"biology-fundamentals.md": """\
# Biology Fundamentals

## Cells

All organisms are made of cells, and every cell comes from a pre-existing cell.
Prokaryotes — bacteria and archaea — have no nucleus and no membrane-bound
organelles. Eukaryotes have both.

The membrane is a phospholipid bilayer: water-attracting heads face outward,
water-repelling tails face inward. This arrangement forms spontaneously in water
and lets the cell control what crosses. Small nonpolar molecules pass freely;
ions and large polar molecules need protein channels or pumps.

Mitochondria produce ATP through cellular respiration. Chloroplasts, in plants
and algae, capture light energy. Both retain their own DNA, evidence that they
descend from free-living bacteria absorbed by an ancestral cell.

## Energy in living systems

Photosynthesis converts carbon dioxide and water into glucose and oxygen using
light energy. Cellular respiration runs the reverse, releasing energy stored in
glucose as ATP. The two processes together cycle carbon and energy through the
biosphere.

Aerobic respiration yields roughly 30–32 ATP per glucose molecule. Without
oxygen, fermentation yields 2 — enough for a sprint, not for sustained work.

Enzymes are protein catalysts that lower activation energy without being
consumed. Each has an active site shaped for its substrate, which is why enzymes
are specific and why heat or pH extremes destroy their function: denaturing the
protein destroys the shape, and the shape is the mechanism.

## Genetics

DNA is a double helix of nucleotides. Adenine pairs with thymine, guanine with
cytosine. Because the pairing is fixed, either strand specifies the other, which
is what makes faithful replication possible.

Genes are transcribed to messenger RNA, which ribosomes translate into proteins.
Three bases — a codon — specify one amino acid. The code is nearly universal
across life, strong evidence for common ancestry.

Mitosis produces two genetically identical diploid cells and handles growth and
repair. Meiosis produces four genetically distinct haploid gametes and generates
variation through crossing over and independent assortment.

Mendelian inheritance follows from this: alleles segregate during gamete
formation, so an organism carrying one dominant and one recessive allele shows
the dominant trait but can still pass on the recessive one. Crossing two such
carriers gives the familiar 3:1 ratio in the offspring.

## Evolution and ecology

Natural selection requires three conditions: variation within a population,
heritability of that variation, and differential reproductive success. Where all
three hold, allele frequencies shift across generations. Selection acts on
existing variation — it cannot produce a trait on demand.

Energy flows through ecosystems in one direction and degrades at each transfer;
roughly ten percent passes from one trophic level to the next, which is why food
chains are short. Matter, by contrast, cycles: carbon, nitrogen, and water move
repeatedly between organisms and the environment.
""",
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def pick_template_pack():
    """Choose an existing pack whose manifest we clone the shape of."""
    ids = [os.path.basename(os.path.dirname(p))
           for p in sorted(glob.glob("packs/*/pack.json"))]
    ids = [i for i in ids if i != PACK_ID]
    if not ids:
        die("No existing packs/*/pack.json found. Run this from ~/modular-ai-packs.")
    for preferred in ("math", "programming", "algorithms"):
        if preferred in ids:
            return preferred
    return ids[0]


def swap_id(obj, old, new):
    """Recursively replace the template pack id inside strings (paths, ids)."""
    if isinstance(obj, dict):
        return {k: swap_id(v, old, new) for k, v in obj.items()}
    if isinstance(obj, list):
        return [swap_id(v, old, new) for v in obj]
    if isinstance(obj, str):
        return obj.replace(old, new)
    return obj


def set_if_present(d, key, value):
    """Only overwrite keys the template actually uses — never invent fields."""
    if key in d:
        d[key] = value
        return True
    return False


def chunk_markdown(text, source):
    """Split a knowledge doc on '## ' headings. One chunk per section."""
    chunks, current = [], []
    for line in text.splitlines():
        if line.startswith("## ") and current:
            chunks.append("\n".join(current).strip())
            current = [line]
        elif line.startswith("# ") and not current:
            continue                      # skip the document title
        else:
            current.append(line)
    if current:
        chunks.append("\n".join(current).strip())
    return [c for c in chunks if c]


def read_vector_meta(template_id):
    """Borrow embedding_model / dimension from an existing pack if we can."""
    path = os.path.join("packs", template_id, "vectors.json")
    model, dim = "all-MiniLM-L6-v2", 384
    if os.path.exists(path):
        try:
            data = json.loads(open(path).read())
            model = data.get("embedding_model", model)
            dim = data.get("dimension", dim)
        except Exception:
            pass
    return model, dim


# --------------------------------------------------------------------------
# Build steps
# --------------------------------------------------------------------------

def write_manifest(template_id):
    tmpl = json.loads(open(os.path.join("packs", template_id, "pack.json")).read())
    man = swap_id(copy.deepcopy(tmpl), template_id, PACK_ID)

    set_if_present(man, "id", PACK_ID)
    set_if_present(man, "name", PACK_NAME)
    set_if_present(man, "description", PACK_DESC)
    set_if_present(man, "tags", list(TAGS))
    set_if_present(man, "version", "0.1.0")

    routing = man.get("routing")
    if isinstance(routing, dict):
        set_if_present(routing, "keywords", list(KEYWORDS))
        set_if_present(routing, "description_for_router", ROUTER_DESC)
    else:
        print("  ! template has no 'routing' block — check the manifest by hand")

    # The science pack ships no executable tools.
    if "tools" in man:
        man["tools"] = []

    path = os.path.join("packs", PACK_ID, "pack.json")
    with open(path, "w") as f:
        json.dump(man, f, indent=2)
        f.write("\n")
    print("  wrote " + path + "  (shape cloned from " + template_id + ")")
    return man


def write_text_files():
    base = os.path.join("packs", PACK_ID)
    with open(os.path.join(base, "prompt.md"), "w") as f:
        f.write(PROMPT_MD)
    with open(os.path.join(base, "examples.md"), "w") as f:
        f.write(EXAMPLES_MD)
    print("  wrote prompt.md, examples.md")

    kdir = os.path.join(base, "knowledge")
    os.makedirs(kdir, exist_ok=True)
    for name, text in KNOWLEDGE.items():
        with open(os.path.join(kdir, name), "w") as f:
            f.write(text)
    print("  wrote " + str(len(KNOWLEDGE)) + " knowledge doc(s)")


def write_vectors(template_id):
    model, dim = read_vector_meta(template_id)
    chunks, n = [], 0
    for name in sorted(KNOWLEDGE):
        for body in chunk_markdown(KNOWLEDGE[name], name):
            n += 1
            chunks.append({
                "id": PACK_ID + "-" + str(n).zfill(3),
                "source": "knowledge/" + name,
                "text": body,
                "vector": [0.0] * 8,      # placeholder; build_vectors.py fills these
            })

    data = {
        "embedding_model": model,
        "dimension": dim,
        "_note": "Placeholder vectors. Run build_vectors.py to generate real ones.",
        "chunks": chunks,
    }
    path = os.path.join("packs", PACK_ID, "vectors.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("  wrote vectors.json with " + str(len(chunks)) + " placeholder chunk(s)")
    return len(chunks)


def folder_size():
    total = 0
    for root, _, files in os.walk(os.path.join("packs", PACK_ID)):
        for name in files:
            total += os.path.getsize(os.path.join(root, name))
    return total


def update_registry(template_id):
    path = os.path.join("registry", "index.json")
    if not os.path.exists(path):
        die("registry/index.json not found. Run this from ~/modular-ai-packs.")

    reg = json.loads(open(path).read())

    # Find the list of packs, whatever it's called in your registry.
    list_key, packs = None, None
    for key, value in reg.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            if any(e.get("id") == template_id for e in value):
                list_key, packs = key, value
                break
    if packs is None:
        die("Could not locate the pack list inside registry/index.json — "
            "add the science entry by hand.")

    template_entry = next(e for e in packs if e.get("id") == template_id)
    entry = swap_id(copy.deepcopy(template_entry), template_id, PACK_ID)

    set_if_present(entry, "id", PACK_ID)
    set_if_present(entry, "name", PACK_NAME)
    set_if_present(entry, "description", PACK_DESC)
    set_if_present(entry, "tags", list(TAGS))
    set_if_present(entry, "version", "0.1.0")
    set_if_present(entry, "size_bytes", folder_size())

    packs = [e for e in packs if e.get("id") != PACK_ID]   # replace, don't duplicate
    packs.append(entry)
    reg[list_key] = packs

    with open(path, "w") as f:
        json.dump(reg, f, indent=2)
        f.write("\n")
    print("  registry now lists: " + ", ".join(e.get("id", "?") for e in packs))


def main():
    if not os.path.isdir("packs") or not os.path.isdir("registry"):
        die("No packs/ or registry/ here. cd ~/modular-ai-packs first.")

    template_id = pick_template_pack()
    print("Using '" + template_id + "' as the structural template.\n")

    os.makedirs(os.path.join("packs", PACK_ID), exist_ok=True)
    write_manifest(template_id)
    write_text_files()
    count = write_vectors(template_id)
    update_registry(template_id)

    print("\nDone. Science pack created with " + str(count) + " knowledge chunk(s).")
    print("\nNext:")
    print("  python build_vectors.py")
    print("  git add . && git commit -m 'Add science pack' && git push")
    print("  cd ~/modular-ai-core && rm -f routing_cache.json && python core.py --refresh")


if __name__ == "__main__":
    main()
