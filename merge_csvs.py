import argparse
import os
from shutil import rmtree
from zipfile import ZipFile

import pandas as pd


class MergeCSV:
    """Merge all the csv files contained in a csv file."""

    output = 'output.csv'
    td = 'tmp_dir'

    def __init__(self, source: str) -> None:
        self.source = source

    def _prepare(self) -> None:
        """Create an environment to work with."""
        if not os.path.isdir(self.td):
            os.mkdir(self.td)
        with ZipFile(self.source, 'r') as zf:
            zf.extractall(self.td)

    def _create_merge(self) -> None:
        """Merge all the csv files located at tmp_dir.

        Raises AssertionError if there is a mismatch in columns across files
        and skips non csv files.
        """
        data = []
        headers = None
        for f in os.listdir(self.td):
            if f.endswith('.csv'):
                df = pd.read_csv(os.path.join(self.td, f))
                if headers is None:
                    headers = df.columns
                else:
                    msg = ('Oh, it seems that there is a mismatch in the ' +
                           'columns across files - {}'.format(f))
                    assert (df.columns.isin(headers)).all(), msg
                data.append(df)
            else:
                print(f'Non csv file found ({f}) in the dir, skipping...')
        pd.concat(data).to_csv(self.output, index=False)
        print(f'File {self.output} generated successfully.')

    def run(self) -> None:
        """Execute the process."""
        self._prepare()
        self._create_merge()
        rmtree(self.td)


def main():
    """Parse command line arguments for MergeCSV and launch the application."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source', type=str,
        help='A zip containing a bunch of csv files (2 at least).')

    args = parser.parse_args()
    m = MergeCSV(args.source)
    if os.getenv('pyTest'):
        return m
    m.run()


if __name__ == '__main__':
    main()
