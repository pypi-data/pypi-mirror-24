#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Fork of dectris cbf header reader
"""

import os
import re
import copy
import time
import ctypes
import base64
import hashlib
from datetime import datetime
import numpy as np
from . import templates, ImageError, _cryio

NON_OPTIONAL_KEYWORDS = {
    # key: (pattern, [value_indeces], type)
    'Detector_identifier': ('Detector ', [slice(1, None)], str),
    'Pixel_size': ('Pixel_size', [1, 4], float),
    'Silicon': ('Silicon', [3], float),
    'Exposure_time': ('Exposure_time', [1], float),
    'Exposure_period': ('Exposure_period', [1], float),
    'Tau': ('Tau', [1], float),
    'Count_cutoff': ('Count_cutoff', [1], int),
    'Threshold_setting': ('Threshold_setting', [1], float),
    'Gain_setting': ('Gain_setting', [1, 2], str),
    'N_excluded_pixels': ('N_excluded_pixels', [1], int),
    'Excluded_pixels': ('Excluded_pixels', [1], str),
    'Flat_field': ('Flat_field', [1], str),
    'Trim_file': ('Trim_file', [1], str),
    'Image_path': ('Image_path', [1], str),
}

OPTIONAL_KEYWORDS = {
    'Wavelength': ('Wavelength', [1], float),
    'Energy_range': ('Energy_range', [1, 2], float),
    'Detector_distance': ('Detector_distance', [1], float),
    'Detector_Voffset': ('Detector_Voffset', [1], float),
    'Beam_xy': ('Beam_xy', [1, 2], float),
    'Beam_x': ('Beam_xy', [1], float),
    'Beam_y': ('Beam_xy', [2], float),
    'Flux': ('Flux', [1], float),
    'Filter_transmission': ('Filter_transmission', [1], float),
    'Start_angle': ('Start_angle', [1], float),
    'Angle_increment': ('Angle_increment', [1], float),
    'Detector_2theta': ('Detector_2theta', [1], float),
    'Polarization': ('Polarization', [1], float),
    'Alpha': ('Alpha', [1], float),
    'Kappa': ('Kappa', [1], float),
    'Phi': ('Phi', [1], float),
    'Phi_increment': ('Phi_increment', [1], float),
    'Omega': ('Omega', [1], float),
    'Omega_increment': ('Omega_increment', [1], float),
    'Chi': ('Chi', [1], float),
    'Chi_increment': ('Chi_increment', [1], float),
    'Oscillation_axis': ('Oscillation_axis', [slice(1, None)], str),
    'N_oscillations': ('N_oscillations', [1], int),
    'Start_position': ('Start_position', [1], float),
    'Position_increment': ('Position_increment', [1], float),
    'Shutter_time': ('Shutter_time', [1], float),
    'Temperature': ('Temperature', [1], float),
    'Blower': ('Blower', [1], float),
    'Lakeshore': ('Lakeshore', [1], float),
}

ALL_KEYWORDS = NON_OPTIONAL_KEYWORDS.copy()
ALL_KEYWORDS.update(OPTIONAL_KEYWORDS)
PILATUS2M = 1679, 1475
PILATUS6M = 2527, 2463
PILATUS300K = 619, 487
PILATUS1M = 1043, 981


class CbfError(ImageError):
    pass


class CbfHeader(object):
    SPACE_EQUIVALENT_CHARACTERS = '#:=,()'
    ALL_KEYWORDS = ALL_KEYWORDS
    pilatus_header_pattern = re.compile(r'''_array_data.header_convention +["']?(SLS|PILATUS)_\d+(\.?\d*)*["']?''')
    contents_pattern = re.compile(r'_array_data.header_contents\s+;.*?;', re.DOTALL)
    date_time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T|\d{4}/\D+/\d{2} )\d{2}:\d{2}:\d{2}.\d+')
    time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}.\d+')

    def __init__(self, filepath=None, non_binary_length=4096):
        self.filepath = filepath
        self.non_binary_length = non_binary_length
        self.header_dict = self.header = {}
        self.header_lines = []
        self.binary_header_dict = {}
        self.dt = None
        self.multiframe = False
        if self.filepath:
            self.name = os.path.basename(filepath)[:-4]
            self.parse()

    def parse(self):
        with open(self.filepath, 'rb') as f:
            cbfmmap = f.read()
            self._rawheader = cbfmmap[:self.non_binary_length].decode(errors='ignore')
            self.parse_header()
            self.parse_binary(cbfmmap)

    def read_header_lines(self):
        contents_match = CbfHeader.contents_pattern.search(self._rawheader)
        if contents_match is None:
            self.header_lines = []
            return
        # noinspection PyArgumentList
        self.header_lines = contents_match.group().splitlines()
        self.has_pilatus_cbf_convention = bool(contents_match)

    def _spaced_header_lines(self):
        spaced_header_lines = []
        for line in self.header_lines:
            for space_equivalent in CbfHeader.SPACE_EQUIVALENT_CHARACTERS:
                line = line.replace(space_equivalent, ' ')
            spaced_header_lines.append(line.strip().split())
        return spaced_header_lines

    def parse_header(self):
        self.read_header_lines()
        if not self.header_lines:
            self.read_header_lines()
        # parse the header lines
        spaced_header_lines = self._spaced_header_lines()
        for key, (pattern, valueindices, datatype) in CbfHeader.ALL_KEYWORDS.items():
            for line in spaced_header_lines:
                if pattern == line[0]:
                    values = []
                    for idx in valueindices:
                        try:
                            # handle multiple or single values
                            if isinstance(idx, slice):
                                values += line[idx]
                            else:
                                values.append(line[idx])
                        except IndexError:
                            pass
                    value = self._datatype_handling(values, key, datatype)
                    if value is not None:
                        self.header_dict[key] = value
        return self

    def _datatype_handling(self, values, key, datatype):
        # handle rare cases of value "not set"
        if not values:
            return 0
        if datatype is float and values[0] == 'not':
            # NON_OPTIONAL_KEYWORDS should always have value, at least NaN
            if key in NON_OPTIONAL_KEYWORDS:
                return float('NaN')
            else:
                return None
        # do the conversion for standard cases
        if len(values) == 1:
            try:
                values = datatype(values[0])
            except ValueError:
                return 0
        else:
            if datatype is str:
                values = ' '.join(values)
            else:
                values = tuple([datatype(v) for v in values])
        return values

    def get_beam_xy_mm(self, factor=1000):
        beam_xy, pixel_size = self.header_dict['Beam_xy'], self.header_dict['Pixel_size']
        return tuple([n * size * factor for n, size in zip(beam_xy, pixel_size)])

    def get_date_time(self):
        if not self.dt:
            self.dt = CbfHeader.date_time_pattern.search(self._rawheader).group().replace('T', ' ').split()
        return self.dt

    def get_date(self):
        return self.get_date_time()[0]

    def get_time(self):
        return self.get_date_time()[1]

    def dateTime(self):
        return datetime.strptime(' '.join(self.get_date_time()), '%Y-%m-%d %H:%M:%S.%f')

    def get_timestamp(self):
        dt = self.dateTime()
        return time.mktime(dt.timetuple()) + dt.microsecond * 1e-6

    date_time = property(get_date_time)
    time = property(get_time)

    def __getitem__(self, item):
        if item == 'Date':
            return self.get_date()
        elif item == 'Time':
            return self.get_time()
        elif item == '!File name':
            return os.path.basename(self.filepath)
        else:
            return self.header_dict[item]

    def get_flux(self):
        return self.header_dict['Flux']

    def parse_binary(self, cbfmmap):
        start_pos = self._rawheader.find('--CIF-BINARY-FORMAT-SECTION--')
        data_pos = cbfmmap.index(b'\xd5') + 1  # seems to be a start of the cbf packed data
        if start_pos == -1 or not data_pos:
            raise CbfError('CBF file %s seems to be non cbf-file :(' % self.name)

        bheader = cbfmmap[start_pos:data_pos].decode(errors='ignore').splitlines()
        for line in bheader:
            line = line.strip()
            try:
                key, val = line.split(':')
            except ValueError:
                continue
            val = val.strip()
            try:
                val = int(val)
            except ValueError:
                pass
            self.binary_header_dict[key] = val

        if 'X-Binary-Size' not in self.binary_header_dict:
            raise CbfError('CBF file {} seems to be corrupted, it does not contain X-Binary-Size '
                           'value in its header'.format(self.name))
        cbf_str = cbfmmap[data_pos:self.binary_header_dict['X-Binary-Size'] + data_pos]
        hsh = base64.b64encode(hashlib.md5(cbf_str).digest()).decode()
        if 'Content-MD5' not in self.binary_header_dict or hsh != self.binary_header_dict['Content-MD5']:
            raise CbfError('CBF file %s seems to be corrupted' % self.name)
        self.cbf_packed_bytes = cbf_str

    def save(self, filepath, fmt='cbf', **kwargs):
        try:
            # noinspection PyCallingNonCallable
            {
                'cbf': self.save_cbf,
            }[fmt](filepath, **kwargs)
        except KeyError:
            raise CbfError('Format is unknown')

    def save_cbf(self, filepath, **kwargs):
        cbf = {
            'name': os.path.basename(filepath)[:-4],
            'datetime': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
        }
        cbf.update(self.header_dict)
        cbf.update(self.binary_header_dict)
        cbf.update(kwargs)
        for key in cbf.copy():
            if '-' in key:
                cbf[key.replace('-', '_')] = cbf[key]
        rendered = templates.env.get_template('cbf').render(cbf)
        padding = ctypes.create_string_buffer(cbf['X-Binary-Size-Padding']).raw
        with open(filepath, 'wb') as f:
            f.write(rendered.encode())
            f.write(templates.cbfHead)
            f.write(self.cbf_packed_bytes)
            f.write(padding)
            f.write(templates.cbfTail)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result


class CbfImage(CbfHeader):
    SUMMABLE_HEADER_KEYS = ('Exposure_time', 'Exposure_period', 'Angle_increment',
                            'Flux', 'Omega_increment', 'Phi_increment', )

    def __init__(self, filepath=None, non_binary_length=4096):
        super(CbfImage, self).__init__(filepath, non_binary_length)
        self.transmission = 0

    def __iter__(self):
        yield self
        raise StopIteration

    def parse_binary(self, cbfmap):
        CbfHeader.parse_binary(self, cbfmap)
        shapeY = self.binary_header_dict['X-Binary-Size-Fastest-Dimension']
        shapeX = self.binary_header_dict['X-Binary-Size-Second-Dimension']
        self.array = np.asarray(_cryio._cbf_decode(shapeX, shapeY, self.cbf_packed_bytes))

    def save(self, filepath, fmt='cbf', **kwargs):
        try:
            {
                'cbf': self.save_cbf,
                'edf': self.save_edf,
            }[fmt](filepath, **kwargs)
        except KeyError:
            raise CbfError('Format is unknown')

    def save_cbf(self, filepath, **kwargs):
        shapeX, shapeY = self.array.shape[0], self.array.shape[1]
        pixels = shapeX * shapeY
        self.binary_header_dict['X-Binary-Size-Fastest-Dimension'] = shapeY
        self.binary_header_dict['X-Binary-Size-Second-Dimension'] = shapeX
        self.binary_header_dict['X-Binary-Number-of-Elements'] = pixels
        if 'X-Binary-Size-Padding' not in self.binary_header_dict:
            self.binary_header_dict['X-Binary-Size-Padding'] = 4095
        self.cbf_packed_bytes = bytes(_cryio._cbf_encode(self.array))
        self.binary_header_dict['X-Binary-Size'] = len(self.cbf_packed_bytes)
        self.binary_header_dict['Content-MD5'] = base64.b64encode(hashlib.md5(self.cbf_packed_bytes).digest()).decode()
        CbfHeader.save_cbf(self, filepath, **kwargs)

    def save_edf(self, filepath, **kwargs):
        try:
            edfInt = {
                'int16': np.int16,
                'int32': np.int32,
            }[kwargs['edfInt']]
        except KeyError:
            edfInt = np.int32
        shapeX, shapeY = self.array.shape[0], self.array.shape[1]
        array = self.array
        if 'edfFlip' not in kwargs or kwargs['edfFlip']:
            array = array[::-1]

        binary_blob = array.astype(edfInt).reshape((shapeX, shapeY)).tostring()
        edf = {
            'binsize': len(binary_blob),
            'headersize': 2560,
            'dim_1': shapeY,
            'dim_2': shapeX,
        }
        edf.update(kwargs)
        header = ''
        if 'edfHeader' not in kwargs or kwargs['edfHeader']:
            header = templates.env.get_template('edf').render(edf)
            header = '{}\n'.format(header[:-2]).encode('ascii', errors='ignore')
        with open(filepath, 'wb') as fedf:
            fedf.write(header)
            fedf.write(binary_blob)

    def __add__(self, other):
        if not isinstance(other, CbfImage):
            return self
        self.array += other.array
        for key in CbfImage.SUMMABLE_HEADER_KEYS:
            try:
                self.header_dict[key] += other.header_dict[key]
            except KeyError:
                continue
        return self

    def float(self):
        self.array = self.array.astype(np.float64)
        return self
