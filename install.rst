Installing and Running Spatiocyte
=================================

The Spatiocyte source code is distributed as open source software under
the GNU General Public License and is available at GitHub. At the time
of writing, the Spatiocyte modules of the E-Cell System have been tested
to run on Linux systems. Spatiocyte does not yet support other operating
systems. Here we describe the installation procedures on a Ubuntu Linux
system.

 

On a freshly installed Ubuntu Linux, Spatiocyte (and E-Cell System version3) require several additional packages:

::

  $ sudo apt-get install git autoconf automake libtool g++ libgsl0-dev python-numpy python-ply libboost-python-dev libgtkmm-2.4-dev libgtkglextmm-x11-1.2-dev libhdf5-serial-dev valgrind


The general installation procedure of the Spatiocyte is as follows:

::

  $ cd
  $ mkdir wrk
  $ cd wrk
  $ git clone git://github.com/ecell/spatiocyte
  $ cd spatiocyte
  $ ./autogen.sh
  $ ./configure --prefix=$HOME/root
  $ make -j3 (or just make, if there is only one CPU core available)
  $ make install (files will be installed in the $HOME/root directory)
  $ gedit ~/.bashrc (other editors such as emacs or vim can also be used here)

The following lines, which specify the environment variables of the
E-Cell System should be appended to the .bashrc file:

::

  export PATH=$HOME/root/bin:$PATH
  export LD_LIBRARY_PATH=$HOME/root/lib:$LD_LIBRARY_PATH
  export PYTHONPATH=$HOME/root/lib/python2.7/site-packages:$PYTHONPATH

In the line 3 above, the Python version number '2.7' should be updated
if it is different in the installed system. Next, we load the new
environment variables:

::

  $ source ~/.bashrc
  $ ecell3-session-monitor (try opening it, the window shown in Figure 1 should appear, and then close it)
 

We can now attempt to run a simple model in the E-Cell Model (EM)
language, simple.em:

::

  $ cd $HOME/wrk/spatiocyte/samples/simple/
  $ ecell3-em2eml simple.em
  $ ecell3-session-monitor
 

Using ecell3-em2eml, the model file simple.em was converted into
simple.eml in Extensible Markup Language (XML) format. The simple.eml
file can now be loaded from the File menu of the E-Cell Session Monitor
or the File open button (see Figure 1). Try running the simulation by
clicking on the Start button.

 

The Spatiocyte package includes the MinDE model (see Figure 2)
reported in (Arjunan and Tomita, 2010). We can now attempt to run the
model with the following steps:

::

  $ cd $HOME/wrk/spatiocyte/samples/2010.arjunan.syst.synth.biol/
  $ ecell3-em2eml 2010.arjunan.syst.synth.biol.wt.em
  $ ecell3-session-monitor
 

Load the model 2010.arjunan.syst.synth.biol.wt.eml and try running the
simulation for 90 seconds.

We can also run Spatioctye models using command line interface of the
E-Cell System:

::

  $ ecell3-session -f 2010.arjunan.syst.synth.biol.wt.em
  <2010.arjunan.syst.synth.biol.wt.eml, t=0>>> run(90)
  <2010.arjunan.syst.synth.biol.wt.eml, t=90>>> exit()
  # Models that are created using the Python script can be run as,
  $ ecell3-session 2012.arjunan.chapter.neuron.py


When running a Spatiocyte model with the VisualizationLogProcess module
enabled, the three-dimensional positional information of a logged
molecule species will be stored in visualLog0.dat (default file name).
The molecules can be viewed in a separate visualizer window even while
the simulation is still running. To view them, we can run
SpatiocyteVisualizer by issuing

::

  $ spatiocyte


The visualizer will load the visualLog0.dat file by default and display
the molecules at every log interval (see Figure 3). The keyboard
shortcuts that are available for the visualizer are listed in the
SpatiocyteVisualizer module section.

To update the local Spatiocyte code to the latest source, under the
ecell3-spatiocyte directory, issue the following:

::

  $ git pull
  $ make clean
  $ make -j3


To checkout a specific committed version of the source:

::

  $ git checkout <10 digit hex commit code>


The 10 digit hex commit codes are available at
`https://github.com/ecell/spatiocyte/commits/master/ <https://github.com/ecell/ecell3-spatiocyte/commits/master/>`__

If the program fails and crashes when loading or running a model, we can
get some debugging information using the Valgrind tool:

::

  $ valgrind --tool=memcheck --num-callers=40 --leak-check=full python
  $HOME/root/bin/ecell3-session -f modelFileName.eml


.. image:: https://raw.github.com/ecell/spatiocyte-docs/master/images/image12.png

 

Figure 1: The E-Cell Session Monitor

