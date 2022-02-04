import os
import time
import busio
import digitalio
import board
import datetime
import pymysql.cursors
import configparser
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#create the config reader
piconfig = configparser.ConfigParser()
piconfig.read('config.ini')

#set GPIO to use the BCM numbering scheme
GPIO.setmode(GPIO.BCM)
PumpPin = piconfig['DEFAULT']['PumpPin']
GPIO.setup(PumpPin, GPIO.OUT)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

#CONSTANTS
MIN_MOISTURE = 50688
MAX_MOISTURE = 23680
FULL_RANGE = MIN_MOISTURE-MAX_MOISTURE

#Find ADC Value
adc = chan0.value
PercentMoisture = abs(((adc - FULL_RANGE)/MAX_MOISTURE)-1)*100

# Connect to the database
connection = pymysql.connect(host=piconfig['DEFAULT']['MySQLIP'],
                             user=piconfig['DEFAULT']['MySQLUser'],
                             password=piconfig['DEFAULT']['MySQLPass'],
                             db=piconfig['DEFAULT']['MySQLDB'],
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        #now represents now in date and time
        now = datetime.datetime.now()
        # Create a new record
        sql = "INSERT INTO " + piconfig['DEFAULT']['MySQLTable'] + " (`PercentMoisture`, `timerecorded`) VALUES (%s, %s)"
        cursor.execute(sql, (PercentMoisture, now))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


# Decide whether to turn on the pump to water the plant
#if PercentMoisture < 40:
#    GPIO.output(PumpPin, GPIO.HIGH)
#    time.sleep(3)
#    GPIO.output(PumpPin, GPIO.LOW)
