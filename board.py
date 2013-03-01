import operator
import pygame
import random
from string import *

class board():
	def __init__(self,width,height,cellsize,screen):
		self.width=width
		self.height=height
		self.cellsize=cellsize
		self.cells_alive={}
		self.screen=screen
		self.board=screen
		self.setcolors()
		self.shiftx=0
		self.shifty=0
		self.extra_labels=[]
		self.myfont = pygame.font.SysFont("monospace",24)

	#add label to be shown
	def addinput(self,label,pos):
		self.extra_labels.append((label,pos))
	
	#del last label
	def delinput(self):
		if self.extra_labels:
			self.extra_labels.pop()

	#board from file: X marks living cell
	def loadfromfile(self,file):
		self.cells_alive={}
		file = open(file,'r')
		y=0
		for line in file:
			x=0
			if not line.startswith("#"):
				for char in line:
					if char=="X":
						self.cells_alive[(x,y)]=1
					x+=1
				y+=1
		self.render()

	def savetofile(self,file):
		file = open(file, 'w')
		a=[]
		for cell in self.cells_alive:
			a.append(cell)

		#sort for second element(row) and then for first(column)
		a.sort(key=operator.itemgetter(1,0))

		s=""
		lastrow=0
		lastcol=0
		for item in a:
			#if new row: newline
			if item[1]-lastrow>0:
				nl=""
				lastcol=0
				for i in range(0,item[1]-lastrow):
					nl+="\n"
				s+=nl
			#put spaces for dead cells
			s=join((s,"X"),"".ljust(item[0]-lastcol))
			lastcol=item[0]
			lastrow=item[1]
		file.write(s)

	def movecamera(self,pos):
		if not (self.shiftx+pos[0]>0):
			self.shiftx+=pos[0]
		if not (self.shifty+pos[1]>0):
			self.shifty+=pos[1]

		self.render()

	def mouseclick(self,pos):
		#which cell was clicked on?
		x=(pos[0]-self.shiftx)/(1+self.cellsize)
		y=(pos[1]-self.shifty)/(1+self.cellsize)

		#toggle clicked on cell
		if (x,y) in self.cells_alive:
			color=self.color_dead
			del self.cells_alive[x,y]
		else:
			color=self.color_alive
			self.cells_alive[x,y]=1

		self.__celltorect(self.__celltocoord((x,y)),color)

	def setcolors(self,alive=(0,0,0),dead=(255,255,255)):
		self.color_alive=alive
		self.color_dead=dead

	#map cell number to corresponding top left pixel of rectangle
	def __celltocoord(self,cell):
		return (cell[0]*self.cellsize+self.shiftx+cell[0]+1,cell[1]*self.cellsize+self.shifty+cell[1]+1)

	def __num_neightbors_alive(self,cell):
		num=0
		#check surrounding cells
		for i in range(-1,2):
			for j in range(-1,2):
				if (i==0 and j==0) or cell[0]+i<0 or cell[1]+j<0:
					continue
				if (cell[0]+i,cell[1]+j) in self.cells_alive:
					num+=1
		return num				

	def render(self):
		#grid
		pxarray=pygame.PixelArray(self.board)
		pxarray[:,:]=(255,255,255)
		pxarray[self.shiftx%(self.cellsize+1)::self.cellsize+1,:]=(178,190,181)
		pxarray[:,self.shifty%(self.cellsize+1)::self.cellsize+1]=(178,190,181)
		del pxarray

		#render cell if cell on screen
		for cell in self.cells_alive:
			if self.__celltocoord(cell)[0]<self.width and self.__celltocoord(cell)[1]<self.height:
				self.__celltorect(self.__celltocoord(cell),self.color_alive)

		#current camera position as label
		label=self.myfont.render(str((-self.shiftx)/(1+self.cellsize))+":"+str((-self.shifty)/(1+self.cellsize)),1,(255,0,100))

		#iterate additional labels
		self.board.blit(label,(0,0))
		for  inputlabel in self.extra_labels:
			self.board.blit(inputlabel[0],inputlabel[1])

		self.screen.blit(self.board,(0,0))

	#draw rectangle
	def __celltorect(self,cell,color):
		pygame.draw.rect(self.board,color,((cell[0],cell[1],self.cellsize,self.cellsize)),0)


	def nextgen(self):
		cells_alive_nextgen={}
		cells_checked=[]

		#living cell w/ 2 or 3 neighbors => survives
		for cell in self.cells_alive:
			nneighbors=self.__num_neightbors_alive(cell)
			if nneighbors==2 or nneighbors==3:
				cells_alive_nextgen[(cell[0],cell[1])]=1
			cells_checked.append(cell)

			#only need to check neighbors of living cells for resurrection
			for i in range(-1,2):
				for j in range(-1,2):
					#check for OOB
					if cell[0]+i<0 or cell[1]+j<0:
						continue
					#don't check cell twice
					if cells_checked.count((cell[0]+i,cell[1]+j))==0:
						nneighbors=self.__num_neightbors_alive((cell[0]+i,cell[1]+j))
						if nneighbors==3:
							cells_alive_nextgen[(cell[0]+i,cell[1]+j)]=1

		self.cells_alive=cells_alive_nextgen

		self.render()

		#for ending, if #cells==0
		return len(self.cells_alive)