Installing and Running Spatiocyte
=================================

The Spatiocyte source code is distributed as open-source software under
the GNU General Public License and is available at GitHub. At the time
of writing, the Spatiocyte has been tested to run on Linux and Mac OS X systems. 

Ubuntu Linux
------------

Spatiocyte has been tested to run well on Ubuntu Linux. On a freshly installed Ubuntu, Spatiocyte requires several additional packages. To install these packages and Spatiocyte, open a terminal and execute the following instructions:

::

  $ wget https://raw.githubusercontent.com/ecell/spatiocyte/master/install-spatiocyte-ubuntu.sh
  $ sh -x install-spatiocyte-ubuntu.h


Mac OSX
-------

Spatiocyte has been tested to run on the Yosemite Mac OS X system. Spatiocyte requires XQuartz and several additional packages. We recommend using homebrew to manage packages. To install these packages and Spatiocyte, open a terminal and peform the following instructions:

::

  $ curl https://raw.githubusercontent.com/ecell/spatiocyte/master/install-spatiocyte-mac.sh
  $ sh -x install-spatiocyte-mac.h

The installation script will take sometime to finish executing on the Mac. Since Spatiocyte also requires the Blender software for rendering and the VLC software to view simulation movies, you can download and install them separately. Blender can be downloaded from http://www.blender.org/, while VLC from http://www.videolan.org/.

Testing the installation and running a model
--------------------------------------------

The above instructions will retrive and execute the Spatiocyte installation script. The script will download all packages required by Spatiocyte and install the software. Enter your password when requested since some packages require the administrator privilege. If you have any issues during install please post error messages during install to the Spatiocyte users forum at https://groups.google.com/forum/?hl=en#!forum/spatiocyte-users
  
Close and reopen the terminal for the installation to take effect. To test if the installation is successful, run the following command in the terminal:

::

  $ ecell3-session-monitor

The window shown in Figure 1 should appear. Congratulations! You have now 
sucessfully installed Spatiocyte. Next, we can try running a simple 1D diffusion model written in Python, 1D.py: 

::

  $ cd $HOME/wrk/spatiocyte/examples/1D
  $ ecell3-session 1D.py
  $ spatiocyte

The Spatiocyte package includes the MinDE model (see Figure 2) as
reported by Arjunan and Tomita, 2010. We can now attempt to run the
model with the following steps:

::

  $ cd $HOME/wrk/spatiocyte/examples/published/2010.arjunan.syst.synth.biol
  $ ecell3-em2eml 2010.arjunan.syst.synth.biol.wt.em
  $ ecell3-session-monitor
 

Load the model 2010.arjunan.syst.synth.biol.wt.eml and try running the
simulation for 180 seconds.

We can also run Spatioctye models using command line interface of the
E-Cell System:

::

  $ ecell3-em2eml 2010.arjunan.syst.synth.biol.wt.em
  $ ecell3-session -f 2010.arjunan.syst.synth.biol.wt.eml
  <2010.arjunan.syst.synth.biol.wt.eml, t=0>>> run(180)
  <2010.arjunan.syst.synth.biol.wt.eml, t=180>>> exit()

When running a Spatiocyte model with the VisualizationLogProcess module
enabled, the three-dimensional positional information of a logged
molecule species will be stored in VisualLog.dat (default file name).
The molecules can be viewed in a separate visualizer window even while
the simulation is still running. To view them, we can run
SpatiocyteVisualizer by issuing

::

  $ spatiocyte


The visualizer will load the VisualLog.dat file by default and display
the molecules at every log interval (see Figure 3). The keyboard
shortcuts that are available for the visualizer are listed in the
SpatiocyteVisualizer module section. There are many example models available in the examples directory. Instructions to run each model are given in the respective README file.

To update the local Spatiocyte code to the latest source, under the
ecell3-spatiocyte directory, issue the following:

::

  $ git pull
  $ make clean
  $ make -j4


To checkout a specific committed version of the source:

::

  $ git checkout <10 digit hex commit code>


The 10 digit hex commit codes are available at
`https://github.com/ecell/spatiocyte/commits/master/ <https://github.com/ecell/ecell3-spatiocyte/commits/master/>`__



.. image:: https://raw.github.com/ecell/spatiocyte-docs/master/images/image12.png

 

Figure 1: The E-Cell Session Monitor

