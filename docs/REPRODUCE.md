# Reproduction instructions

## Environment evidence

The actual tested environment is Windows AMD64, CPython 3.13.5, SymPy 1.13.3, mpmath 1.3.0, NumPy 2.1.3 and Matplotlib 3.10.0. See inputs/tested_environment.json. This records a tested combination, not an independent clean-machine installation or a claim that every Python version is compatible. No compiled optical or GNSS DLL is required.

## Obtain and prepare

An authorized collaborator can download the private repository using GitHub access or clone it after authentication. Choose a new local directory. Do not copy a developer PYTHONPATH or a former research working tree.

On Windows, with Python 3.13 already installed:

    py -3.13 -m venv .venv
    .venv\Scripts\python -m pip install -r requirements.txt

These are installation instructions; the development run did not download or replace numerical packages. Verification-only users need requirements-verify.txt; plotting additionally needs requirements-plots.txt. The exact interval engine and angle-boundary checker use only the standard library.

## Read-only checks

    .venv\Scripts\python scripts/check_manifest.py
    .venv\Scripts\python scripts/verify_paper.py
    .venv\Scripts\python scripts/verify_angle_boundary.py
    .venv\Scripts\python scripts/verify_boundary_records.py

Expected outcomes are manifest PASS, 36 original checks PASS, four angle-boundary checks PASS and all saved boundary records reproduced. Failures return a nonzero exit status. Do not edit saved records to obtain PASS.

The repository attributes disable automatic line-ending conversion so the supplied evidence hashes remain valid after a checkout. Do not resave the original records or normalize their line endings before running the manifest check.

## Recompute and plot

    .venv\Scripts\python scripts/recompute_tables.py --output reproduced/tables
    .venv\Scripts\python scripts/make_figures.py --output reproduced/figures

Use a new output directory for a second run. The table recomputation reproduces the saved primary numerical quantities; the figure generator uses high-precision values converted to plotting coordinates, which can have rendering differences across Matplotlib/font versions. Pixel identity is not an optical claim.

There is no external observational dataset or device driver to acquire. The manuscript, unpublished proof narrative and AI-generated conceptual schematics are deliberately excluded; obtain the article package privately from the corresponding author. This repository contains the numerical material needed for checking and writing about the supplied optical result, not an independent new experiment.
