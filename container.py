
from physics import Physics
from constants import SIZE
import numpy as np
from cell import Cell

class Container:

	def __init__ (self, dt, diff, visc):

		self.size = SIZE
		self.dt = dt
		self.diff = diff
		self.visc = visc

		self.grid = self.InitArr(self.size)

		self.physics = Physics()


	def InitArr(self, size):
		dictionary = {}
		for i in range(0,size+1,1):
			subdict = {}
			for j in range(0,size+1,1):
				subdict[j] = Cell()
			dictionary[i] = subdict
		return dictionary

	def AddDensity(self, x, y, amount):
		self.grid[x][y].density += amount

	def FadeDensity(self, size):
		for y in range(0,size,1):
			for x in range(0,size,1):
				d = self.grid[x][y].density
				self.grid[x][y].densityt = 0 if (d - 0.5) < 0 else (d - 0.5)


	def AddVelocity(self, x, y, amountX, amountY):
		try:
			self.grid[x][y].x += amountX
			self.grid[x][y].y += amountY
		except Exception as e: print('AddVelocity exception', e)


	def Step(self):
		try :
			iterations = 4
			self.physics.Diffuse(1, self.grid, self.visc, self.dt, iterations, self.size, 'px')
			self.physics.Diffuse(2, self.grid, self.visc, self.dt, iterations, self.size, 'py')

			self.physics.Project(self.grid, iterations, self.size)

			self.physics.Advect(1, self.grid, self.dt, self.size)

			self.physics.ProjectPrevious(self.grid, iterations, self.size)
			 

			self.physics.Diffuse(0, self.grid, self.visc, self.dt, iterations, self.size, 'density')
			self.physics.AdvectDensity(1, self.grid, self.dt, self.size)

		except Exception as e: print('Step exception', e)
