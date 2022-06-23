import pandas as pd
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row, widgetbox
from bokeh.palettes import Category20_16
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs
from bokeh.layouts import column, row, WidgetBox

df = pd.read_csv("./data/covid_19_indonesia_time_series_all.csv")
df["Date"] = pd.to_datetime(df["Date"])
data = df[df["Location"].str.contains("Indonesia")==False]
data = data[['Date', 'Location', 'Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']]

lokasi = list(data.Location.unique())

col_list = list(data.columns)

def make_dataset(lokasi, feature):

    
    xs = []
    ys = []
    colors = []
    labels = []

    for i, lokasi in enumerate(lokasi):

        df = data[data['Location'] == lokasi].reset_index(drop = True)
        
        x = list(df['Date'])
        y = list(df[feature])
        
        xs.append(list(x))
        ys.append(list(y))

        colors.append(Category20_16[i])
        labels.append(lokasi)

    new_src = ColumnDataSource(data={'x': xs, 'y': ys, 'color': colors, 'label': labels})

    return new_src

def make_plot(src, feature):
    
    p = figure(plot_width = 700, plot_height = 400, 
            title = 'Covid19-Indonesia All Time Series',
            x_axis_label = 'Date', y_axis_label = 'Feature Selected')

    p.multi_line('x', 'y', color = 'color', legend_field = 'label', line_width = 2, source = src)
    
    tooltips = [
            ('Date','$x'),
            ('Total', '$y'),
           ]
    
    p.add_tools(HoverTool(tooltips=tooltips))

    return p

def update_country(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]

    
    new_src = make_dataset(lokasi_plot, feature_select.value)

    src.data.update(new_src.data)

def update_feature(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]
    
    feature = feature_select.value
    
    new_src = make_dataset(lokasi_plot, feature)

    src.data.update(new_src.data)

lokasi_selection = CheckboxGroup(labels=lokasi, active = [0])
lokasi_selection.on_change('active', update_country)

feature_select = Select(options = col_list[2:], value = 'Total Cases', title = 'Feature Select')
feature_select.on_change('value', update_feature)

initial_country = [lokasi_selection.labels[i] for i in lokasi_selection.active]

src = make_dataset(initial_country, feature_select.value)

p = make_plot(src, feature_select.value)

controls = WidgetBox(feature_select, lokasi_selection)

# Create a row layout
layout = row(controls, p)

#Adding the layout to the current document
curdoc().add_root(layout)
