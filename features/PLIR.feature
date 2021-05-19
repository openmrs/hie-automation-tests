Feature: POST OBSERVATION DATA TO OPENMRS AND CHECK THE DATA IN OpenHIM AND HAPI-FHIR

  Scenario: POST obs data to OpenMRS
      When Obs data is POSTed to OpenMRS
      Then OpenHIM should track the transactions exported by the analytics engine
      Then CQL engine intergrated in HapiFHIR should calculate the TX_PVLS Indicator