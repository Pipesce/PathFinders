#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from Tkinter import *
#from visual import *
#from visual.graph import *
import time
import math
import random
import node as nod
import mind as mnd
import creature as creat

data = open("pathfinder_data.txt", "w")

random.seed(137)

simulationNum = 1000

windowX = 800				        #dimension X de la ventana
windowY = 600				        #dimension Y de la ventana
habX = 760					#dimension X del laberinto
habY = 560					#dimension X del laberinto
wall1X = 680				        #dimension X de la primera muralla
wall1Y = 20					#dimension Y de la primera muralla
wall2X = 680				        #dimension X de la segunda muralla
wall2Y = 20					#dimension Y de la segunda muralla

v_init = 0.0				        #velocidad inicial de cada nave
angle_init = -3.14/2.0		                #angulo inicial de cada nave
vMax = 8.0					#velocidad maxima
v_cap = 3.0					#ponderacion (negativa) para calcular delta_v
angle_cap = 15.0			        #ponderacion (negativa) para calcular delta_teta

np = 400					#numero de naves

timeInterval = 10

brain_debug = 0



Ships = []					#lista de datos de las naves
Shapes = []					#lista de triangulos, graficos de las naves

fitness = []				        #lista con las distancias alcanzadas por las naves

rotationKillCounter = []	                #para terminar la simulacion de naves que no avanzan

habs = Tk()
canvas = Canvas(habs, width=windowX, height=windowY)
canvas.pack(fill='both', expand=1)
habs.title("Pathfinders")
canvas.create_rectangle(0,0,windowX,windowY,fill='#222')
canvas.create_rectangle(20,20,windowX-20,windowY-20,fill='#aaa')
wall_one = canvas.create_rectangle(20,200,20+wall1X,200+wall1Y, fill='#222')
wall_two = canvas.create_rectangle(windowX-20,360,windowX-20-wall2X,360+wall1Y, fill='#222')

brain_i = 1					#indice de la nave mostrada en el cerebro
brain_counter = 0			        #contador interno para el cerebro
brain_redraw_rate = 2		                #cada cuantos pasos se calculan los nodos cerebrales
brain_calc_rate = 100		                #relacion de simulaciones sin y con calculo paso a paso

simulation_counter = 0		                #contador que dice cuantas simulaciones van

if(brain_debug):

	brain = Toplevel()
	brain_canvas = Canvas(brain, height=600, width=800)
	brain.geometry('800x600+360+0')

	brain_canvas.pack(expand=YES, fill=BOTH)
	brain.title("Ship %i Brain – Simulation number %i." % (brain_i, simulation_counter))

	def drawBrain():
		#Dibujar el cerebro en cada nueva iteracion.
		brain_canvas.delete("all")

		mnd.drawNodes(Ships[brain_i].nodeWeb, brain_canvas)
		mnd.drawArrows(Ships[brain_i].W, Ships[brain_i].nodeWeb, brain_canvas)

		brain.title("Ship %i Brain – Simulation number %i." % (brain_i, simulation_counter))
		brain_canvas.update()	

	def redrawBrain():
		#Redibujar el cerebro en cada nueva iteracion.
		mnd.drawNodes(Ships[brain_i].nodeWeb, brain_canvas)
		brain_canvas.update()	

def defineShips():
	#Definir las naves al comienzo
	for i in range(np):

		W_i = []
		mnd.setW(W_i)
		ship_i = creat.Creature(W_i, windowX*8/10, windowY*8/10, v_init, angle_init)   #windowX*0.5 + 240*(random.random()-0.5)
		Ships.append(ship_i)

		fitness.append(10000)

		teta = Ships[i].orientation

		points = [Ships[i].posX, Ships[i].posY, 
			Ships[i].X_2, Ships[i].Y_2, 
			Ships[i].X_3, Ships[i].Y_3]

	
		Shapes.append(canvas.create_polygon(points, outline='gray', fill='red', width=1))

		rotationKillCounter.append(0)

