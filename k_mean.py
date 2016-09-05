import csv
import pdb
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
from random import randint
from random import shuffle
from math import sqrt

def distance(point, centroid):
    square_sum = 0
    for i in range(0, len(point)):
        square_sum += (point[i] - centroid[i])**2
    return sqrt(square_sum)

def k_mean(data, k):
    centroids = []
    random_idx = generate_uniq_randoms(len(data), k)
    # Randomly initializing centroids
    for i in range(0, k):
        new_centroid = []
        for j in range(0, len(data[i])):
            new_centroid.append(data[random_idx[i]][j])
        centroids.append(new_centroid)

    labels = [None]*len(data)
    while True:
        for i in range(0, len(data)):
            labels[i] = assign_label(data[i], centroids)
        cluster_averages = compute_cluster_average(k, 2, data, labels)
        if is_equal(centroids, cluster_averages):
            break
        else:
            for i in range(0, len(centroids)):
                centroids[i] = cluster_averages[i]
    return labels

def is_equal(v, u):
    for i in range(0, len(v)):
        for j in range(0, len(v[i])):
            if v[i][j] != u[i][j]:
                return False
    return True

def compute_cluster_average(k, dimen, data, labels):
    cluster_averages = []
    cluster_population = [0]*k
    # we have k clusters and we are going to initlize 0 values for averages
    for i in range(0, k):
        cluster_averages.append([0]*dimen)

    for i in range(0, len(data)):
        cluster_idx = labels[i]
        cluster_population[cluster_idx] += 1
        for j in range(0, dimen):
            cluster_averages[cluster_idx][j] += data[i][j]

    for i in range(0, k):
        for j in range(0, dimen):
            cluster_averages[i][j] = cluster_averages[i][j]/cluster_population[i]

    return cluster_averages

def generate_uniq_randoms(int_range, k):
    arr = []
    max_int = int_range
    for i in range(0, max_int):
        arr.append(i)
    shuffle(arr)
    return arr[0:k]

def assign_label(point, centroids):
    min_distance = None
    centroid_idx = None
    for i in range(0, len(centroids)):
        dist = distance(point, centroids[i])
        if min_distance == None or dist < min_distance:
            min_distance = dist
            centroid_idx = i
    return centroid_idx

data = []
movie_file = open('movie_metadata.csv', 'rb')
csv_reader = csv.reader(movie_file)
for row in csv_reader:
    if row[8].isdigit():
        gross = float(row[8])/760505847
        rating = float(row[25])/10
        data.append([gross, rating])
labels = k_mean(data, 4)
colors = {0: 'red', 1: 'blue', 2: 'green', 3: 'purple', 4: 'yellow', 5: 'brown'}
figure = pyplot.figure()
axes = figure.add_axes()
sub1 = figure.add_subplot(211)
sub2 = figure.add_subplot(212)
for i in range(0, len(data)):
    sub1.scatter(data[i][0]*760505847, data[i][1]*10)
    sub2.scatter(data[i][0]*760505847, data[i][1]*10, color = colors[labels[i]])

pyplot.xlabel('Gross (in hundred millions $)')
pyplot.ylabel('IMBD Rating')
pyplot.show()
