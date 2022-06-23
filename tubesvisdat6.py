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
            x_axis_label = 'date', y_axis_label = 'Feature Selected')

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

feature_select = Select(options = col_list[2:], value = 'Total Cases', title = 'Feature 1')
feature_select.on_change('value', update_feature)


initial_country = [lokasi_selection.labels[i] for i in lokasi_selection.active]

src = make_dataset(initial_country, feature_select.value)

p = make_plot(src, feature_select.value)

controls = WidgetBox(feature_select, lokasi_selection)

# Create a row layout
layout = row(controls, p)

#Adding the layout to the current document
curdoc().add_root(layout)


#=============================================================
data2 = pd.read_csv("./data/covid_19_indonesia_time_series_all.csv")
df2 = data[['continent','location','date','total_cases','new_cases','total_deaths','new_deaths']]
df2['total_cases'].fillna(0,inplace=True)
df2['new_cases'].fillna(0,inplace=True)
df2['total_deaths'].fillna(0,inplace=True)
df2['new_deaths'].fillna(0,inplace=True)

df_asia = df[df['continent'] == 'Asia']
df_asia['location'].unique()
df_asia.drop(columns='continent',inplace=True)
df_indo = df_asia[df_asia['location'] == 'Indonesia']

df_select = df_asia[df_asia['location'] == 'Indonesia']
df_select2 = df_asia[df_asia['location'] == 'Malaysia']

#Membuat source data untuk plotting data
source1 = ColumnDataSource(data={
    'x' : df_select['date'],
    'y' : df_select['new_cases'],
    
})
source2 = ColumnDataSource(data={
    'x' : df_select2['date'],
    'y' : df_select2['new_cases'],
})


#Mengatur Figure gambar
fig_gambar = figure(title='Data Covid-19 di Asia',
                   plot_height=550, plot_width=1000,
                   x_axis_type = 'datetime',
                   x_axis_label='Date', y_axis_label='Jumlah Orang',
                   tools=['pan', 'wheel_zoom', 'save', 'reset'])

#Negara 1
fig_gambar.line(x='x', y='y',
              color='coral',
              line_width=2,
              source=source1,
              legend_label ='Negara 1')

#Negara 2
fig_gambar.line(x='x', y='y',
              color='cornflowerblue',
              line_width=2,
              source=source2,
              legend_label = 'Negara 2')

#Lokasi & Fitur Legend
fig_gambar.legend.location = 'top_left'
fig_gambar.legend.click_policy = 'mute'

#Menambahkan Hover
fig_gambar.add_tools(HoverTool(tooltips=[
                                ('Date','@x{%F}'),
                                ('new_cases', '@y')
                               ],formatters={'@x': 'datetime'},
                               mode='vline'))

def update_plot(attr, old, new):
    #Mengambil pilihan data Negara
    pilihan1 = select1.value
    pilihan3 = select3.value
    
    #Mengambil pilihan Negara
    pilihan0 = select0.value
    pilihan2 = select2.value
    
    #Membuat data berdasarkan pilihan negara
    df_select = df_asia[df_asia['location'] == pilihan0]
    df_select2 = df_asia[df_asia['location'] == pilihan2]
    
    #Membuat data baru berdasarkan pilihan
    new_source1 = {
        'x' : df_select['date'],
        'y' : df_select[pilihan1]
    }
    new_source2 = {
        'x' : df_select2['date'],
        'y' : df_select2[pilihan3]
    }
    
    #Memasukan data baru ke source plot
    source1.data = new_source1
    source2.data = new_source2

def updateNegara_plot(attr, old, new):
    #Mengambil pilihan data Negara
    pilihan0 = select0.value
    pilihan2 = select2.value

    #Membuat data berdasarkan pilihan negara
    df_select = df_asia[df_asia['location'] == pilihan0]
    df_select2 = df_asia[df_asia['location'] == pilihan2]
    
    #Membuat data baru berdasarkan pilihan
    new_source1 = {
        'x' : df_select['date'],
        'y' : df_select['new_cases']
    }
    new_source2 = {
        'x' : df_select2['date'],
        'y' : df_select2['new_cases']
    }
    
    #Memasukan data baru ke source plot
    source1.data = new_source1
    source2.data = new_source2


#Pilihan pada Select berupa List Seluruh Negara
#Membuat pilihan Negara
option0 = df_asia['location'].unique().tolist()

#Membuat pilihan data Negara
option1 = df_indo.columns.to_list()
del option1[0]
del option1[0]

##Menu pilihan Negara 1
#Select0 untuk memilih Negara 1
select0 = Select(
    options = option0,
    title = 'Pilih Negara 1',
    value = 'Indonesia'
)

#Select1 untuk memilih data Negara 1
select1 = Select(
    options = option1,
    title = 'Pilih Data Negara 1',
    value = 'new_cases'
)

##Menu pilihan Negara 2
#Select2 untuk memilih Negara 2
select2 = Select(
    options = option0,
    title = 'Pilih Negara 2',
    value = 'Malaysia'
)

#Select3 untuk memilih data Negara 2
select3 = Select(
    options = option1,
    title = 'Pilih Data Negara 2',
    value = 'new_cases'
) 

#Jika select dipilih
select0.on_change('value', updateNegara_plot)
select1.on_change('value', update_plot)
select2.on_change('value', updateNegara_plot)
select3.on_change('value', update_plot)


#Membuat layout gambar
layout = row(widgetbox(select0,select1,select2,select3), fig_gambar)

#Membuat Panel gambar
panel1 = Panel(child=layout, title='Visualisasi Perbandingan Data Covid-19')

#Membuat Tabel dengan Panel yang ada
tabs = Tabs(tabs=[panel1,])

curdoc().add_root(tabs)


#====================================================================
