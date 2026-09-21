# Ownership changes and omitted-good exchanges: a rigorous obstruction

## Mathematical examination before implementation

The proposed operations preserve the multiset of the four predecessor bundle
sizes. This invariant can prevent success even when arbitrary EFX ownership
changes and arbitrarily many EFX-preserving exchanges are allowed. No utility
improvement restriction is needed for the obstruction.

Give every agent the identical additive valuation of four large goods at H each
and six small goods at 1 each, where 6 < H < 36. Omit a large good. Allocate the
other three large goods as singletons and all six small goods to the last agent.
This is EFX: removing any good from the six-good bundle leaves 5, while removing
from a singleton leaves zero.

Every EFX predecessor with bundle sizes (1,1,1,6) must put all six small goods in
the six-good bundle. Otherwise that bundle contains t>=1 large goods and at
least two small goods (only four large goods exist). Removing a small good
leaves tH+5-t, which exceeds H for H>1. Every singleton is worth at most H,
contradicting EFX. Thus the omitted good must always be large.

Insertion into a singleton creates a pair of value 2H. The six-small-good agent
has value 6 but sees expected value H after random removal: this fails for H>6.
Insertion into the six-good bundle creates value H+6 and size 7. A singleton
agent requires H >= 6(H+6)/7, equivalent to H>=36. This fails for H<36.

Therefore no EFX predecessor with this profile can be extended, regardless of
which good is omitted or how goods are assigned. In particular every reachable
state under the proposed moves fails. There are exactly four reachable unlabeled
partitions (one for each omitted large good), with all ownership permutations
available. At H=6 and H=36 direct insertion succeeds; H=100 is NOT a trap.

This does not refute unrestricted Mode C, nor EFR existence. For H=10, omit a
small good instead and distribute the four large goods and five small goods as
(large+small, large+small, large+small, large+two small). Values are (11,11,11,12),
and this is EFX. Insert the omitted small good into a value-11 pair. Values become
(12,11,11,12), again EFX and hence EFR.

One simultaneous repair from the trapped partition is to replace one small good
in the six-good bundle by the omitted large good and transfer three remaining
small goods, one to each singleton. This changes the size profile to (2,2,2,3).
The combined step preserves EFX at its endpoints; the individual intermediate
steps need not be EFX. It identifies a concrete need for coordinated rebundling.

## Exact experiment

`exchange_search.py` explores a finite graph of unlabeled partitions. For each
partition it explicitly enumerates all EFX agent assignments. A swap edge exists
only if some labeled EFX assignment remains EFX when the omitted good replaces
one allocated good, before any subsequent ownership change. No welfare-monotonic
restriction is imposed. Returned paths include the actual labeled transitions.

All four insertion targets are checked for every EFX ownership assignment.
TRAPPED means the entire reachable component has been exhausted. A separate
slow checker reconstructs EFX and EFR from their definitions and verifies that
all outgoing legal edges stay inside the supplied component and every insertion
fails. UNKNOWN means a state or time budget was reached, never a counterexample.
An unrestricted oracle separately attempts to find an extension on trapped
valuation profiles. Sorting unlabeled partitions never changes labeled witness
ownership.

`exchange_experiment.py` runs boundary/obstruction regressions and seeded profiles
from four families: independent integer values, near-identical values, sparse
values, and identical values. Each profile starts from an EFX allocation for a
randomly deleted good, plus a second EFX partition sampled from up to 128 random
partition candidates when one is found. This is a biased finite sample, not a
uniform sample of all EFX allocations or a proof of a universal assertion.

The workflow runs seeds 42 and 1729 independently, requests 40 profiles per seed,
and limits each graph exploration to 1000 states and 3 seconds with a 180-second
campaign budget. Raw matrices, starting allocations, paths, and trap certificates
are saved as artifacts. The job has a separate 12-minute outer timeout.

## Consequences for the next research step

1. The universal claim from an arbitrary EFX starting allocation is false for
   ownership changes plus single-good omitted exchanges alone.
2. A proof of unrestricted Mode C needs a suitable starting partition or moves
   that change bundle sizes, potentially changing multiple bundles together.
3. Do not universally restrict to (2,2,2,3): the earlier (100,1,...,1) example
   already rules that out. A family of allowed profiles is needed.
4. A promising next experiment is coordinated rebundling with a small move
   budget, recording the minimum number of moved goods needed to escape each
   certified trap. A proof would need an escape lemma covering all such traps.
