# FTX_demo
FTX demo

run command $flask run

## command 1
```
export FLASK_APP=flask_request.py
flask run
```

## command 2
```
python3 flask_request.py
```
* This command need to specify the sys path and use `pip3 install` to install the relevent packages.
```
import sys
sys.path.append('/Users/bur/opt/anaconda3/lib/python3.9/site-packages')
```

## command 3 (Currently Used)
```
python3 flask_request.py --sys_path [path for python3.9 site-packages]
```
* Use `python -m site` to find the **site-packages**
* example:
```
python3 flask_request.py --sys_path /Users/bur/opt/anaconda3/lib/python3.9/site-packages
```
* Use command args to input the path.

## Generate *requirement.txt*
```
pip3 freeze > requirements.txt
```

# Environment
## MySQL
* `Authentication plugin 'caching_sha2_password' cannot be loaded`
    * [Solution](https://www.jianshu.com/p/9a645c473676)
    ```
    mysql -uroot -p
    [key your password]

    mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '[your password]';
    ```
* [Access database](https://www.hostmysite.com/support/linux/mysql/access/)
    ```
    mysql -u [username] -p [databasename]
    Enter password:
    ```
    * Example:
    ```
    mysql -u root -p test2
    Enter password:
    ```
* Access MySQL in container
    ```
    mysql -u root -p
    mysql> CREATE USER '[user]'@'%' IDENTIFIED BY '[password]';
    mysql> GRANT ALL ON *.* TO '[user]'@'%'  WITH GRANT OPTION;
    mysql> ALTER USER '[user]'@'%' IDENTIFIED WITH mysql_native_password BY '[password]';
    mysql> FLUSH PRIVILEGES;
    ```
    * Example
    ```
    mysql -u root -p
    mysql> CREATE USER 'tvbot'@'%' IDENTIFIED BY 'pass';
    mysql> GRANT ALL ON *.* TO 'tvbot'@'%'  WITH GRANT OPTION;
    mysql> ALTER USER 'tvbot'@'%' IDENTIFIED WITH mysql_native_password BY 'pass';
    mysql> FLUSH PRIVILEGES;
    ```
* Container deployment
    * After use docker-compose to lauch containers (MySQL and app), use CLI to go into MySQL container.
    ```
    mysql -u root -p
    Enter password:[key your password]
    mysql> SELECT user, host FROM mysql.user;
    mysql> DROP USER '[username]'@'[host]';
    ```
    * For example:
    ```
    mysql -u root -p
    Enter password:pass
    mysql> SELECT user, host FROM mysql.user;
    mysql> DROP USER 'root'@'localhost';
    ```
    * After delete **'root'@'localhost'**, re-launch the app container.

* Create table
    ```
    mysql> use test2;
    mysql> CREATE TABLE user_info (dc_id VARCHAR(255), api_key VARCHAR(255), secret_key VARCHAR(255), ftx_sub_account VARCHAR(255), lv2_cert VARCHAR(255), market_info VARCHAR(255));
    ```

## Python
* [From conda create requirements.txt for pip3](https://stackoverflow.com/questions/50777849/from-conda-create-requirements-txt-for-pip3)
```
conda activate <env>
conda install pip
pip list --format=freeze > requirements.txt
```


# Docker
```
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```