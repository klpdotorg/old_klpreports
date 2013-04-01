import web
import psycopg2
import decimal
import jsonpickle
import csv
import re
from web import form
import datetime
import traceback
import simplejson
import codecs
from operator import itemgetter

# Needed to find the templates
import sys, os,traceback
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import db.KLPDB
import utils.QueryConstants
import utils.DemographicsUtil
import utils.FinancesUtil
import utils.InfraUtil
import utils.LibraryUtil
import utils.NutritionUtil
from utils.CommonUtil import CommonUtil

from handlers.Demographics import Demographics
from handlers.Infrastructure import Infrastructure
from handlers.Finances import Finances
from handlers.Library import Library
from handlers.Nutrition import Nutrition 

render = web.template.render('templates/')

urls = (
     '/charts/(.*)/(.*)/(.*)/(.*)','Charts',
)

application = web.application(urls,globals()).wsgifunc()

class Charts:
  
  """Returns the main template"""
  def GET(self,searchby,constid,rep_lang,rep_type):
    constype = int(searchby)
    lang = 2
    if rep_lang=='1':
      lang = 1
    data = {}
    util = CommonUtil()
    if rep_type == '1':
      demographics = Demographics()
      queries = ['schcount','preschcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(demographics.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(utils.DemographicsUtil.getDemographicsText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.demographics(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '2':
      finances = Finances()
      queries = ['abs_schcount','fin_schcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(finances.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(utils.FinancesUtil.getFinancesText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.finances(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '3':
      infra = Infrastructure()
      queries = ['abs_schcount','abs_preschcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(infra.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(utils.InfraUtil.getInfraText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.infrastructure(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '4':
      library = Library()
      queries = ['abs_schcount','abs_preschcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(library.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(utils.LibraryUtil.getLibText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.library(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '5':
      nutrition = Nutrition()
      data.update(nutrition.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(utils.NutritionUtil.getNutriText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.nutrition(simplejson.dumps(data,sort_keys=True))
    else:
      pass

