import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import pandas as pd
import os

def model_Evaluate(y_pred, y_test, model, suffix=None, savepath_graph=None, save_csv=False):
    """
    Plot confusion matrix
    """
    model = model.lower()
    # Print the evaluation metrics for the dataset and make CSV file.
    target_names = ['negative label', 'positive label']
    report = classification_report(y_test, y_pred, output_dict=True, target_names=target_names)
    df = pd.DataFrame.from_dict(report).T
    df = df.drop(['support'], axis=1)
    df = df.rename(columns={'f1-score':'f1_score'})
    df.index.name = 'labels_name'
    print(df)
    if save_csv==True and suffix != None:
        if not os.path.exists(f'test/{model}'):
            os.mkdir(f'test/{model}')
        number_of_tests = len([f for f in os.listdir(f'test/{model}') if suffix in f])
        savepath_csv = f'test/{model}/{suffix}_{number_of_tests}.csv'
        df.to_csv(savepath_csv)
    # Compute and plot the Confusion matrix
    cf_matrix = confusion_matrix(y_test, y_pred)
    categories = ['Negative','Positive']
    group_names = ['True Neg','False Pos', 'False Neg','True Pos']
    group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]
    labels = [f'{v1}n{v2}' for v1, v2 in zip(group_names,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(cf_matrix, annot = labels, cmap = 'Blues',fmt = '',
    xticklabels = categories, yticklabels = categories)
    plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
    plt.ylabel("Actual values" , fontdict = {'size':14}, labelpad = 10)
    plt.title ("Confusion Matrix", fontdict = {'size':18}, pad = 20)
    if savepath_graph is None:
        plt.show()
    else:
        plt.savefig(savepath_graph)

def graphic(y_test, y_pred, savepath=None):
    """
    Plot ROC AUC graph
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC CURVE')
    plt.legend(loc="lower right")
    if savepath is None:
        plt.show()
    else:
        plt.savefig(savepath)