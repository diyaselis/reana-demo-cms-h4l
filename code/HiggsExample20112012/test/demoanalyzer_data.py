import FWCore.ParameterSet.Config as cms
from RecoMuon.TrackingTools.MuonServiceProxy_cff import *
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process = cms.Process("Demo")

# intialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('Demo')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
        limit = cms.untracked.int32(-1)
        )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# define JSON file for 2012 data
goodJSON = '../../../inputs/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt'

myLumis = LumiList.LumiList(filename = goodJSON).getCMSSWString().split(',')

# define the input data set here by inserting the appropriate .txt file list *
import FWCore.Utilities.FileUtils as FileUtils
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
         'root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/10000/F2878994-766C-E211-8693-E0CB4EA0A939.root'
    )
)

# apply JSON file
#   (needs to be placed *after* the process.source input file definition!)
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
process.source.lumisToProcess.extend(myLumis)

process.source.skipEvents = cms.untracked.uint32(0)

process.demo = cms.EDAnalyzer('HiggsDemoAnalyzerGit'
)

process.TFileService = cms.Service("TFileService",
       fileName = cms.string('../../../outputs/DoubleMuParked2012C_10000_Higgs.root')
                                   )

process.p = cms.Path(process.demo)
