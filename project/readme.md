# Final Stretch: ANSYS Fluent Projects on Stampede3

We are approaching the final stages of your course projects. Since PSC Bridges-2 is currently unavailable, we will use TACC's Stampede3 system to run ANSYS Fluent simulations.

Please complete the following steps as soon as possible. Our goal is to ensure that everyone can access Stampede3, obtain an ANSYS license, and run simulations in parallel.

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

Your username, available SUs, and allocation details will differ. The important part is that you reach the `login*.stampede3` prompt.

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

Submit the request promptly. You will need approved licensing before running Fluent jobs.

## (3) Set up and run ANSYS Fluent simulations on Stampede3

You will perform the geometry preparation, meshing, and initial Fluent setup locally using Virtual Andrew or a CMU computer lab. Only the computationally intensive simulations will run on Stampede3.

### A. Prepare your simulation locally

1\. Import and prepare geometry using SpaceClaim. Open ANSYS Workbench and add a Fluid Flow (Fluent) system. Import your CAD geometry into SpaceClaim, check units, repair gaps, and extract the fluid domain. For external flows, create an enclosure and subtract the solid geometry.

2\. Generate the mesh using ANSYS Meshing. Open the Mesh cell, define named selections for inlets, outlets, and walls, and apply appropriate refinement and boundary-layer inflation. Inspect mesh quality before proceeding.

3\. Configure the simulation in Fluent. Open the Setup cell and specify the physical models, materials, boundary conditions, numerical methods, and convergence monitors.

4\. Initialize and test locally. Run approximately 5–10 iterations to ensure the case initializes properly and identify any setup errors.

5\. Export your Fluent files. Save the initialized simulation as:

- `input.cas.h5` — case definition and mesh
- `input.dat.h5` — initialized solution data

Where possible, use the same ANSYS version locally and remotely. TACC lists ANSYS 2025 R2 on Stampede3, so check compatibility with the version used at CMU.

### B. Prepare a Fluent journal file

A journal file tells Fluent what to do automatically when it runs on Stampede3.

Create a plain-text file named `run.jou` containing:

```
/file/read-case-data input.cas.h5
/solve/iterate 500
/file/write-case-data result.cas.h5
/exit yes
```

This script reads your initialized simulation (`input.cas.h5` and `input.dat.h5`), runs 500 iterations, writes the results (`result.cas.h5` and `result.dat.h5`), and exits.

For your first test on Stampede3, change `500` to `10`.

For transient simulations, replace the `/solve/iterate` line with:

```
/solve/dual-time-iterate 100 30
```

This requests 100 time steps with up to 30 inner iterations per step. Set the time-step size in Fluent beforehand.

Important: Test the journal file locally before transferring it. Set periodic autosaving for longer production simulations, and use a new output filename when restarting calculations to avoid overwriting earlier results.

### C. Transfer your files to Stampede3

From a terminal on your local computer, upload your Fluent case, data, and journal files:

```
scp input.cas.h5 input.dat.h5 run.jou \
YOUR_TACC_USERNAME@stampede3.tacc.utexas.edu:~/
```

This places the files in your Stampede3 home directory. Next, connect to Stampede3:

```
ssh YOUR_TACC_USERNAME@stampede3.tacc.utexas.edu
```

Create a project directory in your scratch space and move the files into it:

```
mkdir -p $SCRATCH/fluent_project
mv ~/input.cas.h5 ~/input.dat.h5 ~/run.jou \
   $SCRATCH/fluent_project/

cd $SCRATCH/fluent_project
ls
```

You should see all three files.

TACC recommends running simulations from `$SCRATCH` rather than `$HOME` or `$WORK`. Files in `$SCRATCH` that go unused for an extended period may be purged, so download your results when a run finishes.

Upload any additional files your case needs the same way, such as boundary-condition profiles, lookup tables, or user-defined functions (UDFs). Windows-compiled UDF libraries cannot be used directly on Stampede3's Linux nodes; compile UDFs on Stampede3 instead.

### D. Set up your parallel submission script

Stampede3 uses the Slurm scheduler. You must submit computational jobs to Slurm rather than running Fluent directly on the login node.

Stampede3 has several CPU configurations:

| Partition | Cores per node | Memory per node |
| --------- | -------------- | --------------- |
| `skx`     | 48             | 192 GB          |
| `icx`     | 80             | 256 GB          |
| `spr`     | 112            | 128 GB HBM      |

For your initial Fluent jobs, I suggest using the `skx` partition, which provides 48 CPU cores per node and sufficient memory for many moderate CFD cases.

First, check the ANSYS installation:

```
module spider ansys
module help ansys
module load ansys
```

Loading the module does not put `fluent` on your `PATH`, so `which fluent` will not find it. The Fluent executable is located at:

```
/home1/apps/ANSYS/2025R2/v252/fluent/bin/fluent
```

Confirm that it exists:

```
ls -l /home1/apps/ANSYS/2025R2/v252/fluent/bin/fluent
```

If the license has been approved, you should be able to launch Fluent using this full path.

#### Example Slurm script (16 CPU processes)

Create `submit.slurm` in your project directory:

```
nano submit.slurm
```

Paste the following:

