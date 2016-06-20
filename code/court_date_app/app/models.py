import pandas as pd
from app import engine


def search_last(last):
    sql_text = 'SELECT * FROM odyssey WHERE lastname_stripped LIKE "%' + last + '%";'
    df = pd.read_sql_query(sql_text, engine)
    return df


if __name__ == "__main__":

    last_name = 'AAGAARD'
    df_db_out = search_last(last_name)
    print
    print "FROM MAIN:"
    print df_db_out.to_html()
