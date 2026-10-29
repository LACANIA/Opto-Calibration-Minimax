# Model and interfaces

The model assumes unpolarized normal incidence, unit pass-axis amplitude, real diattenuation, no extra retardance, fixed component amplitudes in [0,Q], and freely set outer axes at one operating point. It does not model a continuous mechanical travel, a measured calibration process, depolarization, stray light or spectral averaging.

## Exact rational reading interface

src/bounded_policy.py exposes policy(Q, epsilon, hat_z) and consistent(Q, epsilon, hat_z, z). Use integers, Fraction values or exact decimal strings. The function returns u, a, cos2 and epsilon0 as rational values. It rejects invalid Q, negative epsilon, out-of-range readings, nonfinite values and inconsistent actual middle amplitudes. A returned sufficient_condition=False means the existing theorem is not applicable; it does not prove infeasibility.

The policy uses u=clip(hat_z+epsilon,0,Q), a=Q^2 for u<=Q^2, otherwise a=u(1+Q^2)/(1+u). The outer settings are theta and -theta with cos^2(theta)=(a-Q^2)/(1-Q^2), modulo pi. The reading may legally be negative or exceed Q within its declared error. The interface does not access the actual unknown outer amplitudes.

## Reproduction entry points

scripts/verify_paper.py: original portable symbolic and numerical consistency checks. Its independent 90-digit intervals are checked for overlap with the separately rounded primary intervals; overlap is a consistency cross-check, not a claim of bitwise identical endpoints or a proof from finite samples.

scripts/verify_angle_boundary.py: standard-library exact-rational reproduction of the existing sufficient boundary.

scripts/verify_boundary_records.py: recomputes every saved rational boundary control and checks the declared reading consistency; it does not replace a continuous proof.

scripts/recompute_tables.py: recomputes the primary 70-digit/160-term rational enclosures using src/exact_interval.py and compares them with saved primary table entries. It writes a new output directory and refuses a nonempty one.

scripts/make_figures.py: regenerates the two quantitative plot groups from the existing formulas using 80-digit mpmath evaluation. Plot sampling is presentation only. Only the existing sufficient region is colored; a point outside that region is not classified as impossible.

No input-loader injection, historical module import or hidden scientific initial state is used. All paths are resolved from the repository location or the explicit --output argument.
