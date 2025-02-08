"""
This module contains adata_dict wrappers for `scanpy`.
"""

import scanpy as sc

from anndata import AnnData

from anndict.adata_dict import (
    AdataDict,
    adata_dict_fapply,
    adata_dict_fapply_return,
    build_adata_dict,
    concatenate_adata_dict,
    check_and_create_stratifier,
)


def subsample_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Subsamples each :class:`AnnData` in ``adata_dict`` using :func:`sc.pp.subsample`.
    
    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.subsample`

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    n_obs = kwargs.get('n_obs', None)
    fraction = kwargs.get('fraction', None)

    if n_obs is None and fraction is None:
        fraction = 1
        kwargs['fraction'] = fraction

    def subsample_adata(adata, **kwargs):
        if n_obs is None or adata.n_obs > n_obs:
            sc.pp.subsample(adata, **kwargs)

    adata_dict_fapply(adata_dict, subsample_adata, **kwargs)


def resample_adata(
    adata: AnnData,
    strata_keys: list[str],
    min_num_cells: int,
    n_largest_groups: int | None = None,
    **kwargs
) -> AnnData:
    """
    Resample ``adata`` based on specified strata keys and drop strata with fewer than the minimum number of cells.

    Parameters
    -----------
    adata
        An :class:`AnnData`.

    strata_keys
        List of column names in adata.obs to use for stratification.

    min_num_cells
        Minimum number of cells required to retain a stratum.

    kwargs
        Additional keyword arguments to pass to the subsample function.

    Returns
    --------
    Concatenated :class:`AnnData` object after resampling and filtering.

    Raises
    --------
    ValueError
        If any of the specified ``strata_keys`` do not exist in ``adata.obs``.
    """
    # Step 1: Create the strata key
    strata_key = check_and_create_stratifier(adata, strata_keys)

    # Step 2: Calculate the size of each category
    category_counts = adata.obs[strata_key].value_counts()

    # Step 3: Identify the top n largest categories or all categories if n is None
    if n_largest_groups is None:
        selected_categories = category_counts.index.tolist()
    else:
        selected_categories = category_counts.nlargest(n_largest_groups).index.tolist()

    # Step 4: Build adata_dict based on the strata key
    strata_dict = build_adata_dict(adata, [strata_key], desired_strata=selected_categories)

    # Step 5: Subsample each AnnData object in the strata_dict
    subsample_adata_dict(strata_dict, **kwargs)

    # Step 6: Drop AnnData objects with fewer than min_num_cells
    filtered_dict = {k: v for k, v in strata_dict.items() if v.n_obs >= min_num_cells}

    # Step 7: Concatenate the filtered_dict back to a single AnnData object
    #setting index_unique=None avoids index modification
    return concatenate_adata_dict(filtered_dict, index_unique=None)


def resample_adata_dict(
    adata_dict: AdataDict,
    strata_keys: list[str],
    n_largest_groups: int | None = None,
    min_num_cells: int = 0,
    **kwargs
) -> AdataDict:
    """
    Resample each :class:`AnnData` in ``adata_dict`` based on specified strata keys and drop strata with fewer than the minimum number of cells.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    strata_keys
        List of column names in `.obs` to use for stratification. Must be present in each adata in ``adata_dict``.

    min_num_cells
        Minimum number of cells required to retain a stratum.

    kwargs
        Additional keyword arguments to pass to :func:`~anndict.wrappers.resample_adata`.

    Returns
    --------
    :class:`AdataDict` of resampled :class:`AnnData` after filtering.
    """
    return adata_dict_fapply_return(adata_dict, resample_adata, strata_keys=strata_keys, n_largest_groups=n_largest_groups, min_num_cells=min_num_cells, **kwargs)


def normalize_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Normalizes each :class:`AnnData` in ``adata_dict`` using :func:`sc.pp.normalize_total`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.normalize_total`

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.pp.normalize_total, **kwargs)


def log_transform_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Log-transforms each :class:`AnnData` in ``adata_dict`` using :func:`sc.pp.log1p`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.log1p`

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.pp.log1p, **kwargs)


def set_high_variance_genes_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Identifies highly variable genes in each :class:`AnnData` in ``adata_dict`` using :func:`sc.pp.highly_variable_genes`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.highly_variable_genes`

    Returns
    --------
    None

    Notes
    ------
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.pp.highly_variable_genes, **kwargs)

