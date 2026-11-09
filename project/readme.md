# Final Stretch: ANSYS Fluent Projects on Stampede3

We are approaching the final stages of your course projects. Since PSC Bridges-2 is currently unavailable, we will use TACC's Stampede3 system to run ANSYS Fluent simulations.

Please complete the following steps as soon as possible. Our goal is to ensure that everyone can access Stampede3, obtain an ANSYS license, and run simulations in parallel.

The steps are:

1. Log in to Stampede3.
2. Request access to ANSYS.
3. Confirm that you have ANSYS access.
4. Run a short test case provided by ANSYS, using the [sample submission script](submit.slurm).
5. Adapt the test script to run your own project case.
6. Apply for an ACCESS allocation for your team (Section 7). One application per team. Do this **now**, alongside steps 1–2, because approval takes time.

You do not have ANSYS access yet. TACC grants it only after you request it (Section 2), so submit that request first. Steps 3 and 4 will not work until TACC approves it.

## (1) Confirm your Stampede3 access

TACC (Texas Advanced Computing Center) operates several HPC systems, including Stampede3. You should now have access to Stampede3 through your ACCESS allocation.

Step 1: Connect through your terminal.

Open Terminal on your computer and enter:

```
ssh YOUR_TACC_USERNAME@stampede3.tacc.utexas.edu
```

Use your TACC username, which I previously suggested keeping the same as your ACCESS username.

Step 2: Authenticate.

You will be prompted for your TACC password, followed by a TACC token code.

Open the Duo Mobile app and locate the six-digit code associated with TACC Third Party MFA.

