import csv
import datetime
from copy import deepcopy

import serial
from logger import get_logger
from csv import DictWriter

logger = None
csv_file = None

CSV_FIELDNAMES = ['cmd', 'adc_a', 'adc_b', 'created_at']

message = b""

ts_start = None
last_byte = None


flag = False


def write_log(ts):
    global ts_start, logger, message, csv_file

    message.replace(b'\x55\x00', b'\x55')
    cmd = int.from_bytes(bytes(message[:1]), byteorder='big')
    adc_a = int.from_bytes(bytes(message[1:5]), byteorder='big')
    adc_b = int.from_bytes(bytes(message[5:9]), byteorder='big')

    # logger.info(f'Decrypt data:  CMD: %s, ADC_A: %s, ADC_B: %s' % (cmd, adc_a, adc_b))

    created_at = ts - ts_start

    print(''.join(r'\x'+hex(letter)[2:] for letter in message), cmd, adc_a, adc_b)
    with open(csv_file, 'a+') as file:
        csv_writer = DictWriter(file, CSV_FIELDNAMES, delimiter=';')
        csv_writer.writerow({
                'cmd': cmd,
                'adc_a': adc_a,
                'adc_b': adc_b,
                'created_at': created_at
            }
        )


def serial_byte_receiver(data_byte):
    global message, last_byte, ts_start, flag

    if last_byte == b'\x55':
        if data_byte == b'\x01':
            message = b''
            flag = True

        elif flag and data_byte == b'\x02':
            ts = int(datetime.datetime.utcnow().timestamp() * 1000)
            if ts_start is None:
                ts_start = ts

            write_log(ts=ts)
            message = b''

    else:
        if data_byte != '\x55':
            message += data_byte

    last_byte = data_byte


def listen(port, log_path, csv_path):
    global message, ts_start, logger, csv_file

    csv_file = csv_path
    logger = get_logger(port, log_path)
    logger.debug("Start script")

    with open(csv_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES, delimiter=';')
        writer.writeheader()

    ser = serial.Serial(port, 460800, timeout=0)

    while True:
        b = ser.read(1)
        if b:
            serial_byte_receiver(b)
