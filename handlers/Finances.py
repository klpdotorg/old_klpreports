import web
import psycopg2
import traceback
import sys, os,traceback
from operator import itemgetter
import db.KLPDB
import db.Queries
from utils.CommonUtil import CommonUtil

connection = db.KLPDB.getConnection()
cursor = connection.cursor()

class Finances:

  def generateData(self,cons_type, constid):
    data = {}
    constype = "mp"
    if cons_type == 1:
      data["const_type"]='MP'
      constype = "mp"
    elif cons_type == 2:
      data["const_type"]='MLA'
      constype = "mla"
    elif cons_type == 3:
      data["const_type"]='Corporator'
      constype = "corporator"
    data["const_name"]=str(constid[0])
    data.update(self.constituencyData(constype,constid))
    data.update(self.getTLMGrant(constype,constid))
    data.update(self.getAnnualGrant(constype,constid))
    data.update(self.getMaintenanceGrant(constype,constid))
    return data

  def getTLMGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'tlmgrant_sch' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      tabledata['grant_amount'] = str(row[3])
      tabledata['teacher_count'] = str(int(row[3])/int(row[2]))
    data[querykey] = tabledata
    data['total_tlm']=int(tabledata['grant_amount'])
    connection.commit()
    return data
  
  def getAnnualGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'annualgrant_sch' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    total_grant = 0
    for row in result:
      tabledata[row[1]] = [str(row[3]),str(row[4])]
      total_grant = total_grant + int(row[4])
    data[querykey] = tabledata
    data['total_annual'] = total_grant
    connection.commit()
    return data
   
  def getMaintenanceGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'mtncgrant_sch' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    total_grant = 0
    for row in result:
      tabledata[row[2]] = [str(row[3]), str(row[4])]
      total_grant = total_grant + int(row[4])
    data[querykey] = tabledata
    data['total_mntc'] = total_grant
    connection.commit()
    return data

  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype 
    tabledata = {}
    try:
      if len(neighbours) > 0:
        crit='neighbor_'
        query_keys = ['tlm','annual','mntnc'] 
        for key in query_keys:
          cursor.execute(db.Queries.getDictionary(constype)[constype_str+'_'+crit+key], [tuple(neighbours)])
          result = cursor.fetchall()
          for row in result:
            if row[0].strip() in tabledata.keys():
              if key in tabledata[row[0].strip()].keys():
                addedup = int(tabledata[row[0].strip()][key]) + int(row[3])
                tabledata[row[0].strip()][key] = addedup
              else:
                tabledata[row[0].strip()][key] = row[3]
            else:
              tabledata[row[0].strip()]={key:row[3]}
      data['neighbours_grant'] = tabledata
      connection.commit()
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    data.update(self.neighboursData(ret_data[1],ret_data[2]))
    return data
