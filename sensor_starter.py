# -*- coding: utf-8 -*-
"""Sensor Starter

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qQULv0K7VoQkxT3m4h3Ly-UKSqeexCPW
"""

#@title Configuration parameters
#@markdown Forms support many types of fields.

dataset_url = 'http://extrasensory.ucsd.edu/data/primary_data_files/ExtraSensory.per_uuid_features_labels.zip'  #@param {type: "string"}

"""# starter code

Using sensors to predict activity. This part of the assignment uses the [ExtraSensory dataset](http://extrasensory.ucsd.edu/). You can download the dataset from [here](http://extrasensory.ucsd.edu/data/primary_data_files/ExtraSensory.per_uuid_features_labels.zip). The starter code expects that this dataset has been unpacked in a folder called `data` that is in the same parent folder as this notebook. You can read more about the dataset in [this README file](http://extrasensory.ucsd.edu/data/primary_data_files/README.txt).
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sklearn.metrics as metrics
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

"""## Location of the .csv.gz files"""

data_dir = Path('data')

!mkdir -p $data_dir
!curl $dataset_url > $data_dir/dataset.zip
!unzip -o $data_dir/dataset.zip -d $data_dir/
!rm $data_dir/dataset.zip

"""## Some utility functions

The first one loads a pandas dataframe given a user UUID. The second one extracts specified feature columns $X$ and target column $y$ from a dataframe and converts these to numpy.
"""

def load_data_for_user(uuid):
    return pd.read_csv(data_dir / (uuid + '.features_labels.csv.gz'))

def get_features_and_target(df, feature_names, target_name):
    
    # select out features and target columns and convert to numpy
    X = df[feature_names].to_numpy()
    y = df[target_name].to_numpy()
    
    # remove examples with no label
    has_label = ~np.isnan(y)
    X = X[has_label,:]
    y = y[has_label]
    return X, y

def get_dataset_for_user(uuid):
  
  df = load_data_for_user(uuid)
  X, y = get_features_and_target(df, acc_sensors, target_column)

  return X, y

def print_classifier_accuracy(clf, X_test, y_test, label=''):
  score = clf.score(X_test, y_test)
  print(f'Score for classifier {label}: {score:0.4f}')
  
  y_pred = clf.predict(X_test)
  accuracy = metrics.balanced_accuracy_score(y_test, y_pred)
  print(f'Balanced accuracy for classifier {label}: {accuracy:0.4f}')

  precision = metrics.precision_score(y_test, y_pred)
  print(f'Precision score for classifier {label}: {precision:0.4f}')
  
  recall = metrics.recall_score(y_test, y_pred)
  print(f'Recall score for classifier {label}: {recall:0.4f}')

  f1 = metrics.f1_score(y_test, y_pred)
  print(f'F1-score for classifier {label}: {f1:0.4f}')

  roc_auc = metrics.roc_auc_score(y_test, y_pred)
  print(f'ROC-AUC score for classifier {label}: {f1:0.4f}')

"""## Load in some data 
Load in the data for a user and display the first few rows of the dataframe
"""

initial_uuid = '1155FF54-63D3-4AB2-9863-8385D0BD0A13'
df = load_data_for_user(initial_uuid)
df.head()

"""## What columns are available?"""

df.columns.to_list()

"""## Feature selection

The columns that start with `label:` correspond to potential y values. Let's look at using the accelerometer features. These start with `raw_acc:` and `watch_acceleration:`
"""

acc_sensors = [s for s in df.columns if 
               s.startswith('raw_acc:') or 
               s.startswith('watch_acceleration:')]

target_column = 'label:FIX_walking'

"""## Extract our training data"""

X_train, y_train = get_features_and_target(df, acc_sensors, target_column)
print(f'{y_train.shape[0]} examples with {y_train.sum()} positives')

"""## Preprocessing

We want to make the learning problem easier by making all columns have a mean of zero and a standard deviation of one. There are also lots of missing values in this dataset. We'll use mean imputation here to get rid of them. Since our data is scaled to have zero mean, this will just zero out missing values.
"""

scaler = StandardScaler()
imputer = SimpleImputer(strategy='mean')

X_train = scaler.fit_transform(X_train)
X_train = imputer.fit_transform(X_train)

"""## Fitting a model
Let's fit a logistic regression model to this user. We can then test it's predictive power on a different user
"""

clf = LogisticRegression(solver='liblinear', max_iter=1000, C=1.0)
clf.fit(X_train, y_train)

"""## Training accuracy

Let's see the accuracy on the training set. The score function can be used to do this:
"""

print(f'Training accuracy: {clf.score(X_train, y_train):0.4f}')

