# Visual Standards Guide

Consistent formatting for ANSYS screenshots and figures across the portfolio.

---

## Screenshot Checklist

Before saving any ANSYS screenshot:

- [ ] **Legend visible** — include the color bar with min/max values and units
- [ ] **Title in legend** — shows what quantity is displayed (e.g., "Equivalent (von-Mises) Stress")
- [ ] **Deformation scale noted** — if showing deformed shape, note the scale factor (Auto Scale or True Scale)
- [ ] **Clean background** — use white or dark gray (avoid default gradient)
- [ ] **Orientation visible** — include the coordinate triad (XYZ axes)
- [ ] **No floating toolbars** — hide UI elements that obstruct the model
- [ ] **Consistent zoom** — same part fills roughly the same portion of frame across comparisons

---

## Color Maps

### Stress / Strain / Temperature Contours
- **Default:** Rainbow (ANSYS default) — acceptable for most cases
- **Preferred for portfolio:** Blue-to-Red diverging — more accessible, prints better in grayscale
  - Set in ANSYS: right-click contour → Edit Legend → Color Band
- **For deformation only:** Single-color gradient (blue or gray)

### CFD (Fluent)
- **Velocity:** Rainbow or cool-to-warm (blue = low, red = high)
- **Pressure:** Blue-to-Red diverging (blue = low pressure, red = high)
- **Temperature:** Cool-to-warm (blue = cold, red = hot)
- **Streamlines:** Use contrasting solid color against contour background

---

## Camera Angles

For each simulation, save these standard views:

| View | Purpose | Camera Position |
|------|---------|----------------|
| **Isometric** | Overall shape and context | Default isometric (ANSYS "Iso" button) |
| **Front/Side** | Show loading direction and deformation | Align with primary load direction |
| **Detail** | Stress concentration / weld toe / contact zone | Zoom to critical region |
| **Section cut** | Internal stress distribution | Use Section Planes tool |

Save views to ANSYS named views for consistency across the same model.

---

## Figure Labeling

### File Naming Convention

```
[sim_number]_[description]_[view].png

Examples:
sim_001_cantilever_stress_iso.png
sim_001_cantilever_stress_detail.png
sim_001_cantilever_deformation_front.png
sim_001_cantilever_mesh.png
sim_001_cantilever_convergence.png
```

### Caption Format

Use this format in validation reports:

```markdown
**Figure X:** [Quantity] for [model description]. Max [value] [unit] at [location].
Element type: [type], [count] elements.
```

Example:
> **Figure 3:** Von Mises stress for cantilever beam under 1 kN tip load. Max 142.3 MPa at fixed support. Element type: SOLID186, 8,400 elements.

---

## Convergence Plots

Generated with `scripts/mesh_convergence.py`. Standard format:

- **X-axis:** Element count (log scale)
- **Y-axis:** Quantity of interest (e.g., max stress in MPa)
- **Annotations:** % change between successive refinements
- **Horizontal dashed line:** Converged value
- **Title:** "[Quantity] Mesh Convergence — [Model Name]"
- **Grid:** On (major gridlines)
- **Font:** 12pt minimum for all text (legible in reports)

---

## ANSYS Settings for Screenshots

To get clean screenshots in ANSYS Mechanical:

1. **Background:** View → Background → Solid Color → White
2. **Edge display:** For mesh screenshots, show element edges. For contour plots, edges off.
3. **Resolution:** Use "Image to File" (not Print Screen) — set to 1920×1080 minimum
4. **Format:** PNG (lossless). Avoid JPEG for technical figures.
5. **Legend:** Ensure number format shows enough significant digits (3–4)

---

## Portfolio Presentation Tips

- Use the same color map across all sims of the same type (all stress plots use same scheme)
- When comparing before/after or different designs, use the same contour range (lock min/max)
- Include the mesh screenshot alongside stress results — shows reviewer you thought about mesh quality
- For mode shapes, show wireframe overlay on deformed shape
- For CFD, include both contour and streamline views

---

*Template: templates/visual_guide.md*
