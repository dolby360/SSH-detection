#Installation:
https://www.youtube.com/watch?v=uqaoGTnxqNw

# to integrate python install 

```Bash
pip install mysql-connector-python-rf 
```

#ERROR:
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)

#solution

First of all, you have to stop mysql service.

```Bash
sudo service mysql stop
```

Second, Add 'skip-grant-tables' in your my.conf or my.cnf file.

In my case (MySQL v5.7.17), mysqld.cnf is in the '/etc/mysql/mysql.conf.d'.

Almost my.conf / my.cnf file shows like this.

```Bash
[mysqld]
user         = mysql
pid-file     = /var/run/mysqld/mysqld.pid
socket       = /var/run/mysqld/mysqld.sock
port         = 3306
basedir      = /usr
datadir      = /var/lib/mysql
tmpdir       = /tmp
lc-messages-dir = /usr/share/mysql

skip-external-locking

skip-grant-tables         /*** You Add this code! ***/
```

Next, restart mysql service.

```Bash
sudo service mysql start
```