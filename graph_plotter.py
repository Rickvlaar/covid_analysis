from scipy import stats, optimize
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


def plot_statistics(data_set, start_date, no_days_to_predict, linear_regres=True, exp_curve=True):
    """
    Parameters
    ----------
    data_set: list of DutchStatistics
        pass data set containing statistics to plot
    start_date: datetime.date
        date to start plotting the data e.g datetime.date(2020, 7, 30)
    no_days_to_predict: int, optional
        number of dates to predict in the future
    linear_regres: boolean, optional
        defaults to true; add a linear regression line up to days to predict
    exp_curve: boolean, optional
        defaults to true; plots an exponential curve on the dataset

    :return:
    Plots a graph with measured cases and optionaly adds statistical prediction
    """

    if no_days_to_predict > 0 and not exp_curve and not linear_regres:
        msg = 'Choose either exponential and/or linear prediction when using no_days_to_predict'
        raise RuntimeError(msg)

    # Convert the data set for use in the plotter
    statistics = data_set
    dates = []
    cases = []
    for stat in statistics:
        if stat[0] >= start_date:
            dates.append(stat[0])
            cases.append(stat[1])

    # Convert dates to integers for easy calculations
    dates = mdates.date2num(dates)

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
        plt.plot(predicted_dates, cases_expected, color='green', label='linear regression')

    # Add an exponential curve to the plot
    if exp_curve:
        def exponent(x, a, b):
            return a * np.exp(x * b)

        # convert for calculation
        calc_range = np.linspace(start=1, stop=len(dates), num=len(dates))
        calc_range = np.flip(calc_range)

        predict_range = np.linspace(start=1, stop=len(predicted_dates), num=len(predicted_dates))
        predict_range = np.flip(predict_range)

        # Determine best fit for curve and add to plot, include standard deviation
        popt, pcov = optimize.curve_fit(exponent, calc_range, cases)
        perr = np.sqrt(np.diag(pcov))

        prediction_low = exponent(np.array(predict_range), popt[0] - perr[0], popt[1] - perr[1])
        prediction_optimum = exponent(np.array(predict_range), popt[0], popt[1])
        prediction_high = exponent(np.array(predict_range), popt[0] + perr[0], popt[1] + perr[1])

        # Plot the optimum as line and the rest as area
        plt.plot(predicted_dates, prediction_optimum, color='blue', label='curve fit')
        plt.gca().fill_between(predicted_dates, prediction_low, prediction_high, alpha=0.2)

    # Plot final results
    plt.title('Cases over Time')
    plt.plot(dates, cases, color='red', label='positive tests')

    # Tweak the output
    fig = plt.gcf()
    ax = plt.gca()

    # Convert dates to legible format and show grid on day level
    days = mdates.DayLocator()
    fmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_formatter(fmt)
    fig.autofmt_xdate(rotation=45, which='both')
    plt.grid(True, which='both')

    # Set ticks on y axis
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(25))

    # Show values for predictions and latest count
    ax.annotate(str(cases[0]), xy=(dates[0], cases[0]))

    # Other tweaks for the graph
    plt.xlim(left=start_date, right=predicted_dates[0])
    plt.ylim(bottom=0)
    fig.set_size_inches(12, 8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()
    # Finally show the plot
    fig.savefig('frontend/static/test.png')
    return fig


def cases_per_municipality(data_set, start_date):
    """
    Parameters
    ----------
    data_set: list of DutchStatistics
        pass data set containing statistics to plot
    start_date: datetime.date
        date to start plotting the data e.g datetime.date(2020, 7, 30)

    :return:
    stack-bar plot of cases per municipality. A.K.A The guilt-chart
    """

