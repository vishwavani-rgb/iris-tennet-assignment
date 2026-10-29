

import os

SOURCE_NAME = "Netbeheer Nederland capacity map — TenneT"
SOURCE_URL = os.getenv(
    "TENNET_SOURCE_URL",
    "https://services.arcgis.com/nSZVuSZjHpEZZbRo/arcgis/rest/services/Capaciteitskaart_Tennet_afname/FeatureServer/1/query",
)
REQUEST_TIMEOUT_SECONDS = int(os.getenv("TENNET_REQUEST_TIMEOUT", "20"))
TARGET_OPERATOR = "TenneT"
OUTPUT_DIR = os.getenv("TENNET_OUTPUT_DIR", "data/tennet")
RAW_DIR_NAME = "raw"
PROCESSED_DIR_NAME = "processed"
REJECTED_DIR_NAME = "rejected"
USER_AGENT = "IRIS-TenneT-Assignment/1.0"
