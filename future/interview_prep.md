# FEA Interview Prep

How to talk about simulation work in technical and behavioral interviews. Organized by question type.

---

## The Core Message

You're not selling "I know ANSYS." You're selling: **I can set up a simulation, verify it's correct, and explain why I trust the result.** That's engineering judgment, and it's what separates you from someone who watched a tutorial.

Lead with the validation, not the software.

---

## Technical Questions

### "Walk me through how you'd approach a new FEA problem."

**Framework (use this every time):**

1. Understand the engineering question — what quantity do I need? What decisions depend on it?
2. Hand calculation — estimate the answer before touching the software. Sets expectations and catches gross errors.
3. Model setup — choose analysis type, element type, simplifications. Justify each choice.
4. Mesh — start coarse, refine at critical regions, run convergence study.
5. Solve — check convergence, reaction forces, energy balance.
6. Validate — compare to hand calc. If error is large, investigate systematically (mesh, BCs, material, assumptions).
7. Document — report the result, the error, and what I'd do differently.

**Example answer:**
> "For the welded bracket project, I started with a hand calc using Shigley's weld stress formula — τ = F over 0.707 h l — which gave me 47 MPa. Then I built the model in ANSYS with SOLID186 elements, bonded contact at the weld, and ran a mesh convergence study. The FEA gave 49.2 MPa at the weld toe — 4.7% error, which I was comfortable with given the simplifications in the hand calc. I documented the full comparison in a validation report."

### "What element type would you use for [X]?"

Refer to `checklists/element_guide.md`. Key talking points:

- **Thin-walled structures** → shell elements (SHELL181/281). Mention: "I'd check t/L ratio first."
- **Solid parts, simple geometry** → hex (SOLID186) with mapped mesh. "Hex converge faster than tet."
- **Complex geometry** → tet (SOLID187) with local refinement. "I'd refine near stress concentrations."
- **Beams/frames** → beam elements (BEAM188) for quick checks, solid for detailed stress.
- **Always quadratic** → "Quadratic elements capture stress gradients. Linear tets are too stiff."

The key is to **justify the choice**, not just name the element.

### "How do you know your mesh is fine enough?"

> "I run a mesh convergence study. I start coarse, double the element count, re-solve, and compare the quantity of interest. When the result changes less than 2% between refinements, I call it converged. I also refine locally at stress concentrations rather than globally — it's more efficient."

**Follow-up they might ask:** "What if the stress keeps going up and never converges?"
> "That's a stress singularity — a sharp re-entrant corner or point load. The mesh will never converge there because the theoretical stress is infinite. I'd either add a fillet to the geometry to make it realistic, or extract the stress slightly away from the singularity. It depends on whether the singularity exists in the real part."

### "How do you handle contact in FEA?"

> "I start with the simplest model that captures the physics. Bonded contact if the parts are welded or glued. Frictional contact if there's sliding — I specify the friction coefficient and check that it matches the material pair. I always check the contact status after solving to make sure surfaces are behaving as expected — sticking where they should, separating where they should."

### "What's the difference between linear and nonlinear analysis?"

> "Linear assumes small deformations, linear elastic material, and no contact status changes. It's fast and the answer is proportional to the load — double the load, double the stress. Nonlinear covers everything else: plasticity, large deformation, changing contact. It's iterative — ANSYS uses Newton-Raphson — so it's slower and can fail to converge. I only go nonlinear when the linear assumptions are violated, like stresses above yield or deformations larger than 10% of the characteristic dimension."

### "Explain your validation approach."

> "I compute the expected answer analytically before running the simulation — that's key, because if I run ANSYS first, I'll rationalize any result. Then I compare the FEA result to the hand calc and compute percent error. For simple structural problems I target under 5%, for CFD under 10%, for fatigue I'm happy within a factor of 2 since scatter is inherently large. If the error is bigger than expected, I investigate systematically: mesh convergence, BCs, material properties, then assumptions."

---

## Behavioral Questions

### "Tell me about a time a simulation didn't match your expectations."

**Use the STAR format.** Pull from your post-mortems (templates/post_mortem.md).

> **Situation:** "I was modeling a simply supported beam and expected the ANSYS deflection to match PL³/48EI within 5%."
> **Task:** "The result was off by 18%, which was way outside my threshold."
> **Action:** "I investigated systematically. First I checked the mesh — it was converged. Then I checked the BCs and found I'd applied the support on the wrong edge — it was partially constrained, so it was acting stiffer than simply supported. I corrected the BC."
> **Result:** "After the fix, error dropped to 2.3%. I added a checklist item: visually verify BC application in the viewport before solving. That's now part of my pre-solve workflow."

The point: **show the debugging process**, not just the fix.

### "Tell me about a project you're proud of."

Walk through your best case study. Hit these points:
1. The engineering question (not "I used ANSYS" — "I needed to determine if this weld would survive 10⁶ cycles")
2. One interesting decision you made (element type, modeling simplification, validation approach)
3. The result and how you validated it
4. What you learned or would do differently

### "How do you handle uncertainty in your results?"

> "Every simulation has sources of error — mesh discretization, material property uncertainty, modeling simplifications. I address mesh error through convergence studies. For material properties, I use textbook values and note the source. For modeling simplifications — like using a 2D model for a 3D problem — I document the assumption and estimate its effect. If I'm not confident, I run a sensitivity study: vary the uncertain parameter by ±10% and see how much the result changes."

---

## Questions to Ask Them

Show you think like an engineer, not just a software user:

- "What solver do you use for [structural/CFD]? And do you have established V&V procedures?"
- "What's a typical mesh size for your models? Thousands of elements or millions?"
- "Do you use scripting/automation for parametric studies, or is it mostly GUI-driven?"
- "What's the path from simulation results to a design decision? Who reviews the analysis?"
- "Do you correlate simulation with physical testing?"

---

## Portfolio Talking Points

When they look at your GitHub Pages site:

| They see... | You say... |
|-------------|-----------|
| Contour plot | "The max stress is 142 MPa at the fillet — I validated that against σ = My/I which gave 140 MPa, so 1.4% error." |
| Convergence plot | "I refined the mesh 5 times until the result stabilized within 2%." |
| Hand calc notebook | "I compute the analytical solution in Python before running ANSYS, so I have an independent check." |
| Cross-solver comparison | "I ran the same problem in ANSYS and [LS-DYNA/Abaqus] to show the result is solver-independent." |
| Post-mortem | "This one didn't work the first time — here's what went wrong and what I changed." |

The post-mortems are often the most impressive piece. They show you can learn from mistakes.

---

## Red Flags to Avoid

Things that make interviewers doubt your simulation skills:

- "ANSYS gave me this result" — without explaining why you trust it
- "I used the default mesh" — implies you didn't check convergence
- "The error was 25% but that's close enough" — without justification
- Talking about software features instead of engineering judgment
- Not knowing what element type you used or why
- "I used Von Mises stress" without knowing what it represents

---

## One-Page Cheat Sheet

Before any interview, review:

1. Your V&V workflow (methodology.md) — be able to recite it
2. Your best case study — rehearse the 2-minute version
3. Your best post-mortem — the "debugging story" is gold
4. Element selection basics (checklists/element_guide.md)
5. Mesh convergence (what it is, when it fails, stress singularities)
6. Linear vs nonlinear (when to switch)
7. Your questions for them (above)
