import pandas as pd
import sqlalchemy as sa
#from sqlalchemy import create_engine
# http://pandas.pydata.org/pandas-docs/stable/io.html#engine-connection-examples
#engine = sa.create_engine('sqlite:///odyssey.db')

def search_last(last):
    print "IN SEARCH"
    engine = sa.create_engine('sqlite:///app/odyssey.db')
    print "ENGINE ", engine
    sql_text = 'SELECT * FROM odyssey WHERE lastname_stripped LIKE "%' + last + '%";'
    df = pd.read_sql_query(sql_text, engine)
    print "DF SEARCH: ", df.to_html()
    return df

if __name__ == "__main__":

    #defendant = 'AAGAARD, KATHIE J'
    #read_odyssey()

    #df_db_out = \
        #pd.read_sql_query('SELECT * FROM df_odyssey where lastname_stripped LIKE "AAGAARD";',
                                 #engine)
    #defendant = 'AAGAARD, KATHIE J'
    last_name = 'AAGAARD'
    df_db_out = search_last(last_name)
    print
    print "FROM MAIN:"
    print df_db_out.to_html()
