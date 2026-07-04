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
     "finishTime": 1783178068871,
     "inputWidgets": {},
     "nuid": "ec308f42-9949-43f1-82a4-5be1a7833d84",
     "showTitle": false,
     "startTime": 1783178051060,
     "submitTime": 1783178050474,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "import unicodedata\n",
    "from pyspark.sql import functions as F\n",
    "from pyspark.sql.functions import udf\n",
    "from pyspark.sql.types import StringType\n",
    "\n",
    "def remove_acentos(texto):\n",
    "    if texto is None:\n",
    "        return None\n",
    "    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')\n",
    "\n",
    "remove_acentos_udf = udf(remove_acentos, StringType())"
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
     "finishTime": 1783178178880,
     "inputWidgets": {},
     "nuid": "b02845da-36f6-4434-a072-e62194f6bc55",
     "showTitle": false,
     "startTime": 1783178160368,
     "submitTime": 1783178160324,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_customers\")\n",
    "df = df.withColumn('customer_city', F.initcap(F.trim(F.col('customer_city'))))\n",
    "df = df.withColumn('customer_state', F.upper(F.trim(F.col('customer_state'))))\n",
    "df = df.withColumn('customer_zip_code_prefix', F.lpad(F.col('customer_zip_code_prefix').cast('string'), 5, \"0\"))\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_customers')"
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
     "finishTime": 1783178269102,
     "inputWidgets": {},
     "nuid": "95f667d3-42f2-482c-b685-1f4909560db8",
     "showTitle": false,
     "startTime": 1783178248666,
     "submitTime": 1783178248624,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_geolocation\")\n",
    "df = df.dropDuplicates()\n",
    "df = df.withColumn('geolocation_city', F.initcap(F.trim(remove_acentos_udf(F.col('geolocation_city')))))\n",
    "df = df.withColumn('geolocation_city', F.when(F.length(F.col('geolocation_city')) < 3, None).otherwise(F.col('geolocation_city')))\n",
    "df = df.withColumn('geolocation_zip_code_prefix', F.lpad(F.col('geolocation_zip_code_prefix').cast('string'), 5, '0'))\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_geolocation')\n"
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
     "finishTime": 1783178415894,
     "inputWidgets": {},
     "nuid": "883cfe84-320c-436b-8061-7d04c70f5edd",
     "showTitle": false,
     "startTime": 1783178409500,
     "submitTime": 1783178409454,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_order_items\")\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_order_items')"
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
     "finishTime": 1783178554263,
     "inputWidgets": {},
     "nuid": "7e86b3b8-349d-451f-a003-c58d065383a3",
     "showTitle": false,
     "startTime": 1783178549574,
     "submitTime": 1783178549527,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_order_payments\")\n",
    "df = df.withColumn('payment_suspicious',\n",
    "    F.when((F.col('payment_value') == 0) | (F.col('payment_type') == 'not_defined'), True).otherwise(False))\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_order_payments')"
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
     "finishTime": 1783179418497,
     "inputWidgets": {},
     "nuid": "8d66197e-11f7-4bcc-ac1a-045fd0410040",
     "showTitle": false,
     "startTime": 1783179413483,
     "submitTime": 1783179413430,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_order_reviews\")\n",
    "df = df.withColumn('review_score', \n",
    "    F.when(F.col('review_score').isin('1', '2', '3', '4', '5'), \n",
    "           F.col('review_score'))\n",
    "     .otherwise(None))\n",
    "df = df.withColumn('review_score', F.col('review_score').cast('integer'))\n",
    "df = df.withColumn('review_creation_date', F.expr(\"try_cast(review_creation_date as timestamp)\"))\n",
    "df = df.withColumn('review_answer_timestamp', F.expr(\"try_cast(review_answer_timestamp as timestamp)\"))\n",
    "df = df.withColumn('review_comment_title', F.initcap(F.trim(F.col('review_comment_title'))))\n",
    "df = df.withColumn('review_comment_message', F.initcap(F.trim(F.col('review_comment_message'))))\n",
    "df = df.fillna({'review_comment_message': 'Não Preenchido', 'review_comment_title': 'Não Preenchido'})\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_order_reviews')"
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
     "finishTime": 1783179675456,
     "inputWidgets": {},
     "nuid": "2848cc5b-e264-40dd-ae52-69ec239b7fa9",
     "showTitle": false,
     "startTime": 1783179670795,
     "submitTime": 1783179670751,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_orders\")\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_orders')"
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
     "finishTime": 1783179824911,
     "inputWidgets": {},
     "nuid": "9ad48ffc-c1e7-4391-a673-5b363e564740",
     "showTitle": false,
     "startTime": 1783179820205,
     "submitTime": 1783179820158,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_product_category_name_translation\")\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_product_category_name_translation')"
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
     "finishTime": 1783179970039,
     "inputWidgets": {},
     "nuid": "98fc20a7-0caf-44dc-afb3-d01351415e01",
     "showTitle": false,
     "startTime": 1783179965789,
     "submitTime": 1783179965746,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_products\")\n",
    "df = df.fillna({'product_category_name': 'Não Preenchido'})\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('silver_products')"
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
     "finishTime": 1783180030517,
     "inputWidgets": {},
     "nuid": "a76f147e-d836-4f54-8343-ed96ec958164",
     "showTitle": false,
     "startTime": 1783180022205,
     "submitTime": 1783180022171,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [],
   "source": [
    "df = spark.read.table(\"workspace.default.bronze_sellers\")\n",
    "df = df.withColumn('seller_zip_code_prefix', F.lpad(F.col('seller_zip_code_prefix').cast('string'), 5, '0'))\n",
    "df = df.withColumn('seller_city', F.initcap(F.trim(remove_acentos_udf(F.col('seller_city')))))\n",
    "df = df.withColumn('seller_city', F.when(\n",
    "    (F.length(F.col('seller_city')) < 3) |\n",
    "    (F.col('seller_city').contains('-')) |\n",
    "    (F.col('seller_city').contains(r'\\\\')) |\n",
    "    (F.col('seller_city').contains('/')) |\n",
    "    (F.col('seller_city').contains('@')),\n",
    "    None).otherwise(F.col('seller_city')))\n",
    "df = df.withColumn('seller_state', F.upper(F.col('seller_state')))\n",
    "df.write.format('delta').mode('overwrite').saveAsTable(\"silver_sellers\")"
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
     "finishTime": 1783180126946,
     "inputWidgets": {},
     "nuid": "29a34935-1950-44a2-aaec-ed48e4a35f8e",
     "showTitle": false,
     "startTime": 1783180120590,
     "submitTime": 1783180120548,
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
       "</style><div class='table-result-container'><table class='table-result'><thead style='background-color: white'><tr><th>database</th><th>tableName</th><th>isTemporary</th></tr></thead><tbody><tr><td>default</td><td>bronze_customers</td><td>false</td></tr><tr><td>default</td><td>bronze_geolocation</td><td>false</td></tr><tr><td>default</td><td>bronze_order_items</td><td>false</td></tr><tr><td>default</td><td>bronze_order_payments</td><td>false</td></tr><tr><td>default</td><td>bronze_order_reviews</td><td>false</td></tr><tr><td>default</td><td>bronze_orders</td><td>false</td></tr><tr><td>default</td><td>bronze_product_category_name_translation</td><td>false</td></tr><tr><td>default</td><td>bronze_products</td><td>false</td></tr><tr><td>default</td><td>bronze_sellers</td><td>false</td></tr><tr><td>default</td><td>silver_customers</td><td>false</td></tr><tr><td>default</td><td>silver_geolocation</td><td>false</td></tr><tr><td>default</td><td>silver_order_items</td><td>false</td></tr><tr><td>default</td><td>silver_order_payments</td><td>false</td></tr><tr><td>default</td><td>silver_order_reviews</td><td>false</td></tr><tr><td>default</td><td>silver_orders</td><td>false</td></tr><tr><td>default</td><td>silver_product_category_name_translation</td><td>false</td></tr><tr><td>default</td><td>silver_products</td><td>false</td></tr><tr><td>default</td><td>silver_sellers</td><td>false</td></tr></tbody></table></div>"
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
        ],
        [
         "default",
         "silver_customers",
         false
        ],
        [
         "default",
         "silver_geolocation",
         false
        ],
        [
         "default",
         "silver_order_items",
         false
        ],
        [
         "default",
         "silver_order_payments",
         false
        ],
        [
         "default",
         "silver_order_reviews",
         false
        ],
        [
         "default",
         "silver_orders",
         false
        ],
        [
         "default",
         "silver_product_category_name_translation",
         false
        ],
        [
         "default",
         "silver_products",
         false
        ],
        [
         "default",
         "silver_sellers",
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
   "notebookName": "02_silver_transform",
   "widgets": {}
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}