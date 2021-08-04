import csv
import datetime
from copy import deepcopy

import serial
from logger import get_logger
from csv import DictWriter


CSV_FIELDNAMES = ['cmd', 'adc_a', 'adc_b', 'created_at']


def write_log(ts, message, csv_path, ts_start):
    message.replace(b'\x55\x00', b'\x55')
    cmd = int.from_bytes(bytes(message[:1]), byteorder='big')
    adc_a = int.from_bytes(bytes(message[1:5]), byteorder='big')
    adc_b = int.from_bytes(bytes(message[5:9]), byteorder='big')

    # logger.info(f'Decrypt data:  CMD: %s, ADC_A: %s, ADC_B: %s' % (cmd, adc_a, adc_b))

    created_at = ts - ts_start

    print(''.join(r'\x'+hex(letter)[2:] for letter in message), cmd, adc_a, adc_b)
    with open(csv_path, 'a+') as file:
        csv_writer = DictWriter(file, CSV_FIELDNAMES, delimiter=';')
        csv_writer.writerow({
                'cmd': cmd,
                'adc_a': adc_a,
                'adc_b': adc_b,
                'created_at': created_at
            }
        )


def listen(port, log_path, csv_path):
    message = b""

    ts_start = None
    last_byte = None

    flag = False

    logger = get_logger(port, log_path)
    logger.debug("Start script")

    with open(csv_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES, delimiter=';')
        writer.writeheader()

    ser = serial.Serial(port, 460800, timeout=0)

    while True:
        b = ser.read(1)
        if b:
            if last_byte == b'\x55':
                if b == b'\x01':
                    message = b''
                    flag = True

                elif flag and b == b'\x02':
                    ts = int(datetime.datetime.utcnow().timestamp() * 1000)
                    if ts_start is None:
                        ts_start = ts

                    write_log(ts=ts, message=message, ts_start=ts_start, csv_path=csv_path)
                    message = b''

            else:
                if b != '\x55':
                    message += b

            last_byte = b
