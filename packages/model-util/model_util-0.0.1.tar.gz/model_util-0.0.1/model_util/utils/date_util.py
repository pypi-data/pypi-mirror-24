# coding:utf-8
import calendar
import datetime


class DateUtil(object):
    @staticmethod
    def to_datetime(date, date_format='%Y-%m-%d'):
        a = datetime.datetime.strptime(date, date_format)
        return a

    @staticmethod
    def to_date(date, date_format='%Y-%m-%d'):
        a = datetime.datetime.strptime(date, date_format).date()
        return a

    @staticmethod
    def to_string(date, date_format='%Y-%m-%d'):
        return date.strftime(date_format)

    @staticmethod
    def get_today(date_format='%Y-%m-%d'):
        return datetime.datetime.today().strftime(date_format)

    @staticmethod
    def get_yesterday(date_format='%Y-%m-%d'):
        return (datetime.date.today() + datetime.timedelta(days=-1)).strftime(date_format)

    @staticmethod
    def date_add(date='', day=0, date_format='%Y-%m-%d'):
        a_datetime = datetime.datetime.strptime(date, date_format)
        b_datetime = a_datetime + datetime.timedelta(days=day)
        return b_datetime.strftime(date_format)

    @staticmethod
    def add_months(date='', months=0, date_format='%Y-%m-%d'):
        source_date = datetime.datetime.strptime(date, date_format)
        month = source_date.month - 1 + months
        year = int(source_date.year + month / 12)
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    @staticmethod
    def add_years(date='', years=0, date_format='%Y-%m-%d'):
        source_date = datetime.datetime.strptime(date, date_format)
        new_year = source_date.year + years
        if (source_date.month == 2 and source_date.day == 29 and  # leap day
                calendar.isleap(source_date.year) and not calendar.isleap(new_year)):
            new_date = source_date.replace(year=new_year, day=28)
        else:
            new_date = source_date.replace(year=new_year)
        return new_date.strftime(date_format)

    @staticmethod
    def date_add_to_datetime(date='', day=0, date_format='%Y-%m-%d'):
        a = datetime.datetime.strptime(date, date_format)
        b = a + datetime.timedelta(days=day)
        return b

    @staticmethod
    def date_add_to_date(date='', day=0, date_format='%Y-%m-%d'):
        a = datetime.datetime.strptime(date, date_format).date()
        b = a + datetime.timedelta(days=day)
        return b

    @staticmethod
    def datetime_offset_by_month(datetime1, n=1):
        # create a shortcut object for one day
        one_day = datetime.timedelta(days=1)

        # first use div and mod to determine year cycle
        q, r = divmod(datetime1.month + n, 12)

        # create a datetime2
        # to be the last day of the target month
        datetime2 = datetime.datetime(
            datetime1.year + q, r + 1, 1) - one_day

        # if input date is the last day of this month
        # then the output date should also be the last
        # day of the target month, although the day
        # may be different.
        # for example:
        # datetime1 = 8.31
        # datetime2 = 9.30
        if datetime1.month != (datetime1 + one_day).month:
            return datetime2

        # if datetime1 day is bigger than last day of
        # target month, then, use datetime2
        # for example:
        # datetime1 = 10.31
        # datetime2 = 11.30
        if datetime1.day >= datetime2.day:
            return datetime2

        # then, here, we just replace datetime2's day
        # with the same of datetime1, that's ok.
        return datetime2.replace(day=datetime1.day)

    @staticmethod
    def get_last_day_of_last_month(date):
        '''
         获取上一个月的最后一天
        :return:
        '''
        today = DateUtil.to_datetime(date)
        first = datetime.date(day=1, month=today.month, year=today.year)
        lastMonth = first - datetime.timedelta(days=1)
        return lastMonth

    @staticmethod
    def is_last_day(date_str):
        '''
        判断是不是月末
        :param date:
        :return:
        '''
        pre_day = DateUtil.to_date(date_str) + datetime.timedelta(days=1)
        if pre_day.day == 1:
            return True
        return False
