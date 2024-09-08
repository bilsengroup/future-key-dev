# Predicting the Next Generation of Key Developers: A Dual-Methodology Approach

This repository contains the replication package for the paper titled **"Predicting the Next Generation of Key Developers: A Dual-Methodology Approach"**, authored by **Fereshteh Vedadi, Ali Emir Güzey, Giray Akyol, and Eray Tüzün**.

## Overview

This research introduces a dual-methodology approach for predicting future key developers in software projects. By analyzing historical data of developers' early contributions and using predictive models such as k-Nearest Neighbors (kNN), Logistic Regression (LR), Naïve Bayes (NB), and Random Forest (RF), as well as a neural embedding algorithm with diachronic alignment techniques, we aim to forecast which developers will become key contributors. Our study demonstrates that combining both methodologies yields better prediction accuracy than using them individually, with Random Forest and AlignOP alignment technique being particularly effective.

## Research Questions

The study addresses the following research questions:

- **RQ1**: What is the most effective predictive model to predict future key developers among well-known predictive models (kNN, LR, RF, NB)?
- **RQ2**: Which diachronic alignment technique is more applicable to future key developer prediction using neural embeddings?
- **RQ3**: Does combining the best performers of the first and second methodologies improve the prediction of future key developers in a software project?

## Project Structure

The project contains three main folders:

1. **method1/**: This folder contains the implementation of the first methodology, which answers **RQ1** and **RQ3**. It contains the code used to generate the dataset and the models used for predicting future key developers using various machine learning algorithms (kNN, LR, NB, RF).
   
2. **method2/**: This folder contains the implementation of the second methodology, which answers **RQ2** and provides additional features for enhancing predictions in **RQ3** using aligned embeddings.

3. **additional_feature/**: This folder computes the code survival feature used in **method1** to measure the quality and longevity of code contributions.

Each folder contains a detailed README with further instructions specific to that section.

## Instructions for Replication

1. Clone this repository to your local environment:
   
   ```bash
   git clone https://github.com/bilsengroup/future-key-dev/tree/future_key_dev
   
2. Navigate to the specific methodology folder (either `method1/` or `method2/`) and follow the instructions in the corresponding README file to run the experiments.

3. To compute the additional feature for method1 (code survival), run the script in the `additional_feature/` folder.
