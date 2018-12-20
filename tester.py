from sklearn.model_selection import StratifiedShuffleSplit
from feature_format import featureFormat, targetFeatureSplit
from IPython.display import display
import numpy as np
import pandas as pd 

PERF_FORMAT_STRING = "\
Accuracy: {:>0.{display_precision}f}\tPrecision: {:>0.{display_precision}f}\
\tRecall: {:>0.{display_precision}f}\tF1: {:>0.{display_precision}f}\tF2: {:>0.{display_precision}f}"
RESULTS_FORMAT_STRING = "Total predictions: {:4d}\tTrue positives: {:4d}\tFalse positives: {:4d}\
\nFalse negatives: {:4d}\tTrue negatives: {:4d}"

def test_classifier(clf, dataset, feature_list, folds = 1000, to_print=True):
    '''
    A function that performs cross validation and computes a number of
    different metrics for a given classifier using a test set.
    '''
    data = featureFormat(dataset, feature_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    cv = StratifiedShuffleSplit(folds, random_state = 42)
    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0
    for train_idx, test_idx in cv.split(features, labels): 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
        
        # fit the classifier using training set, and test on test set
        clf.fit(np.array(features_train), np.array(labels_train))
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
            else:
                print("Warning: Found a predicted label not == 0 or 1.")
                print("All predictions should take value 0 or 1.")
                print("Evaluating performance for processed predictions:")
                break
    try:
        total_predictions = true_negatives + false_negatives + false_positives + true_positives
        accuracy = 1.0*(true_positives + true_negatives)/total_predictions
        precision = 1.0*true_positives/(true_positives+false_positives)
        recall = 1.0*true_positives/(true_positives+false_negatives)
        f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
        f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
        #results = dict(accuracy=accuracy, precision=precision, recall=recall, f1=f1, f2=f2,
        #               total_predictions=total_predictions, true_positives=true_positives,
        #               false_positives=false_positives, false_negatives=false_negatives,
        #               true_negatives=true_negatives)
        #results_df = pd.DataFrame.from_dict(results)
        #print(results_df)
        if to_print:
            print(PERF_FORMAT_STRING.format(accuracy, precision, recall, f1, f2, display_precision = 5))
            print(RESULTS_FORMAT_STRING.format(total_predictions, true_positives, false_positives, false_negatives, true_negatives))
            print()
        else:
            return (precision, recall, f1, accuracy)
    except:
        print("Got a divide by zero when trying out:", clf)
        print("Precision or recall may be undefined due to a lack of true positive predicitons.")

def main():
    test_classifier(clf, dataset, feature_list)

if __name__ == '__main__':
    main()
