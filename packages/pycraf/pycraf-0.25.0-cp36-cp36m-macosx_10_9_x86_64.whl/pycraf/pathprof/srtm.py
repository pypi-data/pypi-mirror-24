#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Note, there are various versions of SRTM data. Quasi-official are Versions 1
and 2.1 available on https://dds.cr.usgs.gov/srtm/. There is even a NASA
version 3, but we couldn't find a site for direct download. It may work
with an EarthData Account on https://lpdaac.usgs.gov/data_access/data_pool.

Then, there is V4.1 by CGIAR
(ftp://srtm.csi.cgiar.org/SRTM_V41/SRTM_Data_GeoTiff/)
and an unofficial version by viewfinderpanoramas.org (see
http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm).

For automatic download we should use the 2.1 version by NASA. V4.1 is in
GeoTiff format, which we currently don't support. viewfinderpanoramas.org
is probably superior to 2.1 (maybe even to V4.1), but not official.

V4.1 and viewfinderpanoramas forbid commercial use (without explicit
permission).
'''


from __future__ import (
    absolute_import, unicode_literals, division, print_function
    )

# from functools import partial, lru_cache
import os
import shutil
from zipfile import ZipFile
import re
import json
import glob
from functools import lru_cache
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from astropy.utils.data import get_pkg_data_filename, download_file
from astropy import units as apu
from .. import utils


__all__ = ['SrtmConf', 'srtm_height_data']


HGT_RES = 90.  # m; equivalent to 3 arcsec resolution

_NASA_JSON_NAME = get_pkg_data_filename('data/nasa.json')
_VIEWPANO_NAME = get_pkg_data_filename('data/viewpano.npy')

with open(_NASA_JSON_NAME, 'r') as f:
    NASA_TILES = json.load(f)

VIEWPANO_TILES = np.load(_VIEWPANO_NAME)


class TileNotAvailable(Exception):

    pass


class SrtmConf(utils.MultiState):
    '''
    Provide a global state to adjust SRTM configuration.

    By default, `~pycraf` will look for SRTM '.hgt' files (the terrain data)
    in the SRTMDATA environment variable. If this is not defined, the
    local directory ('./') is used for look-up. It is possible during
    run-time to change the directory where to look for '.hgt' files
    with the `SrtmConf` manager::

        from pycraf.pathprof import SrtmConf
        SrtmConf.set(srtm_dir='/path/to/srtmdir')

    Alternatively, if only a temporary change of the config is desired,
    one can use `SrtmConf` as a context manager::

        with SrtmConf.set(srtm_dir='/path/to/srtmdir'):
            # do stuff

    Afterwards, the old settings will be re-established.

    It is also possible to allow downloading of missing '.hgt' files::

        SrtmConf.set(download='missing')

    The default behavior is to not download anything (`download='never'`).
    There is even an option, to always force download (`download='always'`).

    The default download server will be `server='nasa_v2.1'`. One could
    also use the (very old) data (`server='nasa_v1.0'`) or inofficial
    tiles from viewfinderpanorama (`server='viewpano'`).

    URLS:

    - `nasa_v2.1 <https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/>`__
    - `nasa_v1.0 <https://dds.cr.usgs.gov/srtm/version1/>`__
    - `viewpano <http://www.viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm>`__
    '''

    _attributes = ('srtm_dir', 'download', 'server')

    # default values
    srtm_dir = os.environ.get('SRTMDATA', '.')
    download = 'never'
    server = 'nasa_v2.1'

    @classmethod
    def validate(cls, **kwargs):
        '''
        This checks, if the provided inputs for `download` and `server` are
        allowed. Possible values are:

        - `download`:  'never', 'missing', 'always'
        - `server`:  'nasa_v2.1', 'nasa_v1.0', 'viewpano'

        '''

        for k, v in kwargs.items():

            if k == 'srtm_dir':
                if not isinstance(v, str):
                    raise ValueError(
                        '"srtm_dir" option must be a string.'
                        )

            if k == 'download':
                if v not in ['never', 'missing', 'always']:
                    raise ValueError(
                        'Only the values "never", "missing", and "always" '
                        'are supported for "download" option.'
                        )
            if k == 'server':
                if v not in ['nasa_v2.1', 'nasa_v1.0', 'viewpano']:
                    raise ValueError(
                        'Only the values "nasa_v2.1", "nasa_v1.0", and '
                        '"viewpano" are supported for "server" option.'
                        )

        return kwargs


def _hgt_filename(ilon, ilat):
    # construct proper hgt-file name

    return '{:1s}{:02d}{:1s}{:03d}.hgt'.format(
        'N' if ilat >= 0 else 'S',
        abs(ilat),
        'E' if ilon >= 0 else 'W',
        abs(ilon),
        )


def _check_availability(ilon, ilat):
    # check availability of a tile on download servers
    # returns continent name (for NASA server) or zip file name (Pano)

    server = SrtmConf.server
    tile_name = _hgt_filename(ilon, ilat)

    if server.startswith('nasa_v'):

        for continent, tiles in NASA_TILES.items():
            if tile_name in tiles:
                break
        else:
            raise TileNotAvailable(
                'No tile found for ({}d, {}d) in list of available '
                'tiles.'.format(
                    ilon, ilat
                    ))

        return continent

    elif server == 'viewpano':

        tiles = VIEWPANO_TILES['tile']
        idx = np.where(tiles == tile_name)

        if len(tiles[idx]) == 0:
            raise TileNotAvailable(
                'No tile found for ({}d, {}d) in list of available '
                'tiles.'.format(
                    ilon, ilat
                    ))

        return VIEWPANO_TILES['zipfile'][idx][0]

    return None  # should not happen


def _download(ilon, ilat):
    # download the tile to path

    srtm_dir = SrtmConf.srtm_dir
    server = SrtmConf.server

    tile_name = _hgt_filename(ilon, ilat)
    tile_path = os.path.join(srtm_dir, tile_name)

    # Unfortunately, each server has a different structure.
    # NASA stores them in sub-directories (by continents)
    # Panoramic-Viewfinders has a flat structure but has several hgt tiles
    # zipped in a file

    # Furthermore, we need to check against the available tiles
    # (ocean tiles and polar caps are not present); we also do this
    # in the _get_hgt_file function (because it's not only important
    # for downloading). However, we have to figure out, in which
    # subdirectory/zip-file a tile is located.

    if server.startswith('nasa_v'):

        if server == 'nasa_v1.0':
            base_url = 'https://dds.cr.usgs.gov/srtm/version1/'
        elif server == 'nasa_v2.1':
            base_url = 'https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/'

        continent = _check_availability(ilon, ilat)

        # downloading
        full_url = base_url + continent + '/' + tile_name + '.zip'
        tmp_path = download_file(full_url)

        # move to srtm_dir
        shutil.move(tmp_path, tile_path + '.zip')

        # unpacking
        with ZipFile(tile_path + '.zip', 'r') as zf:
            zf.extractall(srtm_dir)

        os.remove(tile_path + '.zip')

    elif server == 'viewpano':

        base_url = 'http://viewfinderpanoramas.org/dem3/'

        zipfile_name = _check_availability(ilon, ilat)
        super_tile_path = os.path.join(srtm_dir, zipfile_name)

        # downloading
        full_url = base_url + zipfile_name
        tmp_path = download_file(full_url)

        # move to srtm_dir
        shutil.move(tmp_path, super_tile_path)

        # unpacking
        with ZipFile(super_tile_path, 'r') as zf:
            zf.extractall(srtm_dir)

        os.remove(super_tile_path)


def _extract_hgt_coords(hgt_name):
    '''
    Extract coordinates from hgt-filename (lower left corner).

    Properly handles EW and NS substrings. Longitude range: -180 .. 179 deg
    '''

    _codes = {'E': 1, 'W': -1, 'N': 1, 'S': -1}

    yc, wy0, xc, wx0 = re.search(
        ".*([NS])(-?\d*)([EW])(\d*).hgt.*", hgt_name
        ).groups()

    return _codes[xc] * int(wx0), _codes[yc] * int(wy0)


def _get_hgt_diskpath(tile_name):
    # check, if a tile already exists in srtm directory (recursive)

    srtm_dir = SrtmConf.srtm_dir
    _files = glob.glob(os.path.join(srtm_dir, '**', tile_name), recursive=True)

    if len(_files) > 1:
        raise IOError('{} exists {} times in {}'.format(
            tile_name, len(_files), srtm_dir
            ))
    elif len(_files) == 0:
        return None
    else:
        return _files[0]


def get_hgt_file(ilon, ilat):

    _check_availability(ilon, ilat)

    srtm_dir = SrtmConf.srtm_dir
    tile_name = _hgt_filename(ilon, ilat)
    hgt_file = _get_hgt_diskpath(tile_name)

    download = SrtmConf.download
    if download == 'always' or (hgt_file is None and download == 'missing'):

        _download(ilon, ilat)

    hgt_file = _get_hgt_diskpath(tile_name)
    if hgt_file is None:
        raise IOError(
            'No hgt-file found for ({}d, {}d), was looking for {}\n'
            'in directory: {}'.format(
                ilon, ilat, tile_name, srtm_dir
                ))

    return hgt_file


def get_tile_data(ilon, ilat):
    # angles in deg

    tile_size = 1201
    dx = dy = 1. / (tile_size - 1)
    x, y = np.ogrid[0:tile_size, 0:tile_size]
    lons, lats = x * dx + ilon, y * dy + ilat

    try:
        hgt_file = get_hgt_file(ilon, ilat)
        tile = np.fromfile(hgt_file, dtype='>i2')
        tile = tile.reshape((tile_size, tile_size))[::-1]

        bad_mask = (tile == 32768) | (tile == -32768)
        tile = tile.astype(np.float32)
        tile[bad_mask] = np.nan

    except TileNotAvailable:
        tile = np.zeros((tile_size, tile_size), dtype=np.float32)

    return lons, lats, tile


@lru_cache(maxsize=36, typed=False)
def get_tile_interpolator(ilon, ilat):
    # angles in deg

    lons, lats, tile = get_tile_data(ilon, ilat)
    # have to treat NaNs in some way; set to zero for now
    tile = np.nan_to_num(tile)

    _tile_interpolator = RegularGridInterpolator(
        (lons[:, 0], lats[0]), tile.T
        )

    return _tile_interpolator


def _srtm_height_data(lons, lats):
    # angles in deg

    # coordinates could span different tiles, so first get the unique list
    lons = np.atleast_1d(lons)
    lats = np.atleast_1d(lats)

    assert lons.ndim == 1 and lats.ndim == 1

    heights = np.empty(lons.shape, dtype=np.float32)

    ilons = np.floor(lons).astype(np.int32)
    ilats = np.floor(lats).astype(np.int32)

    uilonlats = set((a, b) for a, b in zip(ilons, ilats))

    for uilon, uilat in uilonlats:

        mask = (ilons == uilon) & (ilats == uilat)
        heights[mask] = get_tile_interpolator(uilon, uilat)(
            (lons[mask], lats[mask])
            )

    return heights


@utils.ranged_quantity_input(
    lons=(-180, 180, apu.deg),
    lats=(-90, 90, apu.deg),
    strip_input_units=True,
    output_unit=apu.m
    )
def srtm_height_data(lons, lats):
    '''
    SRTM terrain data (bi-linearly interpolated) extracted from ".hgt" files.

    Parameters
    ----------
    lons, lats : `~astropy.units.Quantity`
        Geographic longitudes/latitudes for which to return height data [deg]

    Returns
    -------
    heights : `~astropy.units.Quantity`
        SRTM heights [m]

    Notes
    -----
    - `distances` contains distances from Transmitter.
    - `SRTM data <https://www2.jpl.nasa.gov/srtm/>`_ need to be downloaded
      manually by the user. An environment variable `SRTMDATA` has to be
      set to point to the directory containing the .hgt files; see
      :ref:`srtm_data`.
    '''

    return _srtm_height_data(lons, lats)


if __name__ == '__main__':
    print('This not a standalone python program! Use as module.')
