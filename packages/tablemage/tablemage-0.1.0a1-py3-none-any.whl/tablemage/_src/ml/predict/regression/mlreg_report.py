import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal
import warnings
from .base import BaseR
from ....data.datahandler import DataHandler
from ....metrics.visualization import plot_obs_vs_pred
from ....display.print_utils import (
    print_wrapped,
    color_text,
    bold_text,
    list_to_string,
    fill_ignore_format,
    quote_and_color,
    format_two_column,
)
from ....display.print_options import print_options
from ....feature_selection import BaseFSR, VotingSelectionReport


warnings.simplefilter("ignore", category=UserWarning)


class SingleModelSingleDatasetMLRegReport:
    """
    Class for generating regression-relevant plots and
    tables for a single machine learning model on a single dataset.
    """

    def __init__(self, model: BaseR, dataset: Literal["train", "test"]):
        """
        Initializes a SingleModelSingleDatasetMLReport object.

        Parameters
        ----------
        model : BaseRegression
            The data for the model must already be
            specified. The model should already be trained on the specified data.

        dataset : Literal['train', 'test']
        """
        self._model = model
        if dataset not in ["train", "test"]:
            raise ValueError('dataset must be either "train" or "test".')
        self._dataset = dataset

    def metrics(self) -> pd.DataFrame:
        """Returns a DataFrame containing the goodness-of-fit statistics
        for the model on the specified data.

        Returns
        ----------
        pd.DataFrame
        """
        if self._dataset == "train":
            return (
                self._model._train_scorer.stats_df()
                .astype(float)
                .round(print_options._n_decimals)
            )
        else:
            return (
                self._model._test_scorer.stats_df()
                .astype(float)
                .round(print_options._n_decimals)
            )

    def cv_metrics(self, average_across_folds: bool = True) -> pd.DataFrame | None:
        """Returns a DataFrame containing the cross-validated goodness-of-fit
        statistics for the model on the specified data.

        Parameters
        ----------
        average_across_folds : bool
            Default: True. If True, returns a DataFrame
            containing goodness-of-fit statistics averaged across all folds.
            Otherwise, returns a DataFrame containing goodness-of-fit
            statistics for each fold.

        Returns
        ----------
        pd.DataFrame | None
            None is returned if cross validation fit statistics are not available.
        """
        if not self._model.is_cross_validated():
            print_wrapped(
                "Cross validation statistics are not available "
                + "for models that are not cross-validated.",
                type="WARNING",
            )
            return None
        if self._dataset == "train":
            if average_across_folds:
                return (
                    self._model._cv_scorer.stats_df()
                    .astype(float)
                    .round(print_options._n_decimals)
                )
            else:
                return (
                    self._model._cv_scorer.cv_stats_df()
                    .astype(float)
                    .round(print_options._n_decimals)
                )
        else:
            print_wrapped(
                "Cross validation statistics are not available for test data.",
                type="WARNING",
            )
            return None

    def plot_obs_vs_pred(
        self, figsize: tuple[float, float] = (5, 5), ax: plt.Axes | None = None
    ) -> plt.Figure:
        """Returns a figure that is a scatter plot of the observed (y-axis) and
        predicted (x-axis) values.

        Parameters
        ----------
        figsize : tuple[float, float]
            Default: (5, 5). The size of the figure.

        ax : plt.Axes | None
            Default: None. The axes on which to plot the figure. If None,
            a new figure is created.

        Returns
        -------
        plt.Figure
        """
        if self._dataset == "train":
            y_pred = self._model._train_scorer._y_pred
            y_true = self._model._train_scorer._y_true
        else:
            y_pred = self._model._test_scorer._y_pred
            y_true = self._model._test_scorer._y_true
        return plot_obs_vs_pred(y_pred, y_true, self._model._name, figsize, ax)


