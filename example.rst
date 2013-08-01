Parameter Tuning Example
========================

Sometimes it is necessary to tune the parameters of a spatially resolved
RD model, which usually takes a significant amount of effort and time
when done manually. Here we provide a Python script example that
automatically generates the visualization log data for a given range of
a set of parameters. The user can then view the logged data using
SpatiocyteVisualizer to select the set of parameters that most closely
reproduces the expected spatiotemporal behavior of the simulated
molecules. In this particular example, we would like to determine the
parameters of a model that can generate clusters of molecules on the
membrane. We know that the model consists of the following reactions,

::

  A + A → Ac + Ac
  A + Ac → Ac + Ac
  Ac → A

where A is a diffusing surface species and Ac is a nondiffusing surface
cluster species. The first two reactions have the binding probabilities
p1 and p2, respectively, while the third reaction has the rate k. We
would like to determine the values of p1, p2 and k such that several Ac
clusters are formed on the membrane. First, we need to create a Python
model file that describes the reactions and the diffusion of the
molecules, as shown in Figure 13.

.. code-block:: python
   :linenos:

   message('\\nrunning: ' + FileName)
   theSimulator.createStepper('SpatiocyteStepper', 'SS').VoxelRadius = 0.5
   # Create the system compartment:
   theSimulator.rootSystem.StepperID = 'SS'
   theSimulator.createEntity('Variable', 'Variable:/:LENGTHX').Value = 250
   theSimulator.createEntity('Variable', 'Variable:/:LENGTHY').Value = 250
   theSimulator.createEntity('Variable', 'Variable:/:LENGTHZ').Value = 20
   theSimulator.createEntity('Variable', 'Variable:/:VACANT')
   theSimulator.createEntity('Variable', 'Variable:/:XYPLANE').Value = 3
   theSimulator.createEntity('Variable', 'Variable:/:YZPLANE').Value = 5
   theSimulator.createEntity('Variable', 'Variable:/:XZPLANE').Value = 5
   logger = theSimulator.createEntity('VisualizationLogProcess', 'Process:/:logger')
   logger.LogInterval = 500
   logger.VariableReferenceList = [['\_', 'Variable:/Surface:A'], ['\_', 'Variable:/Surface:Ac']]
   logger.FileName = FileName
   # Create the surface compartment:
   theSimulator.createEntity('System', 'System:/:Surface').StepperID = 'SS'
   theSimulator.createEntity('Variable', 'Variable:/Surface:DIMENSION').Value = 2
   theSimulator.createEntity('Variable', 'Variable:/Surface:VACANT')
   theSimulator.createEntity('Variable', 'Variable:/Surface:A').Value = 15300
   theSimulator.createEntity('Variable', 'Variable:/Surface:Ac').Value = 250
   populator = theSimulator.createEntity('MoleculePopulateProcess', 'Process:/:populate')
   populator.VariableReferenceList = [['\_', 'Variable:/Surface:A'], ['\_', 'Variable:/Surface:Ac']]
   diffuser = theSimulator.createEntity('PeriodicBoundaryDiffusionProcess', 'Process:/:diffuse')
   diffuser.VariableReferenceList = [['\_', 'Variable:/Surface:A']]
   diffuser.D = 4.3e-3
   binder = theSimulator.createEntity('DiffusionInfluencedReactionProcess', 'Process:/:Reaction1')
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:A','-1']]
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:A','-1']]
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]
   binder.p = p1
   binder = theSimulator.createEntity('DiffusionInfluencedReactionProcess', 'Process:/:Reaction2')
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:A','-1']]
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','-1']]
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]
   binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]
   binder.p = p2
   uni = theSimulator.createEntity('SpatiocyteNextReactionProcess', 'Process:/:Reaction3')
   uni.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','-1']]
   uni.VariableReferenceList = [['\_', 'Variable:/Surface:A','1']]
   uni.k = k
   run(100000)

Figure 13: A Python script to create clusters on a membrane. The file is
available in the Spatiocyte source package as
2012.arjunan.chapter.cluster.py.



Next, we execute the Python script shown in Figure 14 by issuing

::

  $ python 2012.arjunan.chapter.parameter.py

to run the cluster model multiple times with different parameter values.
Each run will generate the visualization log data resulting from the
given set of parameters. Finally, we can load and view the log data
using SpatiocyteVisualizer and select the set of parameters that best
captures the expected result. Figure 15 shows an example Python script
that loads all the visualization log files within a directory.

.. code-block:: none
   :linenos:

   import os
   p1 = [2.2e-6]
   p2 = [0.1, 0.2, 0.3]
   k = [2.5e-3]
   FileName = ''
   for x in p1:
     for y in p2:
       for z in k:
         os.system('ecell3-session --parameters=\\"{\\'FileName\\':\\'' + FileName + \\
             str(x) + '\_' + str(y) + '\_' + str(z) + '\_visualLog0.dat\\',\\'p1\\':' + \\
             str(x) + ',\\'p2\\':' + str(y) + ',\\'k\\':' + str(z) +'}\\" \\
             2012.arjunan.chapter.cluster.py')
  
Figure 14: A Python script to run the cluster model multiple times with
different parameter values. The file is available in the Spatiocyte
source package as 2012.arjunan.chapter.parameter.py.

.. code-block:: none
   :linenos:

   import glob
   import os
   files = glob.glob('\*0.dat')
   for i in files:
     print "\\nloading file " + i + "..."
     os.system('spatiocyte ' + i)
  

Figure 15: A Python script to sequentially load multiple visualization
log files. The file is available in the Spatiocyte source package as
2012.arjunan.chapter.loadLogs.py.


