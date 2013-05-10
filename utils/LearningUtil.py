import csv
import traceback

import sys, os,traceback

def getLearningText(data,lang):

    transDict = {}
    f = open(os.path.join(os.getcwd(),'translations/learn_translations_text.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 2:
        transDict[str(text[0])] = text[1]
      else:
        transDict[str(text[0])] = text[2]

    learningintro_txt = transDict['1']
    source_txt = transDict['7']
    angexpln_txt = transDict['13']

    data['learningintro_txt'] = learningintro_txt
    data['source_txt'] = source_txt
    data['angexpln_txt'] = angexpln_txt

    schassess_txt = transDict['2'] + str(data['sch_assess_bang_cnt']) 
    schassess_txt = schassess_txt + transDict['3'] + str(data['sch_assess_cnt'])
    schassess_txt = schassess_txt + transDict['11'] + str(data['sch_assess_stucnt'])
    data['schassess_txt'] = schassess_txt

    angassess_txt = transDict['4']
    angassess_txt = angassess_txt + transDict['5'] + str(data['ang_assess_bang_cnt'])
    angassess_txt = angassess_txt + transDict['6'] + str(data['ang_assess_cnt'])
    angassess_txt = angassess_txt + transDict['12'] + str(data['ang_assess_stucnt'])
    data['angassess_txt'] = angassess_txt
         
    return data

def formatIndian(inputNum) :
  prefStr = ''
  outputString = ''
  minus = ''
  suf = ''
  lastThree = ''
  try:
    inputString = str(inputNum)
    if '.' in inputString:
      numberArray = inputString.split('.', 2)
      pref = int(numberArray[0])
      suf = numberArray[1]
    else:
      pref = inputString
      suf = ''
    outputString = ''
    minus = ''
    if pref < 0:
      minus = '-'
    prefStr = str(pref)
    if len(prefStr) > 3 :
      lastThree = prefStr[len(prefStr)-3: len(prefStr)]
      prefStr = prefStr[0: len(prefStr)-3]
    if len(prefStr) % 2 > 0 :
      outputString = outputString + prefStr[0:1] + ','
      prefStr = prefStr[1: len(prefStr)]

    while (len(prefStr) >= 2) :
      outputString = outputString +  prefStr[0:2] + ','
      prefStr = prefStr[2:len(prefStr)]

    outputString = minus + outputString +  lastThree + suf
    return outputString
  except:
    print 'Error occurred'
    print "Unexpected error:", sys.exc_info()
    traceback.print_exc(file=sys.stdout)
    return 'NaN'
