# cryptocompare
Python3 Wrapper for CryptoCompare

## Usage

```python
import cryptocompare

# COIN INFO
cryptocompare.get_coin_info('BTC')
# {'COIN': 'BTC', 'PRICE': 2854.56, 'HIGH24HOUR': 2954.62, 'LOW24HOUR': 2773.75}
cryptocompare.get_coin_info('BTC', curr='USD')
# {'COIN': 'BTC', 'PRICE': 3326.28, 'HIGH24HOUR': 3464.43, 'LOW24HOUR': 3233.5}
cryptocompare.get_coin_info('BTC', curr='GBP', fields=[cryptocompare.PRICE, cryptocompare.MARKETCAP])
# {'NAME': 'BTC', 'PRICE': 2574.02, 'MKTCAP': 42466084147.24}

# PRICE
cryptocompare.get_price('ETH', curr='EUR')
# 250.16

# 24 HOUR HIGH/LOW
cryptocompare.get_high('BTC', curr='ETH')
# 10.64849324
# ------------------------------------------
cryptocompare.get_low('BTC', curr='XMR')
# 66.8002672

# MARKETCAP
cryptocompare.get_marketcap('LTC', curr='BTC')
# 751229.327212861

# 24 HOUR CHANGE
# in %
cryptocompare.get_change('ZEC')
# 9.42708333333333
# ------------------------------------------
cryptocompare.get_change('ZEC', curr='XRP')
# 8.32401098346785 (XRP)
```

### Fields

* PRICE 
* HIGH 
* LOW 
* VOLUME 
* CHANGE 
* CHANGE\_PERCENT 
* MARKETCAP 

## TODO

- [ ] rewrite to take more than one coin at once, i.e. `get_price(['BTC', 'ETH'], curr='EUR')`
