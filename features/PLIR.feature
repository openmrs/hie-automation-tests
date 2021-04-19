Feature: POST OBSERVATION DATA TO OPENMRS AND CHECK THE DATA IN OpenHIM AND HAPI-FHIR

  Scenario: post obs data to OpenMRS
      When we post data to OpenMRS
      Then OpenHIM should track the Transactions
      Then TXPVLS indicator should be calculated in HapiFHIR