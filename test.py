from cell import Cell
import time
from joblib import Parallel, delayed
import multiprocessing


n_cores = multiprocessing.cpu_count()

print("The system has ", n_cores, "available cores")

def current_milli_time():
    return round(time.time() * 1000)

def getDictionaryParallel(size):

	def Build(i):
		subdict = {}
		for j in range(0,size+1,1):
			subdict[j] = Cell()
			# dictionary[i] = subdict
		return subdict

	return Parallel(n_jobs=n_cores)(delayed(Build)(i) for i in range(0, size+1, 1))



def getDictionary1(size):
	dictionary = {}
	for i in range(0,size+1,1):
		subdict = {}
		for j in range(0,size+1,1):
			subdict[j] = Cell()
			dictionary[i] = subdict

	# for i in range(0,size+1,1):
	# 	for j in range(0,size+1,1):
	# 		x = dictionary[i][j] 
	return dictionary



def getDictionary2(size):
	dictionary = {}
	for i in range(0,size*size,1):
		dictionary[i] = Cell()
	# for i in range(0,size*size,1):
	# 	x = dictionary[i]
	return dictionary




start = current_milli_time()
getDictionaryParallel(3)
print ('size 3', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionaryParallel(10)
print ('size 10', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionaryParallel(100)
print ('size 100', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionaryParallel(200)
print ('size 200', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionaryParallel(400)
print ('size 400', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionaryParallel(800)
print ('size 800', current_milli_time() - start, 'milliseconds')

print('-----------------------------------------')

start = current_milli_time()
getDictionary1(3)
print ('size 3', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(10)
print ('size 10', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(100)
print ('size 100', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(200)
print ('size 200', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(400)
print ('size 400', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(800)
print ('size 800', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(1000)
print ('size 1000', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary1(2000)
print ('size 2000', current_milli_time() - start, 'milliseconds')

print('-----------------------------------------')

start = current_milli_time()
getDictionary2(3)
print ('size 3', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(10)
print ('size 10', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(100)
print ('size 100', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(200)
print ('size 200', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(400)
print ('size 400', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(800)
print ('size 800', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(1000)
print ('size 1000', current_milli_time() - start, 'milliseconds')

start = current_milli_time()
getDictionary2(2000)
print ('size 2000', current_milli_time() - start, 'milliseconds')

# start = current_milli_time()
# getDictionaryParallel(1000)
# print ('size 1000', current_milli_time() - start, 'milliseconds')




# dictionary = {}
# for i in range(0,size+1,1):
# 	subdict = {}
# 	for j in range(0,size+1,1):
# 		subdict[j] = Cell()
# 		dictionary[i] = subdict


# start = current_milli_time()

# for i in range(0,size-1,1):
# 	for j in range(0,size-1,1):
# 		x = dictionary[i][j].density

# stop = current_milli_time() - start
# print ('dictionary as matrix ', size, 'x', size, 'took', stop, 'milliseconds')

# print (ord('a'))
# print (ord('a')+100)

# dictionary = {}
# for i in range(ord('a'),ord('a')+size+1,1):
# 	for j in range(ord('a'),ord('a')+size+1,1):
# 		dictionary[ord('a')+i+j] = Cell()


# start = current_milli_time()

# for i in range(ord('a'),ord('a')+size+1,1):
# 	for j in range(ord('a'),ord('a')+size+1,1):
# 		x = dictionary[ord('a')+i+j].density

# stop = current_milli_time() - start
# print ('dictionary as array ', size, 'x', size, 'took', stop, 'milliseconds')




# def process(i):
#     return i * i
    
# results = Parallel(n_jobs=8)(delayed(process)(i) for i in range(1000000))
# # print(results)

