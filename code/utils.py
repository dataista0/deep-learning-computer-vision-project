import time
import subprocess
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from keras.utils import to_categorical

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

from constants import *

def run(command, print_output=True):
    out = subprocess.check_output(command, shell=True).decode('utf-8')
    if print_output:
        print(out)
    return out

def read(file_path, nrows=None):
    return pd.read_csv(file_path, nrows=nrows)

def show_sample(X):
    plt.imshow(X.sample(1).as_matrix().reshape((28, 28)), cmap='gist_gray');

def plot(model, show_shapes=False):
    display(SVG(model_to_dot(model, show_shapes=show_shapes).create(prog='dot', format='svg')))
    plt.show()

def check_submissions(show=False):
    submissions = run(f"{KAGGLE_CMD} competitions submissions digit-recognizer", print_output=False)
    lines = [line.split() for line in submissions.split("\n")[2:-1]]
    df = pd.DataFrame([(e[0], f"{e[1]} {e[2]}", float(e[-2])) for e in lines],
                   columns=['submission', 'date', 'accuracy']).set_index('submission')

    df['date'] = pd.to_datetime(df['date'])

    if show:
        df[['date', 'accuracy']].set_index('date').plot(figsize=(20, 5), rot=0,
                                                        title="Submission accuracy over time")
        plt.show()
        display(df)

    return df

def submit_to_server(submission, check=True):

    run(f"{KAGGLE_CMD} competitions submit -f {SUBMISSION_PATH}/{submission}.csv -m '{submission}.csv' digit-recognizer",
            print_output=True)

    if check:
        print("Sleeping 30 secs before checking for score...")
        time.sleep(30)
        submissions = check_submissions()
        acc = submissions.loc[f"{submission}.csv", "accuracy"]
        print(f"Model accuracy is {acc}")
        return acc

def submit(model, submission_name, submit_to_kaggle=False):

    test = pd.read_csv(TEST)
    X_test = test.values.reshape((test.shape[0], 28, 28, 1))
    pd.DataFrame({
                    'ImageId': range(1, 28001),
                    'Label': np.argmax(model.predict(X_test), axis=-1)}
                ).to_csv(f"{SUBMISSION_PATH}/{submission_name}.csv", index=False)

    if submit_to_kaggle:
        acc = submit_to_server(submission_name)
        return acc

def load_train():
	train = pd.read_csv(TRAIN)
	y_train = to_categorical(train.iloc[:, 0])
	train = train.iloc[:, 1:]
	X_train = train.values.reshape((train.shape[0], 28, 28, 1))
	return X_train, y_train