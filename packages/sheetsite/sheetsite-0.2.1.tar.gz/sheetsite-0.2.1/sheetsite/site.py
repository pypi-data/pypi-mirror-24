from collections import OrderedDict
import json
import os
import re
import sys
from sheetsite.names import normalize_name
from sheetsite.filtered_spreadsheet import FilteredSpreadsheet
from sheetsite.merged_spreadsheet import MergedSpreadsheet

class Site(object):

    def __init__(self, spreadsheet, geocache_filename=None, censor=True):
        self.workbook = spreadsheet
        self.geocache_filename = geocache_filename
        self.censor = censor
        self.include = None
        self.exclude = None
        self.fill_columns = None
        self.add_columns = {}
        self.address_columns = {}
        self.merge_tables = None
        self.modify = True
        self.geocoder = None

    def add_sheet_filter(self, include, exclude):
        self.include = include
        self.exclude = exclude

    def add_column_fills(self, fill_columns):
        if fill_columns is None:
            self.fill_columns = None
            return
        self.fill_columns = [normalize_name(n) for n in fill_columns]

    def save_local(self, output_file, private_sheets=False, enhance=True):
        self.modify = enhance
        ext = '-'
        if output_file is not None:
            _, ext = os.path.splitext(output_file)
            ext = ext.lower()

        return self.save(output_file, private_sheets)

    def process_cells(self, rows, name):
        if not(self.modify):
            return rows
        rows = self.clean_cells(rows, name)
        rows = self.add_location(rows, name)
        return rows

    def filter(self, sheet, private_sheets):
        title = sheet.title
        core_title = re.sub(r'\(\((.*)\)\)', r'\1', title)
        if self.exclude is not None:
            if core_title in self.exclude:
                return None
        if self.include is not None:
            if core_title in self.include:
                return core_title
            return None
        if (core_title == title) == private_sheets:
            return None
        return core_title

    def private_workbook(self):
        return self.filtered_workbook(True)

    def public_workbook(self):
        return self.filtered_workbook(False)

    def merge(self, wb, merge_tables):
        if merge_tables is None:
            return wb
        return MergedSpreadsheet(wb, merge_tables)

    def filtered_workbook(self, selector_flags):
        workbook = self.merge(self.workbook, self.merge_tables)
        selector = lambda sheet: self.filter(sheet, selector_flags)
        processor = lambda sheet, title: self.process_cells(sheet.get_all_values(), title)
        fs = FilteredSpreadsheet(workbook, selector=selector, processor=processor)
        return fs

    def save(self, output_file, selector_flags):
        from sheetsite.destination import write_destination
        params = { 'output_file': output_file }
        state = { 'workbook': self.filtered_workbook(selector_flags) }
        write_destination(params, state)
        return True

    def sanity_stick(self, locs):
        result = []
        if len(locs) <= 1:
            return locs
        import re
        if len(re.sub(r'[^,]', '', locs[0])) < 3:
            return [' '.join(locs)]
        return locs

    def clean_cells(self, vals, name):
        if len(vals) == 0:
            return vals

        hide_column = {}
        split_column = {}
        for idx, cell in enumerate(vals[0]):
            if cell is None or len(cell)==0 or cell[0] == '(':
                hide_column[idx] = True
            if cell == "Other Addresses":
                split_column[idx] = '\n'

        results = []

        existing = {}
        for ridx, row in enumerate(vals):
            result = []
            for idx, cell in enumerate(row):
                if idx in hide_column:
                    continue
                if cell is not None:
                    try:
                        cell = re.sub(r'\(\(.*\)\)','', cell)
                        cell = re.sub(r'[\n\r]+$','', cell)
                        cell = re.sub(r'^[\t \n\r]+$','', cell)
                    except TypeError:
                        pass
                if ridx > 0:
                    if idx in split_column:
                        if cell is not None:
                            splits = cell.split(split_column[idx])
                            splits = self.sanity_stick(splits)
                            cell = [['address']] + [[x] for x in splits]
                            print(">>>", cell)
                            cell = self.clean_cells(cell, "other")
                            cell = self.add_location(cell, "other")
                            cell = {
                                'columns': cell[0],
                                'rows': [dict(zip(cell[0], row)) for row in cell[1:]]
                            }
                            print("<<<", cell)
                result.append(cell)
                if ridx == 0:
                    existing[cell] = 1
            if name in self.add_columns:
                for col in self.add_columns[name]:
                    if not col in existing:
                        if ridx == 0:
                            result.append(col)
                        else:
                            result.append(None)
            results.append(result)

        return results

    def add_location(self, vals, name):
        if len(vals) == 0:
            return vals

        have_address = False
        have_fill_in = False
        pattern = [0]
        fill_in = []
        offset = 0
        for idx, cell in enumerate(vals[0]):
            nn = normalize_name(cell)
            if nn == 'address':
                pattern = [idx]
                have_address = True
            if cell is not None and len(cell)>0 and cell[0] == '[':
                have_fill_in = True
                vals[0][idx] = cell[1:-1]
                fill_in.append([normalize_name(vals[0][idx]), idx])
            if self.fill_columns is not None:
                if nn in self.fill_columns:
                    have_fill_in = True
                    fill_in.append([nn, idx])
            if self.add_columns is not None:
                if name in self.add_columns:
                    if cell in self.add_columns[name]:
                        offset -= 1
                        fill_in.append([normalize_name(nn), idx])
                        have_fill_in = True
        if self.address_columns is not None:
            if name in self.address_columns:
                have_address = True
                pattern = self.address_columns[name]
                for idx, col in enumerate(pattern):
                    try:
                        pattern[idx] = vals[0].index(col)
                    except ValueError:
                        pass
        print("!!!", name, have_fill_in, have_address)
        if not(have_fill_in) or not(have_address):
            return vals
        from sheetsite.geocache import GeoCache
        cache = GeoCache(self.geocache_filename, geocoder=self.geocoder)
        cache.find_all(vals[1:], pattern, fill_in)
        return vals

    def configure(self, flags):
        self.geocoder = flags.get('geocoder')
        for key, val in flags.items():
            if key == 'add':
                self.add_columns = val
            if key == 'address':
                self.address_columns = val
            if key == 'merge':
                self.merge_tables = val

