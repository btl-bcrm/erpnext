import cx_Oracle

db_host   = "10.0.41.145"
db_usr    = "BSCSREAD"
db_pwd    = "BSCSREAD"
db_db     = "BSCSPROD2"
db_string = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 10.0.41.145)(PORT = 1571)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = BSCSPROD2)))"

def ResultIter(cursor, arraysize=5000):
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

class db:
    def __init__(self):
        try:
            self.dsn = cx_Oracle.makedsn(db_host,1571,db_db)
            self.con = cx_Oracle.connect(db_usr, db_pwd, self.dsn)
            self.cursor = self.con.cursor()
            print 'Connection successfull...'
        except cx_Oracle.DatabaseError,info:
            print "DB_ERROR",info

    def sql(self, query=None):
        if query is None:
            pass
        else:
            try:
                self.cursor.execute(query)
                return ResultIter(self.cursor)
            except Exception,e:
                print 'DB_ERROR: Error while executing the query\n'+str(e)+str(query)
                return False

    def commit(self):
        if self.con:
            self.con.commit()

    def rollback(self):
        if self.con:
            self.con.rollback()

    def close(self):
        if self.con:
            self.con.close()
            print 'Connection closed successfully...'
                
    def columns(self):
        if self.con:
            return [i[0] for i in self.cursor.description]

#
# Queries
#

query = {"customer": """
            select 
                ca.custcode,ca.customer_id,
                decode(ca.cstype,'a','Active','s','Suspended','d','Deactivated','i','Interested',ca.cstype) customer_status,
                decode(cca.cscusttype,'C','Individual','B','Company',cca.cscusttype) as customer_type,
                decode(cca.country,26,c.name,'Rest Of The World') as territory,
                decode(cca.ccsex,'M','Male','F','Female',cca.ccsex) as gender,
                cca.ccname, cca.ccfname, cca.cclname,
                cca.ccemail, cca.ccsmsno,
                cca.ccstreetno, cca.ccstreet, cca.ccaddr1, cca.ccaddr2, cca.ccaddr3,
                cca.cccity, cca.country, c.name, 
                (select bd.description
                from (
                        select bcah.*, rank() over (partition by bcah.customer_id order by bcah.valid_from desc) rnk
                        from billcycle_assignment_history bcah
                        where bcah.customer_id = ca.customer_id
                    ) bc, billcycle_definition bd
                where bc.rnk=1
                and bd.billcycle = bc.billcycle
                ) billcycle_description
            from customer_all ca
                    left outer join ccontact_all cca on cca.customer_id = ca.customer_id and cca.ccseq=1
                    left outer join country c on c.country_id = cca.country
            where exists(select 1
                                    from contract_all co, pr_serv_status_hist sh
                                    where co.customer_id = ca.customer_id 
                                    and sh.co_id = co.co_id
                                    and sh.sncode in (1415,1416,1417,1418,1419,1420,1421,1423,
                                        1425,1426,1427,1428,1429,1430,1431,1817,
                                        1818,1819,1820,1821,1822,1823,1824))
        """,
        "service": """
            select sncode, des, shdes
            from MPUSNTAB
            where sncode in (1415,1416,1417,1418,
                            1419,1420,1421,1423,
                            1425,1426,1427,1428,
                            1429,1430,1431,1817,
                            1818,1819,1820,1821,
                            1822,1823,1824)
        """,
}
