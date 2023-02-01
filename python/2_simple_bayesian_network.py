import numpy as np
import pandas as pd

from causalnex.structure import StructureModel
from causalnex.network import BayesianNetwork
from causalnex.discretiser import Discretiser

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# Path to training table.
TRAINPATH = '../data/training_tables/mapbiomas_lcc_v1.csv'

def main():
    df_mapbiomas = pd.read_csv(TRAINPATH)

    column_names = list(df_mapbiomas.columns)

    # Define a bayesian network in which
    # nonvegatated -> forestloss <- farming
    sm = StructureModel()
    sm.add_edges_from([
        ('nonvegatated', 'forestloss'),
        ('farming', 'forestloss')
    ])
    bn = BayesianNetwork(sm)

    # Classical bayesian networks only accept categorical variables
    # so lets discretize the two explanatory variables into 6 levels using percentiles.
    arr = df_mapbiomas['nonvegatated'].values.flatten()
    percentile_bins = np.percentile(arr, np.array([5, 25, 50, 75, 95])).tolist()
    df_mapbiomas['nonvegatated'] = Discretiser(method="fixed", numeric_split_points=percentile_bins).transform(arr)

    arr = df_mapbiomas['farming'].values.flatten()
    percentile_bins = np.percentile(arr, np.array([5, 25, 50, 75, 95])).tolist()
    df_mapbiomas['farming'] = Discretiser(method="fixed", numeric_split_points=percentile_bins).transform(arr)

    # And also % forestloss into 2 levels, 0 and greater than 0.
    df_mapbiomas['forestloss'] = (df_mapbiomas['forestloss'].values > 0)*1

    # Create training and testing split.
    train, test = train_test_split(df_mapbiomas, train_size=0.90, test_size=0.10, random_state=665)

    # Avoid cases where states in our test set do not exist in the training set.
    bn = bn.fit_node_states(df_mapbiomas)

    # Train bayesian network on training split.
    bn = bn.fit_cpds(train, method="BayesianEstimator", bayes_prior="K2")

    # Predict on test set.
    predictions = bn.predict(test, 'forestloss')

    confusion = confusion_matrix(test['forestloss'], predictions)

    print(confusion)

if __name__ == "__main__":
    main()