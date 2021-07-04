import capture2
import csv

print("HI")
with open('settings.csv') as csv_file:
    print("HI")
    csv_reader = csv.reader(csv_file, delimiter=',')

    next(csv_reader)
    lang_processing_settings = next(csv_reader)

    capture2.main(str(lang_processing_settings[3]), str(lang_processing_settings[4]))
