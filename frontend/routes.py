from frontend import app, forms
from flask import render_template, redirect, url_for, session, request
import graph_plotter
import dutch_statistics
import main


@app.route('/', methods=['GET', 'POST'])
@app.route('/plot', methods=['GET', 'POST'])
def index():
    form = forms.SelectionForm()
    if not session.get('image_name'):
        session['image_name'] = 'test.png'

    if form.validate_on_submit():
        data_set = dutch_statistics.sum_dutch_total_infections(municipality=form.municipality.data,
                                                               province=form.province.data)

        session['image_name'] = graph_plotter.plot_statistics(
                data_set=data_set,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                no_days_to_predict=form.no_days_to_predict.data,
                linear_regres=form.linear_regres.data,
                exp_curve=form.exp_curve.data,
                plot_cases=form.plot_cases.data,
                plot_nice_hospitalised=form.plot_nice_hospitalised.data,
                plot_rivm_hospitalised=form.plot_rivm_hospitalised.data,
                plot_deaths=form.plot_deaths.data)
    return render_template('show_plots.html', form=form, image_name=session.get('image_name'))


@app.route('/reproduction_plotter', methods=['GET', 'POST'])
def reproduction_plotter():
    form = forms.ReproductionPlotForm()

    if not session.get('reproduction_image'):
        session['reproduction_image'] = 'Daily R.png'

    if form.validate_on_submit():
        session['reproduction_image'] = graph_plotter.plot_reproduction_no(
                data_set=dutch_statistics.get_infections_by_date(),
                incubation_time=form.incubation_time.data,
                generational_interval=form.generational_interval.data,
                generational_interval_stdev=form.generational_interval_stdev.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                no_days_to_predict=7)

    return render_template('reproduction_plotter.html', form=form, image_name=session.get('reproduction_image'))


@app.route('/update_stats', methods=['GET'])
def update_database():
    main.refresh_dutch_statistics()
    form = forms.SelectionForm()
    return render_template('show_plots.html', form=form, image_name=session.get('image_name'))
