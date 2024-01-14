'''
Hello, I am George (Gigex), beginner Python developer. I wrote this scrypt to analyze the market data,
it might have some bugs, I am not a professional developer and this is self tought project so don't judge too much.
In case you have questions, have some ideas or want me to work alongside with you on your project ideas
contact me on my email: Giorgigigaia@gmail.com

'''
# We are importing required Modules
import csv

import json

import matplotlib.pyplot as plt
import asyncio
import yfinance as yf
import math

#main function to start the analysis for the provided symbol
def displayStockData(symbol):
    status = bool
    data = None
    #checks if the symbol is crypto or a stock, because sometimes the crypto symbol matches with the stock
    with open("symbolscrypt.json","r") as f:
        file = json.load(f)
        for i in range(len(file)):
            if symbol == file.get(list(file)[i]):
                ticker = yf.Ticker(f"{symbol}-USD")
                data = ticker.history(period="1mo")
                currentPrice = format(data.iloc[-1,3],".2f")
                status = True
                break
            else:
                status = False
                continue
    if status == False:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1mo")
        currentPrice = format(data.iloc[-1,3],".2f")

    else:
        pass


    try:
        PercentChange = (data.iloc[-2,3] - data.iloc[-1,3])/data.iloc[-2,3]*100
        if data.iloc[-2,3]  > data.iloc[-1,3]:
            PercentChange = "-"+ str(format(PercentChange,".2f"))
            PercentChange = float(PercentChange)
        else:
            PercentChange = float(format(PercentChange, ".2f"))
    except:
        PercentChange = 0

#if stock data is too fresh it will pass, meaning if the 1 month count of data is less than 20 days
    if len(data)<20:
        pass
    else:
        datay = []
        datax = []
        for i in range(len(data)):
           datay.append(data.iloc[i,3])
           datax.append(data.index[i])
        plt.plot(datax,datay, label = "Price")
        plt.xlabel("Date")
        plt.ylabel("Price USD")
        plt.title(f"Data for {symbol}")
        return EMA.calculateEMA(data,currentPrice,PercentChange)
    
            

