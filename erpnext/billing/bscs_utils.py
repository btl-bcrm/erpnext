import cx_Oracle
import logging

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
        # Logging
        logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        try:
            self.dsn = cx_Oracle.makedsn(db_host,1571,db_db)
            self.con = cx_Oracle.connect(db_usr, db_pwd, self.dsn)
            self.cursor = self.con.cursor()
            logger.info('|'.join(str(i) for i in ['SUCCESS','Connected to BSCS successfully...']))
        except cx_Oracle.DatabaseError,info:
            logger.exception("|".join(str(i) for i in ["ERROR",'Failed to connect BSCS']))
            return False

    def sql(self, query=None):
        if query is None:
            pass
        else:
            try:
                self.cursor.execute(query)
                return ResultIter(self.cursor)
            except Exception,e:
                print 'SQL_ERROR: Error while executing the query\n'+str(e)+str(query)
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

query = {"customers": """
            select 
                ca.customer_id,ca.custcode,
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
                ) billcycle_description,
                ca.customer_id_high,
                ca.cscurbalance
            from customer_all ca
                    left outer join ccontact_all cca on cca.customer_id = ca.customer_id and cca.ccseq=1
                    left outer join country c on c.country_id = cca.country
            where exists(select 1
                         from contract_all co, pr_serv_status_hist sh
                         where co.customer_id = ca.customer_id 
                         and sh.co_id = co.co_id
                         and sh.sncode in {0})
        """,
        "large_customers": """
            select 
                ca.customer_id,ca.custcode,
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
                ) billcycle_description,
                ca.customer_id_high,
                ca.cscurbalance
            from customer_all ca
                    left outer join ccontact_all cca on cca.customer_id = ca.customer_id and cca.ccseq=1
                    left outer join country c on c.country_id = cca.country
            where exists(select 1
                         from customer_all ca2,contract_all co, pr_serv_status_hist sh
                         where ca2.customer_id_high = ca.customer_id
                         and co.customer_id = ca2.customer_id 
                         and sh.co_id = co.co_id
                         and sh.sncode in {0})
        """,
        "contract": """
            select 
                    co.co_id,
                    co.co_code,
                    co.customer_id, 
                    decode(co.ch_status,'a','Active','s','Suspended','d','Deactivated','o','On-hold',co.ch_status) as contract_status,
                    co.co_installed,
                    co.co_moddate,
                    sc.dn_id,
                    dn.dn_num,
                    dn.dn_status
            from contract_all co
                left outer join contr_services_cap sc on sc.co_id = co.co_id
                left outer join directory_number dn on dn.dn_id = sc.dn_id
            where exists(select 1
                         from pr_serv_status_hist sh
                         where sh.co_id = co.co_id
                         and sh.sncode in {0})
        """,
        "service": """
            select sncode, des, shdes
            from MPUSNTAB
            where sncode in {0}
        """,
        "contract_service": """
            select
                    sh.co_id||'|'||sh.sncode||'|'||sh.profile_id||'|'||sh.histno name,
                    sh.co_id,
                    ca.customer_id,
                    sh.sncode,
                    sn.des,
                    decode(sh.status,'A','Active','S','Suspended','D','Deactivated','O','On-hold',sh.status) as service_status,
                    sh.valid_from_date
            from pr_serv_status_hist sh
                    inner join mpusntab sn on sn.sncode = sh.sncode
                    inner join contract_all co on co.co_id = sh.co_id
                inner join customer_all ca on ca.customer_id = co.customer_id
            where sh.sncode in {0}
        """
}
