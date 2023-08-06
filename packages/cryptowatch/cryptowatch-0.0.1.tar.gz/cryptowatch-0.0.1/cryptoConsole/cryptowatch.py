#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2017 Alex Epstein

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import time
from os import system
from sys import platform


import cryptoPie.cryptoPie as pie
import utils.cryptoUtils as crypto
import utils.cwconfig as cfg
config = cfg.config()

def clear():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        system("clear")
    elif platform == "win32":
        system("cls")

def consoleMonitor(coinType):
    coinType = coinType.lower()
    if coinType == "ethereum":
        cryptoTicker = "ETH"
        address = config.etherAddress
    elif coinType == "bitcoin":
        cryptoTicker = "BTC"
        address = config.bitcoinAddress
    elif coinType == "litecoin":
        cryptoTicker = "LTC"
        address = config.litecoinAddress
    else:
        raise ValueError('Error: invalid coin type')
    response = crypto.queryCMC(coinType)
    exchangeRate = float(crypto.parseCryptoData(response, "ER"))
    hourlyPercentage = float(crypto.parseCryptoData(response, "HP"))
    dailyPercentage = float(crypto.parseCryptoData(response, "DP"))
    totalFiat = float(crypto.getTotalFiat(crypto.parseCryptoData(response, "ER"), coinType))
    totalCrypto = float(totalFiat) / float(exchangeRate)
    with open('.cryptoConsole', 'a+') as file:
        file.write("%s->%s:%.2f\n" % (cryptoTicker, config.fiatCurrency, exchangeRate))
        file.write("1H: %.2f  24H: %.2f\n" % (hourlyPercentage, dailyPercentage))
        if totalFiat != 0 and address is not None :
            file.write("%s: %.2f\n" % (cryptoTicker, totalCrypto))
            file.write("%s: %.2f\n\n" % (config.fiatCurrency, totalFiat))

def main():
    parser = argparse.ArgumentParser(prog="Cryptowatch",description='Track prices and account balances for bitcoin, ethereum, and litecoin')
    parser.add_argument("-m", "--monitor", action="store_true" ,help="Choose which cryptowatch monitor to use")
    parser.add_argument("-v", "--version", action="store_true", help="Display the current version of cryptowatch")
    args = parser.parse_args()
    if args.version:
        print("Cryptowatch Version 0.0.1")
        exit()
    if args.monitor:
        if args.monitor == "pie" or args.monitor == "rpi":
            pie.main()
        elif args.monitor == "web":
            print("Web monitor not implemented yet.")
            exit()
        elif args.monitor == "console":
            print("Loading...")
            open('.cryptoConsole', 'w+').close()
            while True:
                consoleMonitor("ethereum")
                consoleMonitor("bitcoin")
                consoleMonitor("litecoin")
                clear()
                print("Cryptowatch")
                with open('.cryptoConsole', 'r') as file:
                    print(file.read())
                print("Watching...")
                time.sleep(2)
                open('.cryptoConsole', 'w').close()
        else:
            print("Error: invalid monitor type")
            exit()
    else:
            print("Loading...")
            open('.cryptoConsole', 'w+').close()
            consoleMonitor("ethereum")
            consoleMonitor("bitcoin")
            consoleMonitor("litecoin")
            clear()
            print("Cryptowatch")
            with open('.cryptoConsole', 'r') as file:
                print(file.read())
            open('.cryptoConsole', 'w').close()


main()
