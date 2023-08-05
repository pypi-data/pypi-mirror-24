# coding: utf8
from __future__ import unicode_literals, print_function, division

from mock import Mock
from clldutils.testing import WithTempDir
from clldutils.csvw.metadata import TableGroup, ForeignKey
from clldutils.path import copy

from pycldf.tests.util import FIXTURES


class Tests(WithTempDir):
    def _make_tg(self, *tables):
        tg = TableGroup.fromvalue({'tables': list(tables)})
        tg._fname = self.tmp_path('md.json')
        return tg

    def test_add_component(self):
        from pycldf.dataset import Wordlist

        ds = Wordlist.in_dir(self.tmp_path())
        ds['FormTable'].tableSchema.foreignKeys.append(ForeignKey.fromdict({
            'columnReference': 'Language_ID',
            'reference': {'resource': 'languages.csv', 'columnReference': 'ID'}}))
        ds.add_component('LanguageTable', 'glottocode')
        with self.assertRaises(ValueError):
            ds.add_component('LanguageTable')
        ds.add_component('ParameterTable', {'name': 'url', 'datatype': 'anyURI'})

        ds.write(
            FormTable=[
                {'ID': '1', 'Value': 'form', 'Language_ID': 'l', 'Parameter_ID': 'p'}],
            LanguageTable=[{'ID': 'l'}],
            ParameterTable=[{'ID': 'p'}])
        ds.validate()

        ds.write(
            FormTable=[
                {'ID': '1', 'Value': 'form', 'Language_ID': 'l', 'Parameter_ID': 'x'}],
            LanguageTable=[{'ID': 'l'}],
            ParameterTable=[{'ID': 'p'}])
        with self.assertRaises(ValueError):
            ds.validate()

    def test_modules(self):
        from pycldf.dataset import Dataset, Wordlist, Dictionary, StructureDataset

        ds = Dataset(self._make_tg())
        self.assertIsNone(ds.primary_table)
        ds = Dataset(self._make_tg({"url": "data.csv"}))
        self.assertIsNone(ds.primary_table)
        ds = Dataset(self._make_tg({
            "url": "data.csv",
            "dc:conformsTo": "http://cldf.clld.org/v1.0/terms.rdf#ValueTable"}))
        self.assertEqual(ds.primary_table, 'ValueTable')
        self.assertIsNotNone(Wordlist.in_dir(self.tmp_path()).primary_table)
        self.assertIsNotNone(Dictionary.in_dir(self.tmp_path()).primary_table)
        self.assertIsNotNone(StructureDataset.in_dir(self.tmp_path()).primary_table)

    def test_Dataset_from_scratch(self):
        from pycldf.dataset import Dataset

        copy(FIXTURES.joinpath('ds1.csv'), self.tmp_path('xyz.csv'))
        with self.assertRaises(ValueError):
            Dataset.from_data(self.tmp_path('xyz.csv'))

        copy(FIXTURES.joinpath('ds1.csv'), self.tmp_path('values.csv'))
        ds = Dataset.from_data(self.tmp_path('values.csv'))
        self.assertEqual(ds.module, 'StructureDataset')

        self.assertEqual(len(list(ds['ValueTable'])), 2)
        ds.validate()
        ds['ValueTable'].write(2 * list(ds['ValueTable']))
        with self.assertRaises(ValueError):
            ds.validate()
        md = ds.write_metadata()
        Dataset.from_metadata(md)
        repr(ds)
        del ds._tg.common_props['dc:conformsTo']
        Dataset.from_metadata(ds.write_metadata())
        self.assertEqual(len(ds.stats()), 1)

    def test_Dataset_validate(self):
        from pycldf.dataset import StructureDataset

        ds = StructureDataset.in_dir(self.tmp_path('new'))
        ds.write(ValueTable=[])
        ds.validate()
        ds['ValueTable'].tableSchema.columns = []
        with self.assertRaises(ValueError):
            ds.validate()
        ds._tg.tables = []
        with self.assertRaises(ValueError):
            ds.validate()

    def test_Dataset_write(self):
        from pycldf.dataset import StructureDataset

        ds = StructureDataset.from_metadata(self.tmp)
        ds.write(ValueTable=[])
        self.assertTrue(self.tmp_path('values.csv').exists())
        ds.validate()
        ds.sources.add("@misc{key,\ntitle={the title}\n}")
        ds.write(ValueTable=[
            {
                'ID': '1',
                'Language_ID': 'abcd1234',
                'Parameter_ID': 'f1',
                'Value': 'yes',
                'Source': ['key[1-20]'],
            }])
        ds.validate()
        ds.add_component('ExampleTable')
        ds.write(
            ValueTable=[
                {
                    'ID': '1',
                    'Language_ID': 'abcd1234',
                    'Parameter_ID': 'f1',
                    'Value': 'yes',
                    'Source': ['key[1-20]'],
                }],
            ExampleTable=[
                {
                    'ID': '1',
                    'Language_ID': 'abcd1234',
                    'Primary': 'si',
                    'Translation': 'yes',
                    'Analyzed': ['morph1', 'morph2', 'morph3'],
                    'Gloss': ['gl1', 'gl2'],
                }])
        with self.assertRaises(ValueError):
            ds.validate()
        ds['ExampleTable'].write([
            {
                'ID': '1',
                'Language_ID': 'abcd1234',
                'Primary': 'si',
                'Translation': 'yes',
                'Analyzed': ['morph1', 'morph2', 'morph3'],
                'Gloss': ['gl1', 'gl2', 'gl3'],
            }])
        ds.validate()

    def test_validators(self):
        from pycldf.dataset import Dataset

        copy(FIXTURES.joinpath('invalid.csv'), self.tmp_path('values.csv'))
        ds = Dataset.from_data(self.tmp_path('values.csv'))

        with self.assertRaises(ValueError):
            ds.validate()

        log = Mock()
        ds.validate(log=log)
        self.assertEqual(log.warn.call_count, 2)

        for col in ds._tg.tables[0].tableSchema.columns:
            if col.name == 'Language_ID':
                col.propertyUrl.uri = 'http://cldf.clld.org/terms.rdf#glottocode'

        log = Mock()
        ds.validate(log=log)
        self.assertEqual(log.warn.call_count, 3)

    def test_Module(self):
        from pycldf.dataset import get_modules

        self.assertFalse(get_modules()[0].match(5))
