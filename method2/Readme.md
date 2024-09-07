# Guide

Most files are cached in the repo

## Getting Data from GitHub

* Run `GitHub-Issues.ipynb` to get pickle files to train embeddings. Select the corresponding cells for RQ2 or RQ3.

* Run `GitHub-Ground.ipynb` and `GHInsightsData.ipynb` to get GitHub Insight Key developer data.

## Training Embeddings

* Using the saved issue pickle files run `Dev2Vec-Train.ipynb` to train and save embeddings.

* If needed run the bottom part of `Dev2Vec-Train.ipynb` to get csv files for RQ3.

## Train MLP and get RQ2 results

* Run `MLP-Results.ipynb` to read the embeddings using the corresponding cells  align them (AlignOP or AlignNAA) and train the MLP model. Select the corresponding cells to enable/disable Cond2.