.. code-block:: none
   :linenos:

    Stepper SpatiocyteStepper(SS) {
      VoxelRadius 1e-8; # m
      SearchVacant 1; }
    System System(/) {
      StepperID SS;
      Variable Variable(GEOMETRY) { Value 3; } # rod shaped compartment
      Variable Variable(LENGTHX) { Value 4.5e-6; } # m
      Variable Variable(LENGTHY) { Value 1e-6; } # m
      Variable Variable(VACANT) { Value 0; }
      Variable Variable(MinDatp) { Value 0; } # molecule number
      Variable Variable(MinDadp) { Value 1300; } # molecule number
      Variable Variable(MinEE) { Value 0; } # molecule number
      Process DiffusionProcess(diffuseMinDatp) {
        VariableReferenceList [_ Variable:/:MinDatp];
        D 16e-12; } # m^2/s
      Process DiffusionProcess(diffuseMinDadp) {
        VariableReferenceList [_ Variable:/:MinDadp];
        D 16e-12; } # m^2/s
      Process DiffusionProcess(diffuseMinE) {
        VariableReferenceList [_ Variable:/:MinEE];
        D 10e-12; } # m^2/s
      Process VisualizationLogProcess(visualize) {
        VariableReferenceList [_ Variable:/Surface:MinEE]
                              [_ Variable:/Surface:MinDEE]
                              [_ Variable:/Surface:MinDEED]
                              [_ Variable:/Surface:MinD];
        LogInterval 0.5; } # s
      Process MicroscopyTrackingProcess(track) {
        VariableReferenceList [_ Variable:/Surface:MinEE 2]
                              [_ Variable:/Surface:MinDEE 3]
                              [_ Variable:/Surface:MinDEED 4]
                              [_ Variable:/Surface:MinD 1]
                              [_ Variable:/Surface:MinEE -2]
                              [_ Variable:/Surface:MinDEED -2]
                              [_ Variable:/Surface:MinEE -1]
                              [_ Variable:/Surface:MinDEED -4]
                              [_ Variable:/Surface:MinD -1]; }
      Process MoleculePopulateProcess(populate) {
        VariableReferenceList [_ Variable:/:MinDatp]
                              [_ Variable:/:MinDadp]
                              [_ Variable:/:MinEE]
                              [_ Variable:/Surface:MinD]
                              [_ Variable:/Surface:MinDEE]
                              [_ Variable:/Surface:MinDEED]
                              [_ Variable:/Surface:MinEE]; }
    }

    System System(/Surface) {
      StepperID SS;
      Variable Variable(DIMENSION) { Value 2; } # surface compartment
      Variable Variable(VACANT) { Value 0; }
      Variable Variable(MinD) { Value 0; } # molecule number
      Variable Variable(MinEE) { Value 0; } # molecule number
      Variable Variable(MinDEE) { Value 700; } # molecule number
      Variable Variable(MinDEED) { Value 0; } # molecule number
      Process DiffusionProcess(diffuseMinD) {
        VariableReferenceList [_ Variable:/Surface:MinD];
        D 0.02e-12; } # m^2/s
      Process DiffusionProcess(diffuseMinEE) {
        VariableReferenceList [_ Variable:/Surface:MinEE];
        D 0.02e-12; } # m^2/s
      Process DiffusionProcess(diffuseMinDEE) {
        VariableReferenceList [_ Variable:/Surface:MinDEE];
        D 0.02e-12; } # m^2/s
      Process DiffusionProcess(diffuseMinDEED) {
        VariableReferenceList [_ Variable:/Surface:MinDEED];
        D 0.02e-12; } # m^2/s
      Process DiffusionInfluencedReactionProcess(reaction1) {
        VariableReferenceList [_ Variable:/Surface:VACANT -1]
                              [_ Variable:/:MinDatp -1]
                              [_ Variable:/Surface:MinD 1];
        k 2.2e-8; } # m/s
      Process DiffusionInfluencedReactionProcess(reaction2) {
        VariableReferenceList [_ Variable:/Surface:MinD -1]
                              [_ Variable:/:MinDatp -1]
                              [_ Variable:/Surface:MinD 1]
                              [_ Variable:/Surface:MinD 1];
        k 3e-20; } # m^3/s
      Process DiffusionInfluencedReactionProcess(reaction3) {
        VariableReferenceList [_ Variable:/Surface:MinD -1]
                              [_ Variable:/:MinEE -1]
                              [_ Variable:/Surface:MinDEE 1];
        k 5e-19; } # m^3/s
      Process SpatiocyteNextReactionProcess(reaction4) {
        VariableReferenceList [_ Variable:/Surface:MinDEE -1]
                              [_ Variable:/Surface:MinEE 1]
                              [_ Variable:/:MinDadp 1];
        k 1; } # s^{-1}
      Process SpatiocyteNextReactionProcess(reaction5) {
        VariableReferenceList [_ Variable:/:MinDadp -1]
                              [_ Variable:/:MinDatp 1];
        k 5; } # s^{-1}
      Process DiffusionInfluencedReactionProcess(reaction6) {
        VariableReferenceList [_ Variable:/Surface:MinDEE -1]
                              [_ Variable:/Surface:MinD -1]
                              [_ Variable:/Surface:MinDEED 1];
        k 5e-15; } # m^2/s
      Process SpatiocyteNextReactionProcess(reaction7) {
        VariableReferenceList [_ Variable:/Surface:MinDEED -1]
                              [_ Variable:/Surface:MinDEE 1]
                              [_ Variable:/:MinDadp 1];
        k 1; } # s^{-1}
      Process SpatiocyteNextReactionProcess(reaction8) {
        VariableReferenceList [_ Variable:/Surface:MinEE -1]
                              [_ Variable:/:MinEE 1];
        k 0.83; } # s^{-1}
    }

Figure 2: E-Cell Model (EM) description file for the MinDE model. The
file is available in the Spatiocyte source package in the examples directory
as 2010.arjunan.syst.synth.biol.wt.em.

.. image:: https://raw.github.com/ecell/spatiocyte-docs/master/images/image13.png


Figure 3: The SpatiocyteVisualizer displaying simulated membrane-bound
proteins of the MinDE model.
