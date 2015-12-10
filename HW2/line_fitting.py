import Python.audio_example
import scipy
import pylab as plt
import matplotlib
import numpy
import Python.STFT_audio
import random
import math

def find_line(points):
    	if (points[1][0] - points[0][0]) == 0:
        	#when the line is vertical return inf and try again
        	return float("inf")
    	if (points[1][1] - points[0][1]) == 0:
		return float("inf")
	m = (points[1][1]-points[0][1]) / float(points[1][0]-points[0][0])
	b = points[1][1] - m * points[1][0]
    	if float((1 + m**2) + b) == 0:
		return float("inf")
    	return (m, b)

def find_intercept(currentModel, point):
    	m = currentModel[0]
    	b = currentModel[1]
    	x0 = point[0]
    	y0 = point[1]
    	x = (x0 + m*y0 - m*b)/float(1 + m**2)
    	y = m*x + b
    	return (x,y)

def ransac_2D(points):
    	K = 100       #number of iterations
    	thresh = 3    #ransac threshold 
    	ransac_ratio = 0.6   #ratio of inliers for a good model
	ratio = 0.0
    	for i in xrange(K):
		print K
    	    	#estimate line from 2 random points
    	    	currentModel = find_line(random.sample(points, 2))
    	    	#ignore verticle lines
    	    	if currentModel == float("inf"):
   	         	while currentModel == float("inf"):
   	             		currentModel = find_line(random.sample(points, 2))
        	currentInliers = []
        	#find all inliers
        	for point in points:
        	    	intercept = find_intercept(currentModel, point)
        	    	dist = math.sqrt((intercept[0] - point[0])**2 + (intercept[1] - point[1])**2)
			if dist < thresh:
        		        currentInliers.append(point)
        	if len(currentInliers)/float(len(points)) > ratio:
            		ratio = len(currentInliers)/float(len(points))
            		bestModel = currentModel
		#break when we have enough inliers. we have a good model
        	if len(currentInliers) > len(points)*ransac_ratio:
            		break
    	#returns m and b of line
    	return bestModel

def hough_transform(points):
	hough = dict()
	for t1,t2 in points:
		for i in range(1,500):
			if i != 250:
				t = i*math.pi/500
				r = t1*math.cos(t)+t2*math.sin(t)
				r = float(int(r*500)/500.00)
				if hough.has_key((t,r)):
					hough[(t,r)] = hough[(t,r)] + 1
				else:
					hough[(t,r)] = 1
	max = 0
	for para,count in hough.items():
		if count > max:
			max = count
			result = para
			print result
	return result

def findmin(a, b):
	if a < b:
		return a
	return b

def hash_table(data, rate):
	X = Python.audio_example.stft(data[0:10*rate])
        [peaks, yt] = Python.STFT_audio.compute(X, 20)
	y = list()
	l = len(peaks)
	for i in range(0, l-1):
		N = 0
		for j in range(i+1, l):
			if (abs(peaks[i][0] - peaks[j][0]) < 50) and (abs(peaks[i][1] - peaks[j][1]) < 50):
				tuple_ = (findmin(peaks[i][0], peaks[j][0]),peaks[i][1] + abs(peaks[i][0] - peaks[j][0]) + abs(peaks[i][1] - peaks[j][1]))
				y.append(tuple_)
				N = N + 1
			if N >= 100:
				break
	#print len(y)
	return y		

def match_hashvalue(y1, y2, print_matchpair, num):
	l1 = len(y1)
	l2 = len(y2)
	match_pair = list()
	for i in range(0, l1):
		for j in range(0, l2):
			if y1[i][1] == y2[j][1]:
				match_pair.append((y1[i][0], y2[j][0]))
	if print_matchpair:
		print match_pair
	for pair in match_pair:
		plt.scatter(pair[0], pair[1])
	[theta,p] = hough_transform(match_pair)
	x = [0, 200]
	y = [p/math.sin(theta),p/math.sin(theta)-200*math.cos(theta)/math.sin(theta)]
	plt.plot(x,y,label='hough_transform')
	[m,b] = ransac_2D(match_pair)
	x = [0, 200]
	y = [0*m+b, 200*m+b]
	plt.plot(x,y,"r--",label="ransac")
	plt.legend()
	plt.xlim(0,200)
	plt.ylim(0,200)
	plt.savefig('match_hashvalue_' + num + '.png')
	plt.close()

if __name__ == '__main__':
	rate, data = scipy.io.wavfile.read('./Data/tracks/1.wav')
	if len(data.shape) > 1:
		data = data[:,0]
	y1 = hash_table(data, rate)
	rate, data = scipy.io.wavfile.read('./Data/tracks/2.wav')
        if len(data.shape) > 1:
                data = data[:,0]
        y2 = hash_table(data, rate)
	rate, data = scipy.io.wavfile.read('./Data/tracks/3.wav')
        if len(data.shape) > 1:
                data = data[:,0]
        y3 = hash_table(data, rate)
	rate, data = scipy.io.wavfile.read('./Data/tracks/4.wav')
        if len(data.shape) > 1:
                data = data[:,0]
        y4 = hash_table(data, rate)
	match_hashvalue(y1,y2,True,'1vs2')
	match_hashvalue(y1,y3,False,'1vs3')
	match_hashvalue(y1,y4,False,'1vs4')
