#!/bin/env python
# Copyright 2017 StreamSets Inc.

import argparse
import logging
import sys

from streamsets import sdc

# Configuration
logging.basicConfig(level=logging.DEBUG)

# Currently unsupported Sqoop arguments::
# -e, --query
# --where
# --check-column
# -z, --compress
# --compression-codec
# --incremental
# --last-value
# --hive-drop-import-delims
# --hive-delims-replacement
# --map-column-hive
# --enclosed-by
# --escaped-by
# --fields-terminated-by
# --lines-terminated-by
# --mysql-delimiters
# --optionally-enclosed-by
# All HBase related stuff
# All Accumulo related stuff

class SqoopImporter:

    @property
    def _is_mapr(self):
        """Return true if and only if pipeline for MapR is being generated."""
        return "mapr" in self.args.sdc_stagelib

    @property
    def _fs_target_stage(self):
        """Return stage name for FS target based on configured stage library."""
        return 'MapR FS' if self._is_mapr else 'Hadoop FS'

    @property
    def _fs_executor_stage(self):
        """Return stage name for FS executor based on configured stage library."""
        return 'MapR FS File Metadata' if self._is_mapr else 'HDFS File Metadata'

    def parse_arguments(self):
        """Parse command line arguments."""
        # Arguments
        parser = argparse.ArgumentParser()

        # SDC Specific ones
        parser.add_argument('--sdc-url', action='store', required=False, default='http://localhost:18630')
        parser.add_argument('--sdc-stagelib', action='store', required=False, default=None)

        # Sqoop arguments that we actively support (e.g. that changes the pipeline)
        parser.add_argument('--autoreset-to-one-mapper', action='store_true', required=False)
        parser.add_argument('--as-textfile', action='store_true', required=False)
        parser.add_argument('--as-avrodatafile', action='store_true', required=False)
        parser.add_argument('--as-parquetfile', action='store_true', required=False)
        parser.add_argument('--connect', action='store', required=False)
        parser.add_argument('--columns', action='store', required=False)
        parser.add_argument('--delete-target-dir', action='store_true', required=False)
        parser.add_argument('--fetch-size', action='store', required=False)
        parser.add_argument('--hive-database', action='store', required=False)
        parser.add_argument('--hive-import', action='store_true', required=False)
        parser.add_argument('--hive-overwrite', action='store_true', required=False)
        parser.add_argument('--hive-partition-key', action='store', required=False)
        parser.add_argument('--hive-partition-value', action='store', required=False)
        parser.add_argument('--hive-table', action='store', required=False)
        parser.add_argument('--inline-lob-limit', action='store', required=False)
        parser.add_argument('--num-mappers', action='store', required=False)
        parser.add_argument('--null-string', action='store', required=False)
        parser.add_argument('--null-non-string', action='store', required=False)
        parser.add_argument('-m', action='store', required=False)
        parser.add_argument('--map-column-java', action='store', required=False)
        parser.add_argument('--username', action='store', required=False)
        parser.add_argument('--password', action='store', required=False)
        parser.add_argument('--table', action='store', required=False)
        parser.add_argument('--target-dir', action='store', required=False)
        parser.add_argument('--split-by', action='store', required=False)
        parser.add_argument('--relaxed-isolation', action='store_true', required=False)
        parser.add_argument('--warehouse-dir', action='store', required=False)

        # Sqoop arguments that we blindly consume and ignore (as they don't make difference for us)
        parser.add_argument('--append', action='store_true', required=False)
        parser.add_argument('--boundary-query', action='store', required=False)
        parser.add_argument('--connection-manager', action='store', required=False)
        parser.add_argument('--direct', action='store_true', required=False)
        parser.add_argument('--driver', action='store', required=False)
        parser.add_argument('--hadoop-mapred-home', action='store_true', required=False)
        parser.add_argument('--hive-home', action='store', required=False)
        parser.add_argument('--validate', action='store_true', required=False)
        parser.add_argument('--validate-threshold', action='store', required=False)
        parser.add_argument('--validate-failurehandler', action='store', required=False)
        parser.add_argument('--verbose', action='store_true', required=False)

        # Arguments that we consume, but that does require further action on user side
        parser.add_argument('--create-hive-table', action='store', required=False)
        parser.add_argument('--password-file', action='store', required=False)
        parser.add_argument('-P', action='store_true', required=False)

        return parser.parse_args()

    def num_of_threads(self):
        """Calcuate number of threads that should be used."""
        if self.args.m:
            return int(args.m)
        if self.args.num_mappers:
            return int(self.args.num_mappers)

        # Sqoop default is 4
        return 4

    def no_more_data(self, origin):
        """Generate pipeline fragment that will stop pipeline after it's done."""
        assert origin is not None

        selector = self.builder.add_stage('Stream Selector')
        finisher = self.builder.add_stage('Pipeline Finisher Executor')
        trash = self.builder.add_stage('Trash')

        origin >= selector
        selector >> finisher
        selector >> trash

        selector.condition = [
            {'predicate': '${record:eventType() == "no-more-data"}', 'outputLane': selector._data['outputLanes'][0]},
            {'predicate': 'default', 'outputLane': selector._data['outputLanes'][1]}
        ]

    def table_origin(self):
        """Create fragment of pipeline with origin side."""
        # Validate required arguments in this mode
        assert self.args.table is not None
        assert self.args.connect is not None
        assert self.args.username is not None

        table_pattern = {
            'tablePattern': '${TABLE}',
            'partitioningMode': 'BEST_EFFORT' if self.args.autoreset_to_one_mapper else 'REQUIRED',
            'maxNumActivePartitions': self.num_of_threads(),
            'overrideDefaultOffsetColumns': self.args.split_by is not None,
            'offsetColumns': [ self.args.split_by] if self.args.split_by is not None else [],
            'partitionSize' : '1000000'
        }

        origin = self.builder.add_stage('JDBC Multitable Consumer')
        origin.table_configs = [table_pattern]
        origin.configuration['hikariConfigBean.connectionString'] = "${JDBC_URL}"
        origin.configuration['hikariConfigBean.username'] = "${USERNAME}"
        origin.configuration['hikariConfigBean.password'] = "${PASSWORD}"
        origin.configuration['tableJdbcConfigBean.quoteChar'] = "DOUBLE_QUOTES"
        origin.configuration['tableJdbcConfigBean.numberOfThreads'] = self.num_of_threads()
        origin.configuration['hikariConfigBean.maximumPoolSize'] = self.num_of_threads()

        if 'jdbc:mysql://' in self.args.connect:
            origin.configuration['tableJdbcConfigBean.quoteChar'] = 'BACKTICK'

        if self.args.fetch_size:
            origin.configuration['tableJdbcConfigBean.fetchSize'] = int(self.args.fetch_size)

        if self.args.inline_lob_limit:
            origin.configuration['commonSourceConfigBean.maxClobSize'] = int(self.args.inline_lob_limit)
            origin.configuration['commonSourceConfigBean.maxBlobSize'] = int(self.args.inline_lob_limit)

        if self.args.relaxed_isolation:
            origin.configuration['hikariConfigBean.transactionIsolation'] = 'TRANSACTION_READ_UNCOMMITTED'

        # Append portion of the pipeline that will auto-stop after no-more-data will be received
        self.no_more_data(origin)

        return origin

    def write_to_hdfs(self):
        """Create fragment of pipeline that writes incoming data to HDFS."""
        schema_gen = None
        destination = None
        avro_to_parquet = None

        # Avro or Parquet requires that we generate Avro schema
        if self.args.as_avrodatafile or self.args.as_parquetfile:
            schema_gen = self.builder.add_stage('Schema Generator')
            schema_gen.schema_name = '${TABLE}'
            schema_gen.enable_cache = True
            schema_gen.cache_key_expression = '${TABLE}'

        # Real destination
        destination = self.builder.add_stage(self._fs_target_stage, type='destination', library=self.args.sdc_stagelib)
        destination.configuration['hdfsTargetConfigBean.hdfsConfDir'] = '${CONF_DIR}'
        if self.args.as_avrodatafile:
            destination.data_format = 'AVRO'
            destination.configuration['hdfsTargetConfigBean.dataGeneratorFormatConfig.avroSchemaSource'] = 'HEADER'
            destination.directory_template = '${TARGET_DIR}'
        elif self.args.as_parquetfile:
            # Parquet is written as Avro and converted to parquet later
            destination.data_format = 'AVRO'
            destination.configuration['hdfsTargetConfigBean.dataGeneratorFormatConfig.avroSchemaSource'] = 'HEADER'
            destination.directory_template = '${TARGET_DIR}/.avro'
        else:
            destination.data_format = 'DELIMITED'
            destination.directory_template = '${TARGET_DIR}'

        # Parquet requires additional stage to convert avro to parquet
        if  self.args.as_parquetfile:
            avro_to_parquet = self.builder.add_stage('MapReduce', type='executor')
            avro_to_parquet.job_type = 'AVRO_PARQUET'
            avro_to_parquet.output_directory = "${file:parentPath(file:parentPath(record:value('/filepath')))}"

        # With HDFS, we also want to create _SUCCESS file
        stop = self.builder.add_stop_event_stage(self._fs_executor_stage, library=self.args.sdc_stagelib)
        stop.task = 'CREATE_EMPTY_FILE'
        stop.file_path = '${TARGET_DIR}/_SUCCESS'
        stop.configuration['connection.hdfsConfDir'] = '${CONF_DIR}'

        # Optionally we also might need drop the input directory at the begging
        if self.args.delete_target_dir:
            start = self.builder.add_start_event_stage(self._fs_executor_stage, library=self.args.sdc_stagelib)
            start.task = 'REMOVE_FILE'
            start.file_path = '${TARGET_DIR}'
            start.configuration['connection.hdfsConfDir'] = '${CONF_DIR}'

        # Return value in our case is a bit difficult
        if self.args.as_avrodatafile:
            schema_gen >> destination
            return schema_gen
        elif self.args.as_parquetfile:
            schema_gen >> destination
            destination >= avro_to_parquet
            return schema_gen
        else:
            return destination

    def write_to_hive(self):
        """Create fragment of pipeline that writes incoming data to Hive."""
        # Hive processor
        hive_metadata = self.builder.add_stage('Hive Metadata', library=self.args.sdc_stagelib)
        hive_metadata.data_format = 'PARQUET' if self.args.as_parquetfile else 'AVRO'
        hive_metadata.database_expression = '${HIVE_DATABASE}'
        hive_metadata.table_name = '${HIVE_TABLE}'
        hive_metadata.configuration['hiveConfigBean.hiveJDBCUrl'] = '${HIVE_URL}'

        if self.args.hive_partition_key:
            hive_metadata.configuration['partitionList'] = [{
                "name": self.args.hive_partition_key,
                "valueType": "STRING",
                "valueEL": self.args.hive_partition_value
            }]
        else:
            hive_metadata.configuration['partitionList'] = []

        hadoop_fs = self.builder.add_stage(self._fs_target_stage, type='destination', library=self.args.sdc_stagelib)
        hadoop_fs.configuration['hdfsTargetConfigBean.hdfsConfDir'] = '${CONF_DIR}'
        hadoop_fs.data_format = 'AVRO'
        hadoop_fs.avro_schema_location = 'HEADER'
        hadoop_fs.directory_in_header = True

        hive_metastore = self.builder.add_stage('Hive Metastore', type='destination', library=self.args.sdc_stagelib)
        hive_metastore.configuration['conf.hiveConfigBean.hiveJDBCUrl'] = '${HIVE_URL}'

        hive_metadata >> hadoop_fs
        hive_metadata >> hive_metastore

        if self.args.as_parquetfile:
            mapreduce = self.builder.add_stage('MapReduce', type='executor')
            mapreduce.job_type = 'AVRO_PARQUET'
            mapreduce.output_directory = "${file:parentPath(file:parentPath(record:value('/filepath')))}"

            hadoop_fs >= mapreduce

        if self.args.hive_overwrite:
            start = self.builder.add_start_event_stage('Hive Query')
            start.configuration['config.hiveConfigBean.hiveJDBCUrl'] = '${HIVE_URL}'
            start.configuration['config.queries'] = ['truncate table ${HIVE_TABLE}']

        return hive_metadata

    def calculate_target_dir(self):
        """Calculate HDFS location where we should store data."""
        if self.args.target_dir:
            return self.args.target_dir
        elif self.args.warehouse_dir:
            return self.args.warehouse_dir + '/' + self.args.table
        else:
            return '/user/${pipeline:user()}/' + self.args.table

    def prepare_parameters(self, pipeline):
        """Prepare pipeline parameters that other stages are configured with."""
        password = ''
        # Only if the password is on command line, then we will put it to the pipeline directly
        if self.args.password:
            password = self.args.password

        # JDBC based ones
        pipeline.add_parameters(
            TABLE=self.args.table,
            JDBC_URL=self.args.connect,
            USERNAME=self.args.username,
            PASSWORD=password
        )

        if self.args.hive_import:
            pipeline.add_parameters(
                HIVE_URL='jdbc:hive2://localhost:10000/default',
                HIVE_TABLE=self.args.hive_table if self.args.hive_table else self.args.table,
                HIVE_DATABASE=self.args.hive_database if self.args.hive_database else 'default',
                CONF_DIR='hadoop-conf'
            )
        else:
            pipeline.add_parameters(
                CONF_DIR='hadoop-conf',
                TARGET_DIR=self.calculate_target_dir()
            )

    def processing_fragment(self):
        """Create processing fragment (various transformations on top of the data)."""
        stages = []

        # Column filtering we're modeling by selecting everything and then dropping
        # unwanted columns.
        if self.args.columns:
            remover = self.builder.add_stage('Field Remover')
            remover.fields = ['/{}'.format(i) for i in self.args.columns.split(',')]
            remover.action = 'KEEP'

            stages.append(remover)

        # For mapping NULL values we use Value replacer
        if self.args.null_string:
            # Currently we require both string and non string types to behave the same way
            assert self.args.null_string == self.args.null_non_string

            replacer = self.builder.add_stage('Value Replacer')
            replacer.replace_null_values = [{
                'fields' : [ '/*' ],
                'newValue' : self.args.null_string
            }]

            if stages:
                stages[-1] >> replacer
            stages.append(replacer)

        # Column type mapping for Java types
        if self.args.map_column_java:
            configs = []
            for item in self.args.map_column_java.split(','):
                spec = item.split('=')
                configs.append({
                    'fields': [ '/{}'.format(spec[0]) ],
                    'targetType': spec[1].upper(),
                    'treatInputFieldAsDate': False,
                    'dataLocale' : 'en,US',
                    'scale': -1,
                    'decimalScaleRoundingStrategy': 'ROUND_UNNECESSARY',
                    'dateFormat': 'YYYY_MM_DD',
                    'encoding': 'UTF-8'
                })

            converter = self.builder.add_stage('Field Type Converter')
            converter.conversion_method = 'BY_FIELD'
            converter.field_type_converter_configs = configs

            if stages:
                stages[-1] >> converter
            stages.append(converter)

        return stages

    def destination_fragment(self):
        """Create destination fragment (writer side)."""
        return self.write_to_hive() if self.args.hive_import else self.write_to_hdfs()


    def process(self):
        """Main entry point to the object."""

        # Persist parsed arguments in this object
        self.args = self.parse_arguments()

        # Create main builder and pipeline
        logging.info(f'Connecting to SDC running on {self.args.sdc_url}')
        dc = sdc.DataCollector(server_url=self.args.sdc_url)

        # Build roughly equivalent pipeline
        self.builder = dc.get_pipeline_builder()

        origin_fragment = self.table_origin()
        middle_fragment = self.processing_fragment()

        if middle_fragment:
            origin_fragment >> middle_fragment[0]
            middle_fragment[-1] >> self.destination_fragment()
        else:
            origin_fragment >> self.destination_fragment()

        pipeline = self.builder.build(f'Sqoop Import of Table "{self.args.table}"')
        self.prepare_parameters(pipeline)

        # And we're pretty much done
        logging.info(f'Uploading pipeline to SDC')
        dc.add_pipeline(pipeline)


def main(args=None):
    logging.info('Sqoop To StreamSets Data Collector Pipeline converter, version 0.1')

    importer = SqoopImporter()
    importer.process()


if __name__ == "__main__":
    main()
