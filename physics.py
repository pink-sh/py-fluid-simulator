import math
from constants import SIZE


class Physics:

	def SetBnd(self, b, grid, attr, N):
		for i in range(1,N-1,1):
			setattr(grid[i][0], attr, -getattr(grid[i][1], attr) if b==2 else getattr(grid[i][1], attr))
			setattr(grid[i][N-1], attr, -getattr(grid[i][N], attr) if b==2 else getattr(grid[i][N], attr))
		for j in range(1,N-1,1):
			setattr(grid[0][j], attr, -getattr(grid[1][j], attr) if b==2 else getattr(grid[1][j], attr))
			setattr(grid[N-1][j], attr, -getattr(grid[N-2][j], attr) if b==2 else getattr(grid[N-2][j], attr))

		setattr(grid[0][0], attr, 0.5 * getattr(grid[1][0], attr) + getattr(grid[0][1], attr))
		setattr(grid[0][N-1], attr, 0.5 * getattr(grid[1][N-1], attr) + getattr(grid[0][N-2], attr))
		setattr(grid[N-1][0], attr, 0.5 * getattr(grid[N-1][0], attr) + getattr(grid[N][1], attr))
		setattr(grid[N-1][N-1], attr, 0.5 * getattr(grid[N-1][N], attr) + getattr(grid[N][N-1], attr))


	def LinSolve(self, b, grid, a, c, iter, N, attributeSet, attributeGet):
		cRecip = 1.0 / c
		for i in range(0,iter-1,1):
			for y in range (1,N-2,1):
				for x in range(1,N-2,1):
					cell = grid[x][y]
					getP = getattr(cell, attributeGet)
					setattr(grid[x][y], attributeSet, (getP + a * ( getattr(grid[x-1][y], attributeSet) + getattr(grid[x+1][y], attributeSet) + getattr(grid[x][y-1], attributeSet) + getattr(grid[x][y+1], attributeSet)  )) * cRecip)
			# self.SetBnd(b, grid, attributeSet, N)



	def Diffuse(self, b, grid, diff, dt, iter, N, solver):
		movingFactor = dt * diff * (N**2)
		if (solver == 'py'):
			self.LinSolve(b, grid, movingFactor, 1 + 6 * movingFactor, iter, N, 'py', 'y')
		if (solver == 'px'):
			self.LinSolve(b, grid, movingFactor, 1 + 6 * movingFactor, iter, N, 'px', 'x')
		if (solver == 'density'):
			self.LinSolve(b, grid, movingFactor, 1 + 6 * movingFactor, iter, N, 'pDensity', 'density')


	def Project(self, grid, iter, N):
		for y in range(1, N-2, 1):
			for x in range(1, N-2, 1):
				grid[x][y].y = -0.5 * ( grid[x+1][y].px - grid[x-1][y].px + grid[x][y+1].py - grid[x][y-1].py ) / N
				grid[x][y].x = 0

		self.SetBnd(0, grid, 'y', N)
		self.SetBnd(0, grid, 'x', N)
		self.LinSolve(0, grid, 1, 6, iter, N, 'x', 'y')

		for y in range(1, N-2, 1):
			for x in range(1, N-2, 1):
				grid[x][y].px -= 0.5 * ( grid[x+1][y].x - grid[x-1][y].x ) * N
				grid[x][y].py -= 0.5 * ( grid[x][y+1].x - grid[x][y-1].x ) * N

		self.SetBnd(1, grid, 'px', N)
		self.SetBnd(2, grid, 'py', N)



	def ProjectPrevious(self, grid, iter, N):
		for y in range(1, N-2, 1):
			for x in range(1, N-2, 1):
				grid[x][y].py = -0.5 * ( grid[x+1][y].x - grid[x-1][y].x + grid[x][y+1].y - grid[x][y-1].y ) / N
				grid[x][y].px = 0

		self.SetBnd(0, grid, 'py', N)
		self.SetBnd(0, grid, 'px', N)
		self.LinSolve(0, grid, 1, 6, iter, N, 'px', 'py')

		for y in range(1, N-2, 1):
			for x in range(1, N-2, 1):
				grid[x][y].x -= 0.5 * (grid[x+1][y].px - grid[x-1][y].px) * N
				grid[x][y].y -= 0.5 * (grid[x][y+1].px - grid[x][y-1].px) * N

		self.SetBnd(1, grid, 'x', N)
		self.SetBnd(2, grid, 'y', N)



	def Advect(self, b, grid, dt, N):
		Nfloat = N

		dtx = dt * (N - 2);
		dty = dt * (N - 2);

		jfloat = 1
		for j in range(1, N-2, 1):
			ifloat = 1
			for i in range(1, N-2, 1):
				tmp1 = dtx * grid[i][j].px
				tmp2 = dty * grid[i][j].py
				x = ifloat - tmp1
				y = jfloat - tmp2
                
				if (x < 0.5): 
					x = 0.5
				if (x > Nfloat + 0.5):
					x = Nfloat + 0.5

				i0 = math.floor(x)
				i1 = i0 + 1.0

				if (y < 0.5):
					y = 0.5
				if (y > Nfloat + 0.5):
					y = Nfloat + 0.5

				j0 = math.floor(y)
				j1 = j0 + 1.0;

				s1 = x - i0
				s0 = 1.0 - s1
				t1 = y - j0
				t0 = 1.0 - t1
                
				i0i = SIZE if SIZE < int(i0) else int(i0)
				i1i = SIZE if SIZE < int(i1) else int(i1)
				j0i = SIZE if SIZE < int(j0) else int(j0)
				j1i = SIZE if SIZE < int(j1) else int(j1)
                
				try:
					grid[i][j].x = s0 * (t0 * grid[i0i][j0i].px + t1 * grid[i0i][j1i].px) + \
									s1 * (t0 * grid[i1i][j0i].px + t1 * grid[i1i][j1i].px)

					grid[i][j].y = s0 * (t0 * grid[i0i][j0i].py + t1 * grid[i0i][j1i].py) + \
									s1 * (t0 * grid[i1i][j0i].py + t1 * grid[i1i][j1i].py)

				except Exception as e: print('Advect exception', e, i1i, j0i)

				ifloat = ifloat + 1

			jfloat = jfloat + 1

		self.SetBnd(b, grid, 'x', N)

	def AdvectDensity(self, b, grid, dt, N):
		Nfloat = N

		dtx = dt * (N - 2);
		dty = dt * (N - 2);

		jfloat = 1
		for j in range(1, N-2, 1):
			ifloat = 1
			for i in range(1, N-2, 1):
				tmp1 = dtx * grid[i][j].x
				tmp2 = dty * grid[i][j].y
				x = ifloat - tmp1
				y = jfloat - tmp2
                
				if (x < 0.5): 
					x = 0.5
				if (x > Nfloat + 0.5):
					x = Nfloat + 0.5

				i0 = math.floor(x)
				i1 = i0 + 1.0

				if (y < 0.5):
					y = 0.5
				if (y > Nfloat + 0.5):
					y = Nfloat + 0.5

				j0 = math.floor(y)
				j1 = j0 + 1.0;

				s1 = x - i0
				s0 = 1.0 - s1
				t1 = y - j0
				t0 = 1.0 - t1
                
				i0i = SIZE if SIZE < int(i0) else int(i0)
				i1i = SIZE if SIZE < int(i1) else int(i1)
				j0i = SIZE if SIZE < int(j0) else int(j0)
				j1i = SIZE if SIZE < int(j1) else int(j1)
                
				try:
					grid[i][j].density = s0 * (t0 * grid[i0i][j0i].pDensity + t1 * grid[i0i][j1i].pDensity) + \
											s1 * (t0 * grid[i1i][j0i].pDensity + t1 * grid[i1i][j1i].pDensity)

				except Exception as e: print('AdvectDensity exception', e, i1i, j0i)

				ifloat = ifloat + 1

			jfloat = jfloat + 1
		self.SetBnd(b, grid, 'density', N)