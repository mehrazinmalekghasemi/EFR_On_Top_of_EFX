# Coordinated rebundling: proved statements and open conjecture

No counterexample to unrestricted additive EFR existence has been found in this
work. Previously certified traps refute only a restricted repair procedure.
The new computation looks for an EFX predecessor on nine goods, possibly omitting
a different good, that permits EFR insertion. It does not require EFX during
individual microsteps of a simultaneous repair.

## What a changed membership means

Treat four physical bundles and the omitted-good slot as five slots. Whole-bundle
ownership assignments are free, as in the earlier ownership experiment. The
cost of a simultaneous repair is the number of goods whose slots change,
minimized over bijections between the old and new four bundle slots. Final
insertion is not counted. An omitted-good swap costs two changes, not one.
For old A,g and new B,h the exact distance is

    d((A,g),(B,h)) = 10 - 1[g=h] - max_permutation p sum_i |A_i intersect B_p(i)|.

This measures changes to the partition, not the total number of goods whose
agent owner changes. Whole-bundle ownership changes may change many agents'
received goods at zero partition-edit cost.

`rebundle.py` enumerates all 10*11051 unlabeled nine-good partitions/deletions,
sorts candidates into distance layers, and tests EFX ownership and insertion
using the exact matching kernel. The first successful distance is minimal,
because every smaller distance was exhaustively checked. Integer/rational
comparisons and arbitrary-precision fallback are retained. Timeout is UNKNOWN.
Failure at radius r<10 is ABSENT_WITHIN_RADIUS. Even exhaustive MODE_C_ABSENT
would refute the EFX-insertion construction, not EFR existence itself.

## Lemma 1: exact insertion condition

For an EFX predecessor A, g can be inserted into A_k, of size s>0, iff

    v_i(g) <= ((s+1)/s) v_i(A_i) - v_i(A_k), for every i != k.

Proof: EFX implies EFR by averaging the removal inequalities. All unchanged
comparisons remain valid, and the recipient's own value increases. The only
remaining inequalities compare other agents against the enlarged target and
are precisely the displayed inequalities. An empty target always works.

## Lemma 2: a source with enough average value suffices

Suppose no other agent envies k, so Delta_ik=v_i(A_i)-v_i(A_k)>=0. Then

    C_ik = v_i(A_k)/s + ((s+1)/s) Delta_ik.

Thus it suffices that g be worth at most the target bundle's average to each
other agent; more generally the displayed slack permits a larger g. The
recipient's own valuation of g imposes no restriction. This condition does not
require a common least-valued good.

## Lemma 3: common-least-good repair

If g is weakly least-valued for every agent, any EFX predecessor can be repaired
by whole-bundle envy-cycle rotations and then insertion. Cycle rotations increase
own utilities without changing the collection of bundles, so they preserve EFX.
They terminate because there are finitely many ownership permutations and each
rotation strictly improves some utilities without reducing any. A source in the
resulting acyclic envy graph meets Lemma 2. This is a sufficient theorem for that
subclass, conditional on the existence of the initial EFX allocation.

## Lemma 4: five simultaneous membership changes can be necessary

Let all agents have identical values (H,H,H,H,1,1,1,1,1,1), with 6<H<36.
Start with a large omitted good and predecessor (large singleton, large
singleton, large singleton, six small goods). Then the minimum partition-edit
cost of reaching ANY extendable EFX predecessor is exactly five.

Proof of necessity:

1. If a large good is omitted, an agent has no large good and has own value at
   most 6. Any bundle containing a large good and another good violates that
   agent's EFX condition: remove the other good and value at least H remains.
   Thus all three large goods must be singletons, and the six small goods stay
   together. As proved in EXCHANGE_FINDINGS.md, insertion fails for 6<H<36.
2. Therefore an extendable predecessor must omit a small good. It contains four
   large goods and five small goods. Each agent must receive exactly one large
   good: otherwise some agent has value at most 5 while another bundle contains
   two large goods, contradicting EFX after removing one of them.
