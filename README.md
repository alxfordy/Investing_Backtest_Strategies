# Investing Backtest Strategies
 
 ## Introduction
 This repo uses backtrader (a python library for backtesting) to track returns on both DCA and Value Averaging investment strategies.
 For a more comprehensive writeup, see here: https://medium.com/coinmonks/could-you-be-making-better-gains-than-dollar-cost-averaging-5948bb6c7448
 
 ## How To Use It
 The strategies and backtrader settings are stored under components/ with the notebook "Backtrader_Clean" providing the functionality of backtesting and plotting the results
 
 ## Results 
 
```python
Results For Dollar Cost Average on BTC
--------------------------------------------------
Dollar Cost Averaging
Months Passed:		62
Buy Orders:		61
Sell Orders:		0
Total Shares:		7.69
Total Value:		$252,397.48
Total Shares Value:	$251,397.48
Total Cash Value:	$0
Cost:		        $61,000.01
Gross Return:		$191,397.47
ROI:		        313.77%
--------------------------------------------------
```
```python
Results For Value Averaging on BTC
--------------------------------------------------
Value Investing
Months Passed:		62
Buy Orders:		32
Sell Orders:		28
Total Shares:		1.59
Total Value:		$134,273.99
Total Shares Value:	$51,861.88
Total Cash Value:	$82,412.11
Cost:		        $147,138.44
Gross Return:		$-12,864.44
ROI:		        -8.74%
--------------------------------------------------
```

## Plotting

![All_Results](https://user-images.githubusercontent.com/26648341/168373953-e75f8b48-cc5a-4d1d-9065-d44792d1bd97.png)


 
