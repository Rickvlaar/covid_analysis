import dutch_statistics as dutch
import graph_plotter as graphs
import datetime


def refresh_dutch_statistics():
    dutch.get_dutch_stats()
    dutch.calculate_dutch_daily_statistics()
    dutch.sum_dutch_total_infections()
