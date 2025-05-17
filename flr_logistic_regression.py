## This python file contains the logistic regression model used in the jupyter notebook. 

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import pandas as pd

def logistic_regression_analysis(X, y):
    # Split into training and test sets for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Fit logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Evaluate model
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    auc_score = roc_auc_score(y_test, y_prob)

    model_coefficients = pd.Series(model.coef_[0])
    
    logreg_dict = {'model':model, 'x_train': X_train, 'x_test': X_test, 
                   'y_train': y_train, 'y_test':y_test, 'y_pred':y_pred, 'y_prob':y_prob,
                   'conf_matrix': conf_matrix, 'class_report': class_report, 
                   'auc_score': auc_score, 'model_coefficients': model_coefficients}

    return logreg_dict
    