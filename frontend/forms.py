from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, BooleanField, FloatField
from wtforms.validators import Optional
import datetime


class SelectionForm(FlaskForm):
    municipality = StringField('Municipality', [Optional()], default=None)
    province = StringField('Province', [Optional()], default=None)
    start_date = DateField('StartDate', [Optional()], default=datetime.date.today() - datetime.timedelta(days=14))
    end_date = DateField('EndDate', [Optional()], default=None)
    no_days_to_predict = IntegerField('DaysToPredict', [Optional()], default=7)
    linear_regres = BooleanField('LinearRegres', [Optional()], default=False)
    exp_curve = BooleanField('ExpCurve', [Optional()], default=True)
    plot_cases = BooleanField('PlotCases', [Optional()], default=True)
    plot_nice_hospitalised = BooleanField('PlotNiceHospitalised', [Optional()], default=False)
    plot_rivm_hospitalised = BooleanField('PlotRivmHospitalised', [Optional()], default=False)
    plot_deaths = BooleanField('PlotDeaths', [Optional()], default=False)
    submit = SubmitField('Plot!', [Optional()])


class ReproductionPlotForm(FlaskForm):
    start_date = DateField('StartDate', [Optional()], default=datetime.date(2020, 6, 12))
    end_date = DateField('EndDate', [Optional()], default=datetime.date.today() - datetime.timedelta(days=5))
    incubation_time = IntegerField('IncubationTime', [Optional()], default=4)
    generational_interval = FloatField('GenerationalInterval', [Optional()], default=3.86)
    generational_interval_stdev = FloatField('GenerationalIntervalStDev', [Optional()], default=2.65)
    submit = SubmitField('Plot!', [Optional()])


class UpdateStatsForm(FlaskForm):
    submit = SubmitField('Update Stats', [Optional()])
