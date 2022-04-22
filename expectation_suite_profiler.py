from ruamel import yaml
import datetime
import pandas as pd
import great_expectations as ge
import great_expectations.jupyter_ux
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.exceptions import DataContextError
import json
# import simplejson

# MAIN-SCOPE: Initialize a new Expectation Suite by profiling a batch of your data.

# STEPS TO FOLLOW IF YOU DON'T HAVE A DATASOURCE CONFIGURED
# STEP 1: Instantiate your project's DataContext

context = ge.get_context()

# STEP 2: Configure your Datasource

datasource_name = "my_manual_custon_datasource"
datasource_yaml = f"""
name: {datasource_name}
class_name: Datasource
module_name: great_expectations.datasource
execution_engine:
  module_name: great_expectations.execution_engine
  class_name: PandasExecutionEngine
data_connectors:
    default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
            - default_identifier_name
    default_inferred_data_connector_name:
        class_name: InferredAssetFilesystemDataConnector
        base_directory: ..\..\ge_tutorials\data
        default_regex:
          group_names:
            - data_asset_name
          pattern: (.*)
"""

# STEP 3: Test the configuration

context.test_yaml_config(datasource_yaml)

# STEP 4: Save the Datasource configuration to your DataContext

context.add_datasource(**yaml.load(datasource_yaml))

# STEPTS TO FOLLOW TO ACHIVE THE MAIN SCOPE
# STEP 5: Initialize a new Expectation Suite by profiling a batch of your data

batch_request = BatchRequest(
    datasource_name="my_manual_custon_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="yellow_tripdata_sample_2019-02.csv",
)
expectation_suite_name="another_test_suite_with_profiler"
context.create_expectation_suite(
    expectation_suite_name=expectation_suite_name, overwrite_existing=True
)
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name=expectation_suite_name
)
print(validator.head())

# STEP 6: Set the collumns which you would like to ignore

ignored_columns = []

# STEP 7: Run the data profiler

profiler = UserConfigurableProfiler(
    profile_dataset=validator,
    excluded_expectations=None,
    ignored_columns=ignored_columns,
    not_null_only=False,
    primary_or_compound_key=False,
    semantic_types_dict=None,
    table_expectations_only=False,
    value_set_threshold="MANY",
)
suite = profiler.build_suite()

# STEP 8: Save & review your new Expectation Suite

print(validator.get_expectation_suite(discard_failed_expectations=False))
validator.save_expectation_suite(discard_failed_expectations=False)

# STEP 8.1: Create a new checkpoint

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

# STEP 8.2: Save the checkpoint configuration to your DataContext

checkpoint_config_as_JSONstring= str(checkpoint.config)
checkpoint_config_as_yaml = yaml.dump(json.loads(checkpoint_config_as_JSONstring))
context.add_checkpoint(**yaml.safe_load(checkpoint_config_as_yaml))

# STEP 8.3: Run checkpoint validation

checkpoint_result = checkpoint.run()


context.build_data_docs()

validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[0]
context.open_data_docs(resource_identifier=validation_result_identifier)

# checkpoint_config_as_JSONstring = """action_list:
# - name: store_validation_result
#   action:
#     class_name: StoreValidationResultAction
# - name: store_evaluation_params
#   action:
#     class_name: StoreEvaluationParametersAction
# - name: update_data_docs
#   action:
#     class_name: UpdateDataDocsAction
#     site_names: []
# batch_request: {}
# class_name: Checkpoint
# config_version: 1
# evaluation_parameters: {}
# module_name: great_expectations.checkpoint
# name: _tmp_checkpoint_test_suite
# profilers: []
# runtime_configuration: {}
# validations:
# - batch_request:
#     datasource_name: my_manual_custon_datasource
#     data_connector_name: default_inferred_data_connector_name
#     data_asset_name: yellow_tripdata_sample_2019-02.csv
#   expectation_suite_name: test_suite
#   """