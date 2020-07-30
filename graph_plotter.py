from dutch_statistics import sum_dutch_total_infections as dutch_stats
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


def plot_statistics(start_date, no_days_to_predict):
    """
    Parameters
    ----------

    start_date: datetime.date
        date to start predicting e.g datetime.date(2020, 7, 30)
    no_days_to_predict: int, optional
        number of dates to predict in the future

    """
    statistics = dutch_stats()
    dates = []
    cases = []
    for stat in statistics:
        if stat[0] > start_date:
            dates.append(stat[0])
            cases.append(stat[1])

    dates = [datetime.date.toordinal(date) for date in dates]

    # Start predicting from that last day present the dates array
    if no_days_to_predict > 0:
        predicted_dates = []
        while no_days_to_predict != 0:
            predicted_dates.append(dates[0] + no_days_to_predict)
            no_days_to_predict -= 1

        slope, y0, r, p, stderr = stats.linregress(dates, cases)

        predicted_dates.extend(dates)
        dates = predicted_dates
        cases_expected = [y0 + slope * date for date in dates]

        extend_cases_by = len(cases_expected) - len(cases)
        temp_array = cases_expected[:extend_cases_by]
        temp_array.extend(cases)
        cases = temp_array
        plt.plot(predicted_dates, cases_expected, 'r', label='fitted line')

    plt.title('Cases over Time')
    plt.plot(dates, cases)
    plt.show()
