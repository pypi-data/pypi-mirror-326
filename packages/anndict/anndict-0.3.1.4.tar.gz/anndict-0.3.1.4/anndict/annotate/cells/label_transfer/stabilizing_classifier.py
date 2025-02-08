"""
This module handles label transfer via sklearn models.
"""
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import check_random_state
from anndata import AnnData

from anndict.adata_dict import AdataDict
from anndict.utils.pca_density_filter import pca_density_subsets
from anndict.utils.anndata_ import add_col_to_adata_obs

def stable_label(
    X: np.ndarray,
    y: np.ndarray,
    classifier: object,
    *,
    max_iterations: int = 100,
    stability_threshold: float = 0.05,
    moving_average_length: int = 3,
    random_state: int | None = None
) -> tuple[object, list[float], int, np.ndarray]:

    """
    Trains a classifier using a semi-supervised approach where labels are probabilistically reassigned based on classifier predictions.

    Parameters
    -----------
    X
        feature matrix.

    y
        initial labels for all data.

    classifier
        a classifier instance that implements fit and predict_proba methods.

    max_iterations
        maximum number of iterations for updating labels.

    stability_threshold 
        threshold for the fraction of labels changing to consider the labeling stable.

    moving_average_length
        number of past iterations to consider for moving average.

    random_state
        seed for random number generator for reproducibility.

    Returns
    --------
    classifier
        trained classifier.

    history
        percentage of labels that changed at each iteration.

    iterations
        number of iterations run.

    final_labels
        the labels after the last iteration.

    @todo
    - switch pca_density_subsets to use pca_density_filter_main or pca_density_filter_adata
    """
    rng = check_random_state(random_state)
    history = []
    current_labels = y.copy()

    for iteration in range(max_iterations):

        #Call the wrapper function to get the index vector
        dense_on_pca = pca_density_subsets(X, current_labels)

        #Get which labels are non_empty
        has_label = current_labels != -1

        #Train the classifier on cells that are dense in pca space and have labels
        mask = dense_on_pca & has_label
        classifier.fit(X[mask], current_labels[mask])

        # Predict label probabilities
        probabilities = classifier.predict_proba(X)

        #view some predicted probabilities for rows of X
        # print("Sample predicted probabilities for rows of X:", probabilities[:5])

        # Sample new labels from the predicted probabilities
        new_labels = np.array([np.argmax(prob) if max(prob) > 0.8 else current_labels[i] for i, prob in enumerate(probabilities)])
        # new_labels = np.array([np.argmax(prob) for i, prob in enumerate(probabilities)])

        # def transform_row(row, p):
        #     """
        #     Transform an array by raising each element to the power of p and then normalizing these values
        #     so that their sum is 1.

        #     Parameters:
        #     row (np.array): The input array to be transformed.
        #     p (float): The power to which each element of the array is raised.

        #     Returns:
        #     np.array: An array where each element is raised to the power of p and
        #             normalized so that the sum of all elements is 1.
        #     """
        #     row = np.array(row)  # Ensure input is a numpy array
        #     powered_row = np.power(row, p)  # Raise each element to the power p
        #     normalized_row = powered_row / np.sum(powered_row)  # Normalize the powered values
        #     return normalized_row

        # new_labels = np.array([np.random.choice(len(row), p=transform_row(row, 4)) for row in probabilities])

        #randomly flip row label with probability given by confidence in assignment--hopefully prevents "cell type takeover"
        # def random_bool(p):
        #     weights = [p, 1-p]
        #     weights = [w**2 for w in weights]
        #     weights = [w/sum(weights) for w in weights]
        #     return random.choices([False, True], weights=weights, k=1)[0]

        # new_labels = np.array([np.random.choice(len(row)) if random_bool(max(row)) else current_labels[i] for i, row in enumerate(probabilities)])

        # Determine the percentage of labels that changed
        changes = np.mean(new_labels != current_labels)

        # Record the percentage of labels that changed
        history.append(changes)

        # Compute moving average of label changes over the last n iterations
        if len(history) >= moving_average_length:
            moving_average = np.mean(history[-moving_average_length:])
            if moving_average < stability_threshold:
                break

        #update current labels
        current_labels = new_labels

        if len(np.unique(current_labels)) == 1:
            print("converged to single label.")
            break

    return classifier, history, iteration + 1, current_labels