class SingleModelMLRegReport:
    """SingleModelMLRegReport: generates regression-relevant plots and
    tables for a single machine learning model.
    """

    def __init__(self, model: BaseR):
        """
        Initializes a SingleModelMLRegReport object.

        Parameters
        ----------
        model : BaseR
            The data for the model must already be specified.
            The model should already be trained on the specified data.
        """
        self._model = model

    def train_report(self) -> SingleModelSingleDatasetMLRegReport:
        """Returns a SingleModelSingleDatasetMLReport object for the training data.

        Returns
        -------
        SingleModelSingleDatasetMLReport
        """
        return SingleModelSingleDatasetMLRegReport(self._model, "train")

    def test_report(self) -> SingleModelSingleDatasetMLRegReport:
        """Returns a SingleModelSingleDatasetMLReport object for the test data.

        Returns
        -------
        SingleModelSingleDatasetMLReport
        """
        return SingleModelSingleDatasetMLRegReport(self._model, "test")

    def model(self) -> BaseR:
        """Returns the model.

        Returns
        -------
        BaseR
        """
        return self._model

    def plot_obs_vs_pred(
        self,
        dataset: Literal["train", "test"],
        figsize: tuple[float, float] = (5, 5),
        ax: plt.Axes | None = None,
    ) -> plt.Figure:
        """Returns a figure that is a scatter plot of the observed (y-axis) and
        predicted (x-axis) values for the specified dataset.

        Parameters
        ----------
        dataset : Literal['train', 'test']
            The dataset for which to plot the observed vs predicted values.

        figsize : tuple[float, float]
            Default: (5, 5). The size of the figure.

        ax : plt.Axes | None
            Default: None. The axes on which to plot the figure. If None,
            a new figure is created.

        Returns
        -------
        plt.Figure
        """
        if dataset == "train":
            return self.train_report().plot_obs_vs_pred(figsize, ax)
        elif dataset == "test":
            return self.test_report().plot_obs_vs_pred(figsize, ax)
        else:
            raise ValueError('dataset must be either "train" or "test".')

    def fs_report(self) -> VotingSelectionReport | None:
        """Returns the feature selection report. If feature selectors were
        specified at the model level or not at all, then this method will return None.

        Returns
        -------
        VotingSelectionReport | None
            None is returned if no feature selectors were specified.
        """
        return self._model.fs_report()

    def feature_importance(self) -> pd.DataFrame | None:
        """Returns the feature importances for the model. If the model does not
        have feature importances, the coefficients are returned instead.
        If the model does not have feature importances or coefficients,
        None is returned.

        Returns
        -------
        pd.DataFrame | None
            None is returned if the model does not have feature importances.
        """
        return (
            self._model.feature_importance()
            .astype(float)
            .round(print_options._n_decimals)
        )


