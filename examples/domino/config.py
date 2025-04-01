# Domino stone hits another stone
def crash(act, old):
	import math
	
	active = int(old.get_parameter('active')) + 1
	fallen = int(old.get_parameter('fallen'))
				
	D_val = old.get_parameter('D')
	Z_val = old.get_parameter('Stones[1].Z')
 
	phipush = math.asin(D_val/Z_val)
	KO = (1 + math.cos(2 * phipush))/2
	KR = 1 - math.cos(phipush)

	o = []
	p = []
	for i in range(1, active):
		omega = old.get_endValue(f'Stones[{i}].omega')
		phi = old.get_endValue(f'Stones[{i}].phi')
		p.append(phi)
		if i == active - 1:
			o.append(omega * KR)
		else:
			o.append(omega)
			
	act.set_parameters({'active': active,'fallen': fallen})
	act.compile()
	act.read_init()
		
	for i in range(1, active):
		act.set_initialValue(f'Stones[{i}].omega', o[i - 1])
		act.set_initialValue(f'Stones[{i}].phi', p[i - 1])
	act.set_initialValue(f'Stones[{active}].omega', o[-1] * KO / KR)
	act.set_initialValue(f'Stones[{active}].phi', 0)
	
# Domino stone falls
def fall(act, old):
	active = int(old.get_endValue('active')) - 1
	fallen = int(old.get_endValue('fallen')) + 1

	o = []
	p = []
	for i in range(2, active+2):
		omega = old.get_endValue('Stones['+str(i)+'].omega')
		phi = old.get_endValue('Stones['+str(i)+'].phi')
		o.append(omega)
		p.append(phi)
		
	act.set_parameters({'active':active,'fallen':fallen})
	act.compile()
	act.read_init()
	
	for i in range(1, active+1):
		act.set_initialValue('Stones['+str(i)+'].omega', o[i-1])
		act.set_initialValue('Stones['+str(i)+'].phi', p[i-1])
	
# End of simulation     
def end(act, old):
	t = old.get_endValue('time')
	act.get_model().stopTime = t

model.translate = True
model.default_solver = Solver("dassl")
model.init = {'Stones[1].omega': 0.1}
model.stopTime = 5
model.startTime = 0
model.observe = ['Stones[1].phi','Stones[2].phi','Stones[1].omega']  

mode = Mode()
mode.files = ['Domino.mo'] # Modelica file
mode.modeRef = "Domino.Stones" # Modelica model
mode.synonym={'Stones[1].phi':'Stones[1].phi', 'Stones[1].omega':'Stones[1].omega'}

# Stone hit
trans1 = Transition() 
trans1.post = mode # Transition to itself
trans1.init_function = crash # Function call
trans1.mapping = {} # No mapping

# Stone fallen
trans2 = Transition()
trans2.post = mode # Transition to itself
trans2.init_function = fall # Function call
trans2.mapping = {} # No mapping

# End of simulation
trans3 = Transition()
trans3.post = mode # Transition to itself
trans3.init_function = end # Function call
trans3.mapping = {} # No mapping

mode.transitions = [trans1, trans2, trans3] 

model.modes = [mode]

# Create plots
plot1 = VariablePlot()
plot1.vars = {'Stones[1].phi' : Color.MAGENTA}
plot1.drawGrid = 1  #0 = no, 1 = yes
plot1.labelXAxis = "x-axis"
plot1.labelYAxis = "y-axis"
plot1.fileName = 'variableplot.png'
plot1.show = True

# Set the plots
model.plots = [plot1]
