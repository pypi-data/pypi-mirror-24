import heliopy.data.wind as wind
import heliopy.data.mms as mms
import heliopy.data.helios as helios
import heliopy.data.cluster as cluster
import heliopy.data.ace as ace
import heliopy.data.artemis as artemis
import heliopy.data.imp as imp
import heliopy.data.ulysses as ulysses
import heliopy.data.messenger as messenger
from heliopy import config

import pandas as pd
from datetime import datetime
import urllib
import pytest


def check_datetime_index(df):
    'Helper funciton to check all dataframes have a datetime index'
    assert type(df.index[0]) == pd.Timestamp


@pytest.mark.data
class TestMessenger:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(2010, 1, 1, 0, 0, 0)
        self.endtime = datetime(2010, 1, 2, 1, 0, 0)

    def test_mag(self):
        df = messenger.mag_rtn(self.starttime, self.endtime)
        check_datetime_index(df)


@pytest.mark.data
class TestUlysses:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(1993, 1, 1, 0, 0, 0)
        self.endtime = datetime(1993, 1, 2, 0, 0, 0)

    def test_fgm_hires(self):
        df = ulysses.fgm_hires(self.starttime, self.endtime)
        check_datetime_index(df)

    def test_swoops_ions(self):
        df = ulysses.swoops_ions(self.starttime, self.endtime)
        check_datetime_index(df)


@pytest.mark.data
class TestArtemis:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(2008, 1, 1, 0, 0, 0)
        self.endtime = datetime(2008, 1, 2, 0, 0, 0)
        self.probe = 'a'

    def test_fgm(self):
        df = artemis.fgm(self.probe, 'h', 'dsl', self.starttime, self.endtime)
        check_datetime_index(df)

        with pytest.raises(ValueError):
            artemis.fgm('123', 'h', 'dsl', self.starttime, self.endtime)
        with pytest.raises(ValueError):
            artemis.fgm('1', '123', 'dsl', self.starttime, self.endtime)
        with pytest.raises(ValueError):
            artemis.fgm('1', 'h', '123', self.starttime, self.endtime)


@pytest.mark.data
class TestAce:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(2016, 1, 1, 0, 0, 0)
        self.endtime = datetime(2016, 1, 2, 0, 0, 0)

    def test_mfi_h0(self):
        df = ace.mfi_h0(self.starttime, self.endtime)
        check_datetime_index(df)


@pytest.mark.data
class TestImp:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(1976, 1, 1, 0, 0, 0)
        self.endtime = datetime(1976, 1, 2, 0, 0, 0)
        self.probe = '8'

    def test_mag320ms(self):
        df = imp.mag320ms(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)

    def test_mag15s(self):
        df = imp.mag15s(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)

    def test_mitplasma_h0(self):
        df = imp.mitplasma_h0(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)

    def test_mereged(self):
        df = imp.merged(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)


@pytest.mark.data
@pytest.mark.skipif(config['DEFAULT']['cluster_cookie'] == 'none',
                    reason='Cluster download cookie not set')
class TestCluster():
    @classmethod
    def setup_class(self):
        self.probe = '3'

    def test_fgm(self):
        starttime = datetime(2004, 6, 18, 11, 35, 0)
        endtime = datetime(2004, 6, 19, 18, 35, 0)
        df = cluster.fgm(self.probe, starttime, endtime)
        check_datetime_index(df)

    def test_peace_moments(self):
        starttime = datetime(2009, 12, 22, 4, 0, 0)
        endtime = datetime(2009, 12, 22, 6)
        df = cluster.peace_moments(self.probe, starttime, endtime)
        check_datetime_index(df)

    def test_cis_hia_onboard_moms(self):
        starttime = datetime(2009, 1, 1, 0, 0, 0)
        endtime = datetime(2009, 1, 1, 2, 0, 0)
        df = cluster.cis_hia_onboard_moms(self.probe, starttime, endtime)
        check_datetime_index(df)

    def test_cis_codif_h1_moms(self):
        starttime = datetime(2009, 1, 1, 0, 0, 0)
        endtime = datetime(2009, 1, 1, 2, 0, 0)
        df = cluster.cis_codif_h1_moms(self.probe, starttime, endtime)
        check_datetime_index(df)


@pytest.mark.data
class TestWind:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(2010, 1, 1, 0, 0, 0)
        self.endtime = datetime(2010, 1, 1, 23, 59, 59)

    def test_mfi_h0(self):
        df = wind.mfi_h0(self.starttime, self.endtime)
        check_datetime_index(df)

    def test_mfi_h2(self):
        df = wind.mfi_h2(self.starttime, self.endtime)
        check_datetime_index(df)

    def test_threedp_pm(self):
        df = wind.threedp_pm(self.starttime, self.endtime)
        check_datetime_index(df)

    def test_swe_h3(self):
        df = wind.swe_h3(self.starttime, self.endtime)


@pytest.mark.data
class TestMMS:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(2016, 1, 2, 0, 0, 0)
        self.endtime = datetime(2016, 1, 2, 1, 0, 0)
        self.probe = '1'

    def test_fgm_survey(self):
        df = mms.fgm_survey(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)

    def test_fpi_dis_moms(self):
        df = mms.fpi_dis_moms(self.probe, 'fast', self.starttime, self.endtime)
        check_datetime_index(df)


@pytest.mark.data
class TestHelios:
    @classmethod
    def setup_class(self):
        self.starttime = datetime(1976, 1, 10, 0, 0, 0)
        self.endtime = datetime(1976, 1, 10, 23, 59, 59)
        self.probe = '1'

    def test_merged(self):
        df = helios.merged(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)

        starttime = datetime(2000, 1, 1, 0, 0, 0)
        endtime = datetime(2000, 1, 2, 0, 0, 0)
        with pytest.raises(ValueError):
            helios.merged(self.probe, starttime, endtime)

    def test_6sec_ness(self):
        df = helios.mag_ness(self.probe, self.starttime, self.endtime)
        df = helios.mag_ness(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)

    def test_mag_4hz(self):
        df = helios.mag_4hz(self.probe, self.starttime, self.endtime)
        df = helios.mag_4hz(self.probe, self.starttime, self.endtime)
        check_datetime_index(df)