class MLRegressionReport:
    """Class for reporting model goodness of fit.
    Fits the model based on provided DataHandler.
    """

    def __init__(
        self,
        models: list[BaseR],
        datahandler: DataHandler,
        target: str,
        predictors: list[str],
        feature_selectors: list[BaseFSR] | None = None,
        max_n_features: int | None = None,
        outer_cv: int | None = None,
        outer_cv_seed: int = 42,
        verbose: bool = True,
    ):
        """MLRegressionReport.
        Fits the model based on provided DataHandler.

        Parameters
        ----------
        models : list[BaseR]
            The models will be trained by the MLRegressionReport object.

        datahandler : DataHandler
            The DataHandler object that contains the data.

        target : str
            The name of the target variable.

        predictors : list[str]
            The names of the predictor variables.

        feature_selectors : list[BaseFSR] | None
            Default: None.
            The feature selectors for voting selection. Feature selectors
            can be used to select the most important predictors.

        max_n_features : int | None
            Default: None.
            Maximum number of predictors to utilize. Ignored if feature_selectors
            is None.

        outer_cv : int | None
            Default: None.
            If not None, reports training scores via nested k-fold CV.

        outer_cv_seed : int
            Default: 42. The random seed for the outer cross validation loop.

        verbose : bool
            Default: True. If True, prints progress.
        """
        self._models: list[BaseR] = models

        for model in self._models:
            if not isinstance(model, BaseR):
                raise ValueError(
                    f"Model {quote_and_color(str(model))} is not an instance "
                    "of BaseR. All models must be instances of BaseR."
                )

        self._id_to_model = {}
        for model in models:
            if model._name in self._id_to_model:
                raise ValueError(
                    f"Duplicate model name: {quote_and_color(model._name)}."
                )
            self._id_to_model[model._name] = model

        self._feature_selection_report = None
        self._feature_selectors = feature_selectors

        self._y_var = target
        self._predictors = predictors
        self._X_vars = predictors

        self._emitter = datahandler.train_test_emitter(y_var=target, X_vars=predictors)
        if feature_selectors is not None:
            for feature_selector in feature_selectors:
                if not isinstance(feature_selector, BaseFSR):
                    raise ValueError(
                        f"Feature selector {quote_and_color(model._name)} "
                        "is not an instance of BaseFSR. "
                        "All feature selectors must be instances of BaseFSR."
                    )

            self._feature_selection_report = VotingSelectionReport(
                selectors=feature_selectors,
                dataemitter=self._emitter,
                max_n_features=max_n_features,
                verbose=verbose,
            )
            self._X_vars = self._feature_selection_report.top_features()
            self._emitter.select_predictors(self._X_vars)

        self._emitters = None

        if outer_cv is not None:
            self._emitters = datahandler.kfold_emitters(
                y_var=target,
                X_vars=predictors,
                n_folds=outer_cv,
                shuffle=True,
                random_state=outer_cv_seed,
            )
            if feature_selectors is not None:
                for emitter in self._emitters:
                    fold_selection_report = VotingSelectionReport(
                        selectors=feature_selectors,
                        dataemitter=emitter,
                        max_n_features=max_n_features,
                        verbose=verbose,
                    )
                    emitter.select_predictors(fold_selection_report.top_features())

        self._verbose = verbose

        for model in self._models:
            if self._verbose:
                print_wrapped(
                    f"Fitting model {quote_and_color(model._name)}.",
                    type="UPDATE",
                )
            model.specify_data(
                dataemitter=self._emitter,
                dataemitters=self._emitters,
            )

            model.fit(verbose=self._verbose)

            if (
                model._feature_selection_report is not None
                and self._feature_selection_report is not None
            ):
                if self._verbose:
                    print_wrapped(
                        "Feature selectors were specified for all models as well as "
                        f"for the model {quote_and_color(model._name)}. "
                        f"The feature selection report attributed "
                        f"to {quote_and_color(model._name)} "
                        "will be for the model-specific feature selectors. "
                        "Note that the feature selectors for all models "
                        "were used to select a subset of the predictors first. "
                        "Then, the model-specific feature selectors were used to "
                        "select a subset of the predictors from the subset selected "
                        "by the feature selectors for all models.",
                        type="WARNING",
                        level="INFO",
                    )

            if model._feature_selection_report is None:
                model._set_voting_selection_report(
                    voting_selection_report=self._feature_selection_report
                )

            if self._verbose:
                print_wrapped(
                    f"Successfully evaluated model {quote_and_color(model._name)}.",
                    type="UPDATE",
                )

        self._id_to_report = {
            model._name: SingleModelMLRegReport(model) for model in models
        }

    def _model_report(self, model_id: str) -> SingleModelMLRegReport:
        """Returns the SingleModelMLRegReport object for the specified model.

        Parameters
        ----------
        model_id : str
            The id of the model.

        Returns
        -------
        SingleModelMLRegReport
        """
        if model_id not in self._id_to_report:
            raise ValueError(f"Model {model_id} not found.")
        return self._id_to_report[model_id]

    def model(self, model_id: str) -> BaseR:
        """Returns the model with the specified id.

        Parameters
        ----------
        model_id : str
            The id of the model.

        Returns
        -------
        BaseR
        """
        if model_id not in self._id_to_model:
            raise ValueError(f"Model {model_id} not found.")
        return self._id_to_model[model_id]

    def metrics(self, dataset: Literal["train", "test", "both"]) -> pd.DataFrame:
        """Returns a DataFrame containing the metrics for
        all models on the specified data.

        Parameters
        ----------
        dataset : Literal['train', 'test', 'both']
            The dataset for which to return the metrics.

        Returns
        -------
        pd.DataFrame
        """
        if dataset == "train":
            return pd.concat(
                [
                    report.train_report().metrics()
                    for report in self._id_to_report.values()
                ],
                axis=1,
            )
        elif dataset == "test":
            return pd.concat(
                [
                    report.test_report().metrics()
                    for report in self._id_to_report.values()
                ],
                axis=1,
            )
        elif dataset == "both":
            test_metrics = pd.concat(
                [
                    report.test_report().metrics()
                    for report in self._id_to_report.values()
                ],
                axis=1,
            )
            train_metrics = pd.concat(
                [
                    report.train_report().metrics()
                    for report in self._id_to_report.values()
                ],
                axis=1,
            )
            return pd.concat(
                [train_metrics, test_metrics], keys=["train", "test"], names=["Dataset"]
            )
        else:
            raise ValueError('dataset must be either "train", "test", or "both".')

    def cv_metrics(self, average_across_folds: bool = True) -> pd.DataFrame | None:
        """Returns a DataFrame containing the cross-validated goodness-of-fit
        statistics for all models on the training data. Cross validation must
        have been conducted, otherwise None is returned.

        Parameters
        ----------
        average_across_folds : bool
            Default: True.
            If True, returns a DataFrame containing goodness-of-fit
            statistics averaged across all folds.
            Otherwise, returns a DataFrame containing goodness-of-fit
            statistics for each fold.

        Returns
        -------
        pd.DataFrame | None
            None if cross validation was not conducted.
        """
        if not self._models[0].is_cross_validated():
            print_wrapped(
                "Cross validation statistics are not available "
                + "for models that are not cross-validated.",
                type="WARNING",
            )
            return None
        return pd.concat(
            [
                report.train_report().cv_metrics(average_across_folds)
                for report in self._id_to_report.values()
            ],
            axis=1,
        )

    def fs_report(self) -> VotingSelectionReport | None:
        """Returns the feature selection report. If feature selectors were
        specified at the model level or not at all, then this method will return None.

        To access the feature selection report for a specific model, use
        model_report(<model_id>).feature_selection_report().

        Returns
        -------
        VotingSelectionReport | None
            None if feature selectors were not specified.
        """
        if self._feature_selection_report is None:
            print_wrapped(
                "No feature selection report available.",
                type="WARNING",
            )
        return self._feature_selection_report

    def plot_obs_vs_pred(
        self,
        model_id: str,
        dataset: Literal["train", "test"],
        figsize: tuple[float, float] = (5, 5),
        ax: plt.Axes | None = None,
    ) -> plt.Figure:
        """Returns a figure that is a scatter plot of the observed (y-axis) and
        predicted (x-axis) values for the specified model and dataset.

        Parameters
        ----------
        model_id : str
            The id of the model.

        dataset : Literal['train', 'test']
            The dataset for which to plot the observed vs predicted values.

        figsize : tuple[float, float]
            Default: (5, 5). The size of the figure.

        ax : plt.Axes | None
            Default: None. The axes on which to plot the figure. If None,
            a new figure is created.

        Returns
        -------
        plt.Figure
        """
        return self._id_to_report[model_id].plot_obs_vs_pred(dataset, figsize, ax)

    def feature_importance(self, model_id: str) -> pd.DataFrame | None:
        """Returns the feature importances of the model with the specified id.
        If the model does not have feature importances, the coefficients are returned
        instead. Otherwise, None is returned.

        Parameters
        ----------
        model_id : str
            The id of the model.

        Returns
        -------
        pd.DataFrame | None
            None is returned if the model does not have feature importances
            or coefficients.
        """
        return self._id_to_report[model_id].feature_importance()

    def __getitem__(self, model_id: str) -> SingleModelMLRegReport:
        return self._id_to_report[model_id]

    def __str__(self) -> str:
        n_dec = print_options._n_decimals
        max_width = print_options._max_line_width

        top_divider = color_text("=" * max_width, "none") + "\n"
        bottom_divider = "\n" + color_text("=" * max_width, "none")
        divider = "\n" + color_text("-" * max_width, "none") + "\n"
        divider_invisible = "\n" + " " * max_width + "\n"

        title_message = bold_text("ML Regression Report")

        target_var = "'" + self._y_var + "'"
        target_message = f"{bold_text('Target variable:')}\n"
        target_message += fill_ignore_format(
            color_text(target_var, "purple"),
            width=max_width,
            initial_indent=2,
            subsequent_indent=2,
        )

        predictors_message = f"{bold_text('Predictor variables:')}\n"
        predictors_message += fill_ignore_format(
            list_to_string(self._predictors),
            width=max_width,
            initial_indent=2,
            subsequent_indent=2,
        )

        models_str = list_to_string(
            [model._name for model in self._models],
            color="blue",
        )
        models_message = f"{bold_text('Models evaluated:')}\n"
        models_message += fill_ignore_format(
            models_str,
            width=max_width,
            initial_indent=2,
            subsequent_indent=2,
        )

        if self._feature_selectors is not None:
            fs_str = list_to_string(
                [fs._name for fs in self._feature_selectors], color="blue"
            )
        else:
            fs_str = color_text("None", "yellow")
        feature_selectors_message = f"{bold_text('Feature selectors:')}\n"
        feature_selectors_message += fill_ignore_format(
            fs_str,
            width=max_width,
            initial_indent=2,
            subsequent_indent=2,
        )

        top_models_message = f"{bold_text('Best models:')}\n"
        top_models_df = (
            self.metrics("test").T.sort_values("rmse", ascending=True).head(3)
        )
        for i, model in enumerate(top_models_df.index):
            top_models_message += fill_ignore_format(
                format_two_column(
                    f"{i+1}. " + quote_and_color(str(model)),
                    "Test RMSE: "
                    + color_text(
                        str(np.round(top_models_df.loc[model, "rmse"], n_dec)), "yellow"
                    ),
                    total_len=max_width - 2,
                ),
                initial_indent=2,
            )
            if i < len(top_models_df) - 1:
                top_models_message += "\n"

        final_message = (
            top_divider
            + title_message
            + divider
            + target_message
            + divider_invisible
            + predictors_message
            + divider_invisible
            + models_message
            + divider_invisible
            + feature_selectors_message
            + divider
            + top_models_message
            + bottom_divider
        )

        return final_message

    def _repr_pretty_(self, p, cycle):
        p.text(str(self))

    def _to_dict(self) -> dict:
        return {
            "train_metrics": self.metrics("train").to_dict("index"),
            "test_metrics": self.metrics("test").to_dict("index"),
            "model_info": [model._to_dict() for model in self._models],
        }
