from misc import *

def printTable(data,columnTitles=None,rowTitles=None,splitColumnTitles=False):
  """
  Prints out a nicely formatted table of data.

  data is a list of lists
    each element of data is a line, and each element of that is a row entry

  If splitColumnTitles is True, then will split titles into multiple lines at spaces to make narrower
  """

  def splitString(instr, length):
    sstr = instr.split(" ")
    result = []
    for substr in sstr:
      if len(result) == 0:
        result.append(substr) # make new line
        continue
      lastLen = len(result[-1])
      if lastLen >= length:
        result.append(substr) # make new line
        continue
      substrLen = len(substr)
      if lastLen + substrLen > length + 5:
        result.append(substr) # make new line
        continue
      result[-1] += " "+substr # add text to existing line
    return result

  nRows = len(data)
  if nRows == 0:
    return
  if rowTitles and (len(rowTitles) != nRows):
    exceptionStr = "Different number of rows ({}) and rowTitles ({})".format(nRows,len(rowTitles))
    raise Exception(exceptionStr)
  if splitColumnTitles: # keep from modifying referenced argument passed in
    columnTitles = copy.deepcopy(columnTitles)
  nCols = None
  colLengths = None
  for row in data:
    if nCols is None:
      nCols = len(row)
      colLengths = [0]*nCols
    else:
      if len(row) != nCols:
        exceptionStr = "Row ({}) has a different number of columns from the rest ({})".format(row,nCols)
        raise Exception(exceptionStr)
    for iCol in range(nCols):
      if type(row[iCol])!=str:
        exceptionStr = "Row ({}) has an element ({}) that isn't a string".format(row,row[iCol])
        raise Exception(exceptionStr)
      colLengths[iCol] = max(len(row[iCol]),colLengths[iCol])
  nColumnTitleRows = 1
  if columnTitles:
    if len(columnTitles) != nCols:
        exceptionStr = "Length of column titles ({}) doesn't equal number of columns ({})".format(len(columnTitles),nCols)
        raise Exception(exceptionStr)
    for iCol in range(nCols):
      if type(columnTitles[iCol])!=str:
        exceptionStr = "Column title ({}) isn't a string".format(columnTitles[iCol])
        raise Exception(exceptionStr)
      if splitColumnTitles:
        columnTitles[iCol] = splitString(columnTitles[iCol],colLengths[iCol])
        for colTitleRow in columnTitles[iCol]:
          colLengths[iCol] = max(len(colTitleRow),colLengths[iCol])
      else:
        colLengths[iCol] = max(len(columnTitles[iCol]),colLengths[iCol])
    if splitColumnTitles:
      for colTitleRow in columnTitles:
        nColumnTitleRows = max(nColumnTitleRows,len(colTitleRow))

  rowCharLength = 0
  for iCol in range(nCols):
    if iCol != 0:
      rowCharLength += 1
    rowCharLength += colLengths[iCol]

  rowTitleLength = 0
  if rowTitles:
    for rowTitle in rowTitles:
      assert(type(rowTitle)==str)
      rowTitleLength = max(len(rowTitle),rowTitleLength)
    rowCharLength += rowTitleLength + 1

  print "="*rowCharLength
  if columnTitles:
    for iColumnTitleRow in range(nColumnTitleRows):
      outStr = ""
      if rowTitles:
        outStr += " "*(rowTitleLength + 1)
      for iCol in range(nCols):
        if iCol != 0:
          outStr += " "
        if splitColumnTitles:
          if len(columnTitles[iCol]) > iColumnTitleRow:
            outStr += ("{:"+str(colLengths[iCol])+"}").format(columnTitles[iCol][iColumnTitleRow])
          else:
            outStr += " "*colLengths[iCol]
        else:
          outStr += ("{:"+str(colLengths[iCol])+"}").format(columnTitles[iCol])
      print outStr
    print "-"*rowCharLength
  for iRow in range(len(data)):
    row = data[iRow]
    outStr = ""
    if rowTitles:
      outStr += ("{:"+str(rowTitleLength)+"} ").format(rowTitles[iRow])
    for iCol in range(nCols):
      if iCol != 0:
        outStr += " "
      outStr += ("{:>"+str(colLengths[iCol])+"}").format(row[iCol])
    print outStr
  print "="*rowCharLength

