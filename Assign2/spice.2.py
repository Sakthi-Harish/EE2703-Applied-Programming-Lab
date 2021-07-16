"""
		EE2703 Applied Programming Lab - 2021
				Assignment 2
	Name: SAKTHI HARISH D T
	Roll: EE19B054
"""
""" Inputs: (in command line)python3 ee19b054_assign2.py <filename>
    Output: Values(in volts) of all Node Voltages and Currents through Voltage source(in amperes)
""" 

import sys  
import numpy as np   
import cmath

args= sys.argv       #Storing the arguments from command line as a list

CIRCUIT= '.circuit'  #variables storing the start and end of the circuit definition
END= '.end'
AC='.ac'

if(len(args)!=2):    #Checking if File Name is given or not (or) if too many arguments are given 
	print("\nRequired Usage: %s <input file>"%args[0])
	exit()

# Checking if File Name is valid using Exception Handling with try-catch
try:          
	with open(args[1]) as f:     #reading the input file
		lines= f.readlines()     #lines of the file are stored as a list
		start= 0; end= 0
		ac_check= False
		frequency= 0
		for line in lines:        #finding the start of the circuit definition
			if line.find(CIRCUIT)!= -1:
				break
			start+=1
		for line in lines:        #finding the end of the circuit defintion
			if line.find(END)!= -1:
				break
			end+=1  
		for line in lines:
			if line.find(AC)!= -1:
				#ac_line_index= index
				ac_check= True
				try:
					frequency= int(line.split()[2])
				except Exception:
					sys.exit("Error in AC line definition")

		if (start + 1 < end):      #checking for valid circuit defintion
			circuitdef= []
			for i in range(start+1, end, 1):
				if lines[i].find('#') != -1:    # Checking for comments and removing if present
					comment = lines[i].find('#')
					newline = lines[i][0:comment]
				else:
					newline = lines[i]
				if newline.find('\n')!= -1:          # Checking for comments and removing if present
					back= newline[i].find('\n')
					newline= newline[0:back]
				if (newline!= '' and newline!= '\n'):  # Checking if the line is not empty
					circuitdef= circuitdef+[newline]				
			

			components= {'Resistor': [],'Inductor': [],'Capacitor': [],'Voltage_Source': [],'Current_Source': [],'VCVS': [],'VCCS': [],'CCVS': [],'CCCS': []}
			ground_provided= False
			for line in circuitdef:
				if (line!= "" or line!= "\n"):
					if line.find("GND")!= -1:
						ground_provided = True
					line= line.split()	
					# Reading the components of the Lines in defintion and storing as a list
					if line[0].isalnum():
						if line[0][0]== 'R':
							try:
								Name, node_A, node_B, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Resistor . \nRequired format is: "R... n1 n2 value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
								components['Resistor'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Resistor. \nRequired format is: "R... n1 n2 value"'.format(line[0]))
						if line[0][0] == 'L':
							try:
								Name, node_A, node_B, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Inductor. \nRequired format is: "L... n1 n2 value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
								components['Inductor'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Inductor. \nRequired format is: "L... n1 n2 value"'.format(line[0]))
						if line[0][0] == 'C': 
							try:
								Name, node_A, node_B, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Capacitor. \nRequired format is: "C... n1 n2 value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
								components['Capacitor'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Capacitor. \nRequired format is: "C... n1 n2 value"'.format(line[0]))
						if line[0][0] == 'V':
							if(ac_check):
								if line[3] == 'ac':
									try:
										Name, node_A, node_B, ac_dc, mag, phase = line
									except:
										sys.exit('Please check the number of arguments in the circuit definition of {} AC Voltage Source. \nRequired format is: "V.. n1 n2 ac mag phase"'.format(line[0]))
									if(node_A.isalnum() and node_B.isalnum() and isinstance(float(mag),float) and isinstance(float(phase),float) and node_A != node_B):
										components['Voltage_Source'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'ac_dc': ac_dc, 'mag': mag, 'phase': phase})
									else:
										sys.exit('Error: Please provide valid inputs for the AC Voltage source. \nRequired format is: "V.. n1 n2 ac mag phase"')
								elif line[3] == 'dc':
									try:
										Name, node_A, node_B, ac_dc, value = line
									except:
										sys.exit('Please check the number of arguments in the circuit definition of {} DC Voltage Source. \nRequired format is: "V.. n1 n2 ac mag phase"'.format(line[0]))
									if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
										components['Voltage_Source'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value, 'ac_dc': ac_dc, 'value': value})
									else:
										sys.exit('Error: Please provide valid inputs for the DC Voltage source. \nRequired format is: "V.. n1 n2 ac mag phase"')
								else:
									sys.exit('Error: Invalid type provided for the {} Voltage source. Specify the voltage sources as dc or ac in the declaration. \nRequired format is: "V.. n1 n2 dc value (or) V.. n1 n2 ac mag phase"'.format(line[0]))
							else:
								try:
									Name, node_A, node_B, value = line
								except:
									sys.exit('Please check the number of arguments in the circuit definition of {} Voltage Source. \nRequired format is: "V... n1 n2 value"'.format(line[0]))
								if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
									components['Voltage_Source'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value, 'value': value})
								else:
									sys.exit('Error: Please provide valid inputs for the {} Voltage Source. \nRequired format is: "V... n1 n2 value"'.format(line[0]))
						if line[0][0] == 'I':
							if(ac_check):
								if line[3] == 'ac':
									try:
										Name, node_A, node_B, ac_dc, mag, phase = line
									except:
										sys.exit('Please check the number of arguments in the circuit definition of {} AC Current Source. \nRequired format is: "I.. n1 n2 ac mag phase"'.format(line[0]))
									if(node_A.isalnum() and node_B.isalnum() and isinstance(float(mag),mag) and isinstance(float(phase),phase) and node_A != node_B):
										components['Current_Source'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'ac_dc': ac_dc, 'mag': mag, 'phase': phase})
									else:
										sys.exit('Error: Please provide valid inputs for the {} AC Current source. \nRequired format is: "I.. n1 n2 ac mag phase"')
								elif line[3] == 'dc':
									try:
										Name, node_A, node_B, ac_dc, value = line
									except:
										sys.exit('Please check the number of arguments in the circuit definition of {} DC Current Source. \nRequired format is: "I.. n1 n2 ac mag phase"'.format(line[0]))
									if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
										components['Current_Source'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value, 'ac_dc': ac_dc, 'value': value})
									else:
										sys.exit('Error: Please provide valid inputs for the {} AC Current source. \nRequired format is: "I.. n1 n2 ac mag phase"')
								else:
									sys.exit('Error: Invalid type provided for the {} Voltage source. Specify the Current sources as dc or ac in the declaration. \nRequired format is: "I.. n1 n2 dc value (or) I.. n1 n2 ac mag phase"'.format(line[0]))
							else:
								try:
									Name, node_A, node_B, value = line
								except:
									sys.exit('Please check the number of arguments in the circuit definition of {} Voaltge Source. \nRequired format is: "I... n1 n2 value"'.format(line[0]))
								if(node_A.isalnum() and node_B.isalnum() and isinstance(float(value),float) and node_A != node_B):
									components['Current_Source'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'value': value, 'value': value})
								else:
									sys.exit('Error: Please provide valid inputs for the {} Voltage Source. \nRequired format is: "I... n1 n2 value"'.format(line[0]))
						elif line[0][0] == 'E':
							try:
								Name, node_A, node_B, control_voltage_from_node, control_voltage_node_B, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Voltage Controlled Voltage Source. \nRequired format is: "E.. n1 n2 n3 n4 value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and node_A != node_B and control_voltage_from_node.isalnum() and control_voltage_node_B.isalnum() and isinstance(float(value),float)):
								components['VCVS'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B,'control_voltage_from_node': control_voltage_from_node, 'control_voltage_node_B': control_voltage_node_B, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Voltage Controlled Voltage Source. \nRequired format is: "E.. n1 n2 n3 n4 value"'.format(line[0]))
						elif line[0][0] == 'G':
							try:
								Name, node_A, node_B, control_voltage_from_node, control_voltage_node_B, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Voltage Controlled Current Source. \nRequired format is: "G.. n1 n2 n3 n4 value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and node_A != node_B and control_voltage_from_node.isalnum() and control_voltage_node_B.isalnum() and isinstance(float(value),float)):
								components['VCCS'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B,'control_voltage_from_node': control_voltage_from_node, 'control_voltage_node_B': control_voltage_node_B, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Voltage Controlled Current Source. \nRequired format is: "G.. n1 n2 n3 n4 value"'.format(line[0]))
						elif line[0][0] == 'H':
							try:
								Name, node_A, node_B, controlling_voltage, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Current Controlled Voltage Source. \nRequired format is: "H.. n1 n2 V.. value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and node_A != node_B and controlling_voltage.isalnum() and isinstance(float(value),float)):
								components['CCVS'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'controlling_voltage': controlling_voltage, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Current Controlled Voltage Source. \nRequired format is: "H.. n1 n2 V.. value"'.format(line[0]))
						elif line[0][0] == 'F':
							try:
								Name, node_A, node_B, controlling_voltage, value = line
							except:
								sys.exit('Please check the number of arguments in the circuit definition of {} Current Controlled Current Source. \nRequired format is: "F.. n1 n2 V.. value"'.format(line[0]))
							if(node_A.isalnum() and node_B.isalnum() and node_A != node_B and controlling_voltage.isalnum() and isinstance(float(value),float)):
								components['CCCS'].append({'Name': Name, 'node_A': node_A, 'node_B': node_B, 'controlling_voltage': controlling_voltage, 'value': value})
							else:
								sys.exit('Error: Please provide valid inputs for the {} Current Controlled Current Source. \nRequired format is: "F.. n1 n2 V.. value"'.format(line[0]))
					else:
						sys.exit("Error: The circuit definition contains Components with unsupported names. Components must be named in alphanumerics.")

			if ground_provided:				
				if len(components['VCVS']) or len(components['VCCS']) or len(components['CCCS']) or len(components['CCVS']) > 0:
					sys.exit('Circuit defined in the given file contains dependent sources. So, output could not be shown :( ')				
				dict_of_nodes = {}      

				#Presetting the value of Ground Node to 0
				dict_of_nodes['GND'] = 0
				buffer = 1    #variable to count the number of nodes

				#Creating a dictionary to store the nodes involved with the Circuit components
				for component in components['Resistor']:
					if component['node_A'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_A']] = buffer
						buffer += 1
					if component['node_B'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_B']] = buffer
						buffer += 1
				for component in components['Inductor']:
					if component['node_A'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_A']] = buffer
						buffer += 1
					if component['node_B'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_B']] = buffer
						buffer += 1
				for component in components['Capacitor']:
					if component['node_A'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_A']] = buffer
						buffer += 1
					if component['node_B'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_B']] = buffer
						buffer += 1
				for component in components['Voltage_Source']:
					if component['node_A'] in dict_of_nodes: pass						
					else:
						dict_of_nodes[component['node_A']] = buffer
						buffer += 1
					if component['node_B'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_B']] = buffer
						buffer += 1
				for component in components['Current_Source']:
					if component['node_A'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_A']] = buffer
						buffer += 1
					if component['node_B'] in dict_of_nodes: pass
					else:
						dict_of_nodes[component['node_B']] = buffer
						buffer += 1				

				dict_keys = list(dict_of_nodes.keys())                #lists to store keys and values from the node dictionary 
				dict_vals = list(dict_of_nodes.values())
				nodetotal = len(dict_of_nodes)+ len(components['Voltage_Source']) + len(components['VCVS']) - 1 #Counting total number of nodes
				unknowns = []          # A list to store all the unknows to be computed using Nodal Analysis
				for i in range(len(dict_of_nodes) - 1):
					unknowns.append("Voltage at the node "+ dict_keys[dict_vals.index(i+1)])

				#Initializing the values for M and b Matrices
				M = np.zeros((nodetotal, nodetotal), dtype=complex)
				b = np.zeros((nodetotal, 1), dtype=complex)
				for component in components['Resistor']:
					node1 = int(dict_of_nodes[component['node_A']]) - 1
					node2 = int(dict_of_nodes[component['node_B']]) - 1
					g = 1/float(component['value'])         #g is the admittance.
					if node1 != -1 and node2 != -1:          #Assigning the admittance terms to the correct nodes 
						M[node1][node1] += g
						M[node1][node2] -= g
						M[node2][node1] -= g
						M[node2][node2] += g
					elif node1 == -1 and node2 != -1:
						M[node2][node2] += g
					elif node2 == -1 and node1 != -1:
						M[node1][node1] += g
				for component in components['Inductor']:
					node1 = int(dict_of_nodes[component['node_A']]) - 1
					node2 = int(dict_of_nodes[component['node_B']]) - 1
					if(ac_check):
						try: # Computinng the admittance value as per the frequency
							g = complex(0, -(1/(frequency * float(component['value']))))
						except:
							sys.exit('Error: .ac is not declared in the netlist')
					else:
						g = np.inf
					if node1 != -1 and node2 != -1:
						M[node1][node1] += g
						M[node1][node2] -= g
						M[node2][node1] -= g
						M[node2][node2] += g
					elif node1 == -1 and node2 != -1:
						M[node2][node2] += g
					elif node2 == -1 and node1 != -1:
						M[node1][node1] += g
				for component in components['Capacitor']:
					node1 = int(dict_of_nodes[component['node_A']]) - 1
					node2 = int(dict_of_nodes[component['node_B']]) - 1
					if(ac_check):
						try: # Computinng the admittance value as per the frequency
							g = complex(0, frequency * float(component['value']))
						except:
							sys.exit('Error: .ac is not declared in the netlist')
					else:
						g = 0       
					if node1 != -1 and node2 != -1:
						M[node1][node1] += g
						M[node1][node2] -= g
						M[node2][node1] -= g
						M[node2][node2] += g
					elif node1 == -1 and node2 != -1:
						M[node2][node2] += g
					elif node2 == -1 and node1 != -1:
						M[node1][node1] += g
				for component in components['Voltage_Source']:
					# Voltage source contributes to both cuurent and g matrix
					node1 = int(dict_of_nodes[component['node_A']]) - 1
					node2 = int(dict_of_nodes[component['node_B']]) - 1
					if(ac_check):
						if component['ac_dc'] == 'ac':
							voltage = cmath.rect(float(component['mag'])/2, float(component['phase']))
						elif component['ac_dc'] == 'dc':
							voltage = cmath.rect(float(component['value']), 0)
					else:
						voltage = float(component['value'])
					new_var = 'Current passing from node ' + dict_keys[dict_vals.index(node1 + 1)]+' to node ' + dict_keys[dict_vals.index(node2 + 1)]
					unknowns.append(new_var)
					Ix = unknowns.index(new_var)
					if node1 != -1 and node2 != -1:
						M[node1][Ix] += 1
						M[node2][Ix] -= 1
						M[Ix][node1] += 1
						M[Ix][node2] -= 1
						b[Ix][0] += voltage
					elif node1 == -1 and node2 != -1:
						M[node2][Ix] -= 1
						M[Ix][node2] -= 1
						b[Ix][0] += voltage
					elif node2 == -1 and node1 != -1:
						M[node1][Ix] += 1
						M[Ix][node1] += 1
						b[Ix][0] += voltage
				for component in components['Current_Source']:
					node1 = int(dict_of_nodes[component['node_A']]) - 1
					node2 = int(dict_of_nodes[component['node_B']]) - 1
					if(ac_check):
						if component['ac_dc'] == 'ac':
							current = cmath.rect(float(component['mag'])/2, float(component['phase']))
						elif component['ac_dc'] == 'dc':
							current = cmath.rect(float(component['value']), 0)
					else:
						current = float(component['value'])
					if node1 != -1 and node2 != -1:
						b[node1][0] += current
						b[node2][0] -= current
					elif node1 == -1 and node2 != -1:
						b[node2][0] -= current
					elif node1 != -1 and node2 == -1:
						b[node1][0] += current
				# Solving Mx=b using inverse matrix multiplication using numpy
				try:
					output_matrix = np.linalg.solve(M, b)
				except:
					sys.exit('Cannot find the values of Voltages and current as the matrix M is not invertible.')				
				print("The Voltages at the nodes and Currents through the Voltage sources in the circuit are as follows:")
				for i in range(len(unknowns)):                       #Printing the final results in the output
					if unknowns[i][0] == 'V':
						print("\t{} = \t {} Volts".format(unknowns[i], "{:.2e}".format(output_matrix[i][0])))
					if unknowns[i][0] == 'C':
						print("\t{} = \t {} Ampere".format(unknowns[i], "{:.2e}".format(output_matrix[i][0])))			
			else:
				sys.exit('Error: Ground is not specified in the circuit.')
		else:
			print("Invalid Circuit Definition in the Input File")    #Printing when the file does not have valid circuit definition
except IOError:   #IOError thrown when given file is not valid 
	print("%s : This file does not exist"%args[1]) 
	exit()