.. code-block:: none
   :linenos:

   01 Stepper SpatiocyteStepper(SS) { VoxelRadius 1e-8; } # m
   02 System System(/) {
   03   StepperID SS;
   04   Variable Variable(GEOMETRY) { Value 3; } # rod shaped compartment
   05   Variable Variable(LENGTHX) { Value 4.5e-6; } # m
   06   Variable Variable(LENGTHY) { Value 1e-6; } # m
   07   Variable Variable(VACANT) { Value 0; }
   08   Variable Variable(MinDatp) { Value 0; } # molecule number
   09   Variable Variable(MinDadp) { Value 1300; } # molecule number
   10   Variable Variable(MinEE) { Value 0; } # molecule number
   11   Process DiffusionProcess(diffuseMinD) {
   12     VariableReferenceList [\_ Variable:/:MinDatp] [\_Variable:/:MinDadp];
   13     D 16e-12; } # m^2/s
   14   Process DiffusionProcess(diffuseMinE) {
   15     VariableReferenceList [\_ Variable:/:MinEE];
   16     D 10e-12; } # m^2/s
   17   Process VisualizationLogProcess(visualize) {
   18     VariableReferenceList [\_ Variable:/Surface:MinEE] [\_Variable:/Surface:MinDEE] [\_ Variable:/Surface:MinDEED]
   19                           [\_ Variable:/Surface:MinD];
   20     LogInterval 0.5; } # s
   21   Process MicroscopyTrackingProcess(track) {
   22     VariableReferenceList [\_ Variable:/Surface:MinEE 2] [\_Variable:/Surface:MinDEE 3] [\_ Variable:/Surface:MinDEED 4]
   23                           [\_ Variable:/Surface:MinD 1] [\_Variable:/Surface:MinEE -2] [\_ Variable:/Surface:MinDEED -2]
   24                           [\_ Variable:/Surface:MinEE -1] [\_Variable:/Surface:MinDEED -4] [\_ Variable:/Surface:MinD -1];
   25     FileName "microscopyLog0.dat"; }
   26   Process MoleculePopulateProcess(populate) {
   27     VariableReferenceList [\_ Variable:/:MinDatp] [\_Variable:/:MinDadp] [\_ Variable:/:MinEE] [\_ Variable:/Surface:MinD]
   28                           [\_ Variable:/Surface:MinDEE] [\_Variable:/Surface:MinDEED] [\_ Variable:/Surface:MinEE]; }
   29 }
   30
   31 System System(/Surface) {
   32   StepperID SS;
   33   Variable Variable(DIMENSION) { Value 2; } # surface compartment
   34   Variable Variable(VACANT) { Value 0; }
   35   Variable Variable(MinD) { Value 0; } # molecule number
   36   Variable Variable(MinEE) { Value 0; } # molecule number
   37   Variable Variable(MinDEE) { Value 700; } # molecule number
   38   Variable Variable(MinDEED) { Value 0; } # molecule number
   39   Process DiffusionProcess(diffuseMinD) {
   40     VariableReferenceList [\_ Variable:/Surface:MinD];
   41     D 0.02e-12; } # m^2/s
   42   Process DiffusionProcess(diffuseMinEE) {
   43     VariableReferenceList [\_ Variable:/Surface:MinEE];
   44     D 0.02e-12; } # m^2/s
   45   Process DiffusionProcess(diffuseMinDEE) {
   46     VariableReferenceList [\_ Variable:/Surface:MinDEE];
   47     D 0.02e-12; } # m^2/s
   48   Process DiffusionProcess(diffuseMinDEED) {
   49      VariableReferenceList [\_ Variable:/Surface:MinDEED];
   50     D 0.02e-12; } # m^2/s
   51   Process DiffusionInfluencedReactionProcess(reaction1) {
   52     VariableReferenceList [\_ Variable:/Surface:VACANT -1] [\_Variable:/:MinDatp -1] [\_ Variable:/Surface:MinD 1];
   53     k 2.2e-8; } # m/s
   54   Process DiffusionInfluencedReactionProcess(reaction2) {
   55     VariableReferenceList [\_ Variable:/Surface:MinD -1] [\_Variable:/:MinDatp -1] [\_ Variable:/Surface:MinD 1]
   56                           [\_ Variable:/Surface:MinD 1];
   57     k 3e-20; } # m^3/s
   58   Process DiffusionInfluencedReactionProcess(reaction3) {
   59     VariableReferenceList [\_ Variable:/Surface:MinD -1] [\_Variable:/:MinEE -1] [\_ Variable:/Surface:MinDEE 1];
   60     k 5e-19; } # m^3/s
   61   Process SpatiocyteNextReactionProcess(reaction4) {
   62     VariableReferenceList [\_ Variable:/Surface:MinDEE -1] [\_Variable:/Surface:MinEE 1] [\_ Variable:/:MinDadp 1];
   63     k 1; } # s^{-1}
   64   Process SpatiocyteNextReactionProcess(reaction5) {
   65     VariableReferenceList [\_ Variable:/:MinDadp -1] [\_Variable:/:MinDatp 1];
   66     k 5; } # s^{-1}
   67   Process DiffusionInfluencedReactionProcess(reaction6) {
   68     VariableReferenceList [\_ Variable:/Surface:MinDEE -1] [\_Variable:/Surface:MinD -1] [\_ Variable:/Surface:MinDEED 1];
   69     k 5e-15; } # m^2/s
   70   Process SpatiocyteNextReactionProcess(reaction7) {
   71     VariableReferenceList [\_ Variable:/Surface:MinDEED -1] [\_Variable:/Surface:MinDEE 1] [\_ Variable:/:MinDadp 1];
   72     k 1; } # s^{-1}
   73   Process SpatiocyteNextReactionProcess(reaction8) {
   74     VariableReferenceList [\_ Variable:/Surface:MinEE -1] [\_Variable:/:MinEE 1];
   75     k 0.83; } # s^{-1}
   76 }
  
 

Figure 2: E-Cell Model (EM) description file for the MinDE model. The
file is available in the Spatiocyte source package as
2010.arjunan.syst.synth.biol.wt.em.

.. image:: https://raw.github.com/ecell/spatiocyte-docs/master/images/image13.png

 

Figure 3: The SpatiocyteVisualizer displaying simulated membrane-bound
proteins of the MinDE model.



