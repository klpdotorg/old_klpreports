import web
import psycopg2
import traceback
import sys, os,traceback
import db.KLPDB
import db.Queries

cursor = db.KLPDB.getWebDbConnection()

class Links:

  def getMPreports(self):
    mps = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_mp_ids'])
    for row in result:
      mps[row['const_ward_name']] = row['mp_const_id']
    return mps
        
  def getMLAreports(self):
    mlas = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_mla_ids'])
    for row in result:
      mlas[row['const_ward_name']] = row['mla_const_id']
    return mlas

  def getWardreports(self):
    pass

  def getSchDistreports(self):
    pass

  def getBlkreports(self):
    blks = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_block'])
    for row in result:
      blks[row['block']] = row['blck_id']
    return blks 

  def getClusreports(self):
    clus = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_cluster'])
    for row in result:
      clus[row['clust']] = row['clst_id']
    return clus 

  def getPreDistreports(self):
    pass

  def getProjreports(self):
    pass

  def getCircreports(self):
    pass

