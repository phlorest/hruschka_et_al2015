import re
import pathlib

import phlorest

# The trees from the original analysis have two numbers separated by pipe as branch lengths.
# We simply discard the second number.
PIPE_PLUS_NUMBER = re.compile(r'\|[0-9]*\.?[0-9]*')

def relabel(x):
    return PIPE_PLUS_NUMBER.sub('', x)


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "hruschka_et_al2015"

    def cmd_makecldf(self, args):
        self.init(args)
        nex = self.raw_dir.read_nexus(
            'bp-noF-AS-reg-Relaxed-cS_t8.trees',
            preprocessor=relabel
        )
        nex.trees.detranslate()

        nex_mcc = self.run_treeannotator('-burnin 0 -heights median', nex.write())
        nex_mcc.trees.detranslate()
        args.writer.add_summary(
            nex_mcc.trees.trees[0],
            self.metadata,
            args.log)
        
        args.writer.add_posterior(
            nex.trees.trees,
            self.metadata, 
            args.log)