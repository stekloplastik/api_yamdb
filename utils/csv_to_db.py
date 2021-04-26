import csv
import logging

from django.db import IntegrityError, transaction


def fill_db(file_path, model):
    with open(file_path, newline='') as csv_file:
        file_reader = csv.reader(csv_file, delimiter=',')
        model_fields = next(file_reader)
        for row in file_reader:
            attr_dict = {
                model_fields[n]: row[n]
                for n in range(len(model_fields))
            }
            try:
                with transaction.atomic():
                    model(**attr_dict).save()
            except IntegrityError:
                logging.warning(
                    f'{model.__name__} '
                    f'with {row} params already exists'
                )
