{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116572164,
     "inputWidgets": {},
     "nuid": "0851d832-e11f-466e-aa97-41bf1894b9ad",
     "showTitle": false,
     "startTime": 1783116567874,
     "submitTime": 1783116567821,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_orders_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_orders')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116616938,
     "inputWidgets": {},
     "nuid": "9661ddd3-6936-47d0-9b32-a458b503e93e",
     "showTitle": false,
     "startTime": 1783116612000,
     "submitTime": 1783116611960,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_customers_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_customers')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116663464,
     "inputWidgets": {},
     "nuid": "8366c186-2907-4da7-981c-f073446154cc",
     "showTitle": false,
     "startTime": 1783116658060,
     "submitTime": 1783116658020,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_order_items_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_order_items')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116835065,
     "inputWidgets": {},
     "nuid": "f932b79f-9f5f-4364-b807-3924dccde070",
     "showTitle": false,
     "startTime": 1783116829658,
     "submitTime": 1783116829615,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_order_payments_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_order_payments')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116839769,
     "inputWidgets": {},
     "nuid": "26cab514-b9ba-45a9-91e7-c4acd7e25480",
     "showTitle": false,
     "startTime": 1783116835106,
     "submitTime": 1783116831126,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_order_reviews_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_order_reviews')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116843875,
     "inputWidgets": {},
     "nuid": "2e97e023-1ab4-462c-b8a2-e4a8d46cdee6",
     "showTitle": false,
     "startTime": 1783116839787,
     "submitTime": 1783116833742,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_products_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_products')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116873717,
     "inputWidgets": {},
     "nuid": "83205413-8ad9-46d6-bef0-41289f1836a9",
     "showTitle": false,
     "startTime": 1783116869044,
     "submitTime": 1783116869006,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_sellers_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_sellers')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783116918483,
     "inputWidgets": {},
     "nuid": "9eaace0f-0ab2-4c04-ab2d-3c140e011fab",
     "showTitle": false,
     "startTime": 1783116911307,
     "submitTime": 1783116911272,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/olist_geolocation_dataset.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_geolocation')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "finishTime": 1783179715772,
     "inputWidgets": {},
     "nuid": "68f02afc-4539-477f-9287-47d4f2defa5e",
     "showTitle": false,
     "startTime": 1783179707835,
     "submitTime": 1783179705307,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"/Volumes/workspace/default/raw/product_category_name_translation.csv\", header=True, inferSchema=True)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('workspace.default.bronze_product_category_name_translation')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {
      "byteLimit": 2048000,
      "rowLimit": 10000
     },
     "collapsed": true,
     "finishTime": 1783117087068,
     "inputWidgets": {},
     "nuid": "0368d57a-cac6-4110-9dde-d6a12eb6f813",
     "showTitle": false,
     "startTime": 1783117081395,
     "submitTime": 1783117081366,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [
    {
     "output_type": "display_data",
     "data": {
      "text/html": [
       "<style scoped>\n",
       "  .table-result-container {\n",
       "    max-height: 300px;\n",
       "    overflow: auto;\n",
       "  }\n",
       "  table, th, td {\n",
       "    border: 1px solid black;\n",
       "    border-collapse: collapse;\n",
       "  }\n",
       "  th, td {\n",
       "    padding: 5px;\n",
       "  }\n",
       "  th {\n",
       "    text-align: left;\n",
       "  }\n",
       "</style><div class='table-result-container'><table class='table-result'><thead style='background-color: white'><tr><th>database</th><th>tableName</th><th>isTemporary</th></tr></thead><tbody><tr><td>default</td><td>bronze_customers</td><td>false</td></tr><tr><td>default</td><td>bronze_geolocation</td><td>false</td></tr><tr><td>default</td><td>bronze_order_items</td><td>false</td></tr><tr><td>default</td><td>bronze_order_payments</td><td>false</td></tr><tr><td>default</td><td>bronze_order_reviews</td><td>false</td></tr><tr><td>default</td><td>bronze_orders</td><td>false</td></tr><tr><td>default</td><td>bronze_product_category_name_translation</td><td>false</td></tr><tr><td>default</td><td>bronze_products</td><td>false</td></tr><tr><td>default</td><td>bronze_sellers</td><td>false</td></tr></tbody></table></div>"
      ]
     },
     "metadata": {
      "application/vnd.databricks.v1+output": {
       "addedWidgets": {},
       "aggData": [],
       "aggError": "",
       "aggOverflow": false,
       "aggSchema": [],
       "aggSeriesLimitReached": false,
       "aggType": "",
       "arguments": {},
       "columnCustomDisplayInfos": {},
       "data": [
        [
         "default",
         "bronze_customers",
         false
        ],
        [
         "default",
         "bronze_geolocation",
         false
        ],
        [
         "default",
         "bronze_order_items",
         false
        ],
        [
         "default",
         "bronze_order_payments",
         false
        ],
        [
         "default",
         "bronze_order_reviews",
         false
        ],
        [
         "default",
         "bronze_orders",
         false
        ],
        [
         "default",
         "bronze_product_category_name_translation",
         false
        ],
        [
         "default",
         "bronze_products",
         false
        ],
        [
         "default",
         "bronze_sellers",
         false
        ]
       ],
       "datasetInfos": [],
       "dbfsResultPath": null,
       "isJsonSchema": true,
       "metadata": {},
       "overflow": false,
       "plotOptions": {
        "customPlotOptions": {},
        "displayType": "table",
        "pivotAggregation": null,
        "pivotColumns": null,
        "xColumns": null,
        "yColumns": null
       },
       "removedWidgets": [],
       "schema": [
        {
         "metadata": "{}",
         "name": "database",
         "type": "\"string\""
        },
        {
         "metadata": "{}",
         "name": "tableName",
         "type": "\"string\""
        },
        {
         "metadata": "{}",
         "name": "isTemporary",
         "type": "\"boolean\""
        }
       ],
       "type": "table"
      }
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "display(spark.sql(\"SHOW TABLES IN workspace.default\"))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "application/vnd.databricks.v1+cell": {
     "cellMetadata": {},
     "inputWidgets": {},
     "nuid": "4d8db115-627b-46d8-972d-4f2b0ee6e4d0",
     "showTitle": false,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "source": []
  }
 ],
 "metadata": {
  "application/vnd.databricks.v1+notebook": {
   "computePreferences": null,
   "dashboards": [],
   "environmentMetadata": {
    "base_environment": "",
    "environment_version": "5"
   },
   "inputWidgetPreferences": null,
   "language": "python",
   "notebookMetadata": {
    "pythonIndentUnit": 4
   },
   "notebookName": "01_bronze_ingest",
   "widgets": {}
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}