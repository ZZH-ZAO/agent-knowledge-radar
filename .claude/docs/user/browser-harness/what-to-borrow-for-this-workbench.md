# What To Borrow From browser-harness For This Workbench

## Summary

- Project name: browser-harness -> current workbench
- Project path: `https://github.com/browser-use/browser-harness` -> `D:\claude-code-sourcemap`
- Document type: user
- Purpose: explain which design ideas from browser-harness are worth borrowing into the current workbench and which ones should not be copied directly

## First Conclusion

The most valuable things to borrow are:

- thin substrate thinking
- interaction-skill vs domain-skill separation
- explicit write-back of learned browser knowledge

The least valuable thing to copy blindly is the repo's anti-structure posture.
Its thinness is a strength for browser execution, but your current workbench still needs stronger archival and traceability layers than browser-harness itself emphasizes.

## What Is Most Worth Borrowing

### 1. Separate Reusable Mechanics From Domain Knowledge

This is the single strongest reusable idea.

The split between:

- `interaction-skills/`
- `domain-skills/`

should influence the current workbench whenever a capability area starts growing.

This pattern is powerful because it prevents one recurring mistake:

- mixing universal mechanics with site-specific or case-specific observations

For the current workbench, the analogous lesson is:

- keep reusable method layers separate from case-local lessons
- keep generic workflow mechanics separate from one-project quirks

### 2. Learned Knowledge Should Be Written Back

The repo strongly reinforces:

- if the agent learns a durable browser trick, it should write it back into a skill

That is very aligned with the workbench's broader promotion philosophy.

What is worth borrowing is not just the existence of skill files.
It is the stronger behavioral norm:

- use should create better reusable assets

### 3. Thin Entrypoints Can Be Better Than Thick Wrappers

The tiny `run.py` and short dependency list are a good reminder that not every useful system needs a large orchestration shell.

For the current workbench, this suggests:

- when a capability can live in one simple command, keep it simple
- do not add managers and abstraction layers unless a real bottleneck appears

### 4. Verification Should Be First-Class

The screenshot-first and re-screenshot-after-action discipline is worth remembering beyond browser tasks.

The broader lesson is:

- after any meaningful side effect, verify visible state before assuming success

That principle can travel well into other workbench tool designs.

## What Should Not Be Copied Directly

### 1. Do Not Copy The “No Rails” Attitude Everywhere

In browser-harness, low structure is part of the product thesis.
In your workbench, low structure everywhere would be a regression.

You still need:

- reports
- sessions
- memory boundaries
- promotion tracking
- auditability

So borrow thinness where it helps capability execution, but not where it would destroy knowledge governance.

### 2. Do Not Assume Coordinate-First Interaction Generalizes Everywhere

The screenshot-and-coordinate approach is a strong browser tactic, but it should stay domain-specific.

It is not a universal interaction principle for all agent systems.

### 3. Do Not Treat Live Helper Mutation As A Default Everywhere

Editing helpers during the task is exactly right for this harness.
But that pattern is not always right for more sensitive or larger systems.

The lesson to borrow is:

- capability can evolve through use

not:

- every live task should freely mutate runtime code

## Concrete Workbench Implications

The most reasonable future effects of this case on the current workbench would be:

1. strengthen the distinction between generic interaction patterns and case-local domain patterns
2. keep future tool entrypoints thin unless complexity is clearly paying for itself
3. reinforce a stronger “learn -> write back” expectation in capability areas that grow through real use

## Final Takeaway

`browser-harness` is worth keeping in the case library because it teaches an important substrate lesson:

you do not always need more framework.
Sometimes you need a thinner substrate, stronger verification habits, and a better habit of writing learned patterns back into reusable assets.
