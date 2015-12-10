import Python.audio_example
import scipy
import scipy.io.wavfile
import pylab
import matplotlib
import numpy

def I(x):
	temp = []
	for i in xrange(1, len(x), 2):
		temp.append((x[i] + x[i-1])/float(2))
	return temp

def haar(x):
	transformed = []
	for i in xrange(0, len(x)-2, 2):
		I_temp = I(x)
		temp = []
		for j in xrange(0, len(I_temp),1):
			temp.extend([x[j*2] - I_temp[j]])
		x = I_temp
		transformed = temp + transformed
		if len(x) == 1:
			transformed = x + transformed    
	return transformed 

def short_time_haar(x, window_len=4096, window_shift=2048):
	haar_result = []
	haar1_result = []
	for i in range(0, len(x)-window_len, window_shift):
		haar_result.append(haar(numpy.array(x[i:i+window_len])))
	return scipy.absolute(haar_result)

if __name__ == '__main__':
	for i in range(0,5):
		name = str(i+1)
		if i == 4:
			name = 'Rerecord'
		rate, data = scipy.io.wavfile.read('./Data/tracks/' + name + '.wav')
		if len(data.shape) > 1:
			data = data[:,0]
		X = numpy.array(short_time_haar(data[0:10*rate]))
		Python.audio_example.plot_transform(X)
		pylab.savefig('haar_spectorgram' + name + '.png')
		pylab.close()
