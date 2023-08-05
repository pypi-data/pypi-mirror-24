#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy.tests.helper import assert_quantity_allclose, remote_data
from astropy import units as apu
from ...pathprof import srtm
from ...utils import check_astro_quantities


TOL_KWARGS = {'atol': 1.e-4, 'rtol': 1.e-4}


@pytest.fixture(scope='session')
def srtm_temp_dir(tmpdir_factory):

    tdir = tmpdir_factory.mktemp('srtmdata')
    return str(tdir)


class TestSrtmConf:

    def test_context_manager(self):

        srtm_dir = srtm.SrtmConf.srtm_dir
        download = srtm.SrtmConf.download

        with srtm.SrtmConf.set(srtm_dir='bar', download='always'):
            pass

        assert srtm_dir == srtm.SrtmConf.srtm_dir
        assert download == srtm.SrtmConf.download

    def test_getter(self):

        assert srtm.SrtmConf.srtm_dir == os.environ.get('SRTMDATA', '.')
        assert srtm.SrtmConf.download == 'never'
        assert srtm.SrtmConf.server == 'nasa_v2.1'

    def test_setter(self):

        with srtm.SrtmConf.set(srtm_dir='foo'):
            assert srtm.SrtmConf.srtm_dir == 'foo'
            assert srtm.SrtmConf.download == 'never'
            assert srtm.SrtmConf.server == 'nasa_v2.1'

        with srtm.SrtmConf.set(download='missing'):
            assert srtm.SrtmConf.srtm_dir == os.environ.get('SRTMDATA', '.')
            assert srtm.SrtmConf.download == 'missing'
            assert srtm.SrtmConf.server == 'nasa_v2.1'

        with srtm.SrtmConf.set(srtm_dir='bar', download='always'):
            assert srtm.SrtmConf.srtm_dir == 'bar'
            assert srtm.SrtmConf.download == 'always'
            assert srtm.SrtmConf.server == 'nasa_v2.1'

        with pytest.raises(RuntimeError):
            srtm.SrtmConf.srtm_dir = 'bar'

        with pytest.raises(RuntimeError):
            srtm.SrtmConf()

    def test_validation(self):

        with pytest.raises(TypeError):
            with srtm.SrtmConf.set(1):
                pass

        with pytest.raises(ValueError):
            with srtm.SrtmConf.set(srtm_dir=1):
                pass

        with pytest.raises(ValueError):
            with srtm.SrtmConf.set(foo='bar'):
                pass

        with pytest.raises(ValueError):
            with srtm.SrtmConf.set(download='bar'):
                pass

        with pytest.raises(ValueError):
            with srtm.SrtmConf.set(server='bar'):
                pass


def test_hgt_filename():

    cases = [
        (10, 10, 'N10E010.hgt'),
        (0, 20, 'N20E000.hgt'),
        (0, 0, 'N00E000.hgt'),
        (-1, -1, 'S01W001.hgt'),
        (-10, -1, 'S01W010.hgt'),
        (10, -1, 'S01E010.hgt'),
        (19, 18, 'N18E019.hgt'),
        (28, 35, 'N35E028.hgt'),
        (-24, -1, 'S01W024.hgt'),
        (-111, -40, 'S40W111.hgt'),
        (119, 12, 'N12E119.hgt'),
        (86, -46, 'S46E086.hgt'),
        (147, -54, 'S54E147.hgt'),
        (-20, -71, 'S71W020.hgt'),
        (-46, -79, 'S79W046.hgt'),
        (-46, -22, 'S22W046.hgt'),
        (6, 25, 'N25E006.hgt'),
        (67, -22, 'S22E067.hgt'),
        (63, -38, 'S38E063.hgt'),
        (-97, 51, 'N51W097.hgt'),
        (148, -38, 'S38E148.hgt'),
        (53, 39, 'N39E053.hgt'),
        (27, -67, 'S67E027.hgt'),
        (57, 20, 'N20E057.hgt'),
        (109, -31, 'S31E109.hgt'),
        (-143, 74, 'N74W143.hgt'),
        ]

    for ilon, ilat, name in cases:
        assert srtm._hgt_filename(ilon, ilat) == name


