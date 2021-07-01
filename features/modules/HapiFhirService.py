import logging
import time
import requests
import os
import json

#constructor
def __init__(context):       
    context.fhirPatientLkUrl = context.configData["HAPI-FHIR"]["baseUrl"] + '/Patient?'
    context.fhirObservationLkUrl = context.configData["HAPI-FHIR"]["baseUrl"] + '/Observation?'
    context.fhirPatientUrl = context.configData["HAPI-FHIR"]["baseUrl"] + '/Patient/'
    context.fhirEncounterUrl =  context.configData["HAPI-FHIR"]["baseUrl"] + '/Encounter?patient='
    context.fhirObservationUrl =  context.configData["HAPI-FHIR"]["baseUrl"] + '/Observation?patient='
    context.evaluateTX_PVLSMeasureUrl = context.configData["HAPI-FHIR"]["baseUrl"] + '/Measure/' + context.configData["TX-PVLS"]["MeasureResourceId"] + '/$evaluate-measure?periodStart=' + context.configData["TX-PVLS"]["IndicatorStartDate"] + '&periodEnd=' + context.configData["TX-PVLS"]["IndicatorEndDate"] 
    context.evaluateTX_CURRMeasureUrl = context.configData["HAPI-FHIR"]["baseUrl"] + '/Measure/' + context.configData["TX-CURR"]["MeasureResourceId"] + '/$evaluate-measure?periodStart=' + context.configData["TX-CURR"]["IndicatorStartDate"] + '&periodEnd=' + context.configData["TX-CURR"]["IndicatorEndDate"] 
    context.Hapi = context.configData["HAPI-FHIR"]
    context.expectedMeasuretx_pvlsScore = context.configData["TX-PVLS"]["MeasureScore"] 
    context.expectedMeasuretx_currCount = context.configData["TX-CURR"]["Count"] 
    
def deleteOldHapiFhirRecords(context, deleteDataFileName): 
    logging.info ('Starting cleaning of previous run HAPI-FHIR data')
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    # clean up old records
    try :
        
        delete_file = os.path.join(cur_dir, deleteDataFileName)        
        with open(delete_file) as deleteFile: 
            data = json.load(deleteFile)                 
                    
        if (len(data['hapiFhirPatientUUID']) == 0) :
            return              
        #delete shr patient record
        
        for hapiFhirPatientId in data['hapiFhirPatientUUID']:   
            deleteFhirPatient(context, hapiFhirPatientId)           
           
    except :
        logging.error ('Encounted error when trying delete Hapi Fhir Person Record')
        
                   
def deleteFhirPatient(context, hapiFhirPatientId):  
    # HAVE to redo this later
    response = requests.get(context.fhirPatientUrl + hapiFhirPatientId, headers={'Connection':'close'})  
    data = response.json()
    familyName = data['name'][0]['family']
    given = data['name'][0]['given'][0]
    
    lkInfo = 'family=' + familyName + "&given=" + given        
    response = requests.get(context.fhirPatientLkUrl + lkInfo, headers={'Connection':'close'})
    data = response.json()
    for entry in data['entry'] :
        resourceID = entry['resource']['id']      
        deleteFhirEncounter (context, resourceID)
        deleteFhirObservation (context, resourceID)
        response = requests.delete(entry['fullUrl'], headers={'Connection':'close'})        
        response.close()
    logging.info("Deleted hapi-fhir person, Encounter, Observation records for " + familyName + "," + given)
        
def deleteFhirEncounter(context, hapiFhirPatientId):      
    response = requests.delete(context.fhirEncounterUrl + hapiFhirPatientId, headers={'Connection':'close'})  
    data = response.json() 
    response.close()    
        
def deleteFhirObservation(context, hapiFhirPatientId):          
    response = requests.delete(context.fhirObservationUrl + hapiFhirPatientId, headers={'Connection':'close'})  
    data = response.json() 
    response.close()    

def checkFhirData(context) :    
    #check person data exists
    logging.info("Check HAPI-FHIR for Patient - " + context.currPatient.givenName)
    count = 0 
    isSuccessful = False
    while (count < 5 and isSuccessful == False) :          
        lkInfo = 'family=' + context.currPatient.familyName + "&given=" + context.currPatient.givenName        
        response = requests.get(context.fhirPatientLkUrl + lkInfo, headers={'Connection':'close'})
        count += 1
        if (response.status_code > 204) :
            time.sleep(5)
            continue
        else :
            isSuccessful = True
            data = response.json() 
            context.currPatient.fhirPatientUUID = data['entry'][0]['resource']['id']           
            break
        
    response.close()         
    assert (isSuccessful)
    
def checkIndicatorMeasureScore(context) :    
    logging.info("Check HAPI-FHIR for Indicator Measure Score")
    count = 0 
    isSuccessful = False
    while (count < 5 and isSuccessful == False) :          
       
        response = requests.get( context.evaluateTX_PVLSMeasureUrl, headers={'Connection':'close'}, auth=(context.Hapi["username"], context.Hapi["password"]))
        count += 1
        if (response.status_code > 204) :
            time.sleep(5)
            continue
        else :
            data = response.json() 
            context.measureScore =  data['group'][0]['measureScore']['value']
            if(round(context.measureScore, 2) == context.expectedMeasuretx_pvlsScore):
                isSuccessful = True        
                break
            else :
                isSuccessful = False
                break
        
    response.close()         
    assert (isSuccessful) 

def checkIndicatorMeasureScoreTx_curr(context) :    
    logging.info("Check HAPI-FHIR for Indicator Measure Score")
    count = 0 
    isSuccessful = False
    while (count < 5 and isSuccessful == False) :          

        response = requests.get( context.evaluateTX_CURRMeasureUrl, headers={'Connection':'close'}, auth=(context.Hapi["username"], context.Hapi["password"]))
        count += 1
        if (response.status_code > 204) :
            time.sleep(5)
            continue
        else :
            data = response.json() 
            context.measureScore =  data['group'][0]['population'][0]['count']

            if(context.measureScore == context.expectedMeasuretx_currCount):
                isSuccessful = True        
                break
            else :
                isSuccessful = False
                break

    response.close()         
    assert (isSuccessful)               
