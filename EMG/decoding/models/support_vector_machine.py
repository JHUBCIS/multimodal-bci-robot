from sklearn import svm
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate some random data for classification
X, y = make_classification(n_samples=2000, n_features=6, n_informative=6, n_redundant=0, random_state=42)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create an SVM classifier
clf = svm.SVC(kernel='linear')

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Make a function for prediction
def predict(input_vector):
    y_new = clf.predict(input_vector)
    return y_new

import os


# <--- For Debugging if Zach Rebases --->
#import os
#current_working_directory = os.getcwd()
#print(f"Current Working Directory: {current_working_directory}")

import joblib

joblib.dump(clf, 'saved_models/svm_model.pkl')
