from collections import OrderedDict
from tqdm import tqdm_notebook
import pandas as pd


def create_marginal_df(L_data, models, lfs_columns, model_names, candidate_ids):
    """
    This function is designed to create a dataframe that will hold
    the marginals outputted from the generative model

    L_data - the sparse matrix generated fromt eh label functions
    models - the list of generative models
    lfs_columns - a listing of column indexes that correspond to desired label fucntions
    model_names - a label for each model
    candidate_ids - a list of candidate ids so the marginals can be mapped back to the candidate
    """
    marginals = [
        model.marginals(L_data[:, columns])
        for model, columns in zip(models, lfs_columns)
    ]
    marginals_df = pd.DataFrame(
           np.array(marginals).T, columns=model_names
    )
    marginals_df['candidate_id'] = candidate_ids
    return marginals_df

def make_sentence_df(candidates):
    """ 
    This function creats a dataframe for all candidates (sentences that contain at least two mentions)
    located in our database.
    
    candidates - a list of candidate objects passed in from sqlalchemy
    """
    rows = list()
    for c in tqdm_notebook(candidates):
        if hasattr(c, 'Disease_cid') and hasattr(c, 'Gene_cid'):
            row = OrderedDict()
            row['candidate_id'] = c.id
            row['compound'] = c[0].get_span()
            row['disease'] = c[1].get_span()
            row['doid_id'] = c.Disease_cid
            row['entrez_gene_id'] = c.Gene_cid
            row['sentence'] = c.get_parent().text
            rows.append(row)
        elif hasattr(c, 'Gene1_cid') and hasattr(c, 'Gene2_cid'):
            row = OrderedDict()
            row['candidate_id'] = c.id
            row['compound'] = c[0].get_span()
            row['disease'] = c[1].get_span()
            row['entrez_gene_id'] = c.Gene_cid
            row['entrez_gene_id'] = c.Gene_cid
            row['sentence'] = c.get_parent().text
            rows.append(row)
        elif hasattr(c, 'Compound_cid') and hasattr(c, 'Gene_cid'):
            row = OrderedDict()
            row['candidate_id'] = c.id
            row['compound'] = c[0].get_span()
            row['disease'] = c[1].get_span()
            row['drugbank_id'] = c.Compound_cid
            row['entrez_gene_id'] = c.Gene_cid
            row['sentence'] = c.get_parent().text
            rows.append(row)
        elif hasattr(c, 'Compound_cid') and hasattr(c, 'Disease_cid'):
            row = OrderedDict()
            row['candidate_id'] = c.id
            row['compound'] = c[0].get_span()
            row['disease'] = c[1].get_span()
            row['drugbank_id'] = c.Compound_cid
            row['doid_id'] = c.Disease_cid
            row['sentence'] = c.get_parent().text
            rows.append(row)
    return pd.DataFrame(rows)
        

def write_candidates_to_excel(candidate_df, spreadsheet_name):
    """
    This function is designed to save the candidates to an excel
    spreadsheet. This is needed for manual curation of candidate 
    sentences
    
    candidate_df - the dataframe that holds all the candidates
    spreadsheet_name - the name of the excel spreadsheet
    """
    writer = pd.ExcelWriter(speadsheet_name)
    (
        candidate_df
        .to_excel(writer, sheet_name='sentences', index=False)
    )
    if writer.engine == 'xlsxwriter':
        for sheet in writer.sheets.values():
            sheet.freeze_panes(1, 0)
    writer.close()
    return