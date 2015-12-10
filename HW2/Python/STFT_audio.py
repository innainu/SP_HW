import Python.audio_example
import scipy
import pylab
import matplotlib
import numpy

def question1(path, title, savepath):
	rate, data = scipy.io.wavfile.read(path)
	if len(data.shape) > 1:
		data = data[:,0]
	y = data
	x = range(0,len(data))
	pylab.plot(x, y)
	pylab.title(title)
	pylab.savefig(savepath)
	pylab.close()
	return rate,y	

def compute(data, K):
	ans = []
	yt = [0]*len(data)
	for i in range(0, len(data) - K + 1):
		for j in range(0, len(data[0]) - K + 1):
			X = data[i:i+K,j:j+K]
			index = numpy.argmax(X) 
			max_ = numpy.max(X)
			f = index%20
			s = (index - index%20)/20
			if (f == K/2) & (s == K/2):
				tuple_s = (s+i,f+j)
				ans.append(tuple_s)
				yt[s+i] = max_
	return ans, yt
	
if __name__ == '__main__':
	start = [3.07, 0, 0.92, 4.21, 3.57]
	end = [4.11, 1.24, 1.97, 5.32, 4.61]
	yt_ = []
	for i in range(0,5):
		name = str(i+1)
		if i == 4:
			name = 'Rerecord'
		[rate, data] = question1('./Data/tracks/' + name + '.wav', name + '.wav', name + 'wav.png')
		X = Python.audio_example.stft(data[0:10*rate])
		Python.audio_example.plot_transform(X)
		pylab.savefig('spectorgram' + name + '.png')
		pylab.close()
		[peaks, yt] = compute(X, 20)
	 	Python.audio_example.plot_peaks(peaks, start[i]*rate/2048, end[i]*rate/2048)
		pylab.xlim([0,207])
		pylab.savefig('peaks_' + name + '.png')
		pylab.close()
		pylab.xlim([0,207])
		yt_.append(yt)
		pylab.plot(yt)
		pylab.savefig('yt_array' + name + '.png')
		pylab.close()
	
		if i != 0:
			cross_correlation = numpy.correlate(yt_[0], yt_[i], 'full')
			pylab.plot(cross_correlation)
			pylab.savefig('cross_correlation_' + name + '.png')
			pylab.close()
