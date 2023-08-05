from yearonequant.util_quant import *


class Factor:
    """Compute indicators to evaluate single factor.

    :param factor_df: a DataFrame of cross sectional factor values, stock in column
    :param price_df: a DataFrame of cross sectional stock price
    """

    def __init__(self, factor_df, price_df):

        self.factor_df = factor_df
        self.price_df = price_df
        self.ret_df = price_df / price_df.shift(1)

        self.performance_by_sets = None
        self.ic_indicator = None

    @staticmethod
    def get_rank_df(df, num_of_sets):
        """get rank row by row, group every row by sets,
            return a DataFrame of rank number
        :param num_of_sets number of sets to be grouped
        """

        rank_df = (df * np.array(0)).fillna(0)  # df of all 0
        rank_name = range(1, num_of_sets + 1)  # [1, 2, 3, ... ]

        # loop over row of df 
        for i in range(0, df.shape[0]):
            factor_series = df.iloc[i]  # the ith row
            # return a df of rank 
            rank_series = pd.qcut(factor_series, num_of_sets, labels=rank_name)
            rank_df.iloc[i] = rank_series

        return rank_df

    @staticmethod
    def get_ic(factor_df, price_df, interval, ic_type='rank'):
        """Return a series of IC value, respect to each time period
        :param factor_df DataFrame of factor values
        :param price_df DataFrame of return values
        :param interval list of intervals in concern
        :param ic_type type of ic, rank for spearman, normal for pearson
        """
        valid_type = ['rank', 'normal']
        if ic_type not in valid_type:
            print("Invalid IC type! Feasible input: ['rank', 'normal']")
            return

        ic_df = pd.DataFrame(np.nan, index=factor_df.index, columns=interval)

        for n in range(0, len(interval)):

            ic_series = pd.Series(np.nan, factor_df.index)
            ret_df = price_df / price_df.shift(interval[n]) - 1

            if ic_type == 'rank':

                for i in range(interval[n], factor_df.shape[0]):  # loop over rows

                    previous_factor = factor_df.iloc[i - interval[n]]
                    current_ret = ret_df.iloc[i]
                    data = pd.concat([previous_factor, current_ret], axis=1).dropna()
                    # first returned value is coefficient
                    ic = scipy.stats.spearmanr(data)[0]
                    ic_series[i] = ic

            elif ic_type == 'normal':

                for i in range(interval[n], factor_df.shape[0]):  # loop over rows

                    previous_factor = factor_df.iloc[i - interval[n]]
                    current_ret = ret_df.iloc[i]
                    data = pd.concat([previous_factor, current_ret], axis=1).dropna()

                    ic = scipy.stats.pearsonr(data.ix[:, 0], data.ix[:, 1])[0]
                    ic_series[i] = ic

            ic_df.iloc[:, n] = ic_series

        return ic_df

    def get_performance_of_factor(self, interval, window_size, ic_type='rank'):
        """Return a DataFrame of factor indicators
        :param interval list of interval in concern
        :param window_size: window size for moving average
        :param ic_type: can be normal or rank
        :return: DataFrame of factor's performance by set
        """

        ic = self.get_ic(self.factor_df, self.price_df, interval, ic_type)

        ic_ma = ic.rolling(window=window_size).mean()
        ic_std = ic.rolling(window=window_size).std()

        ir = ic_ma / ic_std

        ic_dp = pd.Panel({'information_coefficient': ic,
                          'rolling_mean_IC': ic_ma,
                          'rolling_std_IC': ic_std,
                          'information_ratio': ir})

        self.ic_indicator = ic_dp

        return ic_dp

    def quantile_returns(self, num_of_sets):
        """
        Return rate by set, column is set number, row is period
        :param num_of_sets number of sets
        """
        ret_of_sets = pd.DataFrame(np.nan, index=self.factor_df.index, columns=range(1, num_of_sets + 1))

        for i in range(1, len(self.factor_df)):

            # get factor data at t-1
            previous_factor = self.factor_df[i - 1:i].dropna(axis=1)

            if previous_factor.shape[1] > 0:
                # corresponding ranks at t-1, ascending
                previous_rank = previous_factor.rank(axis=1)
                # transform (1, n) dataframe to a (n, ) series,
                # therefor the output of pd.qcut() function will have indexes
                rank_series = pd.Series(previous_rank.values[0], index=previous_rank.columns)

                # label given data
                label = pd.qcut(x=rank_series, q=num_of_sets, labels=range(1, num_of_sets + 1))
                label.name = 'label'
                # get realized returns at t
                current_ret = self.ret_df[i:i + 1].dropna(axis=1)
                # eliminate the impact of external data, such as recent listed stocks
                labeled_data = pd.concat([current_ret.T, label], axis=1).dropna()

                # calculate returns for each set and update
                current_sets_ret = labeled_data.groupby(by='label').mean().T[:1]
                ret_of_sets.ix[current_sets_ret.index] = current_sets_ret

        return ret_of_sets

    def quantile_performance(self, num_of_sets):
        """
        Get performance of each set
        :param num_of_sets:
        :return:
        """

        quantile_ret = self.quantile_returns(num_of_sets)

        nv = pd.Series((quantile_ret + 1).cumprod()[-1:].values[0], index=quantile_ret.columns)
        mu = quantile_ret.mean()
        sigma = quantile_ret.std()
        sharpe = mu / sigma

        performance_df = pd.DataFrame({'Ending_NV': nv,
                                       'Mean_Return': mu,
                                       'Stdev': sigma,
                                       'Sharpe_Ratio': sharpe})

        performance_df = performance_df.T

        return performance_df

    # def get_contribution_coefficient(number_of_sets):
    #     """(last set's return - first set's return) / (last set's return - first set's return),
    #         numerator is grouped by factor, denominator is grouped by return
    #     """
    #     ret_of_sets_by_factor = self.get_ret_by_sets()

    #     # compute return of sets, where sets are grouped by return
    #     rank_of_ret = self.get_rank_df(self.ret_df, number_of_sets)
    #     ret_of_sets_by_return = pd.DataFrame()

    #     # loop over set number to get mean of each set
    #     for i in range(1, self.num_of_sets + 1):

    #         shifted_rank_of_ret = rank_of_ret.shift(1)  # shift down one row, ignore first NaN row of ret
    #         ret_of_sets_by_return[i] = np.mean(ret[shifted_rank_of_ret == i], axis = 1) - 1

    #     numerator = abs(ret_of_sets_by_factor[self.num_of_sets] - ret_of_sets_by_factor[1])
    #     denominator = abs(ret_of_sets_by_return[self.num_of_sets] - ret_of_sets_by_return[1])

    #     return numerator / denominator
