import dutch_statistics as dutch
import graph_plotter
import datetime


def refresh_dutch_statistics():
    dutch.get_dutch_stats()
    dutch.calculate_dutch_daily_statistics()


def quick_caller():
    graph_plotter.plot_statistics(data_set=dutch.sum_dutch_total_infections(None), start_date=datetime.date(2020, 7, 5),
                                  no_days_to_predict=7)
