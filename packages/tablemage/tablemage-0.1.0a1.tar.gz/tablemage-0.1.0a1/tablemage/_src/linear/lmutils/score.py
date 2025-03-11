from typing import Literal
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
from ...data import DataEmitter


def compute_aic_bic(
    estimator, X_train, y_train=None, aic=True  # y_train needed only for OLS
):
    """
    Compute AIC or BIC for OLS, Logit, or MNLogit models.

    Parameters:
    - estimator: the fitted model (could be OLS, Logit, or MNLogit)
    - X_train: the training data (features)
    - y_train: the training data (target), needed only for OLS
    - aic: bool, if True compute AIC, else compute BIC

    Returns:
    - AIC or BIC value
    """
    # Get the number of observations (n) and features (k)
    n = X_train.shape[0]
    k = np.sum(estimator.params != 0)  # Number of non-zero parameters

    # Handle based on model type
    if hasattr(estimator, "llf"):  # For Logit and MNLogit (log-likelihood is available)
        log_likelihood = estimator.llf  # Extract log-likelihood

    else:  # OLS case (no llf, so compute log-likelihood manually)
        if y_train is None:
            raise ValueError("y_train must be provided for OLS models.")

        # Predict and compute residuals
        y_pred = estimator.predict(X_train)
        residuals = y_train - y_pred

        # Compute the RSS (residual sum of squares)
        rss = np.sum(residuals**2)

        # Estimate sigma^2 with a small epsilon to prevent division by zero
        sigma2 = rss / (n - k + 1e-8)

        # Compute log-likelihood for OLS with normal errors
        log_likelihood = -0.5 * n * (np.log(2 * np.pi * sigma2) + 1)

    # Compute AIC or BIC
    if aic:
        return 2 * k - 2 * log_likelihood
    else:
        return np.log(n) * k - 2 * log_likelihood


def score_model(
    emitter: DataEmitter,
    feature_list: list[str],
    model: Literal["ols", "logit", "mnlogit"],
    alpha: float,
    l1_weight: float,
    metric: Literal["aic", "bic"],
    y_label_encoder: LabelEncoder | None = None,
) -> float:
    """Scores a linear model.

    Parameters
    ----------
    emitter : DataEmitter
        The data emitter.

    feature_list : list[str]
        The list of features to use in the model. These should be
        PRE-one-hot encoded features.

    model : Literal["ols", "logit", "mnlogit"]
        The model to use.

    alpha : float
        The alpha value for the model.

    l1_weight : float
        The l1 weight for the model.

    metric : Literal["aic", "bic"]
        The metric to use for scoring.

    y_label_encoder : LabelEncoder | None
        The label encoder for the target variable, by default None.
        Only used for the binomial model.
    """
    if len(feature_list) == 0:
        return np.inf

    # obtain the data
    emitter.select_predictors_pre_onehot(feature_list)
    X_train, y_train = emitter.emit_train_Xy()

    # like typical fitting, we enforce a constant, regardless of prior existence
    X_train_w_constant = sm.add_constant(X_train, has_constant="add")

    # fit the appropriate model, no need for heterscedasticity robust standard errors
    if model == "ols":
        new_model = sm.OLS(y_train, X_train_w_constant)
    elif model == "logit":
        if y_label_encoder is not None:
            y_train = y_label_encoder.transform(y_train)
        new_model = sm.Logit(y_train, X_train_w_constant)
    elif model == "mnlogit":
        if y_label_encoder is not None:
            y_train = y_label_encoder.transform(y_train)
        new_model = sm.MNLogit(y_train, X_train_w_constant)
    else:
        raise ValueError("Model must be one of 'ols', 'logit', or 'mnlogit'.")

    max_iter = 100

    if alpha == 0:
        output = new_model.fit(maxiter=max_iter)
        stat = 0
        if metric == "aic":
            stat = output.aic
        elif metric == "bic":
            stat = output.bic
        else:
            raise ValueError("Metric must be one of 'aic', 'bic'")
    else:
        output = new_model.fit_regularized(
            alpha=alpha, L1_wt=l1_weight, maxiter=max_iter
        )
        stat = compute_aic_bic(
            output, X_train_w_constant, y_train, True if metric == "aic" else False
        )

    if isinstance(stat, float):
        return stat
    else:
        return stat.mean()
