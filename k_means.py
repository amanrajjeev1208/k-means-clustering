from pandas import DataFrame
import pandas as pd
import math
import matplotlib.pyplot as plt


#***************************************************************************
#**********************GENERAL PURPOSE FUNCTIONS****************************
#***************************************************************************

#function to get the input from excel file
def get_input():
	df = pd.read_excel('Datapoints.xlsx', sheet_name=0)
	df.head()
	return df

#function to get the values from the read input dataframe
def get_values(df):
	label = []
	x_cords = []
	y_cords = []
	Datapoints = []
	for i in range (0,32):
		label.append(df.iat[i,0])
		Datapoints.append([df.iat[i,1], df.iat[i,2]])
	return label, Datapoints

#function to calculate the distance between the cordiinates of 2 points
def calc_distance(x1, y1, x2, y2):
	x_diff = x1 - x2
	y_diff = y1 - y2
	distance = math.sqrt((x_diff * x_diff) + (y_diff * y_diff))
	return distance

#function to calculate the mean of the given cluster
def calc_mean(list):
	sum_x = 0
	sum_y = 0
	temp = [0,0]
	for item in list:
		sum_x += item[0]
		sum_y += item[1]
	temp = [sum_x / len(list), sum_y / len(list)]
	return temp

#function to plot the datapoints on a graph
def plot_points(c1, c2, c3, cf):
	x_c1 = []
	y_c1 = []
	x_c2 = []
	y_c2 = []
	x_c3 = []
	y_c3 = []
	x_cf = []
	y_cf = []
	for item in c1:
		x_c1.append(item[0])
		y_c1.append(item[1])
	for item in c2:
		x_c2.append(item[0])
		y_c2.append(item[1])
	for item in c3:
		x_c3.append(item[0])
		y_c3.append(item[1])
	for item in cf:
		x_cf.append(item[0])
		y_cf.append(item[1])
	plt.scatter(x_c1, y_c1, color= "green", marker= ".", s=30)
	plt.scatter(x_c2, y_c2, color= "yellow", marker= ".", s=30)
	plt.scatter(x_c3, y_c3, color= "blue", marker= ".", s=30)
	plt.scatter(x_cf, y_cf, color= "red", marker= "*", s=30)
	plt.xlabel('x - axis')
	plt.ylabel('y - axis')
	plt.title('Clusters and their centroids')
	plt.show()

#function to find the clusters
def find_clusters(datapoints, label, cent1, cent2, cent3):
	cluster1_label = []
	cluster2_label = []
	cluster3_label = []
	cluster1_datapoints = []
	cluster2_datapoints = []
	cluster3_datapoints = []
	for i in range(len(datapoints)):
		dist_cent1 = calc_distance(cent1[0], cent1[1], datapoints[i][0], datapoints[i][1])
		dist_cent2 = calc_distance(cent2[0], cent2[1], datapoints[i][0], datapoints[i][1])
		dist_cent3 = calc_distance(cent3[0], cent3[1], datapoints[i][0], datapoints[i][1])
		cluster_value = calc_smallest(dist_cent1, dist_cent2, dist_cent3)
		if cluster_value == 1:
			cluster1_label.append(label[i])
			cluster1_datapoints.append(datapoints[i])
		elif cluster_value == 2:
			cluster2_label.append(label[i])
			cluster2_datapoints.append(datapoints[i])
		else:
			cluster3_label.append(label[i])
			cluster3_datapoints.append(datapoints[i])
	return cluster1_label, cluster2_label, cluster3_label, cluster1_datapoints, cluster2_datapoints, cluster3_datapoints

#function to check the smallest among the 3 values
def calc_smallest(val1, val2, val3):
	smallest = 1
	if val2 < val1 and val2 < val3:
		smallest = 2
	elif val3 < val1:
		smallest = 3
	return smallest

#function to find the new centroids
def find_centroids(data1, data2, data3):
	cent1 = calc_mean(data1)
	cent2 = calc_mean(data2)
	cent3 = calc_mean(data3)
	return cent1, cent2, cent3


#***************************************************************************
#****************************THE MAIN FUNCTION******************************
#***************************************************************************

def main():
	df = get_input()
	label, datapoints = get_values(df)
	iteration = 0
	cluster1_label = []
	cluster2_label = []
	cluster3_label = []
	cluster1_datapoints = []
	cluster2_datapoints = []
	cluster3_datapoints = []
	centroid_initial = []
	centroid_final = []

	#Initial centroids
	cent1 = [2,0]
	cent2 = [0,2]
	cent3 = [3,1]
	centroid_initial = [cent1, cent2, cent3]

	print('\n')
	print("The initial centroids are:")
	print(centroid_initial)

	#final centriods
	new_cent1 = [0,0]
	new_cent2 = [0,0]
	new_cent3 = [0,0]


	if iteration == 0:
		cluster1_label, cluster2_label, cluster3_label, cluster1_datapoints, cluster2_datapoints, cluster3_datapoints = find_clusters(datapoints, label, cent1, cent2, cent3)
		new_cent1, new_cent2, new_cent3 = find_centroids(cluster1_datapoints, cluster2_datapoints, cluster3_datapoints)
		iteration += 1

	while cent1[0] != new_cent1[0] and cent1[1] != new_cent1[1] and cent2[0] != new_cent2[0] and cent2[1] != new_cent2[1] and cent3[0] != new_cent3[0] and cent3[1] != new_cent3[1]:
		cent1 = new_cent1
		cent2 = new_cent2
		cent3 = new_cent3
		cluster1_label, cluster2_label, cluster3_label, cluster1_datapoints, cluster2_datapoints, cluster3_datapoints = find_clusters(datapoints, label, new_cent1, new_cent2, new_cent3)
		new_cent1, new_cent2, new_cent3 = find_centroids(cluster1_datapoints, cluster2_datapoints, cluster3_datapoints)
		iteration += 1

	centroid_final = [new_cent1, new_cent2, new_cent3]
	print('\n')
	print("The final centroids are:")
	print(centroid_final)

	print('\n')
	print("Number of iterations required for convergence: ", iteration)

	print('\nCluster 1: ', cluster1_label)
	print('\nCluster 2: ', cluster2_label)
	print('\nCluster 3: ', cluster3_label)

	print("\n|Cluster 1| + |Cluster 2| + |Cluster 3|: ", len(cluster1_label) + len(cluster2_label) + len(cluster3_label))

	option = input("\nDo you want to see the graph of the datapoints and the regression line? Reply with the Y or N: ")
	if option == 'Y':
		plot_points(cluster1_datapoints, cluster2_datapoints, cluster3_datapoints, centroid_final)
	else:
		sys.exit(0)


#***************************************************************************
#****************************DRIVER CODE************************************
#***************************************************************************

if __name__ == '__main__':
	main()  # calling main function
