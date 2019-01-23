import numpy as np
import re


# This function extract the data from the log
# it return: accuracy list of the testing,loss list of the testing, loss list of the training
def extract_data(filename):

    # training Data
    train_loss_list = np.array([])  # loss list of the training

    # testing Data
    test_accuracy_list = np.array([])  # accuracy list of the testing
    test_loss_list = np.array([])      # loss list of the testing

    for line in open(filename):
        match_acc_test = re.search(r'.* Test net output #0: acc/top-1 = (\d*\.*\d*)', line)
        match_loss_test = re.search(r'.* Test net output #1: loss = (\d*\.*\d*) .*', line)
        match_loss_train = re.search(r'.* Train net output #0: loss = (\d*\.*\d*) .*', line)

        if match_acc_test:
            test_accuracy_list = np.append(test_accuracy_list, float(match_acc_test.group(1)))

        elif match_loss_test:
            test_loss_list = np.append(test_loss_list, float(match_loss_test.group(1)))

        elif match_loss_train:
            train_loss_list = np.append(train_loss_list, float(match_loss_train.group(1)))

    return test_accuracy_list, test_loss_list, train_loss_list


test_accuracy, test_loss, train_loss = extract_data("caffe.log")

print("accuracy list of the testing\n", test_accuracy)
print("loss list of the testing\n", test_loss)
print("loss list of the training\n", train_loss)

