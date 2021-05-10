## TESTING PLIR SETUP
see  [PLIR Archtecture](https://wiki.openmrs.org/display/projects/Architectural+Design+Approach+to+support+an+integrated+approach+to+patient-level+indicator+reporting+for+OpenMRS)

### Assumptions
User has familiarity with OpenMRS, OpenHIM , Python, and BDD framework Behave is assumed. Familiarity with HIE components is recommended.

### Prerequisites

* Python version >= 3.7
* Behave version >= 1.2
*  Debezium-FHIR-Analytics component 
* OpenMRS
* OpenHIM 
* HAPI-FHIR

### Configuration 
Follow the Intructions at https://github.com/openmrs/openmrs-plir-dockerized-setup to run a full configured  PLIR setup. 

Update the Configuration in the config.json file located under the `features/config` folder . ONly OpenMRS , OpenHIM and HapiFHIR are required

NOTE :The deafult  configuration are mapped to the default configuration in the [dockerized PLIR setup](https://github.com/openmrs/openmrs-plir-dockerized-setup)

See sample observation data Posted to OpenMRS under `features/data` ie `obs1.json ,obs2.json ,obs3.json` 
In case any values are adjusted in the above sample data, adjust the expected TX_PVLS score (rounded off to two decimal places) ie `MeasureScore` in the config file 

* The Test will work best before you add any data to OpenMRS

Execute the test with the  command below ,under the root directory ,but first ensure the PLIR pipeline is up and running.

	behave --no-logcapture --include ./features/PLIR
 	
The tests will
 * Post Obs data into OpenMRS 
 * Track the transactions in OpenHIM
 * Check whether the correct TX_PVLS indicator measureScore was calculated in HAPI FHIR   
