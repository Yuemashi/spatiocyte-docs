A guide to modeling reaction-diffusion of molecules with Spatiocyte
===================================================================

| Satya N. V. Arjunan
| satya@riken.jp
| RIKEN Quantitative Biology Center, Furuedai, Suita, Osaka 565-0874, Japan

Abstract
---------

The E-Cell System is an advanced platform intended for mathematical
modeling and simulation of well-stirred biochemical systems. We have
recently implemented the Spatiocyte method as a set of plug in modules
to the E-Cell System, allowing simulations of complicated
multicompartment dynamical processes with inhomogeneous molecular
distributions. With Spatiocyte, the diffusion and reaction of each
molecule can be handled individually at the microscopic scale. Here we
describe the basic theory of the method and provide the installation and
usage guides of the Spatiocyte modules. Where possible, model examples
are also given to quickly familiarize the reader with spatiotemporal
model building and simulation.

Keywords: spatial modeling, stochastic simulation, diffusion, membrane,
multicompartment, intercompartment, Spatiocyte

Introduction
-------------

The E-Cell System version 3 can model and simulate both deterministic
and stochastic biochemical processes (Takakashi et al., 2004). Simulated
molecules are assumed to be dimensionless and homogeneously distributed
in a compartment. Some processes such as cell signaling and cytokinesis,
however, depend on cellular geometry and spatially localized molecules
to carry out their functions. To reproduce such processes using
spatially resolved models in silico, we have developed a lattice-based
stochastic reaction-diffuson (RD) simulation method, called Spatiocyte
(Arjunan and Tomita, 2010), and implemented it as a set of plug in
modules to the E-Cell System (Arjunan and Tomita, 2009). Spatiocyte
allows diffusion and reaction to take place between different
compartments: for example, a volume molecule in the cytoplasm can
diffuse and react with a surface molecule on the plasma membrane. Since
molecules are represented as spheres with dimensions, it can also
reproduce anomalous diffusion of molecules in a crowded compartment (Dix
and Verkman, 2008, Hall and Hoshino, 2010). Using Spatiocyte simulated
microscopy visualization feature, simulation results of spatiotemporal
localization of molecules can be evaluated by directly comparing them
with experimentally obtained fluorescent microscopy images.

 

The theory and algorithm of the Spatiocyte method are provided in
(Arjunan and Tomita, 2010) while the implementation details are
described in (Arjunan and Tomita, 2009). In this chapter, we provide a
guide on how to build spatiotemporal RD models using Spatiocyte modules.
We begin with the basic theory of the method and proceed with the
installation procedures. The properties of each  module are outlined in
the subsequent section. Some example models are given to familiarize the
reader with the common model structures while describing the modules. We
conclude this chapter by outlining the planned future directions of
Spatiocyte development.


