from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base


class DutchIndividualCases(Base):
    __tablename__ = 'DutchIndividualCases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reported_date = Column(Date, index=True)
    statistic_date = Column(Date, index=True)
    hospitalised = Column(Boolean, index=True)
    deceased = Column(Boolean, index=True)
    sex = Column(String, index=True)
    municipal_health_service = Column(String)
    province = Column(String)
    age_group = Column(String)
    week_of_death = Column(Integer)

    def __repr__(self):
        return self.attributes()

    def __str__(self):
        return str(self.attributes())

    def attributes(self):
        return {key: value for key, value in self.__dict__.items() if key[:1] != '_'}

class DutchStatistics(Base):
    __tablename__ = 'DutchStatistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    province = Column(String, index=True)
    municipality = Column(String, index=True)
    city = Column(String, index=True)
    reported_date = Column(Date, index=True)
    cumulative_infections = Column(Integer)
    cumulative_hospitalised = Column(Integer)
    cumulative_hospitalised_nice = Column(Integer)
    cumulative_critical = Column(Integer)
    cumulative_deaths = Column(Integer)
    cumulative_recovered = Column(Integer)
    infections = Column(Integer)
    hospitalised = Column(Integer)
    hospitalised_nice_proven = Column(Integer)
    hospitalised_nice_suspected = Column(Integer)
    critical = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    prevalence_low = Column(Integer)
    prevalence_avg = Column(Integer)
    prevalence_high = Column(Integer)
    reproduction_no = Column(Integer)

    def __repr__(self):
        return self.attributes()

    def __str__(self):
        return str(self.attributes())

    def attributes(self):
        return {key: value for key, value in self.__dict__.items() if key[:1] != '_'}
