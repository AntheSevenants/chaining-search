import requests
import pandas as pd
import json
from chaininglib.wait import *
from chaininglib.queries import _lexicon_query_alllemmata

def _metadata_from_lexicon_query(lex_query):
    '''
    Extract metadata fields from a lexicon query string
    
    Args:
        lex_query: A query string issued to a lexicon, can be constructed using lexicon_query()
    Returns:
        A list of metadata fields
    '''
    # Get part after select, eg: "?x ?y ?concat('',z) as ?a"
    select_match = re.search(r'select\s+(?:distinct)*\s*(.*)\s*(?:where|from)', lex_query, flags=re.IGNORECASE)
    if select_match:
        select_string = select_match.group(1)
        #Delete concat() part and following AS, because it can contain a space we do not want to split on
        string_wh_concat = re.sub(r'concat\(.*\) AS', '', select_string, flags=re.IGNORECASE)
        split_string = string_wh_concat.split()
        for i,elem in enumerate(split_string):
            if elem.lower()=="AS":
                # Remove AS and element before AS
                split_string.pop(i)
                split_string.pop(i-1)
                # Assume only one AS, so we escape loop
                break
        columns = [c.lstrip("?") for c in split_string]
    else:
        raise ValueError("No columns find in lexicon query.")
    return columns

# Deprecated, replaced by LexiconQuery
def search_lexicon_all(lexicon, pos=None):
    '''
    This function gets all lemmata of a lexicon. If needed, the output can be restricted to lemmata with a given part-of-speech
    Args:
        lexicon: a lexicon name
        pos: part-of-speech (optional)
    Returns:
        a Pandas DataFrame containing lexicon data 
        
    >>> df_lexicon = search_lexicon_alllemmata("anw")
    >>> display_df(df_lexicon)
    '''
    query = _lexicon_query_alllemmata(lexicon, pos)
    return search_lexicon(query, lexicon)


# Deprecated, replaced by LexiconQuery
def search_lexicon(query, lexicon):
    '''
    This function searches a lexicon given a query and a lexicon name
    Args:
        query: a lexicon query, typically previously generated by lexicon_query() or such 
        lexicon: a lexicon name
    Returns:
        a Pandas DataFrame with lexicon data 
        
    '''
     # show wait indicator, so the user knows what's happening
    show_wait_indicator('Searching '+lexicon)
    
    # default endpoint, except when diamant is invoked
    endpoint = "http://172.16.4.56:8890/sparql"
    if (lexicon=="diamant"):
        endpoint = "http://svprre02:8080/fuseki/tdb/sparql"
    
    try:
        # Accept header is needed for virtuoso, it isn't otherwise!
        response = requests.post(endpoint, data={"query":query}, headers = {"Accept":"application/sparql-results+json"})
        
        response_json = json.loads(response.text)
        records_json = response_json["results"]["bindings"]
        records_string = json.dumps(records_json)    
        df = pd.read_json(records_string, orient="records")
    
        # make sure cells containing NULL are added too, otherwise we'll end up with ill-formed data
        # CAUSES MALFUNCTION: df = df.fillna('')
        df = df.applymap(lambda x: '' if pd.isnull(x) else x["value"])         
        
        # remove wait indicator, 
        remove_wait_indicator()
        
        return df
    except Exception as e:
        remove_wait_indicator()
        raise ValueError("An error occured when searching lexicon " + lexicon + ": "+ str(e))     