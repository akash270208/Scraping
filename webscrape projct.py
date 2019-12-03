## 29 th nov2019
## Web scrapping project

# scrape quotation , author and tags from first 10 pages and write it to a csv file ##

from bs4 import BeautifulSoup
import requests
import pandas as pd



## creating db using sqlalchemy

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
class quotes(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'quotes'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False)   # , autoincrement=True)
    Author_Name = Column(VARCHAR(40))
    Tags = Column(VARCHAR)
    Quotation = Column(VARCHAR)

engine = create_engine('sqlite:///quote.db')
Base.metadata.create_all(engine)



### scrappiing website now

quotation_list = []
uni_tag_list = []
author_list = []

for i in range(1,11):
    website_address = "http://quotes.toscrape.com/page/"+str(i)+"/"
    result = requests.get(website_address)
    soup=BeautifulSoup(result.text,"html.parser")
    quotes_list=soup.findAll("div",{"class":"quote"})
    for quote in quotes_list:
        quotation=quote.find("span", {"class" : "text"})
        quotation_list.append(quotation.text[1:-1])
        author=quote.find("small", {"class" : "author"})
        author_list.append(author.text)
        tags_list=quote.findAll("a", {"class" : "tag"})
        new_list = []
        for tag in tags_list:
            new_list.append(tag.text)
        all_tags = ", ".join(new_list)
        uni_tag_list.append(all_tags)

dict = {
    'Author': author_list,
    'Tags': uni_tag_list,
    'Quotation': quotation_list
}

df = pd.DataFrame(dict)

df1 = df.set_index('Author') # set index for csv file

df1.to_csv('quote.csv')  ## to write into csv file

df.to_sql(name=quotes.__tablename__, con=engine, if_exists='replace', index_label='id')  ## write to db table without index


resultSet = engine.execute("SELECT Author, Tags, Quotation FROM quotes where Author='Albert Einstein' ").fetchall()
for i in range(len(resultSet)):
    print(str(i+1)+"->\n" + "Author= "+ resultSet[i]['Author']+ "\nTags= " + resultSet[i]['Tags']+ "\nQuote= "+resultSet[i]['Quotation']+ "\n ***")



