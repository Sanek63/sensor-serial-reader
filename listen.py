import csv
import datetime
from copy import deepcopy

import serial
from logger import get_logger
from csv import DictWriter


CSV_FIELDNAMES = ['cmd', 'adc_a', 'adc_b', 'ts', 'created_at']


def listen(port, log_path, csv_path):
    logger = get_logger(port, log_path)
    logger.debug("Start script")

    try:
        with open(csv_path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES, delimiter=';')
            writer.writeheader()

        ser = serial.Serial(port, 115200, timeout=0.01)

        is_first, is_first_ts = True, None
        while True:
            b = ser.read(2000)
            logger.debug('Received %s' % b)

            if len(b) > 0:
                if b[:2] == b'\x55\x01' and b[-2:] == b'\x55\x02':
                    b = b[2:-2]
                else:
                    continue

                b = b.replace(b'\x55\x00', b'\x55')
                logger.debug('Cleaned bytes %s' % b)

                cmd = int.from_bytes(bytes(b[:1]), byteorder='big')
                adc_a = int.from_bytes(bytes(b[1:5]), byteorder='big')
                adc_b = int.from_bytes(bytes(b[5:9]), byteorder='big')
                time = int.from_bytes(bytes(b[9:13]), byteorder='big')

                logger.info(f'Decrypt data:  CMD: %s, ADC_A: %s, ADC_B: %s' % (cmd, adc_a, adc_b))

                ts = int(datetime.datetime.utcnow().timestamp() * 1000)
                if is_first:
                    is_first_ts = deepcopy(ts)
                    created_at = 0
                    is_first = False
                else:
                    created_at = ts - is_first_ts

                with open(csv_path, 'a+') as csv_file:
                    csv_writer = DictWriter(csv_file, CSV_FIELDNAMES, delimiter=';')
                    csv_writer.writerow({
                            'cmd': cmd,
                            'adc_a': adc_a,
                            'adc_b': adc_b,
                            'ts': time,
                            'created_at': created_at
                        }
                    )

    except Exception as e:
        logger.error(e)