If you have trouble authenticating, visit the [TACC Account Portal](https://accounts.tacc.utexas.edu/), sign in, and navigate to the multifactor authentication settings. You can unpair and re-pair your authenticator if necessary.

Step 3: Confirm successful login.

After authentication, you should see a project allocation summary, disk quota information, and a terminal prompt similar to:

```
---------------- Project balances ----------------
Name             Avail SUs      Expires
TG-PHY260370         1109       2027-08-18

---------------- Disk quotas ---------------------
/scratch
/home1
/work

login3.stampede3(1)$
```

`TG-PHY260370` is the **class allocation**, which you have been added to so you can get started. Its SUs are shared by everyone in the class and will not cover everyone's production runs, so each **team** must also apply for its own ACCESS allocation as soon as possible (Section 7).

Your username and disk details will differ. The important part is that you reach the `login*.stampede3` prompt.

If you cannot log in, resolve that issue before continuing.

## (2) Request access to ANSYS on Stampede3

TACC provides ANSYS for non-commercial academic research and educational use, but you must request license access separately.

Every student who will submit ANSYS jobs must complete this step.

1. Visit [TACC ANSYS Documentation](https://docs.tacc.utexas.edu/software/ansys/) and follow the link to submit a help desk ticket.
2. Select Running Jobs or Using TACC Resources.
3. Select Stampede3 as the system.
4. Use the following subject and message.

**Subject: ANSYS Academic License Request for Stampede3**

Hello,

I am a Carnegie Mellon University student in Mechanical Engineering taking a graduate course that uses ANSYS Fluent. For our final project, my team would like to use our ACCESS allocation to run parallel ANSYS Fluent simulations on Stampede3.

All use will be strictly non-commercial and academic. We expect to run simulations through the end of the semester in December.

Could I please be granted access to the ANSYS Fluent license on Stampede3?

Thank you,\
[Your Name]

Submit the request promptly. You will need approved licensing before running Fluent jobs. TACC will reply to your ticket when access has been granted; until then, Sections 3 and 4 will not work.

## (3) Confirm that you have ANSYS access

Log in to Stampede3 (Section 1), then run:

```
module load ansys
groups
```

`groups` lists the Unix groups your account belongs to. Once your ANSYS license request is approved, the list should include `G-815296`, the group that owns the ANSYS installation, for example:

```
G-829645 G-815296
```

Your other group number will differ. If `G-815296` is missing, your request is probably still pending; wait for TACC to reply to your ticket.

Next, confirm that the Fluent executable is available:

```
ls -l /home1/apps/ANSYS/2025R2/v252/fluent/bin/fluent
```

You should see a line ending in `/home1/apps/ANSYS/2025R2/v252/fluent/bin/fluent`.

Note: `module load ansys` does not add `fluent` to your `PATH`, so typing `fluent` or `which fluent` will not find it. Always use the full path above. The scripts in this guide already do.

## (4) Run the ANSYS test case

ANSYS ships a small example case with the Stampede3 installation (the fluid side of an oscillating-plate tutorial, about 3,000 cells). Running it confirms that you can obtain a license, launch Fluent in parallel on a compute node, read a case, iterate, and write results. It takes under a minute and costs at most 0.25 SU.

The test case has no flow on its own, so the solver reports convergence on the first iteration. That is expected; the point is to confirm that everything runs.

### A. Create a test directory and copy the case

On Stampede3, run:

```
mkdir -p $SCRATCH/fluent_test
cd $SCRATCH/fluent_test
cp /home1/apps/ANSYS/2025R2/v252/SystemCoupling/examples/oscillating-plate/Fluid/plate_fluid.cas.h5 input.cas.h5
```

TACC recommends running simulations from `$SCRATCH` rather than `$HOME` or `$WORK`. Files in `$SCRATCH` that go unused for an extended period may be purged, so download results you want to keep.

### B. Download the journal file and submission script

Two files are provided in this repository:

- [`run.jou`](run.jou): the Fluent journal file
- [`submit.slurm`](submit.slurm): the sample Slurm submission script

Download both directly into your test directory on Stampede3:

```
curl -O https://raw.githubusercontent.com/drryjoh/CTP_data/main/project/run.jou
curl -O https://raw.githubusercontent.com/drryjoh/CTP_data/main/project/submit.slurm
```

A journal file tells Fluent what to do when it runs without a graphical interface. `run.jou` contains:

```
/file/read-case input.cas.h5
/mesh/check
/solve/initialize/initialize-flow
/solve/iterate 10
/file/write-case-data result.cas.h5
/exit yes
```

This reads the case, checks the mesh, initializes the solution, runs 10 iterations, writes `result.cas.h5` and `result.dat.h5`, and exits.

### C. The Slurm submission script

Stampede3 uses the Slurm scheduler. Never run Fluent directly on the login node; always submit it as a job. The commands in [`submit.slurm`](submit.slurm) (leaving out its header comments) are:

```
#!/bin/bash
#SBATCH --job-name=fluent_test
#SBATCH --partition=skx
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:10:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

set -euo pipefail

module load ansys

cd "$SLURM_SUBMIT_DIR"

FLUENT=/home1/apps/ANSYS/2025R2/v252/fluent/bin/fluent

# List the compute nodes assigned to this job so Fluent knows where to run
scontrol show hostnames "$SLURM_JOB_NODELIST" > "hosts-${SLURM_JOB_ID}.txt"

"$FLUENT" 3ddp -g -t"${SLURM_NTASKS}" \
    -cnf="hosts-${SLURM_JOB_ID}.txt" \
    -scheduler_custom_script \
    -i run.jou > "fluent-${SLURM_JOB_ID}.log" 2>&1
```

While you only have the class allocation, jobs are charged to it automatically. Once your team has its own allocation (Section 7), you will belong to two projects. In that case, tell Slurm which to charge by changing the commented-out line in `submit.slurm` from `##SBATCH --account=YOUR_PROJECT_ID` to:

```
#SBATCH --account=YOUR_PROJECT_ID
```

replacing `YOUR_PROJECT_ID` with your team's project ID. Use your team's allocation for production runs.

What the script does:

| Line                           | Purpose                                                          |
| ------------------------------ | ---------------------------------------------------------------- |
| `--partition=skx`              | Skylake nodes: 48 cores and 192 GB of memory per node            |
| `--nodes`, `--ntasks`          | Number of nodes and total Fluent processes                       |
| `--time`                       | Maximum run time (hh:mm:ss); the job is stopped when it runs out |
| `scontrol show hostnames ...`  | Writes the list of assigned nodes to a host file                 |
| `3ddp`                         | 3D, double-precision solver (use `2ddp` for 2D cases)            |
| `-g`                           | Run without a graphical interface                                |
| `-t`                           | Number of parallel Fluent processes (taken from `--ntasks`)      |
| `-cnf=hosts-<jobid>.txt`       | Tells Fluent which nodes to run on                               |
| `-scheduler_custom_script`     | Tells Fluent it is being launched from a Slurm script            |
| `-i run.jou`                   | Runs the journal file                                            |

Do not wrap the Fluent command in `ibrun` or `mpirun`; Fluent starts its own MPI processes.

### D. Submit the job

```
sbatch submit.slurm
```

Slurm prints a series of checks and ends with your job ID:

```
--> Checking available allocation (TG-PHY260370)...OK
...
Submitted batch job 3699109
```

Your job ID will differ. Use it in place of `3699109` below.

### E. Check the job

While the job is waiting or running:

```
squeue -u $USER
```

Once it no longer appears in `squeue`, check how it ended:

```
sacct -j 3699109 -o JobID,State,Elapsed,ExitCode
```

A successful run shows `COMPLETED` and exit code `0:0`.

To follow the Fluent log while the job runs (press `Ctrl+C` to stop watching; this does not stop the job):

```
tail -f fluent-3699109.log
```

To cancel a job:

```
scancel 3699109
```

### F. Confirm that the test succeeded

List the directory:

```
ls
```

You should see `result.cas.h5` and `result.dat.h5`, along with the log, host file, Slurm output files, and a `fluent-<date>-<time>.trn` transcript that Fluent writes automatically.

Then check the log for the key steps:

```
grep -E "License Server|Host spawning|Writing to|Total Transcript" fluent-3699109.log
```

A successful run includes lines like:

```
Connected License Server List:  1055@license03.tacc.utexas.edu
Host spawning Node 0 on machine "c479-024.stampede3.tacc.utexas.edu" (unix).
Writing to c479-024...:"/scratch/.../fluent_test/result.cas.h5" in NODE0 mode ...
Writing to c479-024...:"/scratch/.../fluent_test/result.dat.h5" in NODE0 mode ...
Total Transcript Time: 0 Minute 24 Second.
```

A warning such as `reading 4 partition grid onto 16 compute node machine` is normal; Fluent repartitions the mesh automatically.

If the run fails:

- A license error in `fluent-<jobid>.log` means your ANSYS access has not been approved yet (Section 2).
- If the Fluent log is missing or empty, check `slurm-<jobid>.out` and `slurm-<jobid>.err` for errors from Slurm or the module system.
- For anything else, open a TACC support ticket and attach `submit.slurm`, `run.jou`, and the log files.

Once this test succeeds, you are ready to run your own case.

## (5) Run your own case

Prepare your geometry, mesh, and Fluent setup locally using Virtual Andrew or a CMU computer lab. Only the computationally intensive solve runs on Stampede3.

### A. Prepare your case locally

1. **Geometry (SpaceClaim).** In ANSYS Workbench, add a Fluid Flow (Fluent) system. Import your CAD geometry into SpaceClaim, check units, repair gaps, and extract the fluid domain. For external flows, create an enclosure and subtract the solid geometry.
2. **Mesh (ANSYS Meshing).** Define named selections for inlets, outlets, and walls, and apply appropriate refinement and boundary-layer inflation. Inspect mesh quality before proceeding.
3. **Setup (Fluent).** Specify the physical models, materials, boundary conditions, numerical methods, and convergence monitors.
4. **Test locally.** Initialize and run 5–10 iterations to catch setup errors.
5. **Export.** Save the initialized simulation as `input.cas.h5` (case and mesh) and `input.dat.h5` (initialized solution).

Stampede3 runs ANSYS 2025 R2. Where possible, use the same version locally, or check that your local version's files can be read by 2025 R2.

### B. Upload your files

From a terminal on your local computer:

```
scp input.cas.h5 input.dat.h5 YOUR_TACC_USERNAME@stampede3.tacc.utexas.edu:~/
```

Then, on Stampede3, create a project directory and move the files into it:

```
mkdir -p $SCRATCH/fluent_project
mv ~/input.cas.h5 ~/input.dat.h5 $SCRATCH/fluent_project/
cd $SCRATCH/fluent_project
```

Upload any additional files your case needs the same way, such as boundary-condition profiles, lookup tables, or user-defined functions (UDFs). Windows-compiled UDF libraries cannot be used on Stampede3's Linux nodes; compile UDFs on Stampede3 instead.

Download the sample [`submit.slurm`](submit.slurm) as a starting point:

```
curl -O https://raw.githubusercontent.com/drryjoh/CTP_data/main/project/submit.slurm
```

### C. What to change from the test case

Start from the test-case `run.jou` and `submit.slurm` and change only the following.

**In `run.jou`:**

| Change                         | Test case                    | Your case                                                                                     |
| ------------------------------ | ---------------------------- | --------------------------------------------------------------------------------------------- |
| Read case **and** data         | `/file/read-case input.cas.h5` | `/file/read-case-data input.cas.h5` (also reads `input.dat.h5`)                             |
| Mesh check and initialization  | `/mesh/check` and `/solve/initialize/initialize-flow` | Remove both; your case was already initialized locally                 |
| Number of iterations           | `/solve/iterate 10`          | Keep `10` for your first run, then increase (for example, `500`) once it works                |
| Transient cases                | —                            | Replace `/solve/iterate` with `/solve/dual-time-iterate 100 30` (100 time steps, up to 30 inner iterations each); set the time-step size in Fluent beforehand |
| Output filename                | `result.cas.h5`              | Use a new name for each run (for example, `result_run2.cas.h5`) so earlier results are not overwritten |

For your first run, `run.jou` should look like:

```
/file/read-case-data input.cas.h5
/solve/iterate 10
/file/write-case-data result.cas.h5
/exit yes
```

For long runs, set up periodic autosaving in Fluent before exporting your case, so a run that hits its time limit still leaves usable results.

**In `submit.slurm`:**

| Change              | Test case                  | Your case                                                                     |
| ------------------- | -------------------------- | ----------------------------------------------------------------------------- |
| Job name            | `--job-name=fluent_test`   | Any name, for example `--job-name=fluent_project`                             |
| Solver              | `3ddp`                     | `3ddp` for 3D cases, `2ddp` for 2D cases                                      |
| Cores               | `--ntasks=16`              | `--ntasks=48` for a full `skx` node                                           |
| Nodes               | `--nodes=1`                | Keep `1` unless your case is large; `--nodes=2` with `--ntasks=96` for two nodes |
| Run time            | `--time=00:10:00`          | Long enough for your run, for example `--time=04:00:00`                       |
| Allocation          | (class allocation)         | `#SBATCH --account=YOUR_PROJECT_ID` once your team has its own allocation (Section 7) |

Everything else in the script stays the same.

Do not jump straight to the largest job. First run your case for 10 iterations on one node, exactly like the test. Once that works, increase the iterations and run time. Only move to two nodes if one node is too slow, and check that the extra cores actually make it faster.

**Allocation cost.** Stampede3 charges for whole nodes, even if you use fewer cores, at 1 SU per node-hour on `skx`, with a 15-minute minimum per job. For example, a four-hour run on two `skx` nodes uses about 8 SUs. The class allocation (`TG-PHY260370`) is shared by everyone, so use it only for testing and run production jobs on your team's allocation.

### D. Download and analyze your results

`$SCRATCH` is only defined on Stampede3, so first find the full path of your scratch directory. On Stampede3, run:

```
echo $SCRATCH
```

This prints a path such as `/scratch/01234/YOUR_TACC_USERNAME`. Then, from a terminal on your local computer, download both result files using that path:

```
scp "YOUR_TACC_USERNAME@stampede3.tacc.utexas.edu:/scratch/01234/YOUR_TACC_USERNAME/fluent_project/result.*.h5" .
```

Open the results in Fluent through Virtual Andrew or a CMU computer lab workstation. Check convergence, mass and energy conservation, and the physical quantities of interest.

## (6) Documentation and support

- [Stampede3 User Guide](https://docs.tacc.utexas.edu/hpc/stampede3/) — account access, file transfers, allocations, and job submission.
- [TACC ANSYS Documentation](https://docs.tacc.utexas.edu/software/ansys/) — license access, installation, and batch execution.
- [ANSYS Fluent Slurm Documentation](https://ansyshelp.ansys.com/public/Views/Secured/corp/v252/en/pdf/Running_Fluent_Using_a_Load_Manager.pdf) — Fluent launch options and scheduler integration.
- [ANSYS Learning Forum](https://innovationspace.ansys.com/forum/forums/) — meshing, solver configuration, convergence, and Fluent errors.

For Stampede3 account, license, allocation, or cluster problems, submit a TACC support ticket. For Fluent setup and solver problems, consult the ANSYS documentation or forum.

## (7) Apply for your team's ACCESS allocation

The class allocation is only for getting started and testing. **Each team** should apply for its own allocation **as soon as possible**. Only one application is needed per team. Review typically takes a few business days, and you will need the time for your production runs.

ACCESS allocations are awarded in ACCESS Credits, which you then exchange for time on a specific system (here, Stampede3). An Explore project, the smallest type, is enough for a course project; ACCESS lists graduate student projects among its intended uses (see [ACCESS project types](https://allocations.access-ci.org/project-types)).

### A. Decide who applies

Choose one team member to submit the request as **PI**. The other team members are added to the project as users once it is approved.

### B. Prepare the request

Fill in the [ACCESS proposal template](access_proposal_template.md) with your team's project details. It covers everything ACCESS asks for in an Explore request:

- project title, keywords, and field of science;
- a summary of the planned work, with an estimate of the Stampede3 time you need;
- supporting grant: none (this is a course project).

You will also need:

- **A CV or résumé for the PI**, as a PDF. A one-page résumé is fine.
- **An advisor letter.** Because the PI is a graduate student, ACCESS requires a signed letter from an advisor on institutional letterhead. I will provide this letter for each team. Email me the PI's name and your project title, and I will send you a signed PDF to upload.

### C. Submit and set up the allocation

1. **Sign in** at [ACCESS Allocations](https://allocations.access-ci.org/) with the PI's ACCESS ID and select **New Project**, then **Explore ACCESS**. Copy in the details from your completed template and upload the résumé and letter.
2. **Wait for approval.** ACCESS will email the PI when the project is approved, along with a project ID (for example, `TG-XXX000000`).
3. **Add your teammates.** In the allocations portal, add each team member to the project as a user, using their ACCESS ID.
4. **Exchange credits for Stampede3 time.** In the allocations portal, open the project, choose to exchange credits, select **TACC Stampede3**, and request the SUs you estimated in your proposal. The [ACCESS exchange calculator](https://allocations.access-ci.org/exchange_calculator) shows how many Stampede3 SUs your credits buy. You can exchange more of your remaining credits later.
5. **Confirm on Stampede3.** Once the exchange is processed, the new project appears in the "Project balances" table when each team member logs in.
6. **Charge your jobs to it.** Uncomment the account line in `submit.slurm` and set it to your team's project ID (Section 4C):

   ```
   #SBATCH --account=TG-XXX000000
   ```

## Your immediate priorities

1. Log in to Stampede3 (Section 1).
2. Submit the ANSYS license request to TACC (Section 2). Every student does this.
3. As a team, choose a PI, fill in the [proposal template](access_proposal_template.md), and email me for the advisor letter (Section 7). One per team.
4. Once TACC approves your ANSYS access, run the test case (Section 4).