def nextGen(cutoff):
	#funcion que determina qué naves sobreviven, y si mutan.
	

	for i in range(np):

		if((fitness[i] < cutoff) or fitness[i] == min(fitness)):

			
			mnd.mutateW(Ships[i].W) 								#Mutar los genes de las naves

			canvas.itemconfig(Shapes[i], fill="blue") 				# cambiar color

			if(fitness[i] < 100 and fitness[i] != min(fitness)):
				canvas.itemconfig(Shapes[i], fill="cyan") 			# cambiar color				
	#			print "Ship number " + str(i) + " has fitness " + str(int(fitness[i])) + " and survives."

			if(fitness[i] == min(fitness)):
				canvas.itemconfig(Shapes[i], fill="paleturquoise") 			# cambiar color				
	#			print "Ship number " + str(i) + " has fitness " + str(int(fitness[i])) + " and leads. \n"
				
				if(brain_debug):
					brain_i = i
					print str(brain_i)
					brain.title("Ship %i Brain" % (brain_i))

					brain_counter += 1

					if(brain_counter >= brain_redraw_rate and (simulation_counter % brain_calc_rate == 0)):
						redrawBrain()
						brain_counter = 0

			Ships[i].orientation = angle_init
			Ships[i].speed = v_init
			
			Ships[i].posX = windowX*8/10
			Ships[i].posY = windowY*8/10

			Ships[i].X_2 = Ships[i].posX - 5.0
			Ships[i].Y_2 = Ships[i].posY + 20.0

			Ships[i].X_3 = Ships[i].posX + 5.0
			Ships[i].Y_3 = Ships[i].posY + 20.0

			canvas.coords(Shapes[i],Ships[i].posX, Ships[i].posY, Ships[i].X_2, Ships[i].Y_2, Ships[i].X_3, Ships[i].Y_3)
			Ships[i].alive = 1

		else:
			W_i = []
			mnd.setW(W_i)
			Ships[i].W = W_i

			canvas.itemconfig(Shapes[i], fill="red") # change color

			Ships[i].orientation = angle_init
			Ships[i].speed = v_init
			
			Ships[i].posX = windowX*8/10
			Ships[i].posY = windowY*8/10

			Ships[i].X_2 = Ships[i].posX - 5.0
			Ships[i].Y_2 = Ships[i].posY + 20.0

			Ships[i].X_3 = Ships[i].posX + 5.0
			Ships[i].Y_3 = Ships[i].posY + 20.0

			canvas.coords(Shapes[i],Ships[i].posX, Ships[i].posY, Ships[i].X_2, Ships[i].Y_2, Ships[i].X_3, Ships[i].Y_3)
			Ships[i].alive = 1

	for j in range(np):
		fitness[j] = 10000

def getInputs():
	#función que actualiza los valores de entrada en cada iteración
	for i in range(np):

		Ships[i].nodeWeb[0][0].nodeVal = (Ships[i].posX-20)/(habX)
		Ships[i].nodeWeb[0][1].nodeVal = (Ships[i].posY-20)/(habY)
		Ships[i].nodeWeb[0][2].nodeVal = (Ships[i].orientation % 3.14) / (0.5*3.14) - 1
		Ships[i].nodeWeb[0][3].nodeVal = 2.0*(Ships[i].speed/vMax)-1.0

def checkCollision(ship, shipNum):
	#verificador de colisiones entre una nave y los muros
	if(ship.posX < 20 or ship.posX > windowX-20
		or ship.posY < 20 or ship.posY > windowY-20
		or (ship.posX < 700 and 200 < ship.posY < 220)
		or (ship.posX > windowX-700 and 360 < ship.posY < 380)):
		
	#	if(ship.alive == 1):
	#		print "Ship number " + str(shipNum) + " has a fitness of: " + str(int(ship.posY)) + " (crash)."

		fitness[shipNum] = 2.0*ship.posY + ship.posX
		if(210 < ship.posY < 370):
			fitness[shipNum] -= 2.0*ship.posX

		ship.alive = 0
		rotationKillCounter[shipNum] = 0

	if(ship.speed == 0.0 and rotationKillCounter[shipNum] > 150 and ship.alive == 1):
	#	print "Ship number " + str(shipNum) + " has a fitness of: " + str(int(ship.posY)) + " (failure)."
		fitness[shipNum] = 2.0*ship.posY + ship.posX 
		if(210 < ship.posY < 370):
			fitness[shipNum] -= 2.0*ship.posX
		
		ship.alive = 0
		rotationKillCounter[shipNum] = 0

	if(ship.orientation > 2.0*math.pi*4.0 or ship.orientation < -2.0*math.pi*4.0):
	#	print "Ship number " + str(shipNum) + " has a fitness of: " + str(int(ship.posY)) + " (stuck)."
		fitness[shipNum] = 2.0*ship.posY + ship.posX 
		if(210 < ship.posY < 370):
			fitness[shipNum] -= 2.0*ship.posX
		
		ship.alive = 0
		rotationKillCounter[shipNum] = 0

