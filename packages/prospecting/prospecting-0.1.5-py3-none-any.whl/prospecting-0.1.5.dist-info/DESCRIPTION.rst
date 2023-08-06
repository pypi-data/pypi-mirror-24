
Prospecting
===========


Google Sheets with Pandas dataframes, useful when 'prospecting' in analytics work and hacking.


____

**Setup**

  1. Create or select a project in `Google's developer console`__

     - Also, you will need to enable the APIs you plan to use

  #. Get a ``client_secrets.json`` credentials file from the `credentials section`__

     - Select *OAuth client ID* from the dropdown in the `API access pane`__

  #. Load the ``prospecting`` module in a Python session to initialize the ``~/.prospecting/`` folder in your home directory
  #. Place the ``client_secrets.json`` file in the ``~/.prospecting/credentials/`` directory
  #. Load an API class in a Python session, then run apiclass.authenticate() and follow steps

     - You only need to setup authentication once per API unless creds change


.. _DevConsole: https://console.developers.google.com/apis/dashboard
__ DevConsole_

.. _Credentials: https://console.developers.google.com/apis/credentials
__ Credentials_

.. _ApiPane: https://console.developers.google.com/apis/credentials
__ ApiPane_


**Examples**::

    import prospecting as p

---

Use stats sheet to store stats and misc statistics (scopelist defaults to read-only, so pass scopes for writing)::

    ss_stats = p.SheetsApi(spreadsheetid = 'PASTE_GOOGLE_SHEETID_HERE',
                           scopelist=['https://www.googleapis.com/auth/spreadsheets',
                                      'https://www.googleapis.com/auth/drive.metadata'])
    ss_stats.authenticate()
    ss_stats.update('Sheet1', somedataframe)


---

Use a reference sheet to provide a named entity list (or stopwords, vocabulary) for NLP preprocessing::

    ss_reference = p.SheetsApi(spreadsheetid = 'PASTE_GOOGLE_SHEETID_HERE',
                               scopelist=['https://www.googleapis.com/auth/spreadsheets',
                                          'https://www.googleapis.com/auth/drive.metadata'])
    ss_reference.authenticate()
    named_entity_list = list(ss_reference.get('ne!A:B').iloc[:,0].values)


---

Get keywords sheet as dataframe, filter, take sampled subset, upload new df to other tab in spreadsheet::

    ss_kw = p.SheetsApi(spreadsheetid = 'PASTE_GOOGLE_SHEETID_HERE',
                        scopelist=['https://www.googleapis.com/auth/spreadsheets',
                                   'https://www.googleapis.com/auth/drive.metadata'])
    ss_kw.authenticate()

    #  Get data using spreadsheet syntax like ('sheetname') or ('sheetname!A:B25')
    df_query = ss_kw.get('queries')
    df_query_subset = df_query[(df_query['raw_len'] > 1) &
                               (df_query['reject'] != 1)]

    #  Take a subsample of data
    df_query_subset_sample = df_query_subset.sample(frac=0.5)
    df_query_subset_sample.reset_index(drop=True, inplace=True)

    #  Update 'sheetname' with dataframe object
    ss_kw.update('queries_shuffled', df_query_subset_sample)


____


Key changes between 0.1.4 and 0.1.2:

* Switched order of input arguments for ss.update() function::

      From
         ss.update(dataframe, 'sheetname')
      To
         ss.update('sheetname', dataframe)

* Removed Docker files to simplify

____

\

____

|hammer_and_pick| |hammer_and_pick| |hammer_and_pick|

.. |hammer_and_pick| image:: https://storage.googleapis.com/prospecting-151803.appspot.com/hammer_and_pick_60x60.png

