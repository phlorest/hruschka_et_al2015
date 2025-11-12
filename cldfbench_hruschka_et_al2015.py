import re
import pathlib

import phlorest
from phlorest.nexuslib import Tree

# The trees from the original analysis have two numbers separated by pipe as branch lengths.
# We simply discard the second number.
PIPE_PLUS_NUMBER = re.compile(r'\|[0-9]*\.?[0-9]*')


def relabel(x):
    return PIPE_PLUS_NUMBER.sub('', x) + '\nend;'


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "hruschka_et_al2015"

    def cmd_makecldf(self, args):
        self.init(args)
        nex = self.raw_dir.read_nexus(
            'bp-noF-AS-reg-Relaxed-cS_t8.trees',
            normalise=True,
            preprocessor=relabel
        )

        nex_mcc = self.run_treeannotator('-burnin 0 -height median', str(nex))
        #tree = nex_mcc.TREES.TREE
        #tree.newick = nex_mcc.TREES.translate(tree.newick)
        args.writer.add_summary(nex_mcc.TREES.translate(nex_mcc.TREES.TREE), self.metadata, args.log)
        
        args.writer.add_posterior([t.newick for t in nex.TREES.trees], self.metadata, args.log)