def checkDead():
	#funcion que determina si quedan naves vivas
	for i in range(np):
		if(Ships[i].alive == 1):
			return 1

	return 0

def median(lst):
    #calculo de la mediana de una lista
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0	

def percentile(lst,cutoffNum):
    #calculo de cualquier percentil de una lista
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // cutoffNum

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0	

def number_pass(lst,cutoffNum):
    #
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - cutoffNum)

    return sortedLst[index]



#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def main():
	global habs, brain, brain_i, brain_counter, simulation_counter

	avgFitness = 0
	
	defineShips()

	while (simulation_counter < simulationNum):

		simulation_counter += 1

		habs.title("Pathfinders – Simulation %i" % (simulation_counter))
		

		getInputs()
		if(brain_debug):
			drawBrain()

		while (checkDead() == 1):

			getInputs()


			

			for i in range(np):                  # start the dance

			#	print "La velocidad del organismo " + str(i) + " es " + str(Ships[i].speed)
			#	print "La orientación del organismo " + str(i) + " es " + str(Ships[i].orientation) + "\n"
				if (Ships[i].alive == 1):

					inputs_i = [Ships[i].posX, Ships[i].posY, Ships[i].orientation, Ships[i].speed]
				
					mnd.calcNodeVals(Ships[i].nodeWeb, inputs_i, Ships[i].W)

					d_vel = (Ships[i].nodeWeb[-1][0].nodeVal)/v_cap
					d_orient = (Ships[i].nodeWeb[-1][1].nodeVal)/angle_cap

	#				print Ships[i].nodeWeb[-1][1].nodeVal

					Ships[i].speed += d_vel
		
					if (Ships[i].speed > vMax): 
						Ships[i].speed = vMax
					if (Ships[i].speed < 0.1):
						Ships[i].speed = 0.0
						rotationKillCounter[i] += 1

					if (Ships[i].speed > 0.01):
						rotationKillCounter[i] = 0

					Ships[i].orientation = ((Ships[i].orientation + d_orient) ) # % (4.0*math.pi))

	#				print Ships[i].orientation	

					spd = Ships[i].speed
					posX = Ships[i].posX
					posY = Ships[i].posY
					teta = Ships[i].orientation

					dx = spd * math.sin(teta)
					dy = -spd * math.cos(teta)

					Ships[i].posX = posX + dx
					Ships[i].posY = posY + dy

					Ships[i].X_2 = Ships[i].posX - 5.0*math.cos(teta) - 20.0*math.sin(teta)
					Ships[i].Y_2 = Ships[i].posY - 5.0*math.sin(teta) + 20.0*math.cos(teta)

					Ships[i].X_3 = Ships[i].posX + 5.0*math.cos(teta) - 20.0*math.sin(teta)
					Ships[i].Y_3 = Ships[i].posY + 5.0*math.sin(teta) + 20.0*math.cos(teta)		

					canvas.coords(Shapes[i],Ships[i].posX, Ships[i].posY, Ships[i].X_2, Ships[i].Y_2, Ships[i].X_3, Ships[i].Y_3)
			#		canvas.move(Shapes[i], dx, dy)


				checkCollision(Ships[i], i)


			
			habs.update_idletasks()
			habs.update()

		for j in range(np):
			avgFitness += fitness[j]
		avgFitness = avgFitness/np
	#	print " "
		print "Simulation %i: Average fitness is %.0f, best fitness is %.0f." % (simulation_counter, avgFitness, min(fitness))
		
		data.write("%i \t %.2f \t %.2f \t %.2f \t %.2f \n" % (simulation_counter, avgFitness, min(fitness), max(fitness), median(fitness)))
		nextGen(number_pass(fitness,300))


	data.close() 

if __name__ == '__main__':
    main()

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
