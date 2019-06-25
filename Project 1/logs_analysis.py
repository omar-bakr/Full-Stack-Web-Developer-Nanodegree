import psycopg2


DBNAME = "news"


"""problem 1 :- What are the most popular three articles of all time ?"""
def get_best3_articles():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select replace(path,'/article/',''),views from best_articles ;")
  result= c.fetchall()
  print(result)
  db.close()

"""problem 2 :-Who are the most popular article authors of all time ? """
def get_best_authtor():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select name,sum_views from best_author,authors where author=authors.id ;")
  result= c.fetchall()
  print(result)
  db.close()

"""problem 3 :- On which days did more than 1% of requests lead to errors? ? """
def get_err_day():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute('''select all_requests.mydate, round((err.count*1.0/all_requests.count)*100,2) 
  as percentage from all_requests,err where all_requests.mydate=err.mydate and 
  ((err.count*1.0/all_requests.count)*100) > 1 ;''')
  result= c.fetchall()
  print(result)
  db.close()

if __name__ == '__main__':
    get_best3_articles()
    get_best_authtor()
    get_err_day()



