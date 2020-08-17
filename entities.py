default_entities = {
    "edm80opc": {
        "name": "edm 80 opc",
        "description": ""
    },
    "ds_pm10": {
        "name": "PM10 Datastream",
        "description": "Datastream for recording Particulate Matter",
        "properties": {
            "license": {
                "type": "CC0 1.0",
                "owner": "TECO",
                "metadata": "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
            }
        },
        "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
        "unitOfMeasurement": {
            "name": "microgram per cubic meter",
            "symbol": "ug/m^3",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#KilogramPerCubicMeter"
        },
        "ObservedProperty": {"@iot.id": "saqn:op:mcpm10"},
        "Thing": {"@iot.id": ""},
        "Sensor": {"@iot.id": "saqn:s:"},
        "@iot.id": ""
    },
    "ds_pm25": {
        "name": "PM2.5 Datastream",
        "description": "Datastream for recording Particulate Matter",
        "properties": {
            "license": {
                "type": "CC0 1.0",
                "owner": "TECO",
                "metadata": "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
            }
        },
        "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
        "unitOfMeasurement": {
            "name": "microgram per cubic meter",
            "symbol": "ug/m^3",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#KilogramPerCubicMeter"
        },
        "ObservedProperty": {"@iot.id": "saqn:op:mcpm2p5"},
        "Thing": {"@iot.id": ""},
        "Sensor": {"@iot.id": ""},
        "@iot.id": ""
    },
    "ds_pm1": {
        "name": "PM1 Datastream",
        "description": "Datastream for recording Particulate Matter",
        "properties": {
            "license": {
                "type": "CC0 1.0",
                "owner": "TECO",
                "metadata": "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
            }
        },
        "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
        "unitOfMeasurement": {
            "name": "microgram per cubic meter",
            "symbol": "ug/m^3",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#KilogramPerCubicMeter"
        },
        "ObservedProperty": {"@iot.id": "saqn:op:mcpm1"},
        "Thing": {"@iot.id": ""},
        "Sensor": {"@iot.id": ""},
        "@iot.id": ""
    },
    "ds_pm4": {
        "name": "PM4 Datastream",
        "description": "Datastream for recording Particulate Matter",
        "properties": {
            "license": {
                "type": "CC0 1.0",
                "owner": "TECO",
                "metadata": "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
            }
        },
        "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
        "unitOfMeasurement": {
            "name": "microgram per cubic meter",
            "symbol": "ug/m^3",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#KilogramPerCubicMeter"
        },
        "ObservedProperty": {"@iot.id": "saqn:op:mcpm4"},
        "Thing": {"@iot.id": ""},
        "Sensor": {"@iot.id": ""},
        "@iot.id": ""
    },
    "ds_bins": {
        "name": "Number concentration PM10 Datastream",
        "description": "Datastream for recording Particulate Matter",
        "properties": {
            "license": {
                "type": "CC0 1.0",
                "owner": "TECO",
                "metadata": "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
            }
        },
        "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
        "unitOfMeasurement": {
            "name": "microgram per cubic meter",
            "symbol": "ug/m^3",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#KilogramPerCubicMeter"
        },
        "ObservedProperty": {"@iot.id": "saqn:op:ncpm10"},
        "Thing": {"@iot.id": ""},
        "Sensor": {"@iot.id": ""},
        "@iot.id": ""
    },

    "observation": {
        "phenomenonTime": "",
        "result": -1.0,
        "FeatureOfInterest": {
            "name": "1",
            "description": "",
            "encodingType": "application/vnd.geo+json",
            "feature": {
                "type": "Point",
                "coordinates": [-96.80867, 32.77903]
            }
        }
    },

    "things": {
        "name": '',
        "description": ''
    }


}