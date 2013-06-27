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

class Nutrition:

  def generateData(self,cons_type, constid):
    data = {}
    constype = "cluster"
    if cons_type == 4:
      data["const_type"]='CLUSTER'
      constype = "cluster"
    elif cons_type == 5:
      data["const_type"]='BLOCK'
      constype = "block"
    data["const_name"]=str(constid[0])
    try:
      data.update(self.getEnrollment(constype,constid))
      data.update(self.getMidDayMealData(constype,constid))
    except:
      print 'Error occurred....'
      cursor.close()
      traceback.print_exc(file=sys.stderr)
    return data

  def getEnrollment(self,constype,constid):
    data = {}
    querykeys = ['dise_enrol','klp_enrol'] 
    for querykey in querykeys:
      cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      for row in result:
        data[querykey] = {'numboys':row[0],'numgirls':row[1]} 
      connection.commit()
    querykey = 'sch_count'
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      data[querykey] = {'totsch':row[0],'mdmsch':row[1]} 
    connection.commit()
    return data

  def getMidDayMealData(self,constype,constid):
    data = {}
    querykey = 'mdm_agg' 
    cursor.execute(db.Queries.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    tabledata ={}
    for row in result:
      if row[0] in tabledata:
        tabledata[row[0]][row[1]]=[row[2],row[3]]
      else:
        tabledata[row[0]]={row[1]:[row[2],row[3]]}
        data['const_name']=row[4]
    data[querykey] = tabledata
    connection.commit()
    return data
