import SI1132
import BME280
import time
import pytz

from datetime import datetime
from influxdb import InfluxDBClient

client = InfluxDBClient(host='127.0.0.1', port=8086, database='tempsdb')

I2C = '/dev/i2c-1'
TZ = pytz.timezone('UTC')

si1132 = SI1132.SI1132(I2C)
bme280 = BME280.BME280(I2C, 0x03, 0x02, 0x02, 0x02)


while True:
    data = {
        'uv_index': si1132.readUV() / 100.0,
        'visibile': si1132.readVisible(),
        'ir': si1132.readIR(),
        'temperature': bme280.read_temperature(),
        'humidity': bme280.read_humidity(),
        'pressure': bme280.read_pressure() / 100.0
    }
    body = [{
        'measurement': 'weather',
        'tags': { 'station': 'office' },
        'time': TZ.localize(datetime.now()).isoformat(),
        'fields': data
    }]

    print(body)
    print('---------')
    client.write_points(body)
    time.sleep(10)