def stable_label_adata(
    adata: AnnData,
    feature_key: str,
    label_key: str,
    classifier: object,
    **kwargs
) -> tuple[object, list[float], int, np.ndarray, object]:
    """
    A wrapper for :func:`stable_label` that handles categorical labels.

    Parameters
    -----------
    adata
        AnnData object containing the dataset.

    feature_key
        str, key to access the features in adata.obsm.

    label_key
        str, key to access the labels in adata.obs.

    classifier
        classifier instance that implements fit and predict_proba methods.

    **kwargs
        keyword args passed directly to :func:`stable_label`.

    Returns
    -----------
    A tuple containing:
    - classifier: trained classifier.
    - history: percentage of labels that changed at each iteration.
    - iterations: number of iterations run.
    - final_labels: text-based final labels after the last iteration.
    - label_encoder: the label encoder used during training (can be used to convert predictions to semantic labels)
    """
    # Initialize Label Encoder
    label_encoder = LabelEncoder()

    # Extract features and labels from adata
    X = adata.obsm[feature_key]
    y = adata.obs[label_key].values

    # Define a list of values to treat as missing
    missing_values = set(['missing', 'unannotated', '', 'NA'])

    # Replace defined missing values with np.nan
    y = np.array([np.nan if item in missing_values or pd.isna(item) else item for item in y])

    # Encode categorical labels to integers
    encoded_labels = label_encoder.fit_transform(y)

    # Map np.nan's encoding index to -1
    if np.nan in label_encoder.classes_:
        nan_label_index = label_encoder.transform([np.nan])[0]
        encoded_labels[encoded_labels == nan_label_index] = -1

    # Train the classifier using the modified training function that handles probabilistic labels
    trained_classifier, history, iterations, final_numeric_labels = stable_label(X, encoded_labels, classifier, **kwargs)

    # Decode the numeric labels back to original text labels
    final_labels = label_encoder.inverse_transform(final_numeric_labels)

    return trained_classifier, history, iterations, final_labels, label_encoder


def stable_label_adata_dict(
    adata_dict: AdataDict,
    feature_key: str,
    label_key: str,
    classifier_class: object,
    **kwargs
) -> dict[tuple[str,...], dict]:
    """
    Trains a classifier for each AnnData object in adata_dict.

    Parameters
    -----------
    adata_dict
        Dictionary with keys as identifiers and values as AnnData objects.

    feature_key
        Key to access the features in ``adata.obsm``.

    label_key
        Key to access the labels in ``adata.obs``.

    classifier_class
        Classifier instance that implements fit and predict_proba methods.


    **kwargs
        Additional keyword arguments to pass to the classifier constructor and :func:`stable_label_adata`.

    Returns
    --------
    A :class:`dict` where keys keys of ``adata_dict`` and values are ``dictionaries`` containing the outputs from :func:`stable_label_adata`.
    """
    stable_label_results = {}

    max_iterations = kwargs.pop('max_iterations', 100)
    stability_threshold = kwargs.pop('stability_threshold', 0.05)
    moving_average_length = kwargs.pop('moving_average_length', 3)
    random_state = kwargs.pop('random_state', None)


    for stratum, adata in adata_dict.items():
        print(f"Training classifier for {stratum}")

        #create a classifier for this stratum
        classifier = classifier_class(random_state=random_state, **kwargs)


        indices = np.array(adata.obs.index)
        trained_classifier, history, iterations, final_labels, label_encoder = stable_label_adata(
            adata, feature_key, label_key, classifier, max_iterations=max_iterations, stability_threshold=stability_threshold, moving_average_length=moving_average_length, random_state=random_state
        )

        stable_label_results[stratum] = {
            'classifier': trained_classifier,
            'history': history,
            'iterations': iterations,
            'final_labels': final_labels,
            'label_encoder': label_encoder,
            'indices': indices
        }

    return stable_label_results


def update_adata_labels_with_results(
    adata: AnnData,
    results: dict,
    new_label_key: str = 'stable_cell_type'
) -> None:
    """
    Collects indices and labels from results and adds them to the AnnData object using add_col_to_adata_obs function.

    Parameters
    -----------
    adata
        AnnData object to be updated.

    results
        Dictionary containing results, including indices and final_labels.

    new_label_key
        Name of the new column in adata.obs where the labels will be stored.
    
    Returns
    --------
    None

    Notes
    ---------
    This function modifies the input ``adata`` in-place
    """
    # Collect all indices and labels from the results
    all_indices = np.concatenate([info['indices'] for stratum, info in results.items()])
    all_labels = np.concatenate([info['final_labels'] for stratum, info in results.items()])

    # Call the function to add labels to adata
    add_col_to_adata_obs(adata, all_indices, all_labels, new_label_key)



