# -*- coding: utf-8 -*-
# Oscar Saharoy 2017

import sys,pygame,math,numpy,gooey,tkFont,Tkinter

# Config

pygame.init()

info = pygame.display.Info()

x_res = info.current_h/2 # Width of display
y_res = info.current_h/2 # Height of display

p_res = info.current_h/3 # height of settings panel
SP    = p_res * 0.06 # measurement unit

frmrt = 16   # delay between frames in ms

# Palette

white = (255, 255, 255)
black = (  0,   0,   0)
leaf  = ( 30, 255,  30)
jade  = (100, 150, 100)

# settings panel is a tkinter window, seperate from the main display

class IO_Panel(gooey.Tk):

	def __init__(self,parent):

		self.parent = parent

		# creating some sizing variables to use to position widgets and allow scalability

		H  = p_res
		F  = p_res * 0.02
		SP = p_res * 0.06
		L  = p_res * 0.6

		gooey.Tk.__init__(self)
		self.config(padx=SP,pady=SP)
		self.resizable(0,0) # disable resizing

		self.wm_title(' Matrix Manipulation')

		icon = Tkinter.PhotoImage(file='matrix.gif') # setting favicon
		self.tk.call('wm', 'iconphoto', self._w, icon)  

		self.closed = False
		self.protocol("WM_DELETE_WINDOW", self.close) # call self.close() if window is closed by user

		# Creating fonts

		arial_big   = tkFont.Font(family="Arial",   size=int(F*3.5), weight=tkFont.BOLD)
		arial_med   = tkFont.Font(family="Arial",   size=int(F*2),   weight=tkFont.BOLD)

		verdana_big = tkFont.Font(family="Verdana", size=int(F*6))
		verdana_med = tkFont.Font(family="Verdana", size=int(F*2),   weight=tkFont.BOLD)
		verdana_sml = tkFont.Font(family="Verdana", size=int(F*1.4), weight=tkFont.BOLD)

		self.title1 = gooey.Label(self,text='Settings',font=arial_big)
		self.title1.grid(sticky='w',columnspan=2)

		gooey.Spacer(self,height=SP,width=SP).grid()

		self.rotation_title = gooey.Label(self,text='Rotation Angle',font=verdana_med,fg='grey34')
		self.rotation_title.grid(column=1,row=2,sticky='w')

		gooey.Spacer(self,height=SP,width=SP*1.5).grid(column=2,row=2)

		self.rotation_scale = gooey.Scale(self,from_=0,to=math.pi*2,length=L,height=SP*1.3)
		self.rotation_scale.grid(column=3,row=2)

		gooey.Spacer(self,height=SP,width=SP).grid(column=4,row=2)

		self.rotation_label = gooey.Label(self,text='0.0',font=verdana_sml,fg='grey34')
		self.rotation_label.grid(column=5,row=2,sticky='w')

		gooey.Spacer(self,height=SP,width=SP).grid()

		self.scale_title = gooey.Label(self,text='Scale',font=verdana_med,fg='grey34')
		self.scale_title.grid(column=1,row=4,sticky='w')

		self.scale_scale = gooey.Scale(self,from_=-3,to=3,length=L,height=SP*1.3)
		self.scale_scale.grid(column=3,row=4)

		self.scale_scale.set(1.0)

		self.scale_label = gooey.Label(self,text='1.0',font=verdana_sml,fg='grey34')
		self.scale_label.grid(column=5,row=4,sticky='w')

		gooey.Spacer(self,height=SP,width=SP).grid()

		self.trans_title = gooey.Label(self,text='Translation',font=verdana_med,fg='grey34')
		self.trans_title.grid(column=1,row=6,sticky='w')

		self.x_label = gooey.Label(self,text='X',font=verdana_sml,fg='grey34')
		self.x_label.grid(column=2,row=6,sticky='e')

		self.transx_scale = gooey.Scale(self,from_=-H,to=H,length=L,height=SP*1.3)
		self.transx_scale.grid(column=3,row=6)
		self.transx_scale.set(0)

		self.transx_label = gooey.Label(self,text='0.0',font=verdana_sml,fg='grey34')
		self.transx_label.grid(column=5,row=6,sticky='w')

		self.y_label = gooey.Label(self,text='Y',font=verdana_sml,fg='grey34')
		self.y_label.grid(column=2,row=7,sticky='e')

		self.transy_scale = gooey.Scale(self,from_=H,to=-H,length=L,height=SP*1.3)
		self.transy_scale.grid(column=3,row=7)
		self.transy_scale.set(0)

		self.transy_label = gooey.Label(self,text='0.0',font=verdana_sml,fg='grey34')
		self.transy_label.grid(column=5,row=7,sticky='w')

		gooey.Spacer(self,width=SP*5).grid(column=5,row=0)
		gooey.Spacer(self,height=SP*0.33).grid(column=0,row=8)

		# Matrix display at bottom of screen

		self.matrix_frame = gooey.Frame(self,highlightthickness=0)
		self.matrix_frame.grid(row=9,columnspan=6)

		self.left_bracket = gooey.Label(self.matrix_frame,text='×[',font=verdana_big)
		self.left_bracket.grid(column=0,row=0)

		self.middle_bracket = gooey.Label(self.matrix_frame,text=']+[',font=verdana_big)
		self.middle_bracket.grid(column=2,row=0)

		self.right_bracket = gooey.Label(self.matrix_frame,text=']',font=verdana_big)
		self.right_bracket.grid(column=4,row=0)

		self.numbers_frame = gooey.Frame(self.matrix_frame,highlightthickness=0)
		self.numbers_frame.grid(column=1,row=0)

		gooey.Spacer(self.numbers_frame,height=SP*0.66,width=H*0.6).grid(columnspan=2)

		self.top_left = gooey.Label(self.numbers_frame,font=verdana_med)
		self.top_left.grid(column=0,row=1,sticky='e')

		self.bottom_left = gooey.Label(self.numbers_frame,font=verdana_med)
		self.bottom_left.grid(column=0,row=2,sticky='e')

		self.top_right = gooey.Label(self.numbers_frame,font=verdana_med)
		self.top_right.grid(column=1,row=1,sticky='e')

		self.bottom_right = gooey.Label(self.numbers_frame,font=verdana_med)
		self.bottom_right.grid(column=1,row=2,sticky='e')

		self.trans_frame = gooey.Frame(self.matrix_frame,highlightthickness=0)
		self.trans_frame.grid(column=3,row=0,sticky='e')

		gooey.Spacer(self.trans_frame,height=SP*0.66,width=SP*6).grid()

		self.top_trans = gooey.Label(self.trans_frame,font=verdana_med)
		self.top_trans.grid(column=0,row=1,sticky='e')

		self.bottom_trans = gooey.Label(self.trans_frame,font=verdana_med)
		self.bottom_trans.grid(column=0,row=2,sticky='e')

		gooey.Spacer(self,height=SP).grid()

		# top buttons

		self.reset_button = gooey.Button(self,text='Reset',font=arial_med,fg='grey34',command=self.reset)
		self.reset_button.grid(column=5,row=0,sticky='nsew')

		self.help_button = gooey.Button(self,text='?',font=arial_med,fg='grey34',command=self.help)
		self.help_button.grid(column=4,row=0,sticky='nsew')

		self.F  = F
		self.arial_big = arial_big
		self.verdana_med = verdana_med
		self.verdana_sml = verdana_sml

	def close(self):

		self.closed = True
		self.destroy()

	def help(self):
		
		box = gooey.Toplevel(self,padx=SP,pady=SP)

		icon = Tkinter.PhotoImage(file='matrix.gif') # setting favicon
		self.tk.call('wm', 'iconphoto', box._w, icon)  

		help_title = gooey.Label(box,font=self.arial_big,text='Help')
		help_title.grid(sticky='w',columnspan=2,column=0,row=1)

		helpstring = '''Welcome to Matrix Manipulation. This tool is intended to help visualise and understand matrix transformations in 2 dimensions. 
						Left click the display to add a point, or right click one to delete it.
						You can use the sliders to change values such as scale or rotation and view their effects on the points you have placed as well as see the matrix used for the transformation.'''

		text = gooey.Message(box,text=helpstring,font=self.verdana_sml,width=x_res/2)
		text.grid(column=1,row=2,sticky='w')

	def reset(self):

		# reset scales to defualt and refresh display
		self.rotation_scale.set(0)
		self.scale_scale.set(1)

		self.transx_scale.set(0)
		self.transy_scale.set(0)

		self.parent.reset()
		self.get_values()
		self.refresh()

	def update_matrix(self,matrix,trans):

		# sets value of various labels on the settings panel to make the matrix display

		tl = round(matrix[0,0],3)
		bl = round(matrix[1,0],3)
		tr = round(matrix[0,1],3)
		br = round(matrix[1,1],3)

		self.top_left.config(     text=tl)
		self.bottom_left.config(  text=bl)
		self.top_right.config(    text=tr)
		self.bottom_right.config( text=br)

		self.top_trans.config(text=    trans[0])
		self.bottom_trans.config(text=-trans[1])


	def get_values(self):

		# retrieves values of sliders and returns them to be used to make the tranformation matrix

		theta =  round(self.rotation_scale.get(),3)

		scale =  round(self.scale_scale.get(),3)	

		trans = [round(self.transx_scale.get(),3),
				 round(self.transy_scale.get(),3)]

		self.rotation_label.config(text=theta)

		self.scale_label.config(text=scale)

		self.transx_label.config(text=trans[0])
		self.transy_label.config(text=-trans[1]) # y value has to be flipped to make upwards on the screen positive y

		return theta,scale,trans

	def refresh(self):

		if not self.closed:

			# update methods for tkinter window
			self.update_idletasks()
			self.update()


