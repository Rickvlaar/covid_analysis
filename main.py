from frontend import app
import dutch_statistics as dutch
import graph_plotter
import datetime
import util


def refresh_dutch_statistics():
    util.refresh_data_files()
    dutch.get_rivm_stats()
    dutch.get_nice_stats()
    dutch.get_individual_cases_stats()
    dutch.calculate_dutch_daily_statistics()


def quick_caller(municipality=None, province=None):
    return graph_plotter.plot_statistics(
            data_set=dutch.sum_dutch_total_infections(municipality=municipality, province=province),
            start_date=datetime.date(2020, 7, 6),
            no_days_to_predict=7,
            linear_regres=True,
            exp_curve=True)


def quick_caller2():
    graph_plotter.plot_reproduction_no(data_set=dutch.sum_dutch_total_infections(None, None),
                                       incubation_time=5,
                                       generational_interval=3.95,
                                       start_date=datetime.date(2020, 10, 1),
                                       end_date=datetime.date(2020, 10, 30),
                                       no_days_to_predict=7)
