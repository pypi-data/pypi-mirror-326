from sklearn.svm import SVR
from typing import Mapping, Iterable, Literal
from .base import BaseR, HyperparameterSearcher
from optuna.distributions import (
    FloatDistribution,
    IntDistribution,
    CategoricalDistribution,
    BaseDistribution,
)
from ....feature_selection import BaseFSR


class SVMR(BaseR):
    """Support vector machine regressor.

    Hyperparameter optimization is performed automatically during training.
    The hyperparameter search process can be modified by the user.
    """

    def __init__(
        self,
        type: Literal["linear", "poly", "rbf"] = "rbf",
        hyperparam_search_method: Literal["optuna", "grid"] | None = None,
        hyperparam_search_space: (
            Mapping[str, Iterable | BaseDistribution] | None
        ) = None,
        feature_selectors: list[BaseFSR] | None = None,
        max_n_features: int | None = None,
        name: str | None = None,
        **kwargs,
    ):
        """
        Initializes a SVMR object.

        Parameters
        ----------
        type : Literal['linear', 'poly', 'rbf']
            Default: 'rbf'. The type of kernel to use.

        hyperparam_search_method : Literal[None, 'grid', 'optuna']
            Default: None. If None, a model-specific default hyperparameter search
            is conducted.

        hyperparam_search_space : Mapping[str, Iterable | BaseDistribution]
            Default: None. If None, a model-specific default hyperparameter search
            is conducted.

        feature_selectors : list[BaseFSC]
            Default: None. If not None, specifies the feature selectors for the
            VotingSelectionReport.

        max_n_features : int | None
            Default: None.
            Only useful if feature_selectors is not None.
            If None, then all features with at least 50% support are selected.

        model_random_state : int
            Default: 42. Random seed for the model.

        name : str
            Default: None. Determines how the model shows up in the reports.
            If None, the name is set to be the class name.

        **kwargs : dict
            Key word arguments are passed directly into the intialization of the
            HyperparameterSearcher class. See below for options.

            inner_cv : int | BaseCrossValidator
                Default: 5. Number of inner cross validation folds. Inner
                cross validation is used for hyperparameter optimization.

            inner_cv_seed : int
                Default: 42. Random seed for inner cross validation.

            n_jobs : int
                Default: 1. Number of parallel jobs to run.

            verbose : int
                Default: 0. Sets the sklearn verbosity level for the sklearn estimator.
                2 is the most verbose.

            n_trials : int
                Default: 100. Number of trials for hyperparameter optimization. Only
                used if hyperparam_search_method is 'optuna'.
        """
        super().__init__()

        if name is None:
            self._name = f"SVMR({type})"
        else:
            self._name = name

        self._best_estimator = SVR(kernel=type, max_iter=100)
        self._feature_selectors = feature_selectors
        self._max_n_features = max_n_features

        if (hyperparam_search_method is None) or (hyperparam_search_space is None):
            hyperparam_search_method = "optuna"

            if type == "linear":
                hyperparam_search_space = {
                    "C": FloatDistribution(1e-2, 1e2, log=True),
                    "epsilon": FloatDistribution(1e-3, 1e0, log=True),
                }
            elif type == "poly":
                hyperparam_search_space = {
                    "C": FloatDistribution(1e-2, 1e2, log=True),
                    "epsilon": FloatDistribution(1e-3, 1e0, log=True),
                    "degree": IntDistribution(2, 5),
                    "coef0": IntDistribution(0, 10),
                    "gamma": CategoricalDistribution(["scale", "auto"]),
                }
            elif type == "rbf":
                hyperparam_search_space = {
                    "C": FloatDistribution(1e-2, 1e2, log=True),
                    "epsilon": FloatDistribution(1e-3, 1e0, log=True),
                    "gamma": CategoricalDistribution(["scale", "auto"]),
                }
            else:
                raise ValueError(f"Invalid value for type: {type}.")

        self._hyperparam_searcher = HyperparameterSearcher(
            estimator=self._best_estimator,
            method=hyperparam_search_method,
            hyperparam_grid=hyperparam_search_space,
            estimator_name=self._name,
            **kwargs,
        )

        self._validate_inputs()
