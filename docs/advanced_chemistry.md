# Advanced Chemistry System

This module expands the basic chemistry support with new structures for
multi-step reactions, drug metabolism and chemical analysis equipment.
It introduces compound properties such as viscosity, solubility and
reactivity which influence synthesis results.

`ReactionChain` allows complex recipes that require intermediate
compounds to be produced in sequence. Each step can define temperature
constraints so specialized equipment like a reaction chamber is useful.

`Compound` objects carry `ChemicalProperties` and optional
`Pharmacokinetics` data. Drugs degrade over time through the
`degrade()` method and produce active metabolites when processed with
`metabolize()`.

The provided equipment classes – `Centrifuge`, `Spectrometer` and
`ReactionChamber` – model common laboratory devices for refining,
analysing and safely executing reactions.