"""Looks like the model can fit the training data reasonably well anyway. But this says nothing about how well it will generalize to new data. The dataset is also unbalanced, so this figure may be misleading. How accurate would we be if we just predicted zero each time?"""

1 - y_train.sum() / y_train.shape[0]

"""Oh wow. Our model may not be that great after all. Let's try to calculate balanced accuracy, which should better reflect how well the model does on the training data"""

y_pred = clf.predict(X_train)
print(f'Balanced accuracy (train): {metrics.balanced_accuracy_score(y_train, y_pred):0.4f}')

"""## Testing the model

Ok, it seems our model has fit the training data well. How well does it perform on unseen test data? Let's load the data in for a different user.
"""

X_test, y_test = get_dataset_for_user('11B5EC4D-4133-4289-B475-4E737182A406')

"""We also need to preprocess as before. **Note**: we are using the scaler and imputer fit to the training data here. It's very important that you do not call `fit` or `fit_transform` here! Think about why."""

X_test = imputer.transform(scaler.transform(X_test))

"""## Test accuracy"""

print(f'Test accuracy: {clf.score(X_test, y_test):0.4f}')

y_pred = clf.predict(X_test)
print(f'Balanced accuracy (train): {metrics.balanced_accuracy_score(y_test, y_pred):0.4f}')

"""## Improving the test set

Let's take 5 random users
"""

uuids = [
    '00EABED2-271D-49D8-B599-1D4A09240601', '098A72A5-E3E5-4F54-A152-BBDA0DF7B694', '0A986513-7828-4D53-AA1F-E02D6DF9561B',
    '0BFC35E2-4817-4865-BFA7-764742302A2D', '0E6184E1-90C0-48EE-B25A-F1ECB7B9714E'
]

test_scores = []
balanced_accuracies = []
for uuid in uuids:
  X_test, y_test = get_dataset_for_user(uuid)

  X_test = imputer.transform(scaler.transform(X_test))
  score = clf.score(X_test, y_test)
  test_scores.append(score)
  print(f'Test accuracy for {uuid}: {score:0.4f}')
  y_pred = clf.predict(X_test)
  accuracy = metrics.balanced_accuracy_score(y_test, y_pred)
  balanced_accuracies.append(accuracy)
  print(f'Balanced accuracy for {uuid} (train): {accuracy:0.4f}')

print()
print(f'Mean of the test accuracies for the five users: {np.mean(test_scores)}')
print(f'Variance of the test accuracies for the five users: {np.var(test_scores)}')
print()
print(f'Mean of the test balanced accuracies for the five users: {np.mean(balanced_accuracies)}')
print(f'Variance of the test balanced accuracies for the five users: {np.var(balanced_accuracies)}')

"""Let's create a test dataset containing all 5 users"""

def get_testing_dataset():
  X_test_five_users, y_test_five_users = get_dataset_for_user(uuids[0])

  for uuid in uuids[1:]:
      X_test, y_test = get_dataset_for_user(uuid)

      X_test_five_users = np.concatenate((X_test, X_test_five_users), axis=0)
      y_test_five_users = np.concatenate((y_test, y_test_five_users), axis=0)

  X_test_five_users = imputer.transform(scaler.transform(X_test_five_users))

  return X_test_five_users, y_test_five_users

X_test_five_usrs, y_test_five_users = get_testing_dataset()

"""Let's test the accuracy of the model with this data"""

score = clf.score(X_test_five_users, y_test_five_users)
print(f'Test accuracy for all five users: {score:0.4f}')
y_pred_five_users = clf.predict(X_test_five_users)
accuracy = metrics.balanced_accuracy_score(y_test_five_users, y_pred_five_users)
print(f'Balanced accuracy for all five users (train): {accuracy:0.4f}')

"""## Validation data

We can reuse the dataset of the five users as a validation dataset
"""

X_validation = X_test_five_users
y_validation = y_test_five_users

"""## Increased training data

Let's check how the accuracy of the classifier changes when using another user to train the classifier
"""

new_uuid = '9759096F-1119-4E19-A0AD-6F16989C7E1C'
X_new, y_new = get_dataset_for_user(new_uuid)

clf_new = LogisticRegression(solver='liblinear', max_iter=1000, C=1.0)

X_new = imputer.transform(scaler.transform(X_new))
clf_new.fit(X_new, y_new)

"""Calculate score on the new classifier using test data"""

score = clf_new.score(X_test_five_users, y_test_five_users)
print(f'Test accuracy for all five users: {score:0.4f}')
y_pred_five_users = clf_new.predict(X_test_five_users)
accuracy = metrics.balanced_accuracy_score(y_test_five_users, y_pred_five_users)
print(f'Balanced accuracy for all five users (train): {accuracy:0.4f}')

