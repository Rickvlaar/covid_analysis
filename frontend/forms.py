from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, BooleanField, HiddenField
from wtforms.validators import Optional
import datetime


class SelectionForm(FlaskForm):
    municipality = StringField('Municipality', [Optional()], default=None)
    province = StringField('Province', [Optional()], default=None)
    start_date = DateField('StartDate', [Optional()], default=datetime.date.today() - datetime.timedelta(days=14))
    end_date = DateField('EndDate', [Optional()], default=None)
    no_days_to_predict = IntegerField('DaysToPredict', [Optional()], default=7)
    linear_regres = BooleanField('LinearRegres', [Optional()], default=True)
    exp_curve = BooleanField('ExpCurve', [Optional()], default=True)
    submit = SubmitField('Plot!', [Optional()])


class UpdateStatsForm(FlaskForm):
    submit = SubmitField('Update Stats', [Optional()])