def printEvents(infilename,treename,variableNames,cuts={},printFullFilename=False,printFileBasename=False,nMax=100,friendTreeName=None,friendTreeFileName=None):
  tree = root.TChain(treename)
  try:
    if type(infilename) is str:
        tree.AddFile(infilename)
    elif type(infilename) is list:
        for fn in infilename:
            tree.AddFile(fn)
    else:
        raise Exception("")
  except KeyError:
    return
  if friendTreeFileName and friendTreeName:
    tree.AddFriend(friendTreeName,friendTreeFileName)
  nEvents = tree.GetEntries()
  nEvents = min(nEvents,nMax)
  allVals = []
  filenames = []
  for iEvent in range(nEvents):
    tree.GetEntry(iEvent)
    failedCuts = False
    for cutVar in cuts:
      cutOp = cuts[cutVar][0]
      cutVal = cuts[cutVar][1]
      if cutOp == "==" or cutOp == "=":
        if getattr(tree,cutVar) != cutVal:
          failedCuts = True
          break
      elif cutOp == "!=":
        if getattr(tree,cutVar) == cutVal:
          failedCuts = True
          break
      elif cutOp == ">":
        if getattr(tree,cutVar) <= cutVal:
          failedCuts = True
          break
      elif cutOp == "<":
        if getattr(tree,cutVar) >= cutVal:
          failedCuts = True
          break
      elif cutOp == ">=":
        if getattr(tree,cutVar) < cutVal:
          failedCuts = True
          break
      elif cutOp == "<=":
        if getattr(tree,cutVar) > cutVal:
          failedCuts = True
          break
      else:
        raise Exception("Unknown cut op: ",cutOp)
    if failedCuts:
      continue
    runNumber = tree.runNumber
    eventNumber = tree.eventNumber
    try:
        filenames.append(str(tree.infilename))
    except:
        filenames.append("No filename")
    vals = []
    vals.append("{:>05}:{:>05}".format(runNumber,eventNumber))
    for variableName in variableNames:
      try:
        val = getattr(tree,variableName)
      except:
        val = "Error"
      finally:
        if type(val) == root.string:
            val = str(val)
        if type(val) != str:
          try:
              val = val[0]
          except TypeError:
              pass
          except IndexError:
              val = "Empty"
        if type(val) == float:
          val = "{:g}".format(val)
        else:
          val = "{}".format(val)
        #val = variableName + ": "+val
        vals.append(val)
    if printFileBasename or printFullFilename:
      variableName = "infilename"
      try:
        val = getattr(tree,variableName)
      except:
        val = "Error"
      finally:
        val = str(val)
        if not printFullFilename:
          val = os.path.basename(val)
        #val = variableName + ": "+val
        vals.append(val)
    allVals.append(vals)
  columnTitles = ["Event"]+variableNames
  if printFileBasename or printFullFilename:
    columnTitles.append("File")
  printTable(allVals,columnTitles=columnTitles)

