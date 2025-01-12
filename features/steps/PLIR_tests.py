from behave import step, given, then, when
from features.modules import OpenHIMService,OpenMRSService,HapiFhirService
from features.steps import CommonSteps
import json


@when('Obs data is Posted to OpenMRS')
def postObsDataToOpenMRS(context):
    CommonSteps.innitializeData(context) 
    obs1 =  CommonSteps.readJsonData('../data/obs1.json')
    obs2 =  CommonSteps.readJsonData('../data/obs2.json')
    obs3 =  CommonSteps.readJsonData('../data/obs3.json')
    obs4 =  CommonSteps.readJsonData('../data/obs4.json')
    obs5 =  CommonSteps.readJsonData('../data/obs5.json')
    OpenMRSService.postObsFhirData(context ,obs1)
    OpenMRSService.postObsFhirData(context ,obs2)
    OpenMRSService.postObsFhirData(context ,obs3)
    OpenMRSService.postObsFhirData(context ,obs4)
    OpenMRSService.postObsFhirData(context ,obs5)
  

@then('OpenHIM should track the transactions exported by the analytics engine')
def checkOpenHIMTransactions(context):
    CommonSteps.innitializeData(context)    
    OpenHIMService.checkOpenHIMPLIRTransaction(context)
  

@then('CQL engine intergrated in HapiFHIR should calculate the TX_PVLS Indicator')
def CheckTxpvlsMeasureScore(context):
    CommonSteps.innitializeData(context)  
    HapiFhirService.checkIndicatorMeasureScore(context)

@then('CQL engine intergrated in HapiFHIR should calculate the TX_CURR Indicator')
def CheckTxcurrMeasureScore(context):
    CommonSteps.innitializeData(context)  
    HapiFhirService.checkIndicatorMeasureScoreTx_curr(context)      
    
         