"""With this user we get slightly better results. Let's combine the training dataset to have multiple users"""

def get_training_dataset():
  uuids_train = ['9759096F-1119-4E19-A0AD-6F16989C7E1C', '1155FF54-63D3-4AB2-9863-8385D0BD0A13', 'CDA3BBF7-6631-45E8-85BA-EEB416B32A3C',
                'C48CE857-A0DD-4DDB-BEA5-3A25449B2153', 'FDAA70A1-42A3-4E3F-9AE3-3FDA412E03BF']

  X_train, y_train = get_dataset_for_user(uuids_train[0])

  for uuid in uuids_train[1:]:
      X_uuid, y_uuid = get_dataset_for_user(uuid)

      X_train = np.concatenate((X_uuid, X_train), axis=0)
      y_train = np.concatenate((y_uuid, y_train), axis=0)



  X_train = imputer.transform(scaler.transform(X_train))
  return X_train, y_train

X_train, y_train = get_training_dataset()

clf_new = LogisticRegression(solver='liblinear', max_iter=1000, C=1.0)

clf_new.fit(X_train, y_train)

"""We can note that the new classifier has better accuracy than the old one."""

print_classifier_accuracy(clf, X_test_five_users, y_test_five_users, label='single-user')
print_classifier_accuracy(clf_new, X_test_five_users, y_test_five_users, label='multiple-users')

"""## Model Selection

To start, let's define a set of C's to train our model
"""

def get_clf(C):
    return LogisticRegression(solver='liblinear', max_iter=10000, C=C)

Cs = np.linspace(0.00001, 10, 20)

scores = []
balanced_accuracies = []

for C in Cs:
  clf = get_clf(C)
  clf.fit(X_train, y_train)

  score = clf.score(X_train, y_train)
  scores.append(score)
  y_pred = clf.predict(X_train)
  accuracy = metrics.balanced_accuracy_score(y_train, y_pred)
  balanced_accuracies.append(accuracy)

plt.plot(Cs, scores)

plt.xlabel('Values for C')
plt.ylabel('Train scores')
plt.title('Trainscores vs C')

plt.plot(Cs, balanced_accuracies)

plt.xlabel('Values for C')
plt.ylabel('Balanced accuracies')
plt.title('Balanced accuracies vs C')

"""As we can note on the test score, there is a value for C such that incresing it will have no effect on the result (a.k.a performance doesn't change). On the other hand, best value for balanced accuracy is by using the smallest C possible."""

best_score_idx = np.argmax(scores)
best_accuracy_score_idx = np.argmax(balanced_accuracies)

print(f'Best C for score metric: {Cs[best_score_idx]}')
print(f'Best C for balanced accuracy metric: {Cs[best_accuracy_score_idx]}')
print(f'Best score metric: {scores[best_score_idx]}')
print(f'Best balanced accuracy metric: {balanced_accuracies[best_accuracy_score_idx]}')

"""Let's try with the MLP classifier"""

from sklearn.neural_network import MLPClassifier

mlp_clf = MLPClassifier(hidden_layer_sizes=(5, 2), random_state=1, max_iter=2000)

mlp_clf.fit(X_train, y_train)

print_classifier_accuracy(mlp_clf, X_train, y_train)

"""Let's also try with something arguably less complex such as SVC"""

from sklearn.svm import SVC

svc = SVC()

svc.fit(X_train, y_train)

print_classifier_accuracy(svc, X_train, y_train)

"""Amongst these three, the one with best performance is MLP

## Model Testing

Let's see how our MLP model behave on the test dataset
"""

print_classifier_accuracy(mlp_clf, X_validation, y_validation)

"""Let's plot an ROC curve"""

y_pred_proba = mlp_clf.predict_proba(X_validation)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_validation,  y_pred_proba)
auc = metrics.roc_auc_score(y_validation, y_pred_proba)

#create ROC curve
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()

"""We can see that the curve is more leaned towards the top-left corner of the plot. That is a good indicator that the classifier is doing a good job. Also, the AUC is 0.7774, a value that confirms it.

## Predicting other actions

By changing `target_column` we can easily get the new model for the new target column
"""

new_targets = ['label:SITTING', 'label:BICYCLING']

for t in new_targets:
  print(f'Training for column: {t}')
  target_column = t
  X_train, y_train = get_training_dataset()

  mlp = MLPClassifier(hidden_layer_sizes=(5, 2), random_state=1, max_iter=2000)
  mlp.fit(X_train, y_train)

  X_test, y_test = get_testing_dataset()

  print_classifier_accuracy(mlp, X_test, y_test, label='MLP')
  print()