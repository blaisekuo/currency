import requests     # 2.18.4
import pandas as pd # 0.23.0
import io
from datetime import datetime

from bokeh.plotting import figure, output_file, output_notebook, show, save
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Panel, Tabs

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models import DatetimeTickFormatter
from math import pi

#from numpy import pi, arange, sin, linspace
import numpy as np

#import pandas as pd

today=datetime.today().strftime('%Y-%m-%d')

# Building blocks for the URL
entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/' # Using protocol 'https'
resource = 'data'           # The resource for data queries is always'data'
flowRef ='EXR'              # Dataflow describing the data that needs to be returned, exchange rates in this case
keyaud = 'D.AUD.EUR.SP00.A'    # Defining the dimension values, explained below
keyusd = 'D.USD.EUR.SP00.A'    # Defining the dimension values, explained below
keyphp = 'D.PHP.EUR.SP00.A'    # Defining the dimension values, explained below

# Define the parameters
parameters = {
    'startPeriod': '2019-11-30',  # Start date of the time series
    #'endPeriod': '2020-08-07'     # End of the time series
    'endPeriod': today 
}

# Construct the URL: https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.CHF.EUR.SP00.A
request_url = entrypoint + resource + '/'+ flowRef + '/' + keyaud

# Make the HTTP request
responseaud = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})
# Check if the response returns succesfully with response code 200
print(responseaud)

request_url = entrypoint + resource + '/'+ flowRef + '/' + keyusd

# Make the HTTP request
responseusd = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})
# Check if the response returns succesfully with response code 200
#print(responseusd)

request_url = entrypoint + resource + '/'+ flowRef + '/' + keyphp

# Make the HTTP request
responsephp = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})
# Check if the response returns succesfully with response code 200
#print(responsephp)


# Print the full URL
#print(responseaud.url)

# Read the response as a file into a Pandas DataFrame
dfaud = pd.read_csv(io.StringIO(responseaud.text))
dfusd = pd.read_csv(io.StringIO(responseusd.text))
dfphp = pd.read_csv(io.StringIO(responsephp.text))

tsaud = dfaud.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
tsaud['TIME_PERIOD'] = pd.to_datetime(tsaud['TIME_PERIOD'])
curdatadateaud=np.array(tsaud['TIME_PERIOD'].values)
curdataaud=np.array(tsaud['OBS_VALUE'].values)

tsusd = dfusd.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
tsusd['TIME_PERIOD'] = pd.to_datetime(tsusd['TIME_PERIOD'])
curdatadateusd=np.array(tsusd['TIME_PERIOD'].values)
curdatausd=np.array(tsusd['OBS_VALUE'].values)

tsphp= dfphp.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
tsphp['TIME_PERIOD'] = pd.to_datetime(tsphp['TIME_PERIOD'])
curdatadatephp=np.array(tsphp['TIME_PERIOD'].values)
curdataphp=np.array(tsphp['OBS_VALUE'].values)

tab=[]

output_file("index.html",title="Forex Rate")

amount=1
amount2=1000

    #xptoi=sg_dict[i]
    #yptoi=sin(xptoi*2*pi)

source = ColumnDataSource(data={
    'x'      : curdatadateusd,
    'p2u'    : amount*curdataphp/curdatausd,
#    'rp2u'    : curdataphp/curdatausd,
    'p2a'    : amount*curdataphp/curdataaud,
#    'rp2a'    : curdataphp/curdataaud,
    'u2p'    : amount2*curdatausd/curdataphp,
#    'ru2p'    : curdatausd/curdataphp,
    'a2p'    : amount2*curdataaud/curdataphp,
#    'ra2p'    : curdataaud/curdataphp
})

#source = ColumnDataSource(dict(phase=xptoi.flatten()))

#columns = [TableColumn(field="phase", title="Phase")]
    
    #data_table = DataTable(source=source, columns=columns, width=150, height=600)

#list_x = curdatadateaud
#list_y = 1300000*curdataaud/curdataphp
#desc = [str(i) for i in list_y]

#USD-PHP
hover = HoverTool(tooltips=[
    #("index", "$index"),
    ('date','@x{%F}'),
    ('PHP', '₱@{p2u}{,3.2f}'),
#    ('usd to php','@{curdatausd/curdataphp}'),
#    ('php to usd','@p2u'),
#    ('aud to php','@a2p{,3.4f}'),
#    ('php to aud','@p2a{,3.4f}')
    #('desc', '@desc'),
],
                 
                 formatters={
        'x'      : 'datetime', # use 'datetime' formatter for 'date' field
    })


t=pd.to_datetime(str(curdatadateusd[-1]))
convertrate=curdataphp[-1]/curdatausd[-1]

p=(figure(title=str(amount) + " USD converted to PHP, Euro Central Bank rate (" +
          t.strftime('%Y-%m-%d') + ": $1 USD = " + '₱{:.2f}'.format(convertrate) + 
          " PHP)", tools="pan,wheel_zoom,box_zoom,reset", x_axis_label='date', y_axis_label='conversion'))
p.add_tools(hover)
p.line(x='x',y='p2u', color = 'blue', line_width=2,source=source)
#p.line(curdatadateusd,amount*curdatausd/curdataphp, legend="USD", color = 'blue', line_width=2)

p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = pi/4


