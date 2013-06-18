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

 

 

 1 message('\\nrunning: ' + FileName)

 2 theSimulator.createStepper('SpatiocyteStepper', 'SS').VoxelRadius =
0.5

 3 # Create the system compartment:

 4 theSimulator.rootSystem.StepperID = 'SS'

 5 theSimulator.createEntity('Variable', 'Variable:/:LENGTHX').Value =
250

 6 theSimulator.createEntity('Variable', 'Variable:/:LENGTHY').Value =
250

 7 theSimulator.createEntity('Variable', 'Variable:/:LENGTHZ').Value =
20

 8 theSimulator.createEntity('Variable', 'Variable:/:VACANT')

 9 theSimulator.createEntity('Variable', 'Variable:/:XYPLANE').Value = 3

10 theSimulator.createEntity('Variable', 'Variable:/:YZPLANE').Value = 5

11 theSimulator.createEntity('Variable', 'Variable:/:XZPLANE').Value = 5

12 logger = theSimulator.createEntity('VisualizationLogProcess',
'Process:/:logger')

13 logger.LogInterval = 500

14 logger.VariableReferenceList = [['\_', 'Variable:/Surface:A'], ['\_',
'Variable:/Surface:Ac']]

15 logger.FileName = FileName

16 # Create the surface compartment:

17 theSimulator.createEntity('System', 'System:/:Surface').StepperID =
'SS'

18 theSimulator.createEntity('Variable',
'Variable:/Surface:DIMENSION').Value = 2

19 theSimulator.createEntity('Variable', 'Variable:/Surface:VACANT')

20 theSimulator.createEntity('Variable', 'Variable:/Surface:A').Value =
15300

21 theSimulator.createEntity('Variable', 'Variable:/Surface:Ac').Value =
250

22 populator = theSimulator.createEntity('MoleculePopulateProcess',
'Process:/:populate')

23 populator.VariableReferenceList = [['\_', 'Variable:/Surface:A'],
['\_', 'Variable:/Surface:Ac']]

24 diffuser =
theSimulator.createEntity('PeriodicBoundaryDiffusionProcess',
'Process:/:diffuse')

25 diffuser.VariableReferenceList = [['\_', 'Variable:/Surface:A']]

26 diffuser.D = 4.3e-3

27 binder =
theSimulator.createEntity('DiffusionInfluencedReactionProcess',
'Process:/:Reaction1')

28 binder.VariableReferenceList = [['\_', 'Variable:/Surface:A','-1']]

29 binder.VariableReferenceList = [['\_', 'Variable:/Surface:A','-1']]

30 binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]

31 binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]

32 binder.p = p1

33 binder =
theSimulator.createEntity('DiffusionInfluencedReactionProcess',
'Process:/:Reaction2')

34 binder.VariableReferenceList = [['\_', 'Variable:/Surface:A','-1']]

35 binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','-1']]

36 binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]

37 binder.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','1']]

38 binder.p = p2

39 uni = theSimulator.createEntity('SpatiocyteNextReactionProcess',
'Process:/:Reaction3')

40 uni.VariableReferenceList = [['\_', 'Variable:/Surface:Ac','-1']]

41 uni.VariableReferenceList = [['\_', 'Variable:/Surface:A','1']]

42 uni.k = k

43 run(100000)

 

Figure 13: A Python script to create clusters on a membrane. The file is
available in the Spatiocyte source package as
2012.arjunan.chapter.cluster.py.

 

 

Next, we execute the Python script shown in Figure 14 by issuing

$ python 2012.arjunan.chapter.parameter.py

to run the cluster model multiple times with different parameter values.
Each run will generate the visualization log data resulting from the
given set of parameters. Finally, we can load and view the log data
using SpatiocyteVisualizer and select the set of parameters that best
captures the expected result. Figure 15 shows an example Python script
that loads all the visualization log files within a directory.

 

 

 1 import os

 2 p1 = [2.2e-6]

 3 p2 = [0.1, 0.2, 0.3]

 4 k = [2.5e-3]

 5 FileName = ''

 6 for x in p1:

 7   for y in p2:

 8     for z in k:

 9       os.system('ecell3-session --parameters=\\"{\\'FileName\\':\\''
+ FileName + \\

10           str(x) + '\_' + str(y) + '\_' + str(z) +
'\_visualLog0.dat\\',\\'p1\\':' + \\

11           str(x) + ',\\'p2\\':' + str(y) + ',\\'k\\':' + str(z)
+'}\\" \\

12           2012.arjunan.chapter.cluster.py')

 

Figure 14: A Python script to run the cluster model multiple times with
different parameter values. The file is available in the Spatiocyte
source package as 2012.arjunan.chapter.parameter.py.

 

 

1 import glob

2 import os

3 files = glob.glob('\*0.dat')

4 for i in files:

5   print "\\nloading file " + i + "..."

6   os.system('spatiocyte ' + i)

 

Figure 15: A Python script to sequentially load multiple visualization
log files. The file is available in the Spatiocyte source package as
2012.arjunan.chapter.loadLogs.py.