def rank_genes_groups_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Identifies differentially expressed genes in each :class:`AnnData` in ``adata_dict`` using :func:`sc.tl.rank_genes_groups`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.tl.rank_genes_groups`

    Returns
    --------
    None

    Notes
    ------
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.tl.rank_genes_groups, **kwargs)


def scale_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Scales each :class:`AnnData` object in ``adata_dict`` using :func:`sc.pp.scale`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.scale`

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.pp.scale, **kwargs)


def pca_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Performs PCA on each :class:`AnnData` object in ``adata_dict`` using :func:`sc.pp.pca`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.pca`.

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.pp.pca, **kwargs)


def neighbors_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Calculates neighborhood graph for each :class:`AnnData` object in ``adata_dict`` using :func:`sc.pp.neighbors`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.pp.neighbors`.

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.pp.neighbors, **kwargs)


def leiden_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Performs Leiden clustering for each AnnData object in ``adata_dict`` using Scanpy's leiden function.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.tl.leiden`.

    Returns
    --------
    None

    Notes
    -----
    The function modifies ``adata_dict`` in-place.
    """
    adata_dict_fapply(adata_dict, sc.tl.leiden, **kwargs)

def leiden_sub_cluster(
    adata: AnnData,
    groupby: str,
    **kwargs
) -> AnnData:
    """
    Perform Leiden clustering on subgroups of cells.

    This function applies Leiden clustering to subgroups of cells defined by the ``groupby`` parameter.

    Parameters
    -----------
    adata
        An :class:`AnnData`.

    groupby
        Column name in ``adata.obs`` for grouping cells before subclustering.

    kwargs
        Additional keyword arguments to pass to :func:`leiden_adata_dict`.

    Returns
    --------
    None

    Notes
    -----
    The function modifies the input ``AnnData`` object in-place.
    """
    adata_dict = build_adata_dict(adata, strata_keys=[groupby])
    leiden_adata_dict(adata_dict, **kwargs)
    adata = concatenate_adata_dict(adata_dict, index_unique=None) #setting index_unique=None avoids index modification
    return adata


def leiden_sub_cluster_adata_dict(
    adata_dict: AdataDict,
    groupby: str,
    **kwargs
) -> AdataDict:
    """
    Applies the :func:`leiden_sub_cluster` function to each :class:`AnnData` object in ``adata_dict``.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    groupby
        Column name in ``adata.obs`` for grouping cells before subclustering.

    kwargs
        Additional keyword arguments to pass to :func:`leiden_sub_cluster`.

    Returns
    --------
    :class:`AdataDict` of resampled AnnData objects after filtering.
    """
    return adata_dict_fapply_return(adata_dict, leiden_sub_cluster, groupby=groupby, **kwargs)


def calculate_umap_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> AdataDict:
    """
    Calculates UMAP embeddings for each :class:`AnnData` in ``adata_dict`` using :func:`sc.tl.umap`.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments to pass to :func:`sc.tl.umap`.

    Returns
    --------
    :class:`AdataDict` with UMAP coordinates added to each :class:`AnnData`.
    """
    adata_dict_fapply(adata_dict, sc.tl.umap, **kwargs)
    return adata_dict


def plot_umap_adata_dict(
    adata_dict: AdataDict,
    **kwargs
) -> None:
    """
    Plots UMAP embeddings for each :class:`AnnData` in ``adata_dict``, colored by a specified variable.

    Parameters
    -----------
    adata_dict
        An :class:`AdataDict`.

    kwargs
        Additional keyword arguments, including 'color_by' which specifies a variable by which to color the UMAP plots, typically a column in ``.obs``.

    Returns
    --------
    None

    Notes
    -----
    The function creates plots for the each :class:`AnnData`.
    """
    def plot_umap(adata, adt_key=None, **kwargs):
        print(f"Plotting UMAP for key: {adt_key}")
        if 'X_umap' in adata.obsm:
            sc.pl.umap(adata, **kwargs)
        else:
            print(f"UMAP not computed for adata with key {adt_key}. Please compute UMAP before plotting.")
    adata_dict_fapply(adata_dict, plot_umap, use_multithreading=False, **kwargs)
