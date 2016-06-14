
import MySQLdb


bz_config = {
    'host': 'bz3-db3.eng.vmware.com',
    'port': 3306,
    'user': 'mts',
    'passwd': 'mts',
    'db': 'bugzilla'
}


etl_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'passw0rd',
    'db': 'big_e',
    'charset': 'utf8'
}


def mysql_con(config, cur_class=None):
    con = MySQLdb.connect(**config)
    cur = con.cursor(cur_class)
    return con, cur


def get_bz_con(cur_class=None):
    return mysql_con(bz_config, cur_class)


def get_etl_con(cur_class=None):
    return mysql_con(etl_config, cur_class)


if __name__ == '__main__':
    con = get_bz_con()
    print con

    #etl_con()
