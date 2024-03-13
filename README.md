# pymysql

Simplified MySQL library for [mysql.connector](https://dev.mysql.com/doc/connector-python/en/)


## Installation

To install the library on your machine:

```bash
pip install rymysql
```


## Setup

To use the libary in your code you just need to set the credential values:

```py
import pymysql

rymysql.credentials.USER     = 'mysql_user'
rymysql.credentials.PASSWORD = '123'
rymysql.credentials.DATABASE = 'test_database'
rymysql.credentials.HOST     = 'localhost'
```

Or you could use the `fromDict` routine to set the credential values from a dictionary:


```py
import pymysql

my_credentials = dict(
    user     = 'mysql_user',
    password = '123',
    database = 'test_database',
    host     = 'localhost',
)

rymysql.credentials.fromDict(my_credentials)
```


## Commands


Currently there are 3 commands:
  1. `select`
  1. `selectAll`
  1. `modify`


### Select Commands


To select a single record, use the `rymysql.commands.select` routine:

```py
sql = '''
    SELECT n.namefirst, n.namelast 
    FROM Names n  
    WHERE n.id = %s;
'''

parms = tuple(42)
result = rymysql.commands.select(sql, parms)

print(result.data.get('namefirst'))
```

To select multiple records, use the `rymysql.commands.selectAll` routine:

```py
sql = 'SELECT n.namefirst, n.namelast FROM Names n;'
parms = None
result = rymysql.commands.selectAll(sql, parms)

for record in result.data:
    print(record.get('namefirst'))
```

### Modify Command

`rymysql.commands.modify` is for INSERT, UPDATE, or DELETE sql commands.


For example, to insert a record:


```py
sql = 'INSERT INTO Names (namefirst, namelast) VALUES (%s, %s);'
parms = ('Ryan', 'Rickgauer')

result = rymysql.commands.modify(sql, parms)

print(result.data)  # 1 - rowsaffected
```
