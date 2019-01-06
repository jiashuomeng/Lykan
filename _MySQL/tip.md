#### 查看配置文件加载顺序

``` shell
# mysql --help | grep my.cnf

/etc/my.cnf /etc/mysql/my.cnf /usr/etc/my.cnf ~/.my.cnf # 字段冲突，以最后读取到的一个配置为准
```

#### 查看数据库文件保存路径

```Shell
mysql> show variables like 'datadir'\G

*************************** 1. row ***************************
Variable_name: datadir
        Value: /var/lib/mysql/
1 row in set (0.00 sec)
```

#### 查看innodb版本

``` shell
mysql> show variables like 'innodb_version'\G
*************************** 1. row ***************************
Variable_name: innodb_version
        Value: 5.7.17
1 row in set (0.00 sec)
```

#### 查看innodb状态

``` shell
mysql> show engine innodb status\G
```