#p.line(curdatadatephp,curdataphp, legend="PHP", color = 'green', line_width=2)
#p.circle(xptoi, yptoi, name=the_key_st, legend=the_key_st, fill_color="red", line_color="red", size=6)


#tab.append(Panel(child=row(p,data_table), title=the_key_st))
tab.append(Panel(child=row(p), title='USD-PHP'))


#PHP-USD
hover = HoverTool(tooltips=[
    #("index", "$index"),
    ('date','@x{%F}'),
    ('USD', '$@{u2p}{,3.2f}'),
#    ('rate', '@{ru2p}{.15f}'),
#    ('usd to php','@{curdatausd/curdataphp}'),
#    ('php to usd','@p2u'),
#    ('aud to php','@a2p{,3.4f}'),
#    ('php to aud','@p2a{,3.4f}')
    #('desc', '@desc'),
],
                 formatters={
        'x'      : 'datetime', # use 'datetime' formatter for 'date' field
    })

p=(figure(title=str(amount2) + " PHP converted to USD, Euro Central Bank rate (" +
          t.strftime('%Y-%m-%d') + ": $1 USD = " + '₱{:.2f}'.format(convertrate) + 
          " PHP)", tools="pan,wheel_zoom,box_zoom,reset", x_axis_label='date', y_axis_label='conversion'))

p.line(x='x',y='u2p', color = 'red', line_width=2, source=source)
p.add_tools(hover)
#p.line(curdatadateusd,amount*curdatausd/curdataphp, legend="USD", color = 'blue', line_width=2)

p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = pi/4


#p.line(curdatadatephp,curdataphp, legend="PHP", color = 'green', line_width=2)
#p.circle(xptoi, yptoi, name=the_key_st, legend=the_key_st, fill_color="red", line_color="red", size=6)


#tab.append(Panel(child=row(p,data_table), title=the_key_st))
tab.append(Panel(child=row(p), title='PHP-USD'))

#AUD-PHP
hover = HoverTool(tooltips=[
    #("index", "$index"),
    ('date','@x{%F}'),
    ('PHP', '₱@{p2a}{,3.2f}'),
#    ('usd to php','@{curdatausd/curdataphp}'),
#    ('php to usd','@p2u'),
#    ('aud to php','@a2p{,3.4f}'),
#    ('php to aud','@p2a{,3.4f}')
    #('desc', '@desc'),
],
                 
                 formatters={
        'x'      : 'datetime', # use 'datetime' formatter for 'date' field
    })


t=pd.to_datetime(str(curdatadateaud[-1]))
convertrate=curdataphp[-1]/curdataaud[-1]

p=(figure(title=str(amount) + " AUD converted to PHP, Euro Central Bank rate (" +
          t.strftime('%Y-%m-%d') + ": $1 AUD = " + '₱{:.2f}'.format(convertrate) + 
          " PHP)", tools="pan,wheel_zoom,box_zoom,reset", x_axis_label='date', y_axis_label='conversion'))
p.add_tools(hover)
p.line(x='x',y='p2a', color = 'green', line_width=2,source=source)
#p.line(curdatadateusd,amount*curdatausd/curdataphp, legend="USD", color = 'blue', line_width=2)

p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = pi/4


#p.line(curdatadatephp,curdataphp, legend="PHP", color = 'green', line_width=2)
#p.circle(xptoi, yptoi, name=the_key_st, legend=the_key_st, fill_color="red", line_color="red", size=6)


#tab.append(Panel(child=row(p,data_table), title=the_key_st))
tab.append(Panel(child=row(p), title='AUD-PHP'))


#PHP-AUD
hover = HoverTool(tooltips=[
    #("index", "$index"),
    ('date','@x{%F}'),
    ('AUD', '$@{a2p}{,3.2f}'),
#    ('rate', '@{ru2p}{.15f}'),
#    ('usd to php','@{curdatausd/curdataphp}'),
#    ('php to usd','@p2u'),
#    ('aud to php','@a2p{,3.4f}'),
#    ('php to aud','@p2a{,3.4f}')
    #('desc', '@desc'),
],
                 formatters={
        'x'      : 'datetime', # use 'datetime' formatter for 'date' field
    })

p=(figure(title=str(amount2) + " PHP converted to AUD, Euro Central Bank rate (" +
          t.strftime('%Y-%m-%d') + ": $1 AUD = " + '₱{:.2f}'.format(convertrate) + 
          " PHP)", tools="pan,wheel_zoom,box_zoom,reset", x_axis_label='date', y_axis_label='conversion'))

p.line(x='x',y='a2p', color = 'yellow', line_width=2, source=source)
p.add_tools(hover)
#p.line(curdatadateusd,amount*curdatausd/curdataphp, legend="USD", color = 'blue', line_width=2)

p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = pi/4


#p.line(curdatadatephp,curdataphp, legend="PHP", color = 'green', line_width=2)
#p.circle(xptoi, yptoi, name=the_key_st, legend=the_key_st, fill_color="red", line_color="red", size=6)


#tab.append(Panel(child=row(p,data_table), title=the_key_st))
tab.append(Panel(child=row(p), title='PHP-AUD'))



tabs = Tabs(tabs=tab)


#show(tabs)
save(tabs)

#legend = Legend(items=legend_it)
#legend.click_policy="mute"

#p.add_layout(legend, 'right')

#show(p)
#output_notebook()
