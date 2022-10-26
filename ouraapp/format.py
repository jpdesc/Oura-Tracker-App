from datetime import date


def format_date(date):
    '''Format date for display on wellness dashboard.'''
    return date.strftime("%A, %B %-dth")


def str_fmt_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')


def date_fmt_str(string):
    return date.strptime(string, '%Y-%m-%d')