def test_extract_hgt_coords():

    cases = [
        (10, 10, 'N10E010.hgt'),
        (0, 20, 'N20E000.hgt'),
        (0, 0, 'N00E000.hgt'),
        (-1, -1, 'S01W001.hgt'),
        (-10, -1, 'S01W010.hgt'),
        (10, -1, 'S01E010.hgt'),
        (19, 18, 'N18E019.hgt'),
        (28, 35, 'N35E028.hgt'),
        (-24, -1, 'S01W024.hgt'),
        (-111, -40, 'S40W111.hgt'),
        (119, 12, 'N12E119.hgt'),
        (86, -46, 'S46E086.hgt'),
        (147, -54, 'S54E147.hgt'),
        (-20, -71, 'S71W020.hgt'),
        (-46, -79, 'S79W046.hgt'),
        (-46, -22, 'S22W046.hgt'),
        (6, 25, 'N25E006.hgt'),
        (67, -22, 'S22E067.hgt'),
        (63, -38, 'S38E063.hgt'),
        (-97, 51, 'N51W097.hgt'),
        (148, -38, 'S38E148.hgt'),
        (53, 39, 'N39E053.hgt'),
        (27, -67, 'S67E027.hgt'),
        (57, 20, 'N20E057.hgt'),
        (109, -31, 'S31E109.hgt'),
        (-143, 74, 'N74W143.hgt'),
        ]

    for ilon, ilat, name in cases:
        assert srtm._extract_hgt_coords(name) == (ilon, ilat)


def test_check_availability_nasa():

    nasa_tiles = [
        ('Australia', 1060),
        ('South_America', 1807),
        ('Islands', 141),
        ('Africa', 3250),
        ('Eurasia', 5876),
        ('North_America', 2412),
        ]

    for k, v in nasa_tiles:

        assert v == len(srtm.NASA_TILES[k])

    nasa_cases = [
        (19, 18, 'Africa'),
        (28, 35, None),
        (-24, -1, None),
        (-111, -40, None),
        (119, 12, 'Eurasia'),
        (86, -46, None),
        (147, -54, None),
        (-20, -71, None),
        (-46, -79, None),
        (-46, -22, 'South_America'),
        (6, 25, 'Africa'),
        (67, -22, None),
        (63, -38, None),
        (-97, 51, 'North_America'),
        (148, -38, 'Australia'),
        (53, 39, 'Eurasia'),
        (27, -67, None),
        (57, 20, 'Africa'),
        (109, -31, None),
        (-143, 74, None),
        ]

    for ilon, ilat, name in nasa_cases:

        if name is None:
            with pytest.raises(srtm.TileNotAvailable):
                srtm._check_availability(ilon, ilat)
        else:
            assert srtm._check_availability(ilon, ilat) == name


def test_check_availability_pano():

    assert srtm.VIEWPANO_TILES.size == 19297

    pano_cases = [
        (19, 18, 'E34.zip'),
        (28, 35, None),
        (-24, -1, None),
        (-111, -40, None),
        (119, 12, 'D50.zip'),
        (86, -46, None),
        (147, -54, None),
        (-20, -71, None),
        (-46, -79, None),
        (-46, -22, 'SF23.zip'),
        (6, 25, 'G32.zip'),
        (67, -22, None),
        (63, -38, None),
        (-97, 51, 'M14.zip'),
        (148, -38, 'SJ55.zip'),
        (53, 39, 'J39.zip'),
        (27, -67, None),
        (57, 20, 'F40.zip'),
        (109, -31, None),
        (-143, 74, None),
        ]

    with srtm.SrtmConf.set(server='viewpano'):

        for ilon, ilat, name in pano_cases:

            if name is None:
                with pytest.raises(srtm.TileNotAvailable):
                    srtm._check_availability(ilon, ilat)
            else:
                assert srtm._check_availability(ilon, ilat) == name


@remote_data(source='any')
def test_download_nasa(srtm_temp_dir):

    ilon, ilat = 6, 50
    tile_name = srtm._hgt_filename(ilon, ilat)

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir, server='nasa_v2.1'):

        srtm._download(ilon, ilat)

        dl_path = srtm._get_hgt_diskpath(tile_name)

        assert dl_path is not None

        assert dl_path.startswith(srtm_temp_dir)
        assert dl_path.endswith(tile_name)


@remote_data(source='any')
def test_download_pano(srtm_temp_dir):

    ilon, ilat = -175, -4
    tile_name = srtm._hgt_filename(ilon, ilat)

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir, server='viewpano'):

        srtm._download(ilon, ilat)

        dl_path = srtm._get_hgt_diskpath(tile_name)

        assert dl_path is not None

        assert dl_path.startswith(srtm_temp_dir)
        assert dl_path.endswith(tile_name)


