import datetime
import callouts
from database import data_model, database_session
from database.data_model import DutchStatistics
from sqlalchemy.sql import func
from config import Endpoints


def get_rivm_stats():
    session = database_session()
    session.query(DutchStatistics).delete()
    rivm_cumulative = callouts.get_covid_stats(Endpoints.RIVM_CUMULATIVE)
    rivm_prevalence = callouts.get_covid_stats(Endpoints.RIVM_PREVALENCE)
    prevalence_dict = {datetime.date.fromisoformat(record['Date']): record for record in rivm_prevalence}
    for record in rivm_cumulative:
        reported_date = datetime.date.fromisoformat(record['Date_of_report'][0:10])
        dutch_daily_stat = data_model.DutchStatistics(
                province=record['Province'],
                municipality=record['Municipality_name'],
                reported_date=reported_date,
                cumulative_infections=record['Total_reported'],
                cumulative_hospitalised=record['Hospital_admission'],
                cumulative_deaths=record['Deceased']
        )
        related_record = prevalence_dict.get(reported_date)
        if related_record:
            dutch_daily_stat.prevalence_low = related_record['prev_low']
            dutch_daily_stat.prevalence_avg = related_record['prev_avg']
            dutch_daily_stat.prevalence_high = related_record['prev_up']
        session.add(dutch_daily_stat)
    session.commit()
    session.close()


def get_nice_stats():
    """
    NICE daily intake data consists of two arrays:
        the first array contains proven covid cases
        the second array contains suspected covid cases
    """
    session = database_session()
    query = session.query(DutchStatistics).order_by(DutchStatistics.reported_date.desc())
    all_stats = query.all()

    nice_daily_intake = callouts.get_covid_stats(Endpoints.NICE_DAILY_INTAKE)
    nice_intake_cumulative = callouts.get_covid_stats(Endpoints.NICE_CUMULATIVE_INTAKE)

    daily_proven_dict = {datetime.date.fromisoformat(stat.get('date')): stat.get('value') for stat in
                         nice_daily_intake[0]}
    daily_suspected_dict = {datetime.date.fromisoformat(stat.get('date')): stat.get('value') for stat in
                            nice_daily_intake[1]}
    nice_intake_cumulative_dict = {datetime.date.fromisoformat(stat.get('date')): stat.get('value') for stat in
                                   nice_intake_cumulative}

    for record in all_stats:
        record.hospitalised_nice_proven = daily_proven_dict.get(record.reported_date)
        record.hospitalised_nice_suspected = daily_suspected_dict.get(record.reported_date)
        record.cumulative_hospitalised_nice = nice_intake_cumulative_dict.get(record.reported_date)

    session.commit()
    session.close()


def calculate_dutch_daily_statistics():
    session = database_session()
    dutch_cumu_stats = session.query(DutchStatistics).order_by(DutchStatistics.municipality).order_by(
            DutchStatistics.id).all()

    index = 0
    for record in dutch_cumu_stats:
        yesterday_record = dutch_cumu_stats[index - 1]
        if index > 0 and record.municipality is not None and record.municipality == yesterday_record.municipality:
            record.infections = record.cumulative_infections - yesterday_record.cumulative_infections
            record.deaths = record.cumulative_deaths - yesterday_record.cumulative_deaths
            record.hospitalised = record.cumulative_hospitalised - yesterday_record.cumulative_hospitalised
        else:
            record.infections = 0
            record.deaths = 0
            record.hospitalised = 0
        index += 1

    no_municipality_records = session.query(DutchStatistics).filter_by(municipality=None).order_by(
            DutchStatistics.province).order_by(
            DutchStatistics.id).all()

    index = 0
    for record in no_municipality_records:
        yesterday_record = no_municipality_records[index - 1]
        if index > 0 and record.province == yesterday_record.province:
            record.infections = record.cumulative_infections - yesterday_record.cumulative_infections
            record.deaths = record.cumulative_deaths - yesterday_record.cumulative_deaths
            record.hospitalised = record.cumulative_hospitalised - yesterday_record.cumulative_hospitalised
        else:
            record.infections = 0
            record.deaths = 0
            record.hospitalised = 0
        index += 1

    session.commit()
    session.close()


def sum_dutch_total_infections(municipality, province):
    session = database_session()
    query = session.query(DutchStatistics.reported_date,
                          func.sum(DutchStatistics.infections),
                          func.sum(DutchStatistics.hospitalised),
                          func.sum(DutchStatistics.deaths),
                          DutchStatistics.hospitalised_nice_proven) \
        .group_by(DutchStatistics.reported_date) \
        .order_by(DutchStatistics.reported_date.desc())

    if municipality:
        query = query.filter_by(municipality=municipality)

    if province:
        query = query.filter_by(province=province)

    dutch_totals = query.all()

    session.close()
    return dutch_totals


def get_daily_prevalence_numbers():
    session = database_session()
    query = session.query(DutchStatistics.reported_date,
                          DutchStatistics.prevalence_avg) \
        .group_by(DutchStatistics.reported_date) \
        .order_by(DutchStatistics.reported_date.desc())
    average_prevalence = query.all()

    session.close()
    return average_prevalence
