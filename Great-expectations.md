# Here are some **personal** notes regarding GREAT EXPECTATIONS

1. **DATA CONTEXT :** 

- created with command $ **great_expectations init** 
- is the primary entry point for a Great Expectations deployment, with configurations and methods for all supporting components. More info regarding **great_expectations** folder a.k.a the entry point can be found [here](https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_setup#create-a-data-context)
  
2. **DATASOURCE :**

- helps to connect to the actual data
- provides a standard API for accessing and interacting with data from a wide variety of source systems
- create new datasource with command $ **great_expectations datasource new**
- at the end of this action, check **great_expectations.yml** file &rarr; **datasources** field should be populated 
- list datasources with command $ **great_expectations datasource list**

**NOTE: Data assets -> multiple batches**
```python
context.get_available_data_asset_names()
```
- &uarr; This will print out the names of my Datasources, Data Connectors and Data Assets
3. **EXPECTATIONS SUITE :**

-  create a new suite with command $ **great_expectations suite new**
-  at the end of this action, check **expectation** folder, a .json with the expectations suite name should be created
-  edit an existing expectations suite with command $ **great_expectations suite edit <SUITE_NAME>**
 
 **Example :** 
  ```python
  batch_request = {'datasource_name': 'my_custom_datasource', 'data_connector_name': 'default_inferred_data_connector_name', 'data_asset_name': 'yellow_tripdata_sample_2019-01.csv', 'limit': 1000}
  ````
  - &uarr; here I have info regarding retrived data 
 
 **NOTE :** In some old docs will see term ***batch_kwargs***, which now is replaced by ***batch_request***

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
context.list_expectation_suite_names()
```
- &uarr; this will list all the existing expectation suites
  
4. **VALIDATION**

```python
validator = context.get_validator(
    batch_request=BatchRequest(**batch_request),
    expectation_suite_name=expectation_suite_name)
```
-  &uarr; Validator is the key object used to create Expectations, validate Expectations,and get Metrics for Expectations. Additionally, note that Validators are used by Checkpoints under-the-hood
  
```python
validator.expect_column_values_to_be_between(column='passenger_count', max_value=6, min_value=1)
```
-  &uarr; Sample of column expectation 
-  One important thing to mention is the existence of **mostly** parameter, which is acting like a tolerance parameter
```python
validator.expect_column_values_to_be_between(column='passenger_count', max_value=6, min_value=1,mostly=0.90)
```
-  &uarr; That mostly means that 90% of the time I allow my values to be in the range of 1-6 ( => 10% of wrong values )

```python
validator.save_expectation_suite(discard_failed_expectations=False)
```

- &uarr; save the expectation suite as a JSON file in the **great_expectations/expectations**

4.1. **CHECKPOINTS**

This is another way of validating data, by simply linking a specific data asset with a specific expectation suite

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
my_checkpoint_name = "name=my-super-checkpoint" 

yaml_config = f"""
name: {my_checkpoint_name}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-my-run-name-template"
validations:
  - batch_request:
      datasource_name: my_custom_datasource
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: yellow_tripdata_sample_2019-01.csv
      data_connector_query:
        index: -1
    expectation_suite_name: my-first-expectation-suite
"""
# Test the checkpoint configuration
my_checkpoint = context.test_yaml_config(yaml_config=yaml_config) 
# Review the checkpoint
print(my_checkpoint.get_config(mode="yaml"))
# Add the checkpoint
context.add_checkpoint(**yaml.load(yaml_config))
# Run the Checkpoint & Open Data Docs
context.run_checkpoint(checkpoint_name=my_checkpoint_name)
context.open_data_docs()
```
-  &uarr; another way to create a **checkpoint**
```python
checkpoint_result = checkpoint.run()
```
- &uarr; will run the expectation suite defined in the checkpoint against the data from batch_request 
- can specify some parameters like :
  -  template_name: Optional[str] = None,
  -  run_name_template: Optional[str] = None,
  -  expectation_suite_name: Optional[str] = None,
  -  batch_request: Optional[Union[BatchRequestBase, dict]] = None,
  -  action_list: Optional[List[dict]] = None,
  -  evaluation_parameters: Optional[dict] = None,
  -  runtime_configuration: Optional[dict] = None,
  -  validations: Optional[List[dict]] = None,
  -  profilers: Optional[List[dict]] = None,
  -  run_id: Optional[Union[str, RunIdentifier]] = None,
  -  run_name: Optional[str] = None,
  -  run_time: Optional[Union[str, datetime.datetime]] = None,
  -  result_format: Optional[Union[str, dict]] = None,
  -  expectation_suite_ge_cloud_id: Optional[str] = None,
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