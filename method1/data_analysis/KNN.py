import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef
import excel_works as e
from config import root_name , excel_file

# Load the dataset
# Load the dataset
df = pd.read_excel(excel_file)

y = df['ground_truth']  # Target variable
X = df.drop(columns=['key', 'ground_truth'])
keys = df['key']


# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Fit the scaler to the features and transform them
X_normalized = scaler.fit_transform(X)

# convert it back to a DataFrame
X_normalized_df = pd.DataFrame(X_normalized, columns=X.columns)
# print(X_normalized_df.head())
X=X_normalized_df


# Initialize StratifiedKFold
cv_stratified = StratifiedKFold(n_splits=10, random_state=42, shuffle=True)

# Function to compute various scores for each fold
def compute_scores_per_fold(cv, X, y, model, threshold=0.5):
    scores = {
        'AUC': [],
        'MCC': [],
        'Accuracy': [],
        'Precision': [],
        'Recall': [],
        'F1': []
    }
    all_folds = []
    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        keys_train, keys_test = keys.iloc[train_index], keys.iloc[test_index]

        # Train the model
        model.fit(X_train, y_train)

        # Predict probabilities for classifiers that support probability predictions
        if hasattr(model, "predict_proba"):
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            auc_score = roc_auc_score(y_test, y_pred_proba)
            scores['AUC'].append(auc_score)

        # Predict the class labels
        y_pred = model.predict(X_test)




        # Calculate scores
        scores['MCC'].append(matthews_corrcoef(y_test, y_pred))
        scores['Accuracy'].append(accuracy_score(y_test, y_pred))
        scores['Precision'].append(precision_score(y_test, y_pred))
        scores['Recall'].append(recall_score(y_test, y_pred))
        scores['F1'].append(f1_score(y_test, y_pred))

        # calculate true positive, false positive, true negative, false negative
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(len(y_pred)):
            if y_test.iloc[i]==y_pred[i]==1:
                TP += 1
            if y_pred[i]==1 and y_test.iloc[i]!=y_pred[i]:
                FP += 1
            if y_test.iloc[i]==y_pred[i]==0:
                TN += 1
            if y_pred[i]==0 and y_test.iloc[i]!=y_pred[i]:
                FN += 1

        # write keys, y_test, y_pred to a file each fold in an excel file
        data = {
            'keys': keys_test,
            'ground_truth': y_test,
            'predictions': y_pred,
            'probabilities': [None] * (len(keys_test)),
            'MCC': [matthews_corrcoef(y_test, y_pred)] + [None] * (len(keys_test) - 1),
            'Accuracy': [accuracy_score(y_test, y_pred)] + [None] * (len(keys_test) - 1),
            'Precision': [precision_score(y_test, y_pred)] + [None] * (len(keys_test) - 1),
            'Recall': [recall_score(y_test, y_pred)] + [None] * (len(keys_test) - 1),
            'F1': [f1_score(y_test, y_pred)] + [None] * (len(keys_test) - 1),
            'TP': [TP] + [None] * (len(keys_test) - 1),
            'FP': [FP] + [None] * (len(keys_test) - 1),
            'TN': [TN] + [None] * (len(keys_test) - 1),
            'FN': [FN] + [None] * (len(keys_test) - 1)


        }
        all_folds.append(pd.DataFrame(data))

    # Calculate mean scores
    mean_scores = {metric: sum(values) / len(values) for metric, values in scores.items()}

    file_name = 'KNN_folds_' + root_name
    e.write_to_excel(file_name,all_folds)

    return mean_scores


model = KNeighborsClassifier(n_neighbors=3)
# Compute average scores using KNeighbors Classifier with k=17 and 10-fold cross-validation
mean_scores_knn =compute_scores_per_fold(cv_stratified, X, y, model)


main_file_name = 'results_' + root_name
e.update_excel(main_file_name, "KNN", mean_scores_knn)




