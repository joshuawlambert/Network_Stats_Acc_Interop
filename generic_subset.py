import pandas as pd

def subset_wrap(table, groups, bad_value='No Call'):
    """table -- is a GSE data FILE minus the HEADER
       groups -- is a dictionary keys are group labels (phenotype for ex.), values are lists of column labels
       returns a dictionary keys(group labels): values(sub dataframes)
    """
    df = pd.read_table(table, index_col=0)
    df.replace(bad_value, '')
    
    # call generic_subset on each group
    sub_dfs = {}
    for group, col_id_list in groups.items():
        sub_dfs[group] = generic_subset(df, col_id_list)
        
    return sub_dfs
    
def generic_subset(table, group):
    """table -- is a pandas dataframe
       group -- is a list of col labels
    """
    
    subset_table = table.loc[group]
    
    return subset_table.T #return snps-cols, ids-rows

def table_format_helper(table):
    """table input has to be:
       cols: sample ids
       rows: unique identifier
    """
    # table conversion function when inputs are transposed
    pass
