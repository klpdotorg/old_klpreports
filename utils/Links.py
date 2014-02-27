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
      mps[row['const_ward_name']] = [row['mp_const_id'],row['bang_yn']]
    return mps
        
  def getMLAreports(self):
    mlas = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_mla_ids'])
    for row in result:
      mlas[row['const_ward_name']] = [row['mla_const_id'],row['bang_yn']]
    return mlas

  def getWardreports(self):
    wards = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_ward_ids'])
    for row in result:
      wards[row['const_ward_name']] = [row['ward_id'],row['bang_yn']]
    return wards

  def getSchDistreports(self):
    schldists = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_schdist'])
    for row in result:
      schldists[row['district']] = [row['dist_id'],row['bang_yn']]
    return schldists

  def getBlkreports(self):
    blks = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_block'])
    for row in result:
      blks[row['block']] = [row['blck_id'],row['bang_yn']]
    return blks 

  def getClusreports(self):
    clus = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_cluster'])
    for row in result:
      clus[row['clust']] = [row['clst_id'],row['bang_yn']]
    return clus 

  def getPreDistreports(self):
    predists = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_preschdist'])
    for row in result:
      predists[row['district']] = [row['dist_id'],row['bang_yn']]
    return predists

  def getProjreports(self):
    proj = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_proj'])
    for row in result:
      proj[row['block']] = [row['blck_id'],row['bang_yn']]
    return proj

  def getCircreports(self):
    circ = {}
    result = cursor.query(db.Queries.getDictionary("common")['get_cluster'])
    for row in result:
      circ[row['clust']] = [row['clst_id'],row['bang_yn']]
    return circ


