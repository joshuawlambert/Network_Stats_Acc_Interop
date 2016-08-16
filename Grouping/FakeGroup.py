import itertools


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def generate_groups(snp_ids, group_size=250):
    return {i: groups for i, groups in enumerate(chunks(snp_ids, group_size))}