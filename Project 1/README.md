# Log Analysis project 
## Description
This is the first project for the [Udacity full stack web developer nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) ,where reporting tool is created that connect to a postgresql database which is running on a  virtual machine(VM) and the connection to database was made using psycopg2 python module .
## How to run 
1.Download and install last version of Vagrant and Virtual Box

2.Create VM folder and clone the repo there

3.Open your terminal and cd to VM folder then run the folling commands

4.Note that for the fourth command newsdata.sql is not included ,so i am assuimg that you have already this file 
```bash
vagrant up 
vagrant ssh 
cd /vagrant
psql -d news -f newsdata.sql
psql -d news
```
Then copy and paste the creation of the views from below
```bash
\q
python logs_analysis.py
```
## Created Views
**1.best3_articles**
```SQL
create view best3_articles as select path,count(*) as views from log where log.status='200 OK' and log.path like '/article/%'group by path order by views desc limit 3 ;
```

**2.best_articles**
```SQL
create view best_articles as select path,count(*) as views from log where log.status='200 OK' and log.path like '/article/%'group by path order by views desc ;
```

**3. best_author**
```SQL
create view best_author as select author,sum(views) as sum_views from best_articles,articles where replace(best_articles.path,'/article/','')=articles.slug group by author order by sum_views desc ;
```

**4.all_requests**

```SQL
create view all_requests as select count(*),cast(time as date) as mydate from log group by mydate ;

```
**5.err**
```SQL
create view err as select count(*),cast(time as date) as mydate from log where status!='200 OK' group by mydate ;
```

## Example Output 
The most popular three articles are :- 

candidate-is-jerk with 338647 views

bears-love-berries with 253801 views

bad-things-gone with 170098 views

\---------------------------------------------

The most popular article author is :-

The author "Ursula La Multa" has 507594 views

The author "Rudolf von Treppenwitz" has 423457  views

The author "Anonymous Contributor" has 170098 views

The author "Markoff Chaney" has 84557 views

\---------------------------------------------

The days were more than 1% of requests lead to error :-

On day 2016-07-17 the error was 2.26
