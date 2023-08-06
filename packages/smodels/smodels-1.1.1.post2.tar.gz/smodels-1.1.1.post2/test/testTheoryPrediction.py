#!/usr/bin/env python

"""
.. module:: testTheoryPrediction
   :synopsis: Testing the theory prediction.

.. moduleauthor:: Wolfgang Waltenberger <wolfgang.waltenberger@gmail.com>

"""

from __future__ import print_function
import sys
sys.path.insert(0,"../")
import unittest
from smodels.tools.physicsUnits import fb, GeV, pb
from databaseLoader import database
import inspect
import os

class IntegrationTest(unittest.TestCase):
    def configureLogger(self):
        import logging.config
        fc= inspect.getabsfile(self.configureLogger).replace ( 
                "testTheoryPrediction.py", "integration.conf" )
        logging.config.fileConfig( fname=fc, disable_existing_loggers=False )

    def predictions(self):
        return { 'ATLAS-SUSY-2013-02': 572.168935 * fb,
                 'CMS-SUS-13-012': 1.73810052766 * fb }

    def predchi2(self):
        return { 'ATLAS-SUSY-2013-02': None,
                 'CMS-SUS-13-012': 19.9647839329 }

    def checkAnalysis(self,expresult,smstoplist):
        id = expresult.globalInfo.id
        from smodels.theory.theoryPrediction import theoryPredictionsFor
        theorypredictions = theoryPredictionsFor(expresult, smstoplist)
        defpreds=self.predictions()
        if not theorypredictions:
            print ( "no theory predictions for",expresult,"??" )
            import sys
            sys.exit(-1)
        for pred in theorypredictions:
            m0=str(int(pred.mass[0][0]/GeV))
            predval=pred.xsection.value 
            defpredval = defpreds[id]
            self.assertAlmostEqual( predval.asNumber(fb), defpredval.asNumber (fb) )
            pred.computeStatistics()
            self.assertAlmostEqual ( pred.chi2, self.predchi2()[id] )

    def testIntegration(self):
        from smodels.installation import installDirectory
        from smodels.tools.physicsUnits import fb, GeV
        from smodels.theory import slhaDecomposer
        slhafile = '../inputFiles/slha/simplyGluino.slha'
        self.configureLogger()
        smstoplist = slhaDecomposer.decompose(slhafile, .1*fb, doCompress=True,
                doInvisible=True, minmassgap=5.*GeV)
        listofanalyses = database.getExpResults( 
                analysisIDs= [ "ATLAS-SUSY-2013-02", "CMS-SUS-13-012" ], 
                txnames = [ "T1" ] )
        if type(listofanalyses) != list:
            listofanalyses= [ listofanalyses] 
        for analysis in listofanalyses:
            self.checkAnalysis(analysis,smstoplist)

if __name__ == "__main__":
    unittest.main()
