import pandas as pd
import json
from flask import Flask, request, render_template, redirect, url_for
from get_info import get_info
from get_customer_journey import get_customer_journey

from lifetimes import BetaGeoFitter, ModifiedBetaGeoFitter, BetaGeoBetaBinomFitter


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id = request.form["id"]
        try:
            mapped_id = mapping[id]
            if mapped_id not in data['user_id'].values:
                return render_template('home.html')
            else:
                segment, n_purchase, clv = get_info(data, mapped_id)
                fig_data, sp_trans_list = get_customer_journey(transactions, bgf, mapped_id)
                return render_template('home.html', id=id, segment=segment, n_purchase=n_purchase,
                                   clv=clv, fig_data=fig_data, history=sp_trans_list)
        except:
            return render_template('home.html')
    return render_template('home.html')


data = pd.read_csv('data/user_profile_label.csv')
transactions = pd.read_csv('data/transition_ecomm_oct_nov.csv')
f = open('mapping.json')
mapping = json.load(f)

bgf = ModifiedBetaGeoFitter(penalizer_coef=0.0)
bgf.fit(data['frequency'], data['recency'], data['t'])

if __name__ == '__main__':
    app.run()