class EMA:
    '''
    #the section is commented out because firstly it was one file scrypt, will leave it here if it will be useful
    def __init__(self,symbol):
        self.symbol = symbol
        ticker = yf.Ticker(symbol)
        data = ticker.history(period = "max")
        if len(data)<20:
            print("Data for the stock is very fresh!")
        else:
            try:
                changeInPercent = (data.iloc[-3,3]-data.iloc[-1,3])/data.iloc[-3,3]*100
            except:
                try:
                    changeInPercent = (data.iloc[-2,3]-data.iloc[-1,3])/data.iloc[-2,3]*100
                except:
                    changeInPercent = 0
            try: 
                if data.iloc[-3,3] < data.iloc[-1,3]:
                    #changeInPercent = "-"+str(format(changeInPercent,".2f"))
                    changeInPercent = float(changeInPercent)
                else:
                    changeInPercent = float(format(changeInPercent, ".2f"))
            except:
                try:
                    if data.iloc[-2,3] < data.iloc[-1,3]:
                        #changeInPercent = "-"+str(format(changeInPercent,".2f"))
                        changeInPercent = float(changeInPercent)
                    else:
                        changeInPercent = float(format(changeInPercent, ".2f"))
                except:
                    changeInPercent = 0
                    
            currentPrice = data.iloc[-1,3]
            #self.calculateEMA(data,currentPrice,changeInPercent)
    '''

    def calculateEMA(data,currentPrice,changeInPercent):
        #We define variables that will be used globally, tried many ways, this way worked best for now
        EMA.kw = 2/(7+1)
        EMA.emayw = 0
        EMA.dataindex = 0
        EMA.EMAW = 0
        EMA.EMATW = 0

        #Defined async functions which work semitimesly for the recent EMA analysis crossovers it is a bit complex algorithm, but works well
        async def checkEMA(data):
            for i in range(len(data)):
                EMA.emayw = data.iloc[i,3]*EMA.kw+EMA.emayw*(1-EMA.kw)
                EMA.dataindex = i
                EMA.EMAW = data.iloc[-1,3]*EMA.kw+EMA.emayw*(1-EMA.kw)
        EMA.ktw = 2/(14+1)
        EMA.emaytw = 0

        async def checkEMAT(data):
            for i in range(len(data)):
                EMA.emaytw = data.iloc[i,3]*EMA.ktw+EMA.emaytw*(1-EMA.ktw)
                EMA.dataindex = i
                EMA.EMATW = data.iloc[-1,3]*EMA.ktw+EMA.emaytw*(1-EMA.ktw)
                await checkifEqual(data,EMA.dataindex,EMA.EMAW,EMA.EMATW)
        EMA.trend = ""
        async def checkifEqual(data,dataindex,EMAW,EMATW):
            if EMATW - EMAW < EMAW*0.01/100:
                try:
                    if data.iloc[dataindex,3]>data.iloc[dataindex+1,3]:
                        EMA.trend = "Negative"
                        
                    else:
                        EMA.trend = "Positive"

                except:
                    if data.iloc[dataindex,3] > data.iloc[dataindex-1,3]:
                        EMA.trend = "Positive"

                    else:
                        EMA.trend = "Negative"

            else:
                pass
            
        EMA.emaAnalyse = ""
        EMA.bollingerAnalyse = ""
        EMA.message = ""
        EMA.messageBollinger = ""
        asyncio.run(checkEMA(data))
        asyncio.run(checkEMAT(data))
        EMA.bollingerBands(data)
        EMA.sendSignal(EMA.EMAW,EMA.EMATW,EMA.trend)

        if EMA.emaAnalyse == EMA.bollingerAnalyse:
            if EMA.emaAnalyse != "":
                plt.scatter(data.index[-1],data.iloc[-1,3],label = f"Prediction = {EMA.emaAnalyse}")
                plt.legend()
                plt.show()
                return {"message": EMA.emaAnalyse}
            else:
                plt.scatter(data.index[-1],data.iloc[-1,3],label = f"EMA = {EMA.message};Bollinger = {EMA.messageBollinger}")
                plt.legend()
                plt.show()
                return {"message": [EMA.message,EMA.messageBollinger]}
        else:
            plt.scatter(data.index[-1],data.iloc[-1,3], label = f"EMA = {EMA.emaAnalyse}; Bollinger = {EMA.bollingerAnalyse}")
            plt.legend()
            plt.show()

        
    def bollingerBands(data):
        # analysis for bollinger bands with its formula
        SMA = 0
        for i in range(1,21):
            SMA+= data.iloc[-i,3]
        squareOfDMean = 0
        mean = SMA/20
        for i in range(1,21):
            squareOfDMean+= abs(mean - data.iloc[-i,3])**2
        
        SD = math.sqrt(squareOfDMean/20)
        
        upper = SMA/20 + (SD*2)
        lower = SMA/20 - (SD*2)
        plt.scatter(data.index[-1],upper,color = "r", marker = "o", label = "Upper Band")
        plt.scatter(data.index[-1],lower, color = "g", marker = "o", label = "Lower Band")
        
        if upper-data.iloc[-1,3] < (data.iloc[-1,3]*0.5/100) or data.iloc[-1,3] - lower < (data.iloc[-1,3]*0.5/100):
            if upper-data.iloc[-1,3] < (data.iloc[-1,3]*0.1/100)or data.iloc[-1,3] - lower < (data.iloc[-1,3]*0.1/100):
                if upper-data.iloc[-1,3] < (data.iloc[-1,3]*0.05/100) or data.iloc[-1,3] - lower < (data.iloc[-1,3]*0.05/100):
                    if upper-data.iloc[-1,3] < (data.iloc[-1,3]*0.01/100) or data.iloc[-1,3] - lower < (data.iloc[-1,3]*0.01/100):
                        if data.iloc[-2,3] < data.iloc[-1,3]:
                            EMA.bollingerAnalyse = "SELL"
                        elif data.iloc[-2,3] > data.iloc[-1,3]:
                            EMA.bollingerAnalyse = "BUY"
                        else:
                            EMA.messageBollinger = "Super close to changin direction Range 0.05% !"
                else:
                    EMA.messageBollinger = "Very close to changing direction Range 0.1% !"
            else:
                EMA.messageBollinger = "Close to changing direction range  0.5%!"
        else:
            EMA.messageBollinger = "Bollingerbands stable"

        
    def sendSignal(EMAW,EMATW,trend):
        if abs(EMATW - EMAW) < EMAW*0.01/100:
            if trend == "Negative":
                EMA.emaAnalyse = "BUY"
            else:
                EMA.emaAnalyse = "SELL"
        
        else:
            EMA.message ="EMA Indicator Stable"



'''
# this section also commented out as the application was just onefile script, it just filters specific industry and displays the analysis of all assets included

def startAnalysis():
    with open("nasdaq_screener_1704649993170.csv","r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            try:
                if  displayStockData(line[0])["message"] == "BUY":
                    print(f"Buy signal for stock: {line[1]}")
                elif displayStockData(line[0])["message"] == "SELL":
                    print(f"Sell signal for stock: {line[1]}") 
                else:
                    pass
                #print(displayStockData(line[0])["message"])
            except:
                print("Some error gotta check!")
                

        #to count specific industry
        count = 0
        for line in csv_reader:
            if count > 20:
                break
            if line[10] == industry:
                count+=1
                print(f"Company name:{line[1]}")
                EMACrypt(f"{line[0]}")
                displayStockData(f"{line[0]}")
                print("\n----------------------------------")
        
            else:
                pass

'''

