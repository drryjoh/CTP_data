# ACCESS Explore Proposal Template (one per team)

Use this template to request an **Explore ACCESS** allocation for your team's course project. One team member submits the request as PI; the others are added to the project as users after it is approved.

Replace everything in `[square brackets]` with your team's details, and delete these instructions before submitting. Keep the summary under one page.

When you request an Explore project, ACCESS asks for:

| Item | Where it comes from |
| --- | --- |
| Title | Section 1 below |
| Keywords | Section 2 below |
| Field of science | Section 3 below |
| Supporting grant | None; this is a course project (Section 4) |
| Summary of planned work | Section 5 below (paste into the request form) |
| CV or résumé of the PI (and any co-PIs) | One-page PDF résumé from the submitting team member |
| Advisor letter (graduate-student PI) | Signed letter from the course instructor on CMU letterhead, provided by Professor Ryan Johnson; email him your PI's name and project title |

---

## 1. Title

CFD Simulation of [Short Description of Your Flow Problem] Using ANSYS Fluent

*Examples: "CFD Simulation of Flow Over a Ground-Effect Rear Wing Using ANSYS Fluent"; "CFD Simulation of Mixing in a Planar Turbulent Jet Using ANSYS Fluent".*

## 2. Keywords

Computational fluid dynamics; ANSYS Fluent; turbulence modeling; [keyword specific to your problem, e.g. aerodynamics, heat transfer, multiphase flow]; [second specific keyword]

## 3. Field of science

Mechanical Engineering (or Fluid, Particulate, and Hydraulic Systems)

## 4. Supporting grant

None. This work is a graduate course project in 24-618 Computational Analysis of Transport Phenomena, Department of Mechanical Engineering, Carnegie Mellon University, taught by Professor Ryan Johnson, Fall 2026.

## 5. Summary of planned work

**Objectives.** Our team of [number] graduate students in Mechanical Engineering at Carnegie Mellon University will use computational fluid dynamics (CFD) to study [one-sentence description of the flow problem, e.g. "the aerodynamic forces on a rear wing operating in ground effect"]. The goal is to [primary objective, e.g. "quantify how lift and drag vary with ride height and angle of attack"] and to [secondary objective, e.g. "assess the sensitivity of the results to mesh resolution and turbulence model"]. This work is the final project for 24-618 Computational Analysis of Transport Phenomena and will be completed by the end of the semester in December 2026.

**Methods and software.** Geometry and meshing will be prepared on Carnegie Mellon computers using ANSYS SpaceClaim and ANSYS Meshing. The simulations will be solved with ANSYS Fluent 2025 R2, using the academic license provided by TACC on Stampede3. We will solve the [steady / transient] Reynolds-averaged Navier–Stokes equations with the [turbulence model, e.g. k–ω SST] turbulence model [add other physics if relevant, e.g. energy equation, species transport]. We will run each case in parallel using Fluent's built-in MPI on Stampede3's Skylake (`skx`) nodes, and download the results for post-processing on our local machines.

**Computational plan.** We will:

1. Perform a mesh-independence study using [3] meshes of approximately [0.5, 1.5, and 4] million cells.
2. Run a parametric study of [number] cases, varying [parameter(s), e.g. "angle of attack (4 values) and ride height (3 values)"].
3. Repeat [number] cases with [an alternative turbulence model / a finer mesh] to assess modeling uncertainty.

This is about [total number] simulations in all.

**Resource needs.** Based on a short test run on Stampede3, we expect each case to take about [2–4] hours on one 48-core `skx` node, with the finest meshes using up to two nodes. Our estimate:

| Activity | Runs | Node-hours per run | Node-hours |
| --- | --- | --- | --- |
| Testing and debugging | [5] | [0.5] | [2.5] |
| Mesh-independence study | [3] | [4] | [12] |
| Parametric study | [12] | [4] | [48] |
| Model sensitivity | [4] | [4] | [16] |
| Contingency for reruns (~25%) | | | [20] |
| **Total** | | | **[~100] node-hours** |

At 1 SU per node-hour on `skx`, this is about [100] Stampede3 SUs, well within the scope of an Explore allocation. Case and result files are expected to total under [50] GB and will be kept in Stampede3 scratch storage during the project, then copied to Carnegie Mellon storage. No GPUs or large-memory nodes are required.

**Team.** [PI Name] (PI, graduate student), [Team Member 2], [Team Member 3], [Team Member 4]. All team members are Mechanical Engineering graduate students at Carnegie Mellon University and will be added as users on the allocation. The course instructor, Professor Ryan Johnson, is supervising the computational work.

---

## After approval

1. In the [ACCESS allocations portal](https://allocations.access-ci.org/), add your teammates to the project as users.
2. Exchange ACCESS Credits for **TACC Stampede3** time. Use the [ACCESS exchange calculator](https://allocations.access-ci.org/exchange_calculator) to convert your node-hour estimate.
3. Set `#SBATCH --account=YOUR_PROJECT_ID` in `submit.slurm` (see the readme, Section 7).
