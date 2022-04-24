
  The University of Texas at Austin
  COE 347
  Instructor: F. Bisetti (fbisetti@utexas.edu)


  -- OpenFOAM files for the flow around a circular cylinder --

  0/: Folder with initial conditions and boundary conditions,
      U free stream is 1 m/s

  system/: Folder with system files, including decomposeParDict
           probes.template and singleGraph.template

  constant/transportProperties.template:  transport properties file
  system/blockMeshDict.template: blockMeshDict template file


  -- Note on time step size, final time, and write intervals  --

  The case is setup to solve the incompressible Navier-Stokes equations
  with the solver icoFoam, either in serial (1 core) or parallel (multple cores/nodes).

  The user will need to set the following 3 variables in system/controlDict

  endTime         XXXX;
  deltaT          XXXX;
  writeInterval   XXXX;

  * Select the time step size ``deltaT'' so that ``Courant Number max'' (see log.icoFoam) remains
    below 0.5 at all times. Note that when the mesh (and cell sizes) changes, you may need to
    adjust the time step size.

    Decreasing deltaT will reduce the Courant Number by the same factor. Decreasing the cell sizes
    by a factor (for example, increasing the cell count) will increase the Courant Number by the same
    factor.

    ** IMPORTANT ** If the time step size is too large (and the Courant Number much greater than 0.5 or so,)
    you will notice that icoFoam fails catastrophically because the numerical solution grows unstable.
    Try lowering the time step size to remedy such occurrence.

  * Select the end time ``endTime'' so that the velocity and pressure fields are no longer changing
    if the flow is steady. Recall that one time unit corresponds to the time taken at the free stream
    velocity (set to 1 m/s) to traverse a distance equal to the diameter of the circular cylinder
    (set to 1 m).

  * Adjust the time between I/O (solution write) by setting ``writeInterval.''
  

  -- More resources --

  See Canvas OpenFOAM assignment page for more links and resources

