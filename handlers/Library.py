import web
import psycopg2
import traceback
import sys, os,traceback
from operator import itemgetter
import db.KLPDB
import utils.QueryConstants
from utils.CommonUtil import CommonUtil

connection = db.KLPDB.getConnection()
cursor = connection.cursor()

class Library:

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
    data.update(self.getLibInfra(constype,constid))
    data.update(self.getLibMisc(constype,constid))
    data.update(self.getLibTxnsOverTime(constype,constid))
    data.update(self.getLibTxnsOverClass(constype,constid))
    return data

  def getLibInfra(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_count' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      lib_count = row[0]
    data[querykey] = lib_count
    connection.commit()
    querykey = 'lib_status' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    akshara_run = ['Working','Closed']
    akshara_exp = ['Working']
    teachers = ['Handed over','Not Working']
    librarian_count = 0
    teachers_count = 0
    library_exp = 0
    for row in result:
      if len(row[0].strip()) == 0:
        tabledata['No Library Programme'] = row[1]
      else:
        tabledata[row[0]] = row[1]
      if row[0].strip() in akshara_run:
        librarian_count = librarian_count + int(row[1])
      if row[0].strip() in akshara_exp:
        library_exp = library_exp + int(row[1])
      if row[0].strip() in teachers:
        teachers_count = teachers_count + int(row[1])
    data[querykey] = tabledata
    data['librarian_count'] = librarian_count
    data['teachers_count'] = teachers_count
    data['library_exp'] = library_exp
    connection.commit()
    tabledata = {}
    querykey = 'lib_summary' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      tabledata['total_books'] = row[0]
      tabledata['total_racks'] = row[1]
      tabledata['total_tables'] = row[2]
      tabledata['total_chairs'] = row[3]
      tabledata['total_comps'] = row[4]
      tabledata['total_ups'] = row[5]
    data[querykey] = tabledata
    connection.commit()
    return data

  def getLibMisc(self,constype,constid):
    data = {}
    querykey = 'gend_sch' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    chartdata ={}
    for row in result:
      chartdata[str(row[0].strip())] = int(row[1])
    total = chartdata['Boy']+chartdata['Girl']
    data["lib_stucount"] = total 
    connection.commit()

    querykey = 'moi_sch' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    tabledata = {}
    for row in result:
      tabledata[str(row[0].strip().title())] = str(int(row[1]))
    sorted_x = sorted(tabledata.items(), key=itemgetter(1))
    tabledata = dict(sorted_x)
    if len(tabledata.keys()) > 0:
      data["lib_moicount"] = tabledata
    connection.commit()
    return data

  def getLibTxnsOverTime(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_lang' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0] in tabledata.keys():
	tabledata[row[0]][row[2]]=row[3]
      else:
      	tabledata[row[0]]={row[2]:row[3]}
    connection.commit()
    data[querykey] = tabledata
    tabledata = {}
    querykey = 'lib_level' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0] in tabledata.keys():
	tabledata[row[0]][row[2]]=row[3]
      else:
      	tabledata[row[0]]={row[2]:row[3]}
    connection.commit()
    data[querykey] = tabledata
    return data
  
  def getLibTxnsOverClass(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_class_lang' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0]:
        if row[0] in tabledata.keys():
	  tabledata[str(row[0])][row[1]]=row[2]
        else:
      	  tabledata[str(row[0])]={row[1]:row[2]}
    connection.commit()
    data[querykey] = tabledata
    tabledata = {}
    querykey = 'lib_class_level' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0]:
        if row[0] in tabledata.keys():
	  tabledata[row[0]][row[1]]=row[2]
        else:
      	  tabledata[row[0]]={row[1]:row[2]}
    connection.commit()
    data[querykey] = tabledata
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
        crit='neighbours_'
        query_keys = ['libtxn','libinfra','libstu', 'libschcount']
        for key in query_keys:
          cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str+'_'+crit+key], [tuple(neighbours)])
          result = cursor.fetchall()
          for row in result:
            if row[0].strip() in tabledata.keys():
              tabledata[row[0].strip()][key]=row[1]
            else:
              tabledata[row[0].strip()]={key:row[1]}
      data['neighbours_lib'] = tabledata
      connection.commit()
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None
