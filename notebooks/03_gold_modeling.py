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
     "finishTime": 1783180790557,
     "inputWidgets": {},
     "nuid": "60d175e1-ab09-428b-950d-8878595f11b1",
     "showTitle": false,
     "startTime": 1783180790052,
     "submitTime": 1783180790008,
     "tableResultSettingsMap": {},
     "title": ""
    }
   },
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "DataFrame[]"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "spark.sql(\"USE workspace.default\")"
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
     "finishTime": 1783181087616,
     "height": "400",
     "inputWidgets": {},
     "nuid": "47500bbd-6069-4900-866f-66850a53fa5f",
     "showTitle": false,
     "startTime": 1783181079181,
     "submitTime": 1783181079150,
     "tableResultSettingsMap": {},
     "title": "",
     "width": "756"
    }
   },
   "outputs": [],
   "source": [
    "query = '''WITH \n",
    "    unique_oi as (\n",
    "        SELECT \n",
    "        oi.order_id as o_id,\n",
    "        SUM(oi.freight_value) as sum_freight\n",
    "        FROM silver_order_items oi\n",
    "        GROUP BY oi.order_id\n",
    "    ),\n",
    "    most_distant_seller as (\n",
    "        SELECT \n",
    "        oi.order_id,\n",
    "        MAX(oi.seller_id) max_sid\n",
    "        FROM silver_order_items oi\n",
    "        LEFT JOIN (\n",
    "        SELECT\n",
    "        oi.order_id,\n",
    "        MAX(oi.freight_value) as max_freight\n",
    "        FROM silver_order_items oi\n",
    "        GROUP BY oi.order_id\n",
    "        ) as sub\n",
    "        ON oi.order_id = sub.order_id AND oi.freight_value = sub.max_freight\n",
    "        GROUP BY oi.order_id\n",
    "    )\n",
    "    SELECT\n",
    "    o.order_id as id,  \n",
    "    DATEDIFF(o.order_approved_at, o.order_purchase_timestamp) as aprov_time_days,\n",
    "    DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) as deliver_time_days,\n",
    "    CASE\n",
    "        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN TRUE \n",
    "        ELSE FALSE \n",
    "    END as late,\n",
    "    o.order_status,\n",
    "    uoi.sum_freight,\n",
    "    AVG(ow.review_score) as avg_review_score, \n",
    "    c.customer_state,\n",
    "    s.seller_state\n",
    "    FROM silver_orders o\n",
    "    LEFT JOIN unique_oi uoi\n",
    "    ON uoi.o_id = o.order_id\n",
    "    LEFT JOIN silver_order_reviews ow\n",
    "    ON ow.order_id = o.order_id\n",
    "    LEFT JOIN silver_customers c \n",
    "    ON o.customer_id = c.customer_id \n",
    "    LEFT JOIN most_distant_seller mds\n",
    "    ON o.order_id = mds.order_id\n",
    "    LEFT JOIN silver_sellers s\n",
    "    ON s.seller_id = mds.max_sid\n",
    "    GROUP BY \n",
    "    o.order_id, \n",
    "    o.order_status,\n",
    "    o.order_approved_at,\n",
    "    o.order_purchase_timestamp,\n",
    "    o.order_delivered_customer_date,\n",
    "    o.order_estimated_delivery_date,\n",
    "    uoi.sum_freight, \n",
    "    c.customer_state,\n",
    "    s.seller_state\n",
    "    '''\n",
    "\n",
    "df = spark.sql(query)\n",
    "df.write.format('delta').mode('overwrite').saveAsTable('fact_orders')"
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
   "notebookName": "03_gold_modeling",
   "widgets": {}
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}