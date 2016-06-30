import PySQLPool

#bz_config = {
#    'host': 'bz3-db3.eng.vmware.com',
#    'port': 3306,
#    'user': 'mts',
#    'passwd': 'mts',
#    'db': 'bugzilla'
#}

unifiedCon = PySQLPool.getNewConnection(username='root', password='vmware', host='unified.eng.vmware.com', db='unified')
bugzillaCon = PySQLPool.getNewConnection(username='mts', password='mts', host='bz3-db3.eng.vmware.com', db='bugzilla')

def getQueryUnified():
    return PySQLPool.getNewQuery(unifiedCon, commitOnEnd = True)


def getQueryBugzilla():
    return PySQLPool.getNewQuery(bugzillaCon)



if __name__ == '__main__':
    c1 = getQueryUnified()
    print c1
    c2 = getQueryBugzilla()
    print c2