class Engine(object):

	def __init__(self):

		self.surface   = pygame.display.set_mode((x_res,y_res)) # initialise window for drawing
		pygame.display.set_caption(' Matrix Manipulation')

		# setting favicon
		icon = pygame.image.load('matrix.png')
		pygame.display.set_icon(icon)

		# matrix of the triangle which is going to be transformed
		self.tri       = numpy.matrix( [[ x_res/4, x_res/3, x_res/5],
									    [ y_res/3, y_res/5, y_res/4]] )

		self.panel 	   = IO_Panel(self)

		self.mainloop()

	def get_matrix(self,theta,scale,trans):

		# returns matrix to transform coordinates

		cos = math.cos
		sin = math.sin

		# this matrix handles rotation through angle theta
		rotation  = numpy.matrix( [[  cos(theta), sin(theta)],
			    			  	   [ -sin(theta), cos(theta)]] )

		# this matrix scales points from the origin
		scaling   = numpy.matrix( [[scale,0.0],
								   [0.0,scale]])

		self.panel.update_matrix(scaling * rotation,trans)

		return scaling * rotation

	def click(self):

		pressed = pygame.mouse.get_pressed() # list of bools of whether mouse buttons are pressed

		if pressed[2]: # delete a point if right clicked

			mx,my = pygame.mouse.get_pos() # coords of mouse

			for x in range(self.tri.shape[1]):

				# subtract x and y offset from coords which centralise them
				px = self.tri[0,x] + x_res/2
				py = - self.tri[1,x] + y_res/2

				if ((mx-px)**2 + (my-py)**2)**0.5 <= SP/2: # test if dist from mouse to centre of point is less than 5px

					self.tri = numpy.delete(self.tri,x,1) # if yes then delete it
					break

		if pressed[0]: # add a point if the screen is left clicked

			mx,my = pygame.mouse.get_pos()

			# translate mouse coords to undo alignment with centre of screen
			nx =   mx - x_res/2
			ny = - my + y_res/2

			point = numpy.matrix([[nx],
								  [ny]])

			self.tri = numpy.append(self.tri,point,1) # add to end of self.tri

	def draw(self):

		SP = int(p_res * 0.06)

		self.surface.fill(white) # clear screen

		theta, scale, trans = self.panel.get_values()

		pygame.draw.line(self.surface,black, (x_res/2,0), (x_res/2,y_res) ,SP/9) # draw y axis
		pygame.draw.line(self.surface,black, (0,y_res/2), (x_res,y_res/2) ,SP/9) # draw x axis

		tri0  = numpy.matrix([[1,0],
							  [0,-1]]) * self.tri # flip y cordinate to display correctly - positive y is downward on screen

		tri1  = self.get_matrix(theta,scale,trans) * tri0 # transform tri0 by transformation matrix

		tri1 += numpy.matrix([[trans[0]],
							  [trans[1]]]) # translate by translation amount

		centr = numpy.matrix([[x_res/2],
							  [y_res/2]]) # centralization matrix to bring points to middle of screen

		tri0 += centr # centralise both triangle matrices
		tri1 += centr # centralise both triangle matrices

		for p in range(self.tri.shape[1]):

			pygame.draw.circle(self.surface, jade, (int(tri1[0,p]), int(tri1[1,p])) ,SP/6) # draw translated points
			pygame.draw.circle(self.surface, leaf, (int(tri0[0,p]), int(tri0[1,p])) ,SP/6) # draw original points

	def reset(self):

		self.tri = numpy.matrix( [[ x_res/4, x_res/3, x_res/5],
								  [ y_res/3, y_res/5, y_res/4]] )

	def mainloop(self):

		while not self.panel.closed:

			# test for exit request
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			# draw triangles
			self.draw()

			# test for clicks
			self.click()

			# update screen and add delay
			pygame.display.flip()
			pygame.time.delay(frmrt)

			# update methods for tkinter window
			self.panel.refresh()

Engine()