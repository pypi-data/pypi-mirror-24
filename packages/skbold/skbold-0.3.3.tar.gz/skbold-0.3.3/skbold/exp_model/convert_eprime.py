from __future__ import division, print_function, absolute_import
from io import open
import os
import os.path as op
import pandas as pd


class Eprime2tsv(object):
    """ Converts Eprime txt-files to tsv.

    Parameters
    ----------
    in_file : str
        Absolute path to Eprime txt-file.

    Attributes
    ----------
    df : Dataframe
        Pandas dataframe with parsed and cleaned txt-file
    """
    def __init__(self, in_file):

        self.in_file = in_file
        self.log = None
        self.df = None

    def _load(self):

        log = open(self.in_file, 'r')
        log_list = []

        for line in log.readlines():

            parts = line.split(':')
            parts = [x.lstrip().rstrip() for x in parts]
            for repl in ['\x00', '\r', '\n', '\t']:
                parts = [x.replace(repl, '') for x in parts]
            log_list.append(parts)

        log.close()
        self.log = log_list

    def convert(self, out_dir=None):
        """ Converts txt-file to tsv.

        Parameters
        ----------
        out_dir : str
            Absolute path to desired directory to save tsv to (default:
            current directory).
        """
        self._load()

        start_idx = []
        stop_idx = []

        for i, line in enumerate(self.log):

            if line[0] == '*** LogFrame Start ***':
                start_idx.append(i+1)

            if line[0] == '*** LogFrame End ***':
                stop_idx.append(i)

        # Remove last entry because that's meta-data
        from_to = zip(start_idx[:-1], stop_idx[:-1])

        df_list = []
        for fr, to in from_to:

            data = self.log[fr:to]
            df = {}

            for entry in data:
                df[entry[0]] = entry[1]

            df_list.append(pd.DataFrame(df, index=[0]))

        df = pd.concat(df_list)

        if out_dir is None:
            fn = op.join(op.dirname(self.in_file),
                         op.splitext(op.basename(self.in_file))[0])
        else:
            fn = op.join(out_dir, op.splitext(op.basename(self.in_file))[0])

        if not op.isdir(out_dir):
            os.makedirs(out_dir)

        df.columns = [c.strip() for c in df.columns]
        self.df = df
        df.to_csv(fn + '.tsv', sep='\t', index=False)
