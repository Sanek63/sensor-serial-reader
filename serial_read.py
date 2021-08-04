import threading
from listen import listen, CSV_FIELDNAMES
from csv import DictWriter


if __name__ == '__main__':
    usb1_csv = './logs/ttyUSB0.csv'
    usb1 = threading.Thread(target=listen, args=('/dev/ttyUSB0', './logs/ttyUSB0.log', usb1_csv))
    usb1.start()

    usb2_csv = './logs/ttyUSB1.csv'
    usb2 = threading.Thread(target=listen, args=('/dev/ttyUSB1', './logs/ttyUSB1.log', usb2_csv))
    usb2.start()

    while True:
        data = input("Press Enter to separation values > ...")
        with open(usb1_csv, 'a+') as csv_file:
            csv_writer = DictWriter(csv_file, CSV_FIELDNAMES, delimiter=';')
            csv_writer.writerow({'cmd': '', 'adc_a': '', 'adc_b': '', 'ts': '', 'created_at': ''})
        with open(usb2_csv, 'a+') as csv_file:
            csv_writer = DictWriter(csv_file, CSV_FIELDNAMES, delimiter=';')
            csv_writer.writerow({'cmd': '', 'adc_a': '', 'adc_b': '', 'ts': '', 'created_at': ''})
