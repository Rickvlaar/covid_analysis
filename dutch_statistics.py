import datetime
import callouts
from database import data_model, database_session
from database.data_model import DutchStatistics
from sqlalchemy.sql import func
from config import Endpoints


def get_dutch_stats():
    session = database_session()
    session.query(DutchStatistics).delete()
    rivm_statistics = callouts.get_covid_stats(Endpoints.RIVM_CUMULATIVE)
    for record in rivm_statistics:
        dutch_daily_stat = data_model.DutchStatistics(
                province=record['Province'],
                municipality=record['Municipality_name'],
                reported_date=datetime.date.fromisoformat(record['Date_of_report'][0:10]),
                cumulative_infections=record['Total_reported'],
                cumulative_hospitalised=record['Hospital_admission'],
                cumulative_deaths=record['Deceased'],
        )
        session.add(dutch_daily_stat)
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
    query = session.query(DutchStatistics.reported_date, func.sum(DutchStatistics.infections),
                                 func.sum(DutchStatistics.hospitalised),
                                 func.sum(DutchStatistics.deaths)).group_by(DutchStatistics.reported_date).order_by(
            DutchStatistics.reported_date.desc())

    if municipality:
        query = query.filter_by(municipality=municipality)

    if province:
        query = query.filter_by(province=province)

    dutch_totals = query.all()
    return dutch_totals
