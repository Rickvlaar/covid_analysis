from scipy import stats, optimize
import matplotlib.pyplot as plt
import numpy as np
import datetime


def plot_statistics(data_set, start_date, no_days_to_predict, linear_regres=True, exp_curve=True):
    """
    Parameters
    ----------

    data_set: list of DutchStatistics
        pass data set containing statistics to plot
    start_date: datetime.date
        date to start predicting e.g datetime.date(2020, 7, 30)
    no_days_to_predict: int, optional
        number of dates to predict in the future
    linear_regres: boolean, optional
        defaults to true; add a linear regression line up to days to predict
    exp_curve: boolean, optional
        defaults to true; plots an exponential curve on the dataset

    """

    if no_days_to_predict > 0 and not exp_curve and not linear_regres:
        msg = 'Choose either exponential and/or linear prediction when using no_days_to_predict'
        raise RuntimeError(msg)

    # Convert the data set for use in the plotter
    statistics = data_set
    dates = []
    cases = []
    for stat in statistics:
        if stat[0] > start_date:
            dates.append(stat[0])
            cases.append(stat[1])
    # Convert dates to integers for easy calculations
    dates = np.linspace(1, len(dates), len(dates))
    dates = np.flip(dates)

    # Start predicting from that last day present the dates array
    predicted_dates = []
    if no_days_to_predict > 0:
        while no_days_to_predict != 0:
            predicted_dates.append(dates[0] + no_days_to_predict)
            no_days_to_predict -= 1
    predicted_dates.extend(dates)

    # Adds linear regression line to the plot
    if linear_regres:
        # Perform regression and calculate expected cases
        slope, y0, r, p, stderr = stats.linregress(dates, cases)
        cases_expected = [y0 + slope * date for date in predicted_dates]
        plt.plot(predicted_dates, cases_expected, 'r', label='fitted line')

    # Add an exponential curve to the plot
    if exp_curve:
        # Determine best fit for curve and add to plot
        test, bla = optimize.curve_fit(exponent, dates, cases)
        plt.plot(predicted_dates, exponent(np.array(predicted_dates), test[0], test[1]))

    # Finally show the plot
    plt.title('Cases over Time')
    plt.plot(dates, cases)
    plt.show()


def exponent(x, a, b):
    return a * np.exp(x*b)
