Installing and Running Spatiocyte
=================================

The Spatiocyte source code is distributed as open source software under
the GNU General Public License and is available at GitHub. At the time
of writing, the Spatiocyte modules of the E-Cell System have been tested
to run on Linux and Mac OSX systems. However, on Mac OSX the particle 
visualizer is not supported. Here, we first describe the installation 
procedures on a Ubuntu Linux system. The next section gives the procedures
for a Mac OSX system.

Ubuntu Linux
------------
 

On a freshly installed Ubuntu Linux, Spatiocyte requires several additional packages. We can install them with the following instruction:

::

  $ sudo apt-get install git autoconf automake libtool g++ libgsl0-dev python-numpy python-ply python-gtk2 libboost-python-dev libgtkmm-2.4-dev libgtkglextmm-x11-1.2-dev libhdf5-serial-dev libav-tools blender vlc python-numpy python-scipy python-matplotlib valgrind


The general installation procedure of Spatiocyte is as follows:

::

  $ cd
  $ mkdir wrk
  $ cd wrk
  $ git clone git://github.com/ecell/spatiocyte
  $ cd spatiocyte
  $ ./autogen.sh
  $ ./configure --prefix=$HOME/root
  $ make -j4 
  $ make install
  $ gedit ~/.bashrc

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
  $ ecell3-session-monitor
 
The window shown in Figure 1 should appear. Congratulations! You have now 
sucessfully installed Spatiocyte. We can now attempt to run a simple 1D 
diffusion model in written in python, 1D.py:

::

  $ cd $HOME/wrk/spatiocyte/examples/1D
  $ ecell3-session 1D.py
  $ spatiocyte

The Spatiocyte package includes the MinDE model (see Figure 2)
reported in (Arjunan and Tomita, 2010). We can now attempt to run the
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

  $ valgrind --tool=memcheck --num-callers=40 --leak-check=full python $HOME/root/bin/ecell3-session -f modelFileName.eml


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
file is available in the Spatiocyte source package as
2010.arjunan.syst.synth.biol.wt.em.

.. image:: https://raw.github.com/ecell/spatiocyte-docs/master/images/image13.png

 

Figure 3: The SpatiocyteVisualizer displaying simulated membrane-bound
proteins of the MinDE model.

Mac OSX
-------

On Mac OSX, Spatiocyte (and E-Cell System version3) require XQuartz and several additional packages, We recommend using homebrew to manage packages:

- First you need to install XQuartz from http://xquartz.macosforge.org/landing/ and restart Mac OSX
- Next you need to install some dependencies with following commands

::

  $ ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
  $ brew install wget automake autoconf libtool gsl pygtk gcc
  $ brew install boost --with-python
  $ brew install homebrew/science/hdf5 --enable-cxx
  $ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
  $ sudo python ez_setup.py
  $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
  $ sudo python get-pip.py
  $ sudo pip install ply
  $ git clone git://github.com/ecell/spatiocyte
  $ cd spatiocyte
  $ sh autogen.sh
  $ PYTHONPATH=/usr/local/lib/python2.7/site-packages LDFLAGS="-L/usr/local/Cellar/gfortran/4.8.2/gfortran/lib" ./configure --prefix=$HOME/root --disable-visualizer
  $ make
  $ make install

To start ecell3-sesion, run following command from your shell

::

  $ $HOME/root/bin/ecell3-session

To start ecell3-session-monitor, run following command from your shell

::

  $ PYTHONPATH=$HOME/root/lib/python2.7/site-packages:/usr/local/lib/python2.7/site-packages $HOME/root/bin/ecell3-session-monitor

To run a sample for Spatiocyte, run following commands from your shell

::

  $ $HOME/root/bin/ecell3-em2eml samples/2010.arjunan.syst.synth.biol/2010.arjunan.syst.synth.biol.wt.em
  $ $HOME/root/bin/ecell3-session -f 2010.arjunan.syst.synth.biol.wt.eml

If you succeed in Spatiocyte session, run following function with argument (in this case 10) from ecell session(, not from your shell).

::

  <2010.arjunan.syst.synth.biol.wt.eml, t=0>>> run(10)
