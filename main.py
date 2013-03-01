import pygame, sys
from pygame.locals import *
from board import board
from pygame.time import Clock
#check which action to perform
def parseinput(flag,string):
	if flag=="s":
		board.savetofile(string)
	elif flag=="l":
		board.loadfromfile(string)
		pygame.display.update()

#render label and send it to board
def sendlabeltoboard(string,board):
	inputlabel=myfont.render(string,1,(255,0,100))
	board.delinput()
	textpos=inputlabel.get_rect()
	textpos.center = ((800-inputlabel.get_rect().width)/2,(600-inputlabel.get_rect().height)/2)
	board.addinput(inputlabel,textpos.center)
	board.render()
	pygame.display.update()

pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Conway\'s Game of Life')

screen.fill((255, 255, 255))

board=board(800,600,8,screen)

board.loadfromfile("default.board")

pygame.display.update()
leftclick=False
paused=True

#flag for input for saving/loading etc.
stringbuf=False

#saving/loading?
inputflag=""

gamespeed=1
passedtime=0

clock=Clock()

myfont=pygame.font.SysFont("monospace",24)
inputstring=""

while True:

	if not paused:
		passedtime+=clock.tick(30)

		if passedtime>1000/gamespeed:
			passedtime=0
			if board.nextgen()==0:
				paused=True
				print "done"
			pygame.display.update()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			#pressed letter?
			if stringbuf and event.key != pygame.K_RETURN:
				if event.key==K_BACKSPACE:
					inputstring=inputstring[:-1]
				elif event.key==pygame.K_ESCAPE:
					inputstring=""
					board.delinput()
					board.render()
					pygame.display.update()
					stringbuf=False
					continue				
				else:
					try:
						#get pressed letter
						inputstring+=chr(event.key)
					except:
						print "oops"
				#show label on board
				sendlabeltoboard(inputstring,board)

			else:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

				#for single generation steps
				if event.key == pygame.K_SPACE:
					print "nextgen"
					board.nextgen()
					pygame.display.update()

				if event.key == pygame.K_RETURN:
					#input done
					if stringbuf:
						#remove label from board
						board.delinput()
						board.render()
						pygame.display.update()
						#parse input
						parseinput(inputflag,inputstring)
						inputstring=""
						stringbuf=False
					elif paused:
						paused=False
					else:
						paused=True

				if event.key == pygame.K_PLUS:
					gamespeed+=1
					print gamespeed

				if event.key == pygame.K_MINUS:
					if gamespeed >1:
						gamespeed-=1
					print gamespeed

				if event.key == pygame.K_s:
					sendlabeltoboard(inputstring,board)
					inputflag="s"
					stringbuf=True

				if event.key == pygame.K_l:
					sendlabeltoboard(inputstring,board)
					inputflag="l"
					stringbuf=True

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.mouse.get_rel()
			#could be RMB for moving
			if pygame.mouse.get_pressed()==(True,False,False):
				leftclick=True

		if event.type == pygame.MOUSEBUTTONUP:
			#if mousebutton pressed was not for moving
			if leftclick:
				board.mouseclick(pygame.mouse.get_pos())
				pygame.display.update()
				leftclick=False

		if event.type == pygame.MOUSEMOTION:
			if pygame.mouse.get_pressed()==(False,False,True):
				board.movecamera(pygame.mouse.get_rel())
				pygame.display.update()
