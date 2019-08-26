# Functions for dimensionality reduction (PCA, t-SNE)


def pca_scores(df, n_components = 2, random_state = None):
	"""
	Centers and scales the features of a DataFrame and returns the 
	scores matrix from a principal components analysis (PCA).

	Parameters
	----------
	df: DataFrame
	n_components: int, default: 2
		The number of principal components to keep
	random_state: int, default: None

	Returns
	-------
	array
		The scores matrix with shape (df.shape[0], n_components)
	"""

	from sklearn.preprocessing import StandardScaler
	from sklearn.decomposition import PCA

	scale = StandardScaler()
	df_scale = scale.fit_transform(df)
	pca = PCA(n_components = n_components, random_state = random_state)
	return pca.fit_transform(df_scale)


def pca_perc_var_explained(df, n_components = 2, random_state = None):
	"""
	Centers and scales the features of a DataFrame and returns the percentage 
	of variance explained by a principal components analysis (PCA).

	Parameters
	----------
	df: DataFrame
	n_components: int, default: 2
		The number of principal components to keep
	random_state: int, default: None

	Returns
	-------
	one-dimensional array with shape (n_components,)
		The percentage of total variance explained by each principal component  
	"""

	from sklearn.preprocessing import StandardScaler
	from sklearn.decomposition import PCA

	scale = StandardScaler()
	df_scale = scale.fit_transform(df)
	pca = PCA(n_components = n_components, random_state = random_state)
	pca.fit_transform(df_scale)
	return pca.explained_variance_ratio_


def plot_PCA_2D(df, groups, group_labels, file = None, 
				n_components = 2, random_state = None):
	"""
	Takes a DataFrame, centers and scales it, conducts a principal components
	analysis (PCA), and plots the scores of the first two components colored
	by input group labels. Axis labels display the percentage of variance 
	explained by each component.

	Parameters
	----------
	df: DataFrame
	groups: Series
		The groups to color the scores by
		length must equal df.shape[0]
	group_labels: one-dimensional array
		The unique labels for the groups
	file: string, default: None
		Filename to save plot output with
	n_components: int, default: 2
		The number of principal components to keep
	random_state: int, default: None

	Returns
	-------
	scatterplot
		scores plot of PC2 vs. PC1 colored by group_labels  
	"""

	import matplotlib.pyplot as plt
	from itertools import cycle

	scores = pca_scores(df, n_components = n_components, 
    					random_state = random_state)
	perc_var_explained = pca_perc_var_explained(df, n_components = n_components, 
                                                random_state = random_state)
    
	colors = cycle(['r', 'g', 'b', 'c', 'm', 'y', 'orange', 'w', 'aqua', 
    				'yellow', 'black', 'brown'])
	plt.figure(figsize = (12, 10))
	for c, label in zip(colors, group_labels):
	    plt.scatter(scores[groups == label, 0], scores[groups == label, 1],
	                c = c, label = label, edgecolors = 'gray')
	plt.xlabel('PC1 ({}% Variance)'.format((100 * perc_var_explained[0])\
				.round(2)), fontsize = 15)
	plt.ylabel('PC2 ({}% Variance)'.format((100 * perc_var_explained[1])\
				.round(2)), fontsize = 15)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.legend()

	if file:
	    plt.savefig(file, dpi = 100, bbox_inches = 'tight')
	plt.show()
	plt.close()


def plot_tsne(df, groups, group_labels, file = None, n_components = 2, 
			  random_state = None):
	"""
	Plots the first two components from a t-Distributed Stochastic Neighbor
	Embedding (t-SNE) reduction of a DataFrame, colored by input group labels.
	t-SNE is useful for visualizing the clustering behavior of observations, 
	particularly when there are many features. 

	Parameters
	----------
	df: DataFrame
	groups: Series
		The groups to color the scores by
		length must equal df.shape[0]
	group_labels: one-dimensional array
		The unique labels for the groups
	file: string, default: None
		Filename to save plot output with
	n_components: int, default: 2
		The number of t-SNE components to keep
	random_state: int, default: None

	Returns
	-------
	scatterplot
		scores plot of t-SNE component 2 vs. t-SNE component 1 colored 
		by group_labels  
	"""

	import matplotlib.pyplot as plt
	from sklearn.manifold import TSNE
	from itertools import cycle
	
	tsne = TSNE(n_components = n_components, random_state = random_state)
	df_tsne = tsne.fit_transform(df)
	
	colors = cycle(['r', 'g', 'b', 'c', 'm', 'y', 'orange', 'gray', 'aqua', 
					'yellow', 'black', 'brown'])
	plt.figure(figsize = (12, 10))
	for c, label in zip(colors, group_labels):
	    plt.scatter(df_tsne[groups == label, 0], df_tsne[groups == label, 1], 
	                c = c, label = label, s = 30, edgecolor = 'black', 
	                linewidths = 0.1)
	plt.legend(fontsize = 10, loc = 'upper left', frameon = True, 
	           facecolor = '#FFFFFF', edgecolor = '#333333')
	plt.xlim(-100, 100)
	plt.title("AI Tweet Clusters with t-SNE", fontsize = 18)
	plt.ylabel("t-SNE Axis 2", fontsize = 15)
	plt.xlabel("t-SNE Axis 1", fontsize = 15);
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	
	if file:
	    plt.savefig(file, dpi = 100, bbox_inches = 'tight')
	plt.show()
	plt.close()

