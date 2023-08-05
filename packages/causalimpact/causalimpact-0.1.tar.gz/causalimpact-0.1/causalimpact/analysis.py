import numpy as np
import pandas as pd
from pandas.core.common import PandasError
from pandas.util.testing import is_list_like

from causalimpact.misc import standardize_all_variables
from causalimpact.model import construct_model, model_fit
from causalimpact.inferences import compile_posterior_inferences
# from causalimpact.inferences import compile_na_inferences
import warnings


class CausalImpact(object):

    def __init__(self, data=None, pre_period=None, post_period=None,
                 model_args=None, ucm_model=None, post_period_response=None,
                 alpha=0.05, estimation="MLE"):
        warnings.warn(Warning("""This code is still wip and not fully
                tested yet"""))
        self.series = None
        self.model = {}
        if isinstance(data, pd.DataFrame):
            self.data = data.copy()
        else:
            self.data = data
        self.params = {"data": data, "pre_period": pre_period,
                       "post_period": post_period, "model_args": model_args,
                       "ucm_model": ucm_model,
                       "post_period_response": post_period_response,
                       "alpha": alpha, "estimation": estimation}

    def run(self):
        kwargs = self._format_input(self.params["data"],
                                    self.params["pre_period"],
                                    self.params["post_period"],
                                    self.params["model_args"],
                                    self.params["ucm_model"],
                                    self.params["post_period_response"],
                                    self.params["alpha"])

        # Depending on input, dispatch to the appropriate Run* method()
        if self.data is not None:
            self._run_with_data(kwargs["data"], kwargs["pre_period"],
                                kwargs["post_period"], kwargs["model_args"],
                                kwargs["alpha"], self.params["estimation"])
        else:
            self._run_with_ucm(kwargs["ucm_model"],
                               kwargs["post_period_response"],
                               kwargs["alpha"], kwargs["model_args"],
                               self.params["estimation"])

    def _format_input_data(self, data):
        """Check and format the data argument provided to CausalImpact().

        Args:
            data: Pandas DataFrame

        Returns:
            correctly formatted Pandas DataFrame
        """
        # If <data> is a Pandas DataFrame and the first column is 'date',
        # try to convert

        if type(data) == pd.DataFrame and type(data.columns[0]) == str:
            if data.columns[0].lower() in ["date", "time"]:
                data = data.set_index(data.columns[0])

        # Try to convert to Pandas DataFrame
        try:
            data = pd.DataFrame(data)
        except PandasError:
            raise PandasError("could not convert input data to Pandas " +
                              "DataFrame")

        # Must have at least 3 time points
        if len(data.index) < 3:
            raise ValueError("data must have at least 3 time points")

        # Must not have NA in covariates (if any)
        if len(data.columns) >= 2:
            if np.any(pd.isnull(data.iloc[:, 1:])):
                raise ValueError("covariates must not contain null values")

        return data

    def _format_input_prepost(self, pre_period, post_period, data):
        """Check and format the pre_period and post_period input arguments.

        Args:
            pre_period: two-element list
            post_period: two-element list
            data: already-checked Pandas DataFrame, for reference only
        """
        import numpy as np
        import pandas as pd

        if pre_period is None or post_period is None:
            raise ValueError("pre_period and post period must not contain " +
                             "null values")
        if type(pre_period) is not list or type(post_period) is not list:
            raise ValueError("pre_period and post_period must bothe be lists")
        if len(pre_period) != 2 or len(post_period) != 2:
            raise ValueError("pre_period and post_period must both be of " +
                             "length 2")
        if np.any(pd.isnull(pre_period)) or np.any(pd.isnull(post_period)):
            raise ValueError("pre_period and post period must not contain " +
                             "null values")
        if isinstance(data.index, pd.tseries.index.DatetimeIndex):
            pre_period = [pd.to_datetime(date) for date in pre_period]
            post_period = [pd.to_datetime(date) for date in post_period]

        else:
            pre_dtype = np.array(pre_period).dtype
            post_dtype = np.array(post_period).dtype

            if data.index.dtype.kind != pre_dtype.kind or \
               data.index.dtype.kind != post_dtype.kind:
                if data.index.dtype == int:
                    pre_period = [int(elem) for elem in pre_period]
                    post_period = [int(elem) for elem in post_period]
                elif data.index.dtype == float:
                    pre_period = [float(elem) for elem in pre_period]
                    post_period = [float(elem) for elem in post_period]
                else:
                    raise ValueError("pre_period (" + pre_dtype.name +
                                     ") and post_period (" + post_dtype.name +
                                     ") should have the same class as the " +
                                     "time points in the data (" +
                                     data.index.dtype.name + ")")
        loc1 = data.index.get_loc(pre_period[0])
        loc2 = data.index.get_loc(pre_period[1])
        loc3 = data.index.get_loc(post_period[0])
        loc4 = data.index.get_loc(post_period[1])
        if loc2 - loc1 + 1 < 3:
            raise ValueError("pre_period must span at least 3 time points")
        if loc4 < loc3:
            raise ValueError("post_period[1] must not be earlier than " +
                             "post_period[0]")
        if loc3 < loc2:
            raise ValueError("post_period[0] must not be earlier than " +
                             "pre_period[1]")

        if pre_period[0] < data.index.min():
            print("Setting pre_period[1] to start of data: " +
                  str(data.index.min()))
            pre_period[0] = data.index.min()
        if pre_period[1] > data.index.max():
            print("Setting pre_period[1] to end of data: " +
                  str(data.index.max()))
            pre_period[1] = data.index.max()
        if post_period[1] > data.index.max():
            print("post_period[1] is out of bounds - Setting post_period[1] to"
                  " end of data:" + str(data.index.max()))
            post_period[1] = data.index.max()

        return {"pre_period": pre_period, "post_period": post_period}

    def _format_input(self, data, pre_period, post_period, model_args,
                      ucm_model, post_period_response, alpha):
        """Check and format all input arguments supplied to CausalImpact().
           See the documentation of CausalImpact() for details

        Args:
            data:                 Pandas DataFrame or data frame
            pre_period:           beginning and end of pre-period
            post_period:          beginning and end of post-period
            model_args:           dict of additional arguments for the model
            ucm_model:            UnobservedComponents model (instead of data)
            post_period_response: observed response in the post-period
            alpha:                tail-area for posterior intervals
            estimation:           method of estimation for model fitting

        Returns:
            list of checked (and possibly reformatted) input arguments
"""

        import numpy as np
        import pandas as pd

        # Check that a consistent set of variables has been provided
        args = [data, pre_period, post_period, ucm_model,
                post_period_response]

        data_model_args = [True, True, True, False, False]
        ucm_model_args = [False, False, False, True, True]

        if np.any(pd.isnull(args) != data_model_args) and \
           np.any(pd.isnull(args) != ucm_model_args):
            raise SyntaxError("must either provide data, pre_period, " +
                              "post_period, model_args or ucm_model" +
                              "and post_period_response")

        # Check <data> and convert to Pandas DataFrame, with rows
        # representing time points
        if data is not None:
            data = self._format_input_data(data)

        # Check <pre_period> and <post_period>
        if data is not None:
            checked = self._format_input_prepost(pre_period, post_period, data)
            pre_period = checked["pre_period"]
            post_period = checked["post_period"]

        # Parse <model_args>, fill gaps using <_defaults>

        _defaults = {"niter": 1000, "standardize_data": True,
                     "prior_level_sd": 0.01,
                     "nseasons": 1,
                     "season_duration": 1,
                     "dynamic_regression": False}

        if model_args is None:
            model_args = _defaults
        else:
            missing = [key for key in _defaults if key not in model_args]
            for arg in missing:
                model_args[arg] = _defaults[arg]

        """ Check only those parts of <model_args> that are used
            in this file The other fields will be checked in
            FormatInputForConstructModel()"""

        # Check <standardize_data>
        if type(model_args["standardize_data"]) != bool:
            raise ValueError("model_args.standardize_data must be a" +
                             "boolean value")

        """ Check <ucm_model> TODO
        if ucm_model is not None:
            if type(ucm_model) != ucm:
                raise ValueError("ucm_model must be an object of class \
                                 statsmodels_ucm")
        """

        # Check <post_period_response>
        if ucm_model is not None:
            if not is_list_like(post_period_response):
                raise ValueError("post_period_response must be list-like")
            if np.array(post_period_response).dtype.num == 17:
                raise ValueError("post_period_response should not be" +
                                 "datetime values")
            if not np.all(np.isreal(post_period_response)):
                raise ValueError("post_period_response must contain all" +
                                 "real values")

        # Check <alpha>
        if alpha is None:
            raise ValueError("alpha must not be None")
        if not np.isreal(alpha):
            raise ValueError("alpha must be a real number")
        if np.isnan(alpha):
            raise ValueError("alpha must not be NA")
        if alpha <= 0 or alpha >= 1:
            raise ValueError("alpha must be between 0 and 1")

        # Return updated arguments
        kwargs = {"data": data, "pre_period": pre_period,
                  "post_period": post_period, "model_args": model_args,
                  "ucm_model": ucm_model,
                  "post_period_response": post_period_response, "alpha": alpha}
        return kwargs

    def _run_with_data(self, data, pre_period, post_period, model_args, alpha,
                       estimation):
        # Zoom in on data in modeling range
        if data.shape[1] == 1:  # no exogenous values provided
            raise ValueError("data contains no exogenous variables")
        non_null = pd.isnull(data.iloc[:, 1]).nonzero()
        first_non_null = non_null[0]
        if first_non_null.size > 0:
            pre_period[0] = max(pre_period[0], data.index[first_non_null[0]])
        data_modeling = data.copy()
        df_pre = data_modeling.loc[pre_period[0]:pre_period[1], :]
        df_post = data_modeling.loc[post_period[0]:post_period[1], :]

        # Standardize all variables
        orig_std_params = (0, 1)
        if model_args["standardize_data"]:
            sd_results = standardize_all_variables(data_modeling, pre_period,
                                                   post_period)
            df_pre = sd_results["data_pre"]
            df_post = sd_results["data_post"]
            orig_std_params = sd_results["orig_std_params"]

        # Construct model and perform inference
        ucm_model = construct_model(self, df_pre, model_args)
        res = model_fit(self, ucm_model, estimation, model_args["niter"])

        inferences = compile_posterior_inferences(res, df_pre, df_post, None,
                                                  alpha, orig_std_params,
                                                  estimation)

        # "append" to 'CausalImpact' object
        self.inferences = inferences["series"]
        self.model = ucm_model

    def _run_with_ucm(self, ucm_model, post_period_response, alpha, model_args,
                      estimation):
        """ Runs an impact analysis on top of a ucm model.

           Args:
             ucm_model: Model as returned by UnobservedComponents(),
                        in which the data during the post-period was set to NA
             post_period_response: observed data during the post-intervention
                                   period
             alpha: tail-probabilities of posterior intervals"""
        # Guess <pre_period> and <post_period> from the observation vector
        # These will be needed for plotting period boundaries in plot().
        #raise NotImplementedError()
        data_modeling = ucm_model.data.orig_endog

        """
        try:
            indices = infer_period_indices_from_data(y)
        except ValueError:
            raise ValueError("ucm_model must have been fitted on data where " +
                             "the values in the post-intervention period " +
                             "have been set to NA")
        """
        df_pre = ucm_model.data.orig_endog[:-len(post_period_response)]
        df_pre = pd.DataFrame(df_pre)
        post_period_response = pd.DataFrame(post_period_response)
        orig_std_params = (0, 1)
        res = model_fit(self, ucm_model, estimation, model_args["niter"])
        # Compile posterior inferences
        inferences = compile_posterior_inferences(res, df_pre, None,
                                                  post_period_response, alpha,
                                                  orig_std_params, estimation)
        obs_inter = pre_len = res.model.nobs - len(post_period_response)
        self.params["pre_period"] = [0, obs_inter - 1]
        self.params["post_period"] = [obs_inter, -1]
        self.data = pd.concat([df_pre, post_period_response])
        self.inferences = inferences["series"]
        self.model = ucm_model

    def summary(self, output="summary"):
        if output == "summary":
            # Posterior inference {CausalImpact}
            post_period = self.params["post_period"]
            post_inf = self.inferences.loc[post_period[0]:post_period[1], :]
            post_point_resp = post_inf.loc[:, "response"]
            post_point_pred = post_inf.loc[:, "point_pred"]
            post_point_upper = post_inf.loc[:, "point_pred_upper"]
            post_point_lower = post_inf.loc[:, "point_pred_lower"]

            mean_resp = int(post_point_resp.mean())
            cum_resp = int(post_point_resp.sum())
            mean_pred = post_point_pred.mean()
            cum_pred = post_point_pred.sum()
            mean_lower = int(post_point_lower.mean())
            mean_upper = int(post_point_upper.mean())
            mean_ci = [mean_lower, mean_upper]
            cum_lower = int(post_point_lower.sum())
            cum_upper = int(post_point_upper.sum())
            cum_ci = [cum_lower, cum_upper]

            abs_effect = (post_point_resp - post_point_pred).mean()
            cum_abs_effect = (post_point_resp - post_point_pred).sum()
            abs_effect_lower = int((post_point_resp - post_point_lower).mean())
            abs_effect_upper = int((post_point_resp - post_point_upper).mean())
            abs_effect_ci = [abs_effect_lower, abs_effect_upper]
            cum_abs_lower = int((post_point_resp - post_point_lower).sum())
            cum_abs_upper = int((post_point_resp - post_point_upper).sum())
            cum_abs_effect_ci = [cum_abs_lower, cum_abs_upper]

            rel_effect = "{:.1f}%".format(abs_effect/mean_pred*100)
            cum_rel_effect = "{:.1f}%".format(cum_abs_effect/cum_pred * 100)
            rel_effect_lower = "{:.1f}%".format(abs_effect_lower/mean_pred*100)
            rel_effect_upper = "{:.1f}%".format(abs_effect_upper/mean_pred*100)
            rel_effect_ci = [rel_effect_lower, rel_effect_upper]
            cum_rel_effect_lower = cum_abs_lower/cum_pred*100
            cum_rel_effect_lower = "{:.1f}%".format(cum_rel_effect_lower)
            cum_rel_effect_upper = cum_abs_upper/cum_pred*100
            cum_rel_effect_upper = "{:.1f}%".format(cum_rel_effect_upper)
            cum_rel_effect_ci = [cum_rel_effect_lower, cum_rel_effect_upper]

            summary = [
                [mean_resp, cum_resp],
                [int(mean_pred), int(cum_pred)],
                [mean_ci, cum_ci],
                [" ", " "],
                [int(abs_effect), int(cum_abs_effect)],
                [abs_effect_ci, cum_abs_effect_ci],
                [" ", " "],
                [rel_effect, cum_rel_effect],
                [rel_effect_ci, cum_rel_effect_ci]
            ]
            summary = pd.DataFrame(summary, columns=["Average", "Cumulative"],
                               index=["Actual",
                                      "Predicted",
                                      "95% CI",
                                      " ",
                                      "Absolute Effect",
                                      "95% CI",
                                      " ",
                                      "Relative Effect",
                                      "95% CI"])
            print(summary)
        elif output == "report":
            pass
        else:
            raise ValueError("Output argument must be either 'summary' " +
                             "or 'report'")

    def plot(self, panels=["original", "pointwise", "cumulative"]):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(15, 12))

        data_inter = self.params["pre_period"][1]
        inferences = self.inferences.iloc[1:, :]
        # Observation and regression components
        if "original" in panels:
            ax1 = plt.subplot(3, 1, 1)
            plt.plot(inferences["point_pred"], 'r--', linewidth=2,
                     label='model')
            plt.plot(inferences["response"], 'k', linewidth=2, label="endog")

            plt.axvline(data_inter, c='k', linestyle='--')

            plt.fill_between(
                        inferences.index,
                        inferences["point_pred_lower"],
                        inferences["point_pred_upper"],
                        facecolor='gray', interpolate=True, alpha=0.25,
                    )
            plt.setp(ax1.get_xticklabels(), visible=False)
            plt.legend(loc='upper left')
            plt.title('Observation vs prediction')

        if "pointwise" in panels:
            # Pointwise difference
            if 'ax1' in locals():
                ax2 = plt.subplot(312, sharex=ax1)
            else:
                ax2 = plt.subplot(312)
            lift = inferences.point_effect
            plt.plot(lift, 'r--', linewidth=2)
            plt.plot(self.data.index, np.zeros(self.data.shape[0]), 'g-',
                     linewidth=2)
            plt.axvline(data_inter, c='k', linestyle='--')

            lift_lower = inferences.point_effect_lower
            lift_upper = inferences.point_effect_upper

            plt.fill_between(
                inferences.index,
                lift_lower,
                lift_upper,
                facecolor='gray', interpolate=True, alpha=0.25,
            )
            plt.setp(ax2.get_xticklabels(), visible=False)
            plt.title('Difference')

        # Cumulative impact
        if "cumulative" in panels:
            if 'ax1' in locals():
                ax3 = plt.subplot(313, sharex=ax1)
            elif 'ax2' in locals():
                ax3 = plt.subplot(313, sharex=ax2)
            else:
                ax3 = plt.subplot(313)
            plt.plot(
                inferences.index,
                inferences.cum_effect,
                'r--', linewidth=2,
            )

            plt.plot(self.data.index, np.zeros(self.data.shape[0]), 'g-',
                     linewidth=2)
            plt.axvline(data_inter, c='k', linestyle='--')

            plt.fill_between(
                inferences.index,
                inferences.cum_effect_lower,
                inferences.cum_effect_upper,
                facecolor='gray', interpolate=True, alpha=0.25,
            )
            plt.axis([inferences.index[0], inferences.index[-1], None,
                      None])

            ax3.set_xticklabels(inferences.index)
            plt.title('Cumulative Impact')
        plt.xlabel('$T$')
        plt.show()
