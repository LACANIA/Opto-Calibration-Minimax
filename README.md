# Opto Calibration Minimax

Code, exact numerical records and reproduction instructions for a theoretical three-polarizer information-design study. This repository contains no manuscript, unpublished proof document, raw experimental dataset or hardware binary.

The inputs are four declared amplitude specifications and a bounded-readout/angle-error example. Every reported attenuation is relative to incident optical power, with T = 2 Iout / Iin. The principal results reproduced here are the exact-setting limits, bounded-reading formula checks, and a sufficient angular-error performance bound. They are mathematical model results, not measurements.

## Start here

Read [the reproduction guide](docs/REPRODUCE.md), [the data dictionary](docs/DATA_SOURCES.md), and [the model and interfaces](docs/MODEL_AND_INTERFACES.md).

In an existing compatible Python environment:

    python scripts/check_manifest.py
    python scripts/verify_paper.py
    python scripts/verify_angle_boundary.py
    python scripts/verify_boundary_records.py

Recompute the numerical tables and regenerate the two quantitative figures into fresh directories:

    python scripts/recompute_tables.py --output reproduced/tables
    python scripts/make_figures.py --output reproduced/figures

Verification reads repository-relative inputs and writes no files. Generation refuses a nonempty output directory. No source from a former research working tree, network access, GNSS dataset, DLL or LaTeX installation is needed for these operations. Python dependencies must be installed separately.

## Evidence and interpretation

- records/: original saved rational enclosures and controls, retained without edits.
- results/: paper-relevant plotting arrays, two quantitative figure files and readable extracts.
- checks/: an exact-rational evaluation of the existing sufficient angle-error boundary.
- inputs/: the theoretical inputs and actually tested dependency versions.
- scripts/ and src/: portable checks, numerical recomputation and formula plotting.
- docs/: data origins, interfaces, reproduction and limitations.

For Q=0.01, epsilon=0.00009 and eta=0.001 rad, the supplied bound is T <= 1.8e-5 and the same-error advantage lower bound is 1.5570 dB. The exact angular-error minimax value has not been solved. A sampled approximately 10.9 dB estimate is not used as a certified result.

The existing symbolic-control metadata originally recorded eight identities; the saved correction establishes seven. Both the original record and correction are retained. Read docs/EVIDENCE_SCOPE.md before interpreting pass fields or finite control points.

The repository is initially Private. No public archive DOI, independent installation validation, hardware validation or public redistribution license is asserted. See RIGHTS.md for the current rights status.
