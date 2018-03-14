## This scripts uses the Python package Newspaper, an article scraping & curation
## library, to scrape the full text of specific articles when provided with the URL.
## The full text is then stored in the corresponding SQL table.

from mysqldb import db
from contextlib import closing
from newspaper import Article


with closing(db.cursor()) as cur:
    cur.execute("""
    select URL from db.table1 where (Full_Text = '' OR Full_Text IS NULL)
    """)
    rows = cur.fetchall()
    for record in rows:
        url = record[0]
        print url
        if url.find('cisionpoint') == -1:
            try:
                article_get = Article(url=url, language='en')
                article_get.download()
                article_get.parse()
                scraped_content = article_get.text
                scraped_headline = article_get.title
            except:
                print "got error with " + url
                scraped_content = 'None'
        else:
            scraped_content = 'None'
        cur.execute("""
        UPDATE db.table1 SET Full_Text = %s WHERE URL = %s
        """,(scraped_content,url))
        db.commit()