3. Write b_i for the number of small goods accompanying the large good. EFX
   requires max b_i <= min b_i + 1. Since sum b_i=5, the multiset is (2,1,1,1).
4. Under ANY matching of the old and new bundle slots, the old large singleton
   slots retain at most three goods in total, and the old all-small slot retains
   at most two small goods. The omitted slots differ. At most five of the ten
   slot memberships can remain unchanged, so at least five must change.

Sufficiency: exchange a small good for the omitted large good in the all-small
bundle, and send three other small goods, one to each old singleton. The new
predecessor values are (H+1,H+1,H+1,H+2), which is EFX. Insert the omitted unit
into one of the pairs to obtain (H+2,H+1,H+1,H+2), again EFX and hence EFR.
Exactly five memberships changed before insertion. QED.

## Candidate escape lemma, NOT proved

For every nonnegative additive 4x10 instance and every complete EFX predecessor
on nine goods, there exists an extendable EFX predecessor at partition-edit
distance at most five (allowing the omitted good to change).

This would imply the desired EFX-to-EFR construction whenever a nine-good EFX
predecessor exists. Lemma 4 shows that the proposed constant five could not be
improved under this metric. The experiments do not establish this conjecture.
Failure of this stronger arbitrary-start bound would still not refute Mode C,
and failure of Mode C would still not refute unrestricted EFR existence.

A focused next proof/search task is to constrain valuations by EFX of a fixed
canonical starting allocation, then search for valuations invalidating every
extension within distance five. Up to simultaneous relabeling of agents and
goods, only the 18 nondecreasing bundle-size profiles summing to nine are needed
for the starting allocation. This symmetry reduction concerns initial bundle
sizes, not independent sorting of valuation rows. Each profile still represents
an infinite continuous valuation domain; a finite sample cannot certify it.

## Experiment scope

The workflow tests the 13 saved trap starts (four constructed regressions plus
nine sampled starts) and 100 additional seeded heterogeneous cases. In the extra
cases every agent values four large goods independently in 14..30 and six small
goods in 1..2. The initial allocation consists of three large singletons and six
small goods in one bundle; a fourth large good is omitted. These starts are EFX
because a small bundle after any removal has value at most 10, while each large
singleton is worth at least 14. The generator seed is 2026.

All results concern this finite test set. In particular the stress family is
structured and does not cover all valuation profiles or all starting allocations.

## Completed GitHub experiment

[Run 35597667294](https://github.com/mehrazinmalekghasemi/EFR_On_Top_of_EFX/actions/runs/35597667294)
succeeded at code commit `bab19dc089e77682d2d6185357ba9f52b7cae582`.
All 33 tests passed. The run found valid extensions for all 113 starts, with no
UNKNOWN or absence verdict. The exact minimum-distance counts were:

| Minimum memberships changed | Saved traps (13) | New stress starts (100) | Total |
|---|---:|---:|---:|
| 0 | 0 | 20 | 20 |
| 1 | 1 | 0 | 1 |
| 2 | 0 | 35 | 35 |
| 3 | 5 | 15 | 20 |
| 4 | 3 | 28 | 31 |
| 5 | 4 | 2 | 6 |

The four constructed traps each require five changes, consistent with Lemma 4.
The nine earlier sampled traps require one, three, or four changes. Two new
heterogeneous stress starts also require five. No universal upper bound follows
from this structured finite test set.

Every returned local witness was checked for EFX on the nine-good predecessor,
EFR after insertion, and the stated movement count. GitHub's aggregate summary
and all 113 per-case minimum distances matched the local seeded run. Saved
summaries and detailed locally reproduced witnesses for the 13 original traps
and two stress cases requiring five changes are in
`experiment-results/run-35597667294/`. The full original GitHub report is the
`coordinated-rebundling` artifact on the run page.
