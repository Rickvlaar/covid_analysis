from frontend import app
import dutch_statistics as dutch
import graph_plotter
import datetime


def refresh_dutch_statistics():
    dutch.get_dutch_stats()
    dutch.calculate_dutch_daily_statistics()


def quick_caller(municipality=None, province=None):
    return graph_plotter.plot_statistics(
            data_set=dutch.sum_dutch_total_infections(municipality=municipality, province=province),
            start_date=datetime.date(2020, 7, 6),
            no_days_to_predict=7,
            linear_regres=True,
            exp_curve=True)


def quick_caller2():
    graph_plotter.plot_reproduction_no(data_set=dutch.get_daily_prevalence_numbers(),
                                       incubation_time=4,
                                       generational_interval=3,
                                       start_date=datetime.date(2020, 7, 1),
                                       end_date=datetime.date(2020, 9, 1),
                                       no_days_to_predict=7)