class PrintCutTable:

  def __init__(self,fileConfigs,cutConfigs,treename,errors=False,asymerrors=False,interval=False,nMax=sys.maxint):
    """
    similar to plotters, but cutConfigs is a list of dicts with key 
    'cut' as a cut string and 'name' or 'title' for the cut.
    """

    fileNames = self.getFileNames(fileConfigs)
    cutNames = self.getCutNames(cutConfigs)
    for fileConfig in fileConfigs:
      loadTree(fileConfig,treename)
    #countsIndiv = self.getCountsIndividualCut(fileConfigs,cutConfigs,nMax)
    countsCumu = self.getCountsCumulativeCut(fileConfigs,cutConfigs,nMax)
    #countsIndivPerTop = self.getPercOfTopRow(countsIndiv)
    countsCumuPerTop = self.getPercOfTopRow(countsCumu,errors=errors,asymerrors=asymerrors,interval=interval)
    countsCumuPerPrev = self.getPercOfPrevRow(countsCumu,errors=errors,asymerrors=asymerrors,interval=interval)
    #print "Individual Cuts"
    #printTable(countsIndiv,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)
    print "Cumulative Cuts"
    printTable(countsCumu,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)
    #print "Individual Cuts Percentage of Top Row"
    #printTable(countsIndivPerTop,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)
    print "Cumulative Cuts Percentage of Top Row"
    printTable(countsCumuPerTop,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)
    print "Cumulative Cuts Percentage of Previous Row"
    printTable(countsCumuPerPrev,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)

  def getCutNames(self,cutConfigs):
    cutNames = []
    for cutConfig in cutConfigs:
      cutName = ""
      try:
        cutName = cutConfig['title']
      except KeyError:
        try:
          cutName = cutConfig['name']
        except KeyError as e:
          print "cutConfig must have title or name!"
          raise e
      cutNames.append(cutName)
    return cutNames

  def getFileNames(self,fileConfigs):
    fileNames = []
    for fileConfig in fileConfigs:
      fileName = ""
      try:
        fileName = fileConfig['title']
      except KeyError:
        try:
          fileName = fileConfig['name']
        except KeyError as e:
          print "fileConfig must have title or name!"
          raise e
      fileNames.append(fileName)
    return fileNames

  def getEmptyCountsList(self,fileConfigs,cutConfigs):
    counts = []
    for iCut in range(len(cutConfigs)):
      counts.append([])
      for fileConfig in fileConfigs:
        counts[iCut].append("")
    return counts

  def getCountsIndividualCut(self,fileConfigs,cutConfigs,nMax):
    counts = self.getEmptyCountsList(fileConfigs,cutConfigs)
    binning = [1,0,2]
    var = "1"
    histConfig = {}
    for iCut in range(len(cutConfigs)):
      cutConfig = cutConfigs[iCut]
      thisCut = "("+cutConfig['cut']+")"
      for iFile in range(len(fileConfigs)):
        fileConfig = fileConfigs[iFile]
        hist = loadHist(histConfig,fileConfig,binning,var,thisCut,nMax,False)
        counts[iCut][iFile] = "{:.1f}".format(hist.Integral())
    return counts

  def getCountsCumulativeCut(self,fileConfigs,cutConfigs,nMax):
    counts = self.getEmptyCountsList(fileConfigs,cutConfigs)
    binning = [1,0,2]
    var = "1"
    histConfig = {}
    cutString = "(1"
    for iCut in range(len(cutConfigs)):
      cutConfig = cutConfigs[iCut]
      cutString += " && ("+cutConfig['cut']+")"
      for iFile in range(len(fileConfigs)):
        fileConfig = fileConfigs[iFile]
        hist = loadHist(histConfig,fileConfig,binning,var,cutString+")",nMax,False)
        counts[iCut][iFile] = "{:.1f}".format(hist.Integral())
    return counts

  def getPercOfTopRow(self,counts,errors=False,asymerrors=False,interval=False):
    topRow = []
    result = []
    for valStr in counts[0]:
      topRow.append(float(valStr))
    for iRow in range(len(counts)):
      result.append([])
      for iCol in range(len(counts[iRow])):
        val = float(counts[iRow][iCol])
        low, nom, high = getEfficiencyInterval(val,topRow[iCol])
        if iRow == 0:
          low = nom
          high = nom
        percStr = "{:5.1f}".format(nom*100.)
        if errors:
          percStr = "{:5.1f} +/-{:5.1f}".format(nom*100.,max(high-nom,nom-low)*100.)
        if asymerrors:
          percStr = "{:5.1f} +{:5.1f} -{:5.1f}".format(nom*100.,(high-nom)*100.,(nom-low)*100.)
        if interval:
          percStr = "{:5.1f} [{:5.1f},{:5.1f}]".format(nom*100.,low*100.,high*100.)
        result[iRow].append(percStr)
    return result

  def getPercOfPrevRow(self,counts,errors=False,asymerrors=False,interval=False):
    result = []
    for iRow in range(len(counts)):
      result.append([])
      for iCol in range(len(counts[iRow])):
        if iRow == 0:
          percStr = "{:5.1f}".format(100.)
          if errors:
            percStr = "{:5.1f} +/-{:5.1f}".format(100.,0.)
          if asymerrors:
            percStr = "{:5.1f} +{:5.1f} -{:5.1f}".format(100.,0.,0.)
          if interval:
            percStr = "{:5.1f} [{:5.1f},{:5.1f}]".format(100.,100.,100.)
          result[iRow].append(percStr)
        else:
          prevVal = float(counts[iRow-1][iCol])
          if prevVal > 1e-20:
            val = float(counts[iRow][iCol])
            low, nom, high = getEfficiencyInterval(val,prevVal)
            percStr = "{:5.1f}".format(nom * 100.)
            if errors:
              percStr = "{:5.1f} +/-{:5.1f}".format(nom*100.,max(high-nom,nom-low)*100.)
            if asymerrors:
              percStr = "{:5.1f} +{:5.1f} -{:5.1f}".format(nom*100.,(high-nom)*100.,(nom-low)*100.)
            if interval:
              percStr = "{:5.1f} [{:5.1f},{:5.1f}]".format(nom*100.,low*100.,high*100.)
            result[iRow].append(percStr)
          else:
            result[iRow].append("NaN")
    return result


class PrintPercentTable(PrintCutTable):

  def __init__(self,fileConfigs,cutConfigs,treename,errors=False,asymerrors=False,interval=False,nMax=sys.maxint):
    """
    similar to PrintCutTable, but just prints the percentages of the whole (first cutConfig) that each category 
    (remaining cut configs) is
    """

    fileNames = self.getFileNames(fileConfigs)
    cutNames = self.getCutNames(cutConfigs)
    for fileConfig in fileConfigs:
      loadTree(fileConfig,treename)
    countsIndiv = self.getCountsIndividualCut(fileConfigs,cutConfigs,nMax)
    countsIndivPerTop = self.getPercOfTopRow(countsIndiv)
    print "Individual Cuts"
    printTable(countsIndiv,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)
    print "Individual Cuts Percentage of Top Row"
    printTable(countsIndivPerTop,columnTitles=fileNames,rowTitles=cutNames,splitColumnTitles=True)

