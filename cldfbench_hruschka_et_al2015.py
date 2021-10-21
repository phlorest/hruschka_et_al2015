import re
import pathlib

import phlorest

# The trees from the original analysis have two numbers separated by pipe as branch lengths.
# We simply discard the second number.
PIPE_PLUS_NUMBER = re.compile(r'\|[0-9]*\.?[0-9]*')


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "hruschka_et_al2015"

    def cmd_makecldf(self, args):
        self.init(args)
        posterior = PIPE_PLUS_NUMBER.sub('', self.raw_dir.read('bp-noF-AS-reg-Relaxed-cS_t8.trees'))
        with self.nexus_summary() as nex:
            self.add_tree_from_nexus(
                args,
                self.run_treeannotator('-burnin 10 -heights median', posterior),
                nex,
                'summary',
                detranslate=True,
            )
        posterior = self.sample(
            posterior,
            detranslate=True,
            n=100,
            as_nexus=True)

        with self.nexus_posterior() as nex:
            for i, tree in enumerate(posterior.trees.trees, start=1):
                self.add_tree(args, tree, nex, 'posterior-{}'.format(i))
