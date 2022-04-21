# Here are some **personal** notes regarding GREAT EXPECTATIONS
**Data Context :** 

- created with command $ **great_expectations init** 
- is the primary entry point for a Great Expectations deployment, with configurations and methods for all supporting components. More info regarding **great_expectations** folder a.k.a the entry point can be found [here](https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_setup#create-a-data-context)
  
**Datasource :**

- helps to connect to the actual data
- provides a standard API for accessing and interacting with data from a wide variety of source systems
- create new datasource with command $ **great_expectations datasource new**
- at the end of this action, check **great_expectations.yml** file, datasources field should be populated 
- list datasources with command $ **great_expectations datasource list**

**NOTE: Data assets -> multiple batches**

**Expectations suite :**

-  create a new suite with command $ **great_expectations suite new**
-  at the end of this action, check **expectation** folder, a .json with the expectations suite name should be created
-  edit an existing expectations suite with command $ **great_expectations suite edit <SUITE_NAME>**
 
 **Example :** 
  ```python
  batch_request = {'datasource_name': 'my_custom_datasource', 'data_connector_name': 'default_inferred_data_connector_name', 'data_asset_name': 'yellow_tripdata_sample_2019-01.csv', 'limit': 1000}
  ````
  - &uarr; here I have info regarding retrived data 

```python
expectation_suite_name = "my-first-expectation-suite"
```
- &uarr; just defined a name for expectation suite
  
```python
 try:
    suite = context.get_expectation_suite(expectation_suite_name=expectation_suite_name)
    print(f'Loaded ExpectationSuite "{suite.expectation_suite_name}" containing {len(suite.expectations)} expectations.')
except DataContextError:
    suite = context.create_expectation_suite(expectation_suite_name=expectation_suite_name)
    print(f'Created ExpectationSuite "{suite.expectation_suite_name}".')
```
- &uarr; if the suite exist just Load it , otherwise create it 
  
```python
validator = context.get_validator(
    batch_request=BatchRequest(**batch_request),
    expectation_suite_name=expectation_suite_name)
```
-  &uarr; Validator is the key object used to create Expectations, validate Expectations,and get Metrics for Expectations. Additionally, note that Validators are used by Checkpoints under-the-hood

```python
validator.save_expectation_suite(discard_failed_expectations=False)
```

- &uarr; save the expectation suite as a JSON file in the **great_expectations/expectations**

```python
checkpoint_config = {
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": batch_request,
            "expectation_suite_name": expectation_suite_name
        }
    ]
}
checkpoint = SimpleCheckpoint(
    f"_tmp_checkpoint_{expectation_suite_name}",
    context,
    **checkpoint_config
)
```
- &uarr; create a **CHECKPOINT**
- this is taking the data to be validated from *batch_request*
- will run the expectation suite defined earlier against the data from batch_request

```python
checkpoint_result = checkpoint.run()
```
- &uarr; take the info from checkpoint and runs the validation
- info regarding each validation run is stored in **great_expectations/uncommited/validations/<NAME_OF_THE_EXPECTAION_SUITE>/ \_\_none\_\_** 
- for each validation run wil be created a folder that will contain a JSON file, that has all the information regarding that particular run 
  
```python
validation_result_identifier = checkpoint_result.list_validation_result_identifiers()
```
- &uarr; here is the location of the runned validation 
  
```python
context.build_data_docs()
context.open_data_docs(resource_identifier=validation_result_identifier)
```
- &uarr; this will build a data_docs which will display the results of the runned validation