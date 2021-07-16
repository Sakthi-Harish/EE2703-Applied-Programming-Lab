"""
        EE2703 Applied Programming Lab - 2021
                Assignment 1
    Name: SAKTHI HARISH D T
    Roll: EE19B054
"""
import sys      




args= sys.argv       #Storing the arguments from command line as a list

CIRCUIT= '.circuit'  #variables storing the start and end of the circuit definition
END= '.end'

if(len(args)!=2):    #Checking if File name is given or not (or) if too many arguments are given 
    print("\nRequired Usage: %s <input file>"%args[0])
    exit()

# Checking if File name is valid using Exception Handling with try-catch
try:          
    with open(args[1]) as f:     #reading the input file
        lines= f.readlines()     #lines of the file are stored as a list
        start= 0; end= 0
        for line in lines:        #finding the start of the circuit definition
            if line.find(CIRCUIT)!= -1:
                break
            start+=1
        for line in lines:        #finding the end of the circuit defintion
            if line.find(END)!= -1:
                break
            end+=1  
        
        if (start + 1 < end):      #checking for valid circuit defintion
            for i in range(end-1, start, -1):
                if lines[i].find('#') != -1:    # Checking for comments and removing if present
                    comment = lines[i].find('#')
                    newline = lines[i][0:comment]
                else:
                    newline = lines[i]
                if (newline != '' and newline != '\n'):  # Checking if the line is not empty
                    newline = newline.split()           #Converting the string to a list                    
                    newline = ' '.join(newline[::-1])      # Joining the  list elements in reverse into a string
                    print(newline)        #Printing the reverse order of the circuit definition without comments.
        else:
            print("Invalid Circuit Definition in the Input File")    #Printing when the file does not have valid circuit definition
except IOError:   #IOError thrown when given file is not valid 
    print("%s : This file does not exist"%args[1]) 
    exit()


