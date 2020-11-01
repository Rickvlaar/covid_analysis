from datetime import date
from scipy import stats, optimize
import dutch_statistics
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
import random

# Prevent GUI from being triggered which causes crashes
matplotlib.use('agg')


def plot_statistics(data_set, start_date=date.min, end_date=date.max, no_days_to_predict=0, linear_regres=True,
                    exp_curve=True, plot_cases=True, plot_nice_hospitalised=False, plot_rivm_hospitalised=False,
                    plot_deaths=False):
    """
    Parameters
    ----------
    data_set: list of DutchStatistics
        pass data set containing statistics to plot
    start_date: datetime.date, optional
        date to start plotting the data e.g datetime.date(2020, 7, 30)
    no_days_to_predict: int, optional
        number of dates to predict in the future
    end_date: datetime.date, optional
        defaults to infinity; date to end the plot, useful for date ranges
    linear_regres: boolean, optional
        defaults to true; add a linear regression line up to days to predict
    exp_curve: boolean, optional
        defaults to true; plots an exponential curve on the dataset

    :return:
    Plots a graph with measured cases and optionally adds statistical prediction
    """

    if no_days_to_predict > 0 and not exp_curve and not linear_regres:
        msg = 'Choose either exponential and/or linear prediction when using no_days_to_predict'
        raise RuntimeError(msg)

    dates, cases, hospitalised, deaths, hospitalised_nice, predicted_dates = prepare_data_for_graph(data_set,
                                                                                                    start_date,
                                                                                                    end_date,
                                                                                                    no_days_to_predict)

    # Adds linear regression line to the plot
    if linear_regres:
        # Perform regression and calculate expected cases
        slope, y0, r, p, stderr = stats.linregress(dates, cases)
        cases_expected = [y0 + slope * date for date in predicted_dates]
        plt.plot(predicted_dates, cases_expected, color='green', label='linear regression')

    # Add an exponential curve to the plot
    if exp_curve:
        if plot_cases:
            add_curve_to_plot(dates=dates, predicted_dates=predicted_dates, cases=cases, color='blue')
        if plot_rivm_hospitalised:
            add_curve_to_plot(dates=dates, predicted_dates=predicted_dates, cases=hospitalised, color='teal')
        if plot_nice_hospitalised:
            add_curve_to_plot(dates=dates, predicted_dates=predicted_dates, cases=hospitalised_nice, color='purple')
        if plot_deaths:
            add_curve_to_plot(dates=dates, predicted_dates=predicted_dates, cases=deaths, color='brown')

    # Plot final results
    plt.title('Cases over Time')
    if plot_cases:
        plt.plot(dates, cases, color='red', label='positive tests')
    if plot_rivm_hospitalised:
        plt.plot(dates, hospitalised, color='orange', label='hospitalised - RIVM')
    if plot_nice_hospitalised:
        plt.plot(dates, hospitalised_nice, color='purple', label='hospitalised - NICE')
    if plot_deaths:
        plt.plot(dates, deaths, color='grey', label='deaths')

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
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(250))

    # ax.yaxis.set_major_locator(ticker.MultipleLocator(25))

    # Show values for predictions and latest count
    if plot_cases:
        ax.annotate(str(cases[0]), xy=(dates[0], cases[0]))
    if plot_rivm_hospitalised:
        ax.annotate(str(hospitalised[0]), xy=(dates[0], hospitalised[0]))
    if plot_nice_hospitalised:
        ax.annotate(str(deaths[0]), xy=(dates[0], deaths[0]))
    if plot_deaths:
        ax.annotate(str(hospitalised_nice[0]), xy=(dates[0], hospitalised_nice[0]))

    # Other tweaks for the graph
    plt.xlim(left=start_date, right=predicted_dates[0])
    plt.ylim(bottom=0)
    fig.set_size_inches(10, 8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    # Store the image
    random_image_name = str(random.randint(1000000, 9999999)) + '.png'
    fig.savefig('frontend/static/' + random_image_name, bbox_inches='tight')
    plt.close()
    return random_image_name


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


def plot_reproduction_no(data_set, incubation_time=5.2, generational_interval=3.9, start_date=date.min,
                         end_date=date.max,
                         no_days_to_predict=0):
    """
    Parameters
    ----------
    data_set: list of DutchStatistics
        pass data set containing statistics to plot
    incubation_time: decimal, optional
        time in days from infection to disease in order to calculate Re
    generational_interval: decimal, optional
        time in days between generations
    start_date: datetime.date, optional
        date to start plotting the data e.g datetime.date(2020, 7, 30)
    end_date: datetime.date, optional
        defaults to infinity; date to end the plot, useful for date ranges
    no_days_to_predict: int, optional
        number of dates to predict in the future

    :return:
    Plots Re as it changes over time
    """

    dates, cases, hospitalised, deaths, hospitalised_nice, predicted_dates = prepare_data_for_graph(data_set,
                                                                                                    start_date,
                                                                                                    end_date,
                                                                                                    no_days_to_predict)

    rep_no_list = []
    index = 0
    while index <= len(dates) - (incubation_time + 1):
        # calculate growth rate
        calculate_to = index + incubation_time
        popt, pcov, perr = curve_fit_cases(dates[index:calculate_to], cases[index:calculate_to])

        # Calculate reproduction number and add to plot, formula: R=exp(rTc)
        # r = growth_rate
        # Tc = generational_interval
        growth_rate = (exponent(1, popt[0], popt[1]) / exponent(0, popt[0], popt[1])) - 1
        reproduction_no = round(
                np.exp((growth_rate * generational_interval) - (0.5 * (growth_rate ** 2) * (3.8 ** 2))),
                2)

        rep_no_list.append(reproduction_no)
        index += 1

    # Calculate the moving average
    rep_no_series = pd.Series(rep_no_list)
    windows = rep_no_series.rolling(window=5)
    rep_no_list_moving_avg = windows.mean()
    rep_no_list_moving_avg = rep_no_list_moving_avg[3:]

    # Tweak the output
    fig = plt.gcf()
    ax = plt.gca()

    # Convert dates to legible format and show grid on day level
    days = mdates.DayLocator()
    fmt = mdates.DateFormatter('%Y-%m-%d')
    # ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_formatter(fmt)
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    fig.autofmt_xdate(rotation=45, which='both')

    plt.ylim(bottom=0, top=2)
    plt.grid(True, which='both')

    # Add the RIVM reproduction numbers
    rivm_stats = dutch_statistics.get_daily_reproduction_number()
    rivm_rep_no_list = []
    for stat in rivm_stats:
        if end_date >= stat[0] >= start_date:
            rivm_rep_no_list.append(stat[1])
    rivm_rep_no_list = rivm_rep_no_list[incubation_time:]

    end_date_index = len(dates) - incubation_time
    # plt.plot(dates[0:end_date_index], rep_no_list, color='orange', label='Daily Re')
    plt.plot(dates[0:end_date_index], rivm_rep_no_list, color='red', label='Daily Re - RIVM')
    plt.plot(dates[0:end_date_index-3], rep_no_list_moving_avg, color='blue', label='Daily Re - 5 Day Moving Avg')
    # for rep_date, rep_no in zip(dates[0:end_date_index], rep_no_list_moving_avg):
    #     ax.annotate(round(rep_no, 2), xy=(rep_date, rep_no + 0.1), horizontalalignment='center',
    #                 verticalalignment='bottom', rotation=45)

    # Set ticks on y axis
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

    fig.set_size_inches(14, 10)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    # Plot the optimum as line and the rest as area
    fig.savefig('frontend/static/Daily R.png', bbox_inches='tight')


def prepare_data_for_graph(data_set, start_date=date.min, end_date=date.max, no_days_to_predict=0):
    """
    Parameters
    ----------
    data_set: list of DutchStatistics
        pass data set containing statistics to plot
    start_date: datetime.date, optional
        date to start plotting the data e.g datetime.date(2020, 7, 30)
    end_date: datetime.date, optional
        defaults to infinity; date to end the plot, useful for date ranges
    no_days_to_predict: int, optional
        number of dates to predict in the future

    :return:
    dates: list matplotlib.dates
        the original dates converted for use in matplotlib
    cases: list integer
        list of proven cases
    predicted_dates: list matplotlib.dates
        list of dates used for prediction purposes

    """

    # None value should default to max
    if not end_date:
        end_date = date.max

    # Convert the data set for use in the plotter
    statistics = data_set
    dates = []
    cases = []
    hospitalised = []
    deaths = []
    hospitalised_nice = []
    for stat in statistics:
        if end_date >= stat[0] >= start_date:
            dates.append(stat[0])
            cases.append(stat[1])
            hospitalised.append(stat[2])
            deaths.append(stat[3])
            hospitalised_nice.append(stat[4])

    # Convert dates to integers for easy calculations
    dates = mdates.date2num(dates)

    # Start predicting from that last day present the dates array
    predicted_dates = []
    if no_days_to_predict > 0:
        while no_days_to_predict != 0:
            predicted_dates.append(dates[0] + no_days_to_predict)
            no_days_to_predict -= 1
    predicted_dates.extend(dates)

    return dates, cases, hospitalised, deaths, hospitalised_nice, predicted_dates


def curve_fit_cases(dates, cases):
    # convert for calculation
    calc_range = np.linspace(start=1, stop=len(dates), num=len(dates))
    calc_range = np.flip(calc_range)

    # Determine best fit for curve and add to plot, include standard deviation
    popt, pcov = optimize.curve_fit(exponent, calc_range, cases)
    perr = np.sqrt(np.diag(pcov))

    return popt, pcov, perr


def exponent(x, a, b):
    return a * np.exp(x * b)


def add_curve_to_plot(dates, predicted_dates, cases, color):
    popt, pcov, perr = curve_fit_cases(dates, cases)

    # If the popt is too close to linearity, the plot fails, so skip it
    if 0.999 <= popt[0] >= 1.001:
        predict_range = np.linspace(start=1, stop=len(predicted_dates), num=len(predicted_dates))
        predict_range = np.flip(predict_range)

        prediction_low = exponent(np.array(predict_range), popt[0] - perr[0], popt[1] - perr[1])
        prediction_optimum = exponent(np.array(predict_range), popt[0], popt[1])
        prediction_high = exponent(np.array(predict_range), popt[0] + perr[0], popt[1] + perr[1])

        # Calculate reproduction number and add to plot
        growth_factor = round(exponent(1, popt[0], popt[1]) / exponent(0, popt[0], popt[1]), 2)
        # Plot the optimum as line and the rest as area
        plt.plot(predicted_dates, prediction_optimum, color=color, label='growth factor - ' + str(growth_factor))
        plt.gca().fill_between(predicted_dates, prediction_low, prediction_high, alpha=0.2, color=color)