def predict_labels_adata_dict(
    adata_dict: AdataDict,
    stable_label_results: dict,
    feature_key: str
) -> dict:
    """
    Predict labels for each :class:`AnnData` in ``adata_dict`` using the corresponding classifier from ``stable_label_results``,
    and convert numeric predictions back to text labels.

    Parameters
    ------------
    adata_dict
        An :class:`AdataDict`.

    stable_label_results
        Dictionary with keys as identifiers and values as dictionaries containing output from ``stable_label_adata``.

    feature_key
        Key to access the features in ``adata.obsm``.

    Returns
    ------------
    predictions_dict
        Dictionary with keys as identifiers from ``adata_dict`` and values as predicted text labels.
    """
    predictions_dict = {}

    for stratum, adata in adata_dict.items():
        if stratum in stable_label_results:
            classifier = stable_label_results[stratum]['classifier']
            label_encoder = stable_label_results[stratum]['label_encoder']
            X = adata.obsm[feature_key]

            # Predict the numeric labels using the trained classifier
            predicted_numeric_labels = classifier.predict(X)

            # Check if predicted labels are within the range of the label encoder's classes
            valid_labels = set(label_encoder.transform(label_encoder.classes_))
            invalid_labels = set(predicted_numeric_labels) - valid_labels

            if invalid_labels:
                print(f"Error: Predicted labels {invalid_labels} are not in the label encoder's classes for {stratum}")
                continue

            # Convert numeric predictions back to text labels
            predicted_text_labels = label_encoder.inverse_transform(predicted_numeric_labels)

            # Get the indices of the cells
            indices = np.array(adata.obs.index)

            predictions_dict[stratum] = {
                'indices': indices,
                'predicted_labels': predicted_text_labels
            }
        else:
            print(f"No classifier found for {stratum}. Skipping prediction.")

    return predictions_dict


def update_adata_labels_with_stable_label_results_dict(
    adata_dict: AdataDict,
    stable_label_results_dict: dict,
    new_label_key: str = 'stable_cell_type'
):
    """
    Updates each AnnData object in adata_dict with new labels from stable_label_results_dict.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    stable_label_results_dict
        Dictionary of dictionaries containing results, including indices and final_labels for each AnnData key.

    new_label_key
        Name of the new column in adata.obs where the labels will be stored.
    """
    update_adata_dict_with_label_dict(adata_dict, stable_label_results_dict, new_label_key=new_label_key, label_key='final_labels')


def update_adata_labels_with_predictions_dict(
    adata_dict: AdataDict,
    predictions_dict: dict,
    new_label_key: str = 'predicted_cell_type'
    ) -> None:
    """
    Updates each :class:`AnnData` in ``adata_dict`` with new labels from ``predictions_dict``.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    predictions_dict
        Dictionary of predicted labels for each ``AnnData`` key.

    new_label_key
        Name of the new column in adata.obs where the labels will be stored.

    Returns
    --------
    None

    Notes
    ---------
    This function modifies the input ``adata_dict`` in-place.
    """
    update_adata_dict_with_label_dict(adata_dict, predictions_dict, new_label_key=new_label_key, label_key='predicted_labels')


def update_adata_dict_with_label_dict(
    adata_dict: AdataDict,
    results_dict: dict,
    new_label_key: str | None = None,
    label_key: str | None = None
) -> None:
    """
    Wrapper function to update each AnnData object in adata_dict with new labels from results_dict.
    Accepts either 'final_labels' or 'predicted_labels' as the label key.
    results_dict can be either 1) stable_label_results: the object returned by stable_label_adata_dict()
    or 2) predictions_dict: the object returned by predict_labels_adata_dict

    Parameters
    -----------
    adata_dict
        Dictionary of AnnData objects to be updated.

    results_dict
        Dictionary containing results, including indices and labels for each AnnData key.

    new_label_key
        Name of the new column in adata.obs where the labels will be stored.

    label_key
        Key to access the labels in results_dict (either 'final_labels' or 'predicted_labels').

    Returns
    --------
    None

    Notes
    ---------
    This function modifies the input ``adata_dict`` in-place.
    """
    for key, adata in adata_dict.items():
        if key in results_dict:
            subset_results = results_dict[key]
            indices = subset_results['indices']
            labels = subset_results[label_key]

            add_col_to_adata_obs(adata, indices, labels, new_label_key)
