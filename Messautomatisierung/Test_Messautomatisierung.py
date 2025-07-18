# Test für die messautomatisierung

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measurements for Bode plots
Input signal: DF_IN1
Output signal: DF_IN2

@author: Mirco Meiners (HSB)
"""

# %% Init
import time
# from datetime import datetime
import redpitaya_scpi as scpi
import numpy as np
import os 
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# %% Connection params
IP = '192.168.111.182'
rp_s = scpi.scpi(IP)

# %% Measurement / Data Accquisition
DF_IN1 = pd.DataFrame()
DF_IN2 = pd.DataFrame() 

# Parameters
func = 'SINE'
ampl = 1
ampl1 = 1
offset = 0.0
endfreq = 1000
freqs = np.arange(50,endfreq, 10)

print("Messung wird gestartet...")

kondensatoren = ["1uF","0.1uF","0.01uF"]

guete = ["Q1","Q10"]

messung = ["BPF","LPF","HPF","BSF","LPF_Butterworth"]

Anzahl = len(kondensatoren)*len(guete)*len(messung)

print(f"Gesamtanzahl aller Messungen: {Anzahl}")

for f,cwert in enumerate(kondensatoren):
    
    
    while True:
        ready1 = input("Kondensator "+cwert+" angelegt? Antworten sie mit Y: ")

        if ready1.upper() in ["Y"]:
            break
        print("Ungueltige Eingabe. Bitte geben Sie 'Y' ein wenn Sie soweit sind.")
    
  
    startfreq = float(input("Start Frequenz: "))
    endfreq = float(input ("End freqeunz: "))
    schrittweite = float(input("Geben sie die Schrittweite an: "))
    

    freqs = np.arange(startfreq,endfreq, schrittweite)   
    
    for s,gueteval in enumerate(guete):
        while True:
            ready2 = input("Guetewiderstand für: "+gueteval+" angelegt? Antworten sie mit Y: ")

            if ready2.upper() in ["Y"]:
                break
            print("Ungueltige Eingabe. Bitte geben Sie 'Y' ein wenn Sie soweit sind.")


        for i,FilterTyp in enumerate(messung): # Diese schleife sorgt dafür dass Alle Filter Typen durch gemessen werden
            AktuelleFilter = FilterTyp+"_"+gueteval+"_"+cwert
            while True:
                ready3 =  input("Sind sie Bereit fuer die messung: "+AktuelleFilter+" Antworten sie mit Y: ")
                
                if ready3.upper() in ["Y"]:
                    break
                print("Ungueltige Eingabe. Bitte geben Sie 'Y' ein wenn Sie soweit sind.")

            if ready3 == "Y":
                #print("Great Success!")
                for freq in freqs:
                    print("freq:",freq)
                    rp_s.tx_txt('GEN:RST')  # Signal Generator reset
                    rp_s.tx_txt('SOUR1:FUNC ' + str(func).upper())  # Wave form
                    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))  # Magnitude
                    rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))  # Offset
                    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))  # Frequency
                    rp_s.tx_txt('OUTPUT1:STATE ON')  # Output
                    rp_s.tx_txt('SOUR1:TRig:INT')
                    time.sleep(1)

                    # Trigger
                    rp_s.tx_txt('ACQ:RST')  # Input reset
                    rp_s.tx_txt('ACQ:DEC 64')  # Decimation
                    rp_s.tx_txt('ACQ:TRIG:LEV 0.5')  # Trigger level
                    rp_s.tx_txt('ACQ:TRIG:DLY 8192')  # Delay
                    rp_s.tx_txt('ACQ:START')  # Start measurement
                    rp_s.tx_txt('ACQ:TRIG NOW')

                    # Input IN1
                    time.sleep(0.1)  # in seconds
                    rp_s.tx_txt('ACQ:SOUR1:DATA?')  # Readout buffer IN1
                    IN1str = rp_s.rx_txt()
                    IN1str = IN1str.strip('{}\n\r').replace("  ", "").split(',')
                    IN1 = np.array(list(map(float, IN1str)))
                    DF_IN1[str(freq)] = IN1

                    # Input IN2
                    time.sleep(0.1)  # in seconds
                    rp_s.tx_txt('ACQ:SOUR2:DATA?')  # Readout buffer IN2
                    IN2str = rp_s.rx_txt()
                    IN2str = IN2str.strip('{}\n\r').replace("  ", "").split(',')
                    IN2 = np.array(list(map(float, IN2str)))
                    DF_IN2[str(freq)] = IN2

                    rp_s.tx_txt('OUTPUT2:STATE OFF')

            #----------------------------------------- %% Data storage-------------------------------------------

            Data_IN1 = 'Messdaten/IN1_INT_IN_'+AktuelleFilter  # + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))
            Data_IN2 = 'Messdaten/IN2_INT_OUT_'+AktuelleFilter  #+ str(datetime.now().strftime('%Y-%m-%d_%H_%M'))

            #Store data on disk as comma-seperated-values
            
            DF_IN1.to_csv(Data_IN1 + '.csv', index=False)
            DF_IN2.to_csv(Data_IN2 + '.csv', index=False)

            print("Messung: "+AktuelleFilter+" wurde gespeichert")

            

# %% Store data on disk as apache feather
# DF_IN1.to_feather(Data_IN1 + ".feather")
# DF_IN2.to_feather(Data_IN2 + ".feather")

# %% Plot
# plt.plot(DF_IN1['900'], label='IN1')
# plt.plot(DF_IN2['900'], label='IN2')
# plt.legend()
# plt.show()
