# Model
model.default_solver = Solver("dassl")
model.default_solver.tolerance = 1e-6
model.translate = True
model.init = {}
model.startTime = 0
model.stopTime = 10
model.observe = ['x', 'y']

# First mode
mode1 = Mode()
mode1.modeRef = "Pendulum.Pendulum_struc"
mode1.files = ["Pendulum.mo"]
mode1.synonym = {'x' : 'x', 'y' : 'y'}

# Second mode
mode2 = Mode()
mode2.modeRef = "Pendulum.Ball_struc"
mode2.files = ["Pendulum.mo"]
mode2.synonym = {'x' : 'x', 'y' : 'y'}

# Transition from mode 1 to mode 2
trans1_2 = Transition()
trans1_2.post = mode2
trans1_2.mapping = {'x' : 'x', 'y' : 'y', 'vx': 'der(x)' , 'vy':'der(y)'}

# Transition from mode 2 to mode 1
def speed(actMode, oldMode):
	actMode.set_initialValue('dphi', 0.0)

trans2_1 = Transition()
trans2_1.post = mode1
trans2_1.mapping = {'x' : 'x', 'phi' : 'phi'}
trans2_1.init_function = speed

mode1.transitions = [trans1_2]
mode2.transitions = [trans2_1]

# Set the modes
model.modes = [mode1, mode2]

# Create plots
plot1 = ModePlot()
plot1.vars = {'y' : Color.MAGENTA}
plot1.xAxisVar = 'x'
plot1.drawGrid = 1
plot1.labelXAxis = "x"
plot1.labelYAxis = "y"
plot1.fileName = 'modeplot.png'
plot1.show = True

# Set the plots
model.plots = [plot1]
