from decimal import Decimal
from blockcypher import get_address_full
import datetime

import yfinance as yf
import pandas_datareader.data as pdr


def sent_tx(tx_item, address):
    for tx_key, tx_value in tx_item.items():
        if tx_key == 'inputs':
            for input_dict in tx_value:
                if address in input_dict['addresses']:
                    return True
                else:
                    return False


def calculate_total(tx_item, address, is_sent_tx=None):
    total_satoshi = 0

    for tx_key, tx_value in tx_item.items():
        if tx_key == 'inputs':
            for input_dict in tx_value:
                if address in input_dict['addresses']:
                    total_satoshi += input_dict['output_value']

        if tx_key == 'outputs':
            for outputs_dict in tx_value:
                if address in outputs_dict['addresses']:
                    if is_sent_tx is True:
                        total_satoshi -= outputs_dict['value']
                    else:
                        total_satoshi += outputs_dict['value']
    print('Total Satoshi: ', total_satoshi)
    convert_to_decimal = Decimal(total_satoshi / pow(10, 8))
    return convert_to_decimal


# -------------------------FULL DETAILS OF TRANSACTIONS-------------------------
def main(verbose):
    address = '1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ'
    txs = get_address_full(txn_limit=50, address=address)
    balance = txs['final_balance']

    position_in_transactions = 0
    temp_btc_value = 0
    total_btc = 0
    tx_type = ''

    crypto_currency = 'BTC'
    against_currency = 'USD'

    is_next_block_same = False

    for item in txs['txs']:

        total_btc = calculate_total(item, address, is_sent_tx=sent_tx(item, address))
        total_btc += temp_btc_value
        temp_btc_value = 0

        if position_in_transactions < len(txs['txs']) - 1:
            if txs['txs'][position_in_transactions]['block_height'] == txs['txs'][position_in_transactions + 1]['block_height']:
                if verbose:
                    print('-----------------------------Skipping Double Block-----------------------------')
                is_next_block_same = True
                temp_btc_value = total_btc
                if verbose:
                    print(temp_btc_value)

        if is_next_block_same is False:
            for key, value in item.items():
                if key == 'inputs' or key == 'outputs':
                    if verbose:
                        print('-----------------------------', key, '-----------------------------')
                    for item_in_out in value:
                        for key_in_out, value_in_out in item_in_out.items():
                            if verbose:
                                print('\t', key_in_out, ' : ', value_in_out)
                        if verbose:
                            print()
                else:
                    if verbose:
                        print(key, ' : ', value)

            if sent_tx(item, address) is True:
                tx_type = 'SELL'
                if verbose:
                    print('SELL')
                    print('Sent BTC: ', total_btc)
            else:
                tx_type = 'BUY'
                if verbose:
                    print('BUY')
                    print('Sent BTC: ', total_btc)

            tx_date = txs['txs'][position_in_transactions]['confirmed']
            tx_date = tx_date + datetime.timedelta(hours=3)

            total_btc_str = str(total_btc)
            print(type(total_btc_str))

            # start = tx_date
            # end = start + datetime.timedelta(hours=1)

            # data = yf.download(tickers="BTC-USD", start=start, end=end, interval="1m", progress=False)
            # data = data.iloc[-1].tolist()
            # print(data[3])
        transactions.append({'block': txs['txs'][position_in_transactions]['block_height'],
                             'time': tx_date,
                             'type': tx_type,
                             'amount': total_btc})

        position_in_transactions += 1
        is_next_block_same = False
        if verbose:
            print("\n=========================================================================================================================================================\n")

    for key, value in transactions[-1].items():
        if verbose:
            print('\t', key, ' : ', value, ' type: ', type(value))


transactions = []

if __name__ == '__main__':
    main(verbose=True)
else:
    main(verbose=False)

# -------------------------MEDIUM DETAILS OF TRANSACTIONS-------------------------
# for key, value in get_address_details('1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ', before_bh=682694).items():
#     if key == 'txrefs':
#         print('-----------------------------', key, '-----------------------------')
#         for item_in_out in value:
#             for key_in_out, value_in_out in item_in_out.items():
#                 print('\t', key_in_out, ' : ', value_in_out)
#             print()
#     else:
#         print(key, ' : ', value)

# -------------------------DETAILS OF SPECIFIC TRANSACTIONS-------------------------
# for key, value in get_transaction_details('1740788991aeb5bdf65dc53e72f4bb0af581558ef461392db448bb89b2d0afb2').items():
#     print(key, ' : ', value)
#
# print()
#
# for key, value in get_transaction_details('477d19ee2cfc1e9942a7dc6bc70f953b7c5bd22daf4b5fd82c1cba43202cc58c').items():
#     print(key, ' : ', value)