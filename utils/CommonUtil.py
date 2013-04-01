import web
import psycopg2
import traceback
import sys, os,traceback
import db.KLPDB
import utils.QueryConstants

connection = db.KLPDB.getConnection()
cursor = connection.cursor()

class CommonUtil:

  def constituencyData(self,constype,constid):
    data = {}
    result = []
    neighbours = []
    constype_str = constype 
    try:
      #constype_str = "mp"
      #if constype == 1:
      #  constype_str = "mp"
      #elif constype == 2:
      #  constype_str = "mla"
      #elif constype == 3:
      #  constype_str = "corporator"
      cursor.execute(utils.QueryConstants.getDictionary(constype)[constype_str + '_const_details'],constid)
      result = cursor.fetchall()
      for row in result:
        data['const_name'] = row[1].strip() if row[1] != None else ''
        data['const_type'] = row[3].strip() if row[3] != None else ''
        data['const_code'] = row[0] if row[0] != None else ''
        data['const_rep'] = row[2].strip() if row[2] != None else ''
        data['const_party'] = row[5].strip() if row[5] != None else ''
        if row[4] != None:
          neighbours = row[4].strip().split('|')
          neighbours.append(row[0])
      connection.commit()
      return [data,neighbours,constype_str]
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()

  def countsTable(self,cons_type,constid,qkeys):
    try:
      constype = "mp"
      if cons_type == 1:
        constype = "mp"
      elif cons_type == 2:
        constype = "mla"
      elif cons_type == 3:
        constype = "corporator"
      data = {}
      tabledata = {}
      for querykey in qkeys:
        cursor.execute(utils.QueryConstants.getDictionary(constype)[constype + '_' + querykey], constid)
        result = cursor.fetchall()
        for row in result:
          tabledata[querykey] = str(row[0])
      data["inst_counts"] =  tabledata
      connection.commit()
      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None

  def getTranslations(self, lang):
    transDict = {}
    f = open(os.path.join(os.getcwd(),'translations/translations_heading.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 1:
        transDict['H' + str(text[0])] = text[2].strip('\n')
      else:
        transDict['H' + str(text[0])] = text[1]
    f = open(os.path.join(os.getcwd(),'translations/translations_dict.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 1:
        transDict[str(text[0])] = text[1].strip('\n')
      else:
        transDict[str(text[0])] = text[0]
    return transDict
