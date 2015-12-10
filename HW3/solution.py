import numpy as np
import random
from scipy.io import loadmat
from matplotlib import pylab as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from sklearn.manifold import Isomap 
from sklearn.manifold import MDS
from sklearn.decomposition import PCA

def extract_features():
	data, labels = [], []
	d = loadmat('face_data.mat')
	data = d['images']
	labels = d['poses']
	lights = d['lights']
	data = data.transpose()
	labels = labels.transpose()
	#for i in range(0, 698):
	#	face = data[i, :].reshape(64,64)
	#	face = face.transpose()
	#	plt.imshow(face, cmap = cm.Greys_r)
	#	plt.savefig('faces/' + str(i) + '.png')
	#	plt.close()
	return data,labels,lights

def find_NN(data, compare_data, name, face):
	for i in range(0,10):
		distance = float('inf')
		for j in range(0, 698):
			if face[i] != j:
				d = np.sum(np.square(compare_data[j] - compare_data[face[i]]))
				if d < distance:
					distance = d
					location = j
		face_ = data[face[i], :].reshape(64,64)
        face_ = face_.transpose()
        plt.imshow(face_, cmap = cm.Greys_r)
		plt.savefig(name + 'NN/' + str(face[i]) + '.png')
		plt.close()
		face_ = data[location, :].reshape(64,64)
        face_ = face_.transpose()
        plt.imshow(face_, cmap = cm.Greys_r)
        plt.savefig(name + 'NN/' + str(face[i]) + '_NN' + str(location) + '.png')
        plt.close()

def visualize(origindata, data, labels, lights, name):
	X = data[:,0]
	Y = data[:,1]
	plt.scatter(X, Y)
	plt.savefig(name + '.png')
	plt.close()
	X_ = labels[:,0]
	Y_ = labels[:,1]
	plt.scatter(X, X_)
	plt.savefig(name + 'X.png')
	plt.close()
	plt.scatter(Y, Y_)
    plt.savefig(name + 'Y.png')
    plt.close()
	plt.scatter(X, Y_)
    plt.savefig(name + 'X_.png')
    plt.close()
    plt.scatter(Y, X_)
    plt.savefig(name + 'Y_.png')
    plt.close()
	plt.scatter(X, lights)
    plt.savefig(name + 'Xl.png')
    plt.close()
    plt.scatter(Y, lights)
    plt.savefig(name + 'Yl.png')
    plt.close()

def PCA_(data):
	pca = PCA(n_components=2)
	PCA_data = pca.fit_transform(data)
	return PCA_data

def MDS_(data):
	mds = MDS(n_components=2)
	MDS_data = mds.fit_transform(data)
	return MDS_data

def Isomap_(data):
	iso = Isomap(n_components=2)
    Isomap_data = iso.fit_transform(data)
    return Isomap_data

if __name__ == '__main__':
	data,labels,lights = extract_features()
	#selected_face = random.sample(range(696), 10)
	selected_face = [57, 142, 225, 286, 304, 375, 387, 481, 618, 684]
	find_NN(data, data, "", selected_face) 
	PCA_data = PCA_(data)
	MDS_data = MDS_(data)
	Isomap_data = Isomap_(data)
	visualize(data, PCA_data, labels, lights, "PCA_2D")
	visualize(data, MDS_data, labels, lights, "MDS_2D")
	visualize(data, Isomap_data, labels, lights, "Isomap_2D")
	find_NN(data, PCA_data, "PCA_", selected_face)
	find_NN(data, MDS_data, "MDS_", selected_face)
	find_NN(data, Isomap_data, "Isomap_", selected_face)
