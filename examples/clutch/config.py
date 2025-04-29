# Model
model.default_solver = Solver("dassl")
model.default_solver.tolerance = 1e-4
model.translate = True
model.init = {}
model.startTime = 0
model.stopTime = 10
# model.observe = ['w1', 'w2', 'f1', 'f2']
model.observe = ['w1', 'f1']

# First mode
mode1 = Mode()

mode1.modeRef = "Clutch.ClutchUncoupled"
mode1.files = ["Clutch.mo"]
mode1.synonym = {'w1' : 'w1', 'f1' : 'f1'}

# Second mode
mode2 = Mode()

mode2.modeRef = "Clutch.ClutchCoupled"
mode2.files = ["Clutch.mo"]
mode1.synonym = {'w1' : 'w1', 'f1' : 'f1'}

# Transition from mode 1 to mode 2
trans1_2 = Transition()
trans1_2.post = mode2
trans1_2.mapping = {'w1' : 'w1', 'f1' : 'f1'}

trans2_1 = Transition()
trans2_1.post = mode1
trans2_1.mapping = {'w1' : 'w1', 'f1' : 'f1'}

mode1.transitions = [trans1_2]
mode2.transitions = [trans2_1]

# Set the modes
model.modes = [mode1, mode2]

plot1 = VariablePlot()
plot1.vars = {'w1' : Color.MAGENTA}
plot1.xAxisVar = 'time'
plot1.drawGrid = 1  # 0 = no, 1 = yes
plot1.labelXAxis = "time"
plot1.labelYAxis = "w1"
plot1.fileName = "w1.png"
plot1.show = True

plot2 = VariablePlot()
plot2.vars = {'f1' : Color.BLUE}
plot2.xAxisVar = 'time'
plot2.drawGrid = 1  # 0 = no, 1 = yes
plot2.labelXAxis = "time"
plot2.labelYAxis = "f1"
plot2.fileName = "f1.png"
plot2.show = True

# Set the plots
model.plots = [plot1, plot2]
