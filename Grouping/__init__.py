import Grouping.FakeGroup, Grouping.ClinVar

method_map = {'fake': Grouping.FakeGroup.generate_groups,
              'clinvar': Grouping.ClinVar.generate_groups,
              'NoGroup': Grouping.FakeGroup.generate_one_group}