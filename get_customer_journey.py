import pandas as pd
import base64

from matplotlib.figure import Figure
import matplotlib.dates as mdates

from lifetimes.utils import calculate_alive_path
from io import BytesIO

def get_customer_journey(transactions, bgf, id):
    id = int(id)
    days_since_birth = 30
    sp_trans = transactions.loc[transactions['user_id'] == id]
    sp_trans_list = sp_trans.drop('user_id', axis=1).values

    path = calculate_alive_path(bgf, sp_trans, 'event_time', days_since_birth, freq="D")
    path_dates = pd.date_range(start=min(sp_trans['event_time']), periods=len(path), freq="D")

    return create_palive_figure(path, path_dates, sp_trans), sp_trans_list


def create_palive_figure(path, path_dates, sp_trans):
    red = '#B6324F'
    blue = '#176BA0'  # '#4580A9'
    lg = 'grey'

    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()
    ax.plot(path_dates, path, c=blue, label='probability of being alive')
    ax.vlines(sp_trans['event_time'], 0, 1, colors=red, label='purchase events', linestyles='dashed')

    ax.set_xlabel('Time', color=lg, fontsize='large')
    ax.set_ylabel('probability of being alive', color=lg, fontsize='large')

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

    ax.tick_params(axis='x', length=5, colors=lg)
    ax.tick_params(axis='y', length=5, colors=lg)

    ax.spines['bottom'].set_color(lg)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(.5)
    ax.spines['left'].set_linewidth(.5)
    ax.spines['left'].set_color(lg)
    ax.spines['bottom'].set_color(lg)

    fig.legend(edgecolor='w', labelcolor=lg, fontsize='large')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    fig_data = base64.b64encode(buf.getbuffer()).decode("utf8")
    return fig_data