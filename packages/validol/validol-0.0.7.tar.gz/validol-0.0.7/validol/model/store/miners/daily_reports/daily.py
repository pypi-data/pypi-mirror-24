import datetime as dt

from validol.model.utils import date_range
from validol.model.store.resource import Resource
from validol.model.store.miners.weekly_reports.flavor import Platforms
from validol.model.utils import concat


class DailyResource(Resource):
    SCHEMA = [
        ('CONTRACT', 'TEXT'),
        ('SET', 'REAL'),
        ('CHG', 'REAL'),
        ('VOL', 'INTEGER'),
        ('OI', 'INTEGER'),
        ('OIChg', 'INTEGER')
    ]

    def __init__(self, model_launcher, platform_code, active_name, actives_cls, flavor,
                 pdf_helper):
        self.model_launcher = model_launcher
        self.pdf_helper = pdf_helper

        active_id = actives_cls(model_launcher).get_fields(platform_code, active_name, ('id',))[0]
        platform_id = Platforms(model_launcher, flavor).get_platform_id(platform_code)

        Resource.__init__(
            self,
            model_launcher.main_dbh,
            "Active_platform_{platform_id}_active_{active_id}_{flavor}".format(
                platform_id=platform_id,
                active_id=active_id,
                flavor=flavor),
            DailyResource.SCHEMA,
            "UNIQUE (Date, CONTRACT) ON CONFLICT IGNORE")

    def get_flavors(self):
        df = self.read_df('SELECT DISTINCT CONTRACT AS active_flavor FROM "{table}"', index_on=False)

        return df

    def get_flavor(self, contract):
        return self.read_df('SELECT * FROM "{table}" WHERE CONTRACT = ?', params=(contract,))

    def download_dates(self, dates):
        return concat([self.download_date(date) for date in dates])

    def initial_fill(self):
        df = self.pdf_helper.initial(self.model_launcher)

        if not df.empty:
            net_df = self.fill(max(df.Date), dt.date.today())
        else:
            net_df = self.download_dates(self.available_dates())

        return df.append(net_df)

    def fill(self, first, last):
        return self.download_dates(set(self.available_dates()) & set(date_range(first, last)))

    def available_dates(self):
        raise NotImplementedError

    def download_date(self, date):
        raise NotImplementedError