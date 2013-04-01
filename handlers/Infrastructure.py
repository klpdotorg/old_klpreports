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

class Infrastructure:

  def generateData(self,cons_type, constid):
    data = {}
    avgdata = {}
    avgdata = self.getAverages()

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
    data.update(self.getAngInfra(constype,constid,avgdata))
    data.update(self.getSchoolInfra(constype,constid,avgdata))
    return data

  def getAverages(self):
    data = {}
    querykeys = ['get_dise_count_blore','get_sch_count_blore','get_ai_count_blore','get_ang_count_blore']
    for key in querykeys:
      cursor.execute(utils.QueryConstants.getDictionary("common_queries")[key])
      result = cursor.fetchall()
      for row in result:
        data[key.replace("get_","")] = row[0]
      connection.commit()
    querykeys = ['get_dise_avg_blore','get_ai_avg_blore']
    for key in querykeys:
      tabledata = {}
      cursor.execute(utils.QueryConstants.getDictionary("common_queries")[key])
      result = cursor.fetchall()
      for row in result:
        if 'dise' in key:
          tabledata[row[0]] = str(int(row[1]) * 100/int(data['dise_count_blore']))
        else:
          tabledata[row[0]] = str(int(row[1]) * 100/int(data['ai_count_blore']))
      data[key.replace("get_","")] = tabledata
      connection.commit()
    return data

  def getAngInfra(self,constype,constid,data):
    tabledata = {}
    
    blore_count = data['ai_count_blore']
    blore_infra = data['ai_avg_blore']

    querykey = 'infra_count'
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
     infra_count = row[0]
    data[querykey] = infra_count
    connection.commit()

    querykey = 'ang_infra' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0] in ['waste_basket','toilet','toilet_roof','akshara_kits']:
        pass
      else:
        if row[2] in tabledata:
          tabledata[row[2]][row[0]]=[str(int(row[1])*100/int(infra_count)),str(blore_infra[row[0]])]
        else:
          tabledata[row[2]] = {row[0]:[str(int(row[1])*100/int(infra_count)),str(blore_infra[row[0]])]}
    data[querykey] = tabledata
    connection.commit()
    return data

  def getSchoolInfra(self,constype,constid,data):
    tabledata = {}

    blore_count = data['dise_count_blore']
    blore_dise = data['dise_avg_blore']

    querykey = 'dise_count'
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
     dise_count = row[0]
    data[querykey] = dise_count
    connection.commit()

    querykey = 'dise_facility' 
    cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0] in ['toilet_all','ramp','medical']:
        pass
      else:
        if row[2] in tabledata:
          tabledata[row[2]][row[0]]=[str(int(row[1])*100/int(dise_count)),str(blore_dise[row[0]])]
        else:
          tabledata[row[2]] = {row[0]:[str(int(row[1])*100/int(dise_count)),str(blore_dise[row[0]])]}
    data[querykey] = tabledata
    connection.commit()
    return data


  def neighboursData(self, neighbours, constype, constid):
    data = {}
    constype_str = constype
    try:
      querykey = 'neighbours_df_count'
      cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],[tuple(neighbours)])
      result = cursor.fetchall()
      dise_count = {} 
      for row in result:
        dise_count[row[0]] = int(row[1])
      data[querykey] = dise_count
      connection.commit()

      querykey = 'neighbours_ai_count'
      cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],[tuple(neighbours)])
      result = cursor.fetchall()
      infra_count = {} 
      for row in result:
        infra_count[row[0]] = int(row[1])
      data[querykey] = infra_count
      connection.commit()

      if len(neighbours) > 0:
        crit='neighbours_'
        query_keys = ['dise','anginfra']
        for key in query_keys:
          tabledata = {}
          counts_dict = {}
          if key == 'dise' :
            counts_dict = dise_count
          else:
            counts_dict = infra_count
          cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str+'_'+crit+key], [tuple(neighbours)])
          result = cursor.fetchall()
          for row in result:
            if row[1] in ['waste_basket','toilet','toilet_roof','akshara_kits','toilet_all','ramp','medical']:
              pass
            else:
              if row[0].strip() in tabledata.keys():
                  tabledata[row[0].strip()][row[3] + '|' + row[1]] = int(row[2])*100/counts_dict[row[0].strip()]
              else:
                tabledata[row[0].strip()]={row[3]+'|'+ row[1]:int(row[2])*100/counts_dict[row[0].strip()]}

          newtable = {}

          for tabkey in tabledata.keys():
            moddata = {}
            moddata = tabledata[tabkey]
            for each in moddata.keys():
              if each in newtable.keys():
                newtable[each][tabkey] = moddata[each] 
              else:
                newtable.update({ each:{tabkey:moddata[each]}})
          data[crit+key] = newtable

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
    neighboursdata  = self.neighboursData(ret_data[1],ret_data[2],constid)
    if neighboursdata:
      data.update(neighboursdata)
    return data
