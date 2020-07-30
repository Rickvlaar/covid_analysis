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
    cumulative_critical = Column(Integer)
    cumulative_deaths = Column(Integer)
    infections = Column(Integer)
    hospitalised = Column(Integer)
    critical = Column(Integer)
    deaths = Column(Integer)

    def __repr__(self):
        return str(self.municipality) + ', ' + str(self.reported_date) + ', ' + str(self.deaths) + ', ' + \
               str(self.hospitalised) + ', ' + str(self.infections)

    def __str__(self):
        return str(self.municipality) + ', ' + str(self.reported_date) + ', ' + str(self.deaths) + ', ' + \
               str(self.hospitalised) + ', ' + str(self.infections)