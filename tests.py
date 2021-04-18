import csv
import os
import unittest
from io import StringIO
from unittest.mock import patch
from shutil import rmtree
from zipfile import ZipFile

from merge_csvs import MergeCSV, main


class TestMergeCSV(unittest.TestCase):

    zip_file = 'test.zip'

    def setUp(self):
        os.environ['pyTest'] = '1'
        with ZipFile(self.zip_file, 'w') as zf:
            zf.write('sample_a.csv')
            zf.write('sample_b.csv')

        td = MergeCSV.td
        output = MergeCSV.output
        if os.path.isdir(td):
            rmtree(td)

        if os.path.isfile(output):
            os.remove(output)

    def tearDown(self):
        del os.environ['pyTest']

        td = MergeCSV.td
        output = MergeCSV.output
        if os.path.isdir(td):
            rmtree(td)
        if os.path.isfile(self.zip_file):
            os.remove(self.zip_file)
        if os.path.isfile(output):
            os.remove(output)

    def test_prepare_creates_a_dir_if_not_exists_yet(self):
        m = MergeCSV(self.zip_file)
        self.assertFalse(os.path.isdir(m.td))

        m._prepare()
        self.assertTrue(os.path.isdir(m.td))

    def test_prepare_extracts_zip_file(self):
        m = MergeCSV(self.zip_file)
        m._prepare()
        self.assertTrue(os.path.isfile(os.path.join(m.td, 'sample_a.csv')))
        self.assertTrue(os.path.isfile(os.path.join(m.td, 'sample_b.csv')))

    def test_create_merge_merges_both_files(self):
        m = MergeCSV(self.zip_file)
        m._prepare()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            m._create_merge()
            expected_stdout = (
                'File output.csv generated successfully.\n'
            )
            self.assertEqual(fake_out.getvalue(), expected_stdout)

            self.assertTrue(os.path.isfile(m.output))
            with open(m.output) as csv_file:
                reader = csv.reader(csv_file)
                expected_rows = [
                    ['foo', 'bar', 'baz'],
                    ['1', '2', '3'],
                    ['4', '5', '6'],
                ]
                for row, expected in zip(reader, expected_rows):
                    self.assertEqual(row, expected)

    def test_create_merge_skips_non_csv_files(self):
        m = MergeCSV(self.zip_file)
        m._prepare()
        with open(os.path.join(m.td, 'foo.txt'), 'w') as outsider:
            outsider.write('bar')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            m._create_merge()
            expected_stdout = (
                'Non csv file found (foo.txt) in the dir, skipping...\n' +
                'File output.csv generated successfully.\n'
            )
            self.assertEqual(fake_out.getvalue(), expected_stdout)

    def test_create_merge_raises_error_if_header_mismatch(self):
        f = 'sample_mismatch.csv'
        with ZipFile(self.zip_file, 'a') as zf:
            zf.write(f)
        m = MergeCSV(self.zip_file)
        m._prepare()
        msg = ('Oh, it seems that there is a mismatch in the ' +
               'columns across files - {}'.format(f))
        with self.assertRaisesRegex(AssertionError, msg):
            m._create_merge()


class TestMain(unittest.TestCase):
    """Test the main entry point."""

    zip_file = 'test.zip'

    def setUp(self):
        os.environ['pyTest'] = '1'

    def tearDown(self):
        del os.environ['pyTest']

    def test_no_arguments_raises_error(self):
        with patch('argparse._sys.argv', ['merge_csvs.py', ]):
            with self.assertRaises(SystemExit):
                main()

    def test_arguments_creates_output(self):
        with patch('argparse._sys.argv', ['merge_csvs.py', self.zip_file, ]):
            m = main()
            self.assertIsInstance(m, MergeCSV)




if __name__ == '__main__':
    unittest.main()