def test_get_hgt_diskpath(srtm_temp_dir):

    # getting the correct files was already tested above
    # checking the behavior for problematic cases

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        assert srtm._get_hgt_diskpath('foo.hgt') is None

        os.makedirs(os.path.join(srtm_temp_dir, 'd1'))
        os.makedirs(os.path.join(srtm_temp_dir, 'd2'))
        open(os.path.join(srtm_temp_dir, 'd1', 'foo.hgt'), 'w').close()
        open(os.path.join(srtm_temp_dir, 'd2', 'foo.hgt'), 'w').close()

        with pytest.raises(IOError):
            srtm._get_hgt_diskpath('foo.hgt')


@remote_data(source='any')
def test_get_hgt_file_download_never(srtm_temp_dir):

    print(srtm.SrtmConf.srtm_dir)
    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        ilon, ilat = 6, 50
        tile_name = srtm._hgt_filename(ilon, ilat)
        tile_path = srtm.get_hgt_file(ilon, ilat)

        assert tile_path.endswith(tile_name)

        ilon, ilat = -175, -4
        tile_name = srtm._hgt_filename(ilon, ilat)
        tile_path = srtm.get_hgt_file(ilon, ilat)

        assert tile_path.endswith(tile_name)

        ilon, ilat = 12, 50
        tile_name = srtm._hgt_filename(ilon, ilat)

        with pytest.raises(IOError):
            srtm.get_hgt_file(ilon, ilat)


@remote_data(source='any')
def test_get_hgt_file_download_missing(srtm_temp_dir):

    print(srtm.SrtmConf.srtm_dir)
    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir, download='missing'):

        ilon, ilat = 12, 50
        tile_name = srtm._hgt_filename(ilon, ilat)
        tile_path = srtm.get_hgt_file(ilon, ilat)

        assert tile_path.endswith(tile_name)


@remote_data(source='any')
def test_get_hgt_file_download_always(srtm_temp_dir):

    # store last mtime for comparison
    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        ilon, ilat = 12, 50
        tile_path = srtm.get_hgt_file(ilon, ilat)
        mtime1 = os.path.getmtime(tile_path)

    print(srtm.SrtmConf.srtm_dir)
    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir, download='always'):

        ilon, ilat = 12, 50
        tile_path = srtm.get_hgt_file(ilon, ilat)
        mtime2 = os.path.getmtime(tile_path)

    print(mtime1, mtime2)
    assert mtime1 != mtime2


@remote_data(source='any')
def test_get_tile_data(srtm_temp_dir):

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        ilon, ilat = 12, 50
        lons, lats, tile = srtm.get_tile_data(ilon, ilat)

        assert_allclose(lons[::250, 0], np.array([
            12., 12.20833333, 12.41666667, 12.625, 12.83333333
            ]))
        assert_allclose(lats[0, ::250], np.array([
            50., 50.20833333, 50.41666667, 50.625, 50.83333333
            ]))
        assert_allclose(tile[::250, ::250], np.array([
            [776., 543., 542., 622., 652.],
            [562., 641., 470., 471., 480.],
            [522., 487., 733., 939., 970.],
            [466., 359., 454., 518., 560.],
            [335., 319., 255., 342., 339.]
            ]))


def test_get_tile_zero(srtm_temp_dir):

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        # ilon, ilat = 6, 54
        ilon, ilat = 28, 35
        lons, lats, tile = srtm.get_tile_data(ilon, ilat)

        assert_allclose(lons[::250, 0], np.array([
            28., 28.20833333, 28.41666667, 28.625, 28.83333333
            ]))
        assert_allclose(lats[0, ::250], np.array([
            35., 35.20833333, 35.41666667, 35.625, 35.83333333
            ]))
        assert_allclose(tile[::250, ::250], np.zeros((5, 5), dtype=np.float32))


@remote_data(source='any')
def test_srtm_height_data(srtm_temp_dir):

    args_list = [
        (-180, 180, apu.deg),
        (-90, 90, apu.deg),
        ]
    check_astro_quantities(srtm.srtm_height_data, args_list)

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        lons = np.arange(12.1, 12.91, 0.2) * apu.deg
        lats = np.arange(50.1, 50.91, 0.2) * apu.deg
        heights = srtm.srtm_height_data(lons, lats)

        assert_quantity_allclose(heights, np.array([
            581., 559., 708., 467., 294.
            ]) * apu.m)


def test_srtm_height_data_zero(srtm_temp_dir):

    with srtm.SrtmConf.set(srtm_dir=srtm_temp_dir):

        lons = np.arange(28.1, 28.91, 0.2)
        lats = np.arange(35.1, 35.91, 0.2)
        heights = srtm._srtm_height_data(lons, lats)

        assert_allclose(heights, np.zeros(5, dtype=np.float32))
