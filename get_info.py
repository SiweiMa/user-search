
def get_info(data, id):

    idx = data['user_id'] == int(id)

    n_purchase = round(data.loc[idx]['n_purchase'].values[0], 2)
    clv = round(data.loc[idx]['clv'].values[0], 2)
    segment_id = data.loc[idx]['label'].values

    if segment_id == 0:
        return 'potential loyal costumer', n_purchase, clv
    if segment_id == 1:
        return 'dormant costumer', n_purchase, clv
    if segment_id == 2:
        return 'loyal costumer', n_purchase, clv
    if segment_id == 3:
        return 'need attention', n_purchase, clv
    if segment_id == 4:
        return 'dormant costumer', n_purchase, clv
    if segment_id == 5:
        return 'big client', n_purchase, clv