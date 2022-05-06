# pymysql

Simplified MySQL library for [mysql.connector](https://dev.mysql.com/doc/connector-python/en/)


## Installation

To install the library on your machine:

```bash
pip install git+https://github.com/rrickgauer/pymysql.git
```


## Setup

To use the libary in your code you just need to set the credential values:

```py
import pymysql

pymysql.credentials.USER     = 'mysql_user'
pymysql.credentials.PASSWORD = '123'
pymysql.credentials.DATABASE = 'test_database'
pymysql.credentials.HOST     = 'localhost'
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

pymysql.credentials.fromDict(my_credentials)
```


## Commands


Currently there are 3 commands:
  1. `select`
  1. `selectAll`
  1. `modify`


### Select Commands


To select a single record, use the `pymysql.commands.select` routine:

```py
sql = '''
    SELECT n.namefirst, n.namelast 
    FROM Names n  
    WHERE n.id = %s;
'''

parms = tuple(42)


result = pymysql.commands.select(sql, parms)

print(result.data.get('namefirst'))
```

To select multiple records, use the `pymysql.commands.selectAll` routine:

```py
sql = 'SELECT n.namefirst, n.namelast FROM Names n;'
parms = None
result = pymysql.commands.selectAll(sql, parms)

for record in result.data:
    print(record.get('namefirst'))
```

### Modify Command

`pymysql.commands.modify` is for INSERT, UPDATE, or DELETE sql commands.


For example, to insert a record:


```py
sql = 'INSERT INTO Names (namefirst, namelast) VALUES (%s, %s);'
parms = ('Ryan', 'Rickgauer')

result = pymysql.commands.modify(sql, parms)

print(result.data)  # 1 - rowsaffected
```
