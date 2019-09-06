create view best3_articles as select path,count(*) as views from log where log.status='200 OK' and log.path like '/article/%'group by path order by views desc limit 3 ;

create view best_articles as select path,count(*) as views from log where log.status='200 OK' and log.path like '/article/%'group by path order by views desc ;

create view best_author as select author,sum(views) as sum_views from best_articles,articles where replace(best_articles.path,'/article/','')=articles.slug group by author order by sum_views desc ;


create view all_requests as select count(*),cast(time as date) as mydate from log group by mydate ;
create view err as select count(*),cast(time as date) as mydate from log where status!='200 OK' group by mydate ;