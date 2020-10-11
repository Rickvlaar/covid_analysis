from sqlalchemy import Column, Integer, String, Date
from database import Base


class CountryStatistics(Base):
    __tablename__ = 'CountryStatistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, index=True)
    reported_date = Column(Date, index=True)
    infections = Column(Integer)
    hospitalised = Column(Integer)
    critical = Column(Integer)
    deaths = Column(Integer)


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


    def __repr__(self):
        return self.attributes()

    def __str__(self):
        return str(self.attributes())

    def attributes(self):
        return {key: value for key, value in self.__dict__.items() if key[:1] != '_'}
