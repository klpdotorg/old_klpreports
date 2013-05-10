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

class Learning:

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
    data.update(self.getSchoolAssessment(constype,constid))
    data.update(self.getAngAssessment(constype,constid))
    return data

  def getSchoolAssessment(self,constype,constid):
    data = {}
    queries = ['sch_assess_class','sch_assess_gender'] 
    for querykey in queries:
      tabledata = {}
      cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      for row in result:
        if row[0] in tabledata.keys():
          tabledata[row[0]][row[1]] = row[2]
        else:
          tabledata[row[0]] = {row[1]:row[2]}
      for each in tabledata.keys():
        tabledata[each]["total"] = sum(tabledata[each].values())
      data[querykey] = tabledata
      connection.commit()
    queries = ['sch_assess_bang','sch_assess_const'] 
    for querykey in queries:
      tabledata = {}
      cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      for row in result:
        if row[0] not in tabledata.keys():
          tabledata[row[0]] = row[1]
      tabledata["total"] = sum(tabledata.values())
      data[querykey] = tabledata
      connection.commit()
    querykey = 'sch_assess_cnt' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      data[querykey] = row[0]
      data['sch_assess_stucnt'] = row[1]
    querykey = 'sch_assess_bang_cnt' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      data[querykey] = row[0]
    return data
  
  def getAngAssessment(self,constype,constid):
    data = {}
    queries = ['ang_assess_score','ang_assess_bang']
    for querykey in queries:
      tabledata = {}
      cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      for row in result:
        data[querykey] = row[0] 
      connection.commit()
    tabledata = {}
    querykey = 'ang_assess_gender' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      tabledata[row[0]] = row[1]
    data[querykey] = tabledata
    connection.commit()
    querykey = 'ang_assess_cnt' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      data[querykey] = row[0]
      data['ang_assess_stucnt'] = row[1]
    querykey = 'ang_assess_bang_cnt' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      data[querykey] = row[0]
    return data

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    data.update(self.neighboursData(ret_data[1],ret_data[2]))
    return data

  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype
    tabledata = {}
    try:
      if len(neighbours) > 0:
        query_keys = ['ang_assess_neighbor']
        for key in query_keys:
          cursor.execute(db.Queries.getDictionary(constype)[constype_str+'_'+key], [tuple(neighbours)])
          result = cursor.fetchall()
          for row in result:
            if row[0].strip() in tabledata.keys():
              tabledata[row[0].strip()][row[1]]=row[2]
            else:
              tabledata[row[0].strip()]={row[1]:row[2]}
          data[key] = tabledata
      connection.commit()
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None
