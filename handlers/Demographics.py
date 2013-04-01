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

class Demographics:

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

    queries = ['gend_sch','gend_presch']
    data.update(self.genderGraphs(constype,constid,queries))
    queries = ['mt_sch','mt_presch']
    data.update(self.mtGraphs(constype,constid,queries))
    queries = ['moi_sch','cat_sch','enrol_sch','enrol_presch']
    data.update(self.pieGraphs(constype,constid,queries))
    data.update(self.constituencyData(constype,constid))
    return data


  def genderGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      chartdata ={}
      for row in result:
        chartdata[str(row[0].strip())] = int(row[1])
      if len(chartdata.keys()) > 0:
        total = chartdata['Boy']+chartdata['Girl']
        percBoys = round(float(chartdata['Boy'])/total*100,0)
        percGirls = round(float(chartdata['Girl'])/total*100,0)
        data[querykey+"_tb"]=chartdata
      else:
        data[querykey+"_hasdata"] = 0
      connection.commit()
    return data

  def mtGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      tabledata = {}
      invertdata = {}
      order_lst = []
      for row in result:
        invertdata[int(row[1])] = str(row[0].strip().title())
      if len(invertdata.keys()) > 0:
        checklist = sorted(invertdata)
        others = 0
        for i in checklist[0:len(checklist)-4]:
          others = others + i
          del invertdata[i]
        invertdata[others] = 'Others'
        tabledata = dict(zip(invertdata.values(),invertdata.keys()))
        if 'Other' in tabledata.keys():
          tabledata['Others'] = tabledata['Others'] + tabledata['Other']
          del tabledata['Other']
      for i in sorted(tabledata,key=tabledata.get,reverse=True):
        order_lst.append(i)
      if len(tabledata.keys()) > 0:
        data[querykey + "_tb"] = tabledata
        data[querykey + "_ord_lst"] = order_lst 
      else:
        data[querykey + "_hasdata"] = 0
      connection.commit()
    return data

  def pieGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      tabledata = {}
      for row in result:
        tabledata[str(row[0].strip().title())] = str(int(row[1]))
      sorted_x = sorted(tabledata.items(), key=itemgetter(1))
      tabledata = dict(sorted_x)
      if len(tabledata.keys()) > 0:
        data[querykey + "_tb"] = tabledata
      else:
        data[querykey + "_hasdata"] = 0
      connection.commit()
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
    try:
      if len(neighbours) > 0:
        neighbours_sch = {}
        neighbours_presch = {}
        
        cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str + '_neighbour_sch'], [tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_sch[row[0].strip()]={'schcount':str(row[1])}
        connection.commit()

        cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str + '_neighbour_presch'], [tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_presch[row[0].strip()] = {'preschcount':str(row[1])}
        connection.commit()
         
        cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str + '_neighbour_gendsch'],[tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_sch[row[0].strip()][row[1].strip()] = str(row[2])
        connection.commit()
        
        cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str + '_neighbour_gendpresch'],[tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_presch[row[0].strip()][row[1].strip()] = str(row[2])
        
        if len(neighbours_sch.keys()) > 0: 
          data["neighbours_sch"] = neighbours_sch          
        else:
          data["neighbours_sch_hasdata"] = 0

        if len(neighbours_presch.keys()) > 0: 
          data["neighbours_presch"] = neighbours_presch          
        else:
          data["neighbours_presch_hasdata"] = 0
        
        connection.commit()

      else:
        data["neighbours_sch_hasdata"] = 0
        data["neighbours_presch_hasdata"] = 0

      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None
