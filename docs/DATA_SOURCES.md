# Data sources and units

There is no external experimental database to download for this study. Inputs in inputs/spec.json are theoretical specifications, and the numerical results are evaluations of analytic formulas in the stated real-diattenuator model. They are not measured polarizer properties, customer requirements or device calibration records.

## Fixed inputs

Q takes the exact values 1/1000, 1/100, 3/100 and 1/10. The principal example uses Q=1/100, epsilon=9/100000 and eta=1/1000 rad. q is a blocked-axis amplitude, q squared is principal intensity leakage, and 1/q squared is the principal-axis intensity extinction ratio when q is positive. Epsilon is an absolute error in middle amplitude; eta covers total relative angle implementation error. Neither is a standard deviation.

T = 2 Iout / Iin is dimensionless. Physical power transmission is T/2. Absolute attenuation is -10 log10(T/2) dB. No travel-dependent attenuation span is reported.

## Saved evidence

records/limit_01/limits.json contains the preset and exact-information limits from the first optical-limit study. records/limit_02/numerical_certificate.json contains the four values, finite-readout criterion and principal angle-error example. Each lower/upper pair is a rational outward enclosure; a decimal display is a rounded presentation.

records/limit_02/boundary_records.json contains exact finite boundary controls. controls.json contains formula/propagation controls and auxiliary point evaluations. independent_audit.json files preserve previous independent-check records; a saved PASS field is not substituted for running the current checks.

metadata_correction.json preserves the correction from eight recorded symbolic identities to seven actual identities. The original controls record is unchanged. The supplementary-program serialization failure was an engineering-output failure rather than a new optical observation; no failed research result is relabeled as a successful experiment.

results/plot_data.json contains high-precision formula evaluations used for presentation. The two plot groups correspond to the exact limits and bounded-readout/sufficient-angle region. Other legacy illustration arrays in this file are retained for source identity but are not additional experiments or paper measurements. Conceptual raster schematics are not included.

provenance.json maps every directly copied or adapted scientific file to a study-relative source identity and SHA256. These identifiers provide lineage; they are not external download URLs. No GNSS, UrbanNav, navigation reference trajectory or RTKLIB material is needed or included.
