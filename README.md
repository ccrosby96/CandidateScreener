# CandidateScreener

This project serves to identify potential candidates in the market given a number of parameters. The need for identifying good candidates for a buy/write strategy neccessitated
the development of this project. With the help of the EOD Historical API, this program enables the user to filter stocks in the market place by market cap, industry, sector, 
5 day percent gain/loss, and a number of criteria related to a stock's option chain. Specifically, the Screener allows one to check for the existance of an option chain with calls
of a given Implied volatility. A supporting sqlite database has been designed in the second normal form to support the app. It stores previously identified candidate tickers, options data, and a mailing list. An additional table, hold_list, serves to prevent recently identified companies from being identified for the next 5 days. This "cool down period" aligns with the 5 day loss/gain parameter.


[Database Design Visual](screenerdbuml.PNG)
