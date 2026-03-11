Your AI model scored 95%. Your users still hate it.

Most teams building AI products are stuck at offline evals, testing models against fixed datasets before real users ever touch them. The scores go up. Leadership feels good. But Mario Rodriguez, CPO of GitHub, calls out what actually happens: teams build incentive systems to pass the test, not improve the product (Episode 223).

“When a measure becomes a target, it stops being useful” (Goodhart's Law).

The discipline nobody talks about is moving from offline to online evaluations and measuring what users actually do in production.

At GitHub Copilot, they track two metrics: AR (acceptance rate, did the developer accept the suggestion?) and ARC (accepted and retained characters, how much of that code did they actually keep?). A developer might accept a 20-line suggestion, then immediately rewrite 18 of those lines. Offline evals would score that as success. Production data tells the real story.

Mario's advice? Expect offline and online performance to diverge. Don't panic when it happens. Build the online measurement infrastructure early, before you convince yourself the offline score means you're done.

Are you measuring model performance or actual user value?