```
#!/bin/bash
#SBATCH --job-name=fluent_test
#SBATCH --partition=skx
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:30:00
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

If you have multiple allocations, add the following line among the `#SBATCH` directives:

```
#SBATCH --account=YOUR_PROJECT_ID
```

Replace `YOUR_PROJECT_ID` with your applicable ACCESS project.

The Fluent command options have the following meanings:

| Option                     | Purpose                                                       |
| -------------------------- | ------------------------------------------------------------- |
| `3ddp`                     | Three-dimensional, double-precision solver; use `2ddp` for 2D |
| `-g`                       | Run without a graphical interface                             |
| `-t`                       | Specify the number of parallel solver processes               |
| `-cnf=hosts-<jobid>.txt`   | List of compute nodes Fluent should run on (from Slurm)       |
| `-scheduler_custom_script` | Use the environment provided by the custom Slurm script       |
| `-i run.jou`               | Execute the Fluent journal file                               |

ANSYS documents the custom-script option for Slurm jobs. TACC also confirms that ANSYS applications should be launched from a Slurm job without an additional `ibrun` or `mpirun` wrapper.

Note: This is a starting template, not a validated Fluent launch script for Stampede3. TACC's publicly available ANSYS example uses Mechanical rather than Fluent. If Fluent encounters an MPI, host-allocation, or licensing error, send the log and submission script to TACC support for guidance before changing the launch configuration.

### E. Submit a short test

From your Stampede3 project directory:

```
sbatch submit.slurm
```

Slurm will return a job ID, for example:

```
Submitted batch job 1234567
```

Check the job status:

```
squeue -u $USER
```

Inspect the Fluent log:

```
tail -f fluent-1234567.log
```

Replace `1234567` with your actual job ID. If the Fluent log is missing or empty, check `slurm-1234567.out` and `slurm-1234567.err` for errors from Slurm or the module system.

Press `Ctrl+C` to stop watching the log. This does not stop the simulation.

To cancel a running job:

```
scancel 1234567
```

Because Stampede3 charges for whole nodes, this 16-process test is billed the same as a full 48-core node; it is kept small only to make problems easier to diagnose.

For the initial test, verify that Fluent obtains a license, successfully reads the case, launches its parallel processes, completes 10 iterations, and writes the output files.

### F. Submit your production simulations

Once your test succeeds:

1. Edit `run.jou` and increase the iteration count (for example, back to `500`, or however many your case needs to converge).
2. If you are rerunning in the same directory, change the output filename in `run.jou` (for example, `result_run2.cas.h5`) so earlier results are not overwritten.
3. Increase the requested cores and runtime in `submit.slurm`.

For a full 48-core Skylake node, replace the `#SBATCH` lines with:

```
#SBATCH --job-name=fluent_production
#SBATCH --partition=skx
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --time=04:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
```

Keep the rest of the script unchanged.

For larger simulations, two Skylake nodes provide 96 CPU cores. Change the two corresponding lines to:

```
#SBATCH --nodes=2
#SBATCH --ntasks=96
```

Do not immediately use the maximum available number of processors. Establish that the solver runs correctly, then evaluate whether additional cores improve performance.

Allocation considerations: Stampede3 charges for complete compute nodes, even when only part of a node is used. For the `skx` partition, the current charge is 1 SU per node-hour, with a minimum charge of 15 minutes per job. For example, a four-hour simulation using two `skx` nodes consumes approximately 8 SUs.

### G. Download and analyze the results

After the simulation finishes, download both result files to your local machine.

`$SCRATCH` is only defined on Stampede3, so first find the full path of your scratch directory. On Stampede3, run:

```
echo $SCRATCH
```

This prints a path such as `/scratch/01234/YOUR_TACC_USERNAME`. Then, from a terminal on your local computer, download the files using that path:

```
scp "YOUR_TACC_USERNAME@stampede3.tacc.utexas.edu:/scratch/01234/YOUR_TACC_USERNAME/fluent_project/result.*.h5" .
```

Replace the path with the one printed by `echo $SCRATCH`. This copies both `result.cas.h5` and `result.dat.h5` into your current local directory.

Open the results in Fluent through Virtual Andrew or a CMU computer lab workstation. Check convergence, mass and energy conservation, and the physical quantities of interest.

## (4) Documentation and support

- [Stampede3 User Guide](https://docs.tacc.utexas.edu/hpc/stampede3/) — account access, file transfers, allocations, and job submission.
- [TACC ANSYS Documentation](https://docs.tacc.utexas.edu/software/ansys/) — license access, installation, and batch execution.
- [ANSYS Fluent Slurm Documentation](https://ansyshelp.ansys.com/public/Views/Secured/corp/v252/en/pdf/Running_Fluent_Using_a_Load_Manager.pdf) — Fluent launch options and scheduler integration.
- [ANSYS Learning Forum](https://innovationspace.ansys.com/forum/forums/) — meshing, solver configuration, convergence, and Fluent errors.

For Stampede3 account, license, allocation, or cluster-related problems, submit a TACC support ticket. For Fluent setup and solver problems, consult the ANSYS documentation or forum.

Your immediate priorities are to confirm Stampede3 access, submit the ANSYS license request, and prepare your local Fluent simulations. Once license access is granted, each group should submit a small parallel test before beginning its production calculations.