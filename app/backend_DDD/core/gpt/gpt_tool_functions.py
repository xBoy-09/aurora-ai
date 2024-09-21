import json

lums_building_names = [
    "Academic Block",
    "Syed Babar Ali School of Science and Engineering", 
    "SBSSE",
    "SDSB",
    "MGSHSS",
]

class GptToolFunctions:
    
    



    def get_map_buildings( building_names: list) -> dict[str, str]:
        buildings = {
            "Academic Block": "https://www.lums.edu.pk/sites/default/files/inline-images/academic-block.jpg",
            "SBSSE": "https://www.lums.edu.pk/sites/default/files/inline-images/sse.jpg",
            "Syed Babar Ali School of Science and Engineering" : "https://www.lums.edu.pk/sites/default/files/inline-images/sse.jpg",
            "SDSB": "https://www.lums.edu.pk/sites/default/files/inline-images/sdsb.jpg",
            "MGSHSS": "https://www.lums.edu.pk/sites/default/files/inline-images/mgshss.jpg",
        }

        for name in building_names:
            if name not in buildings:
                return json.dumps({
                    "error": f"Building name '{name}' is not valid. Valid building names are: {lums_building_names}"
                }, indent=4)

        # Creating a list of dictionaries for buildings_info
        buildings_info = [
            {
                "building_name": building_name,
                "building_image_link": building_image_link
            } for building_name, building_image_link in buildings.items() if building_name in building_names
        ]


        # Convert the list of dictionaries into a JSON string
        return json.dumps({
            "buildings_info": buildings_info
        }, indent=4)


    def get_map_buildings_response_format(building_names: list) -> dict:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "get_map_buildings",
                "description": "Returns a list building names and its image links",
                "strict": True,
                "schema": {
                    "type": "object",  # Root type is "object"
                    "properties": {
                        "buildings_info": {
                            "description": "A list of building names and their image links",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "building_name": {
                                        "type": "string",
                                        "description": "The name of LUMS building for which you want to get the map. eg. 'Academic Block' 'mgshss'.",
                                        # "enum": lums_building_names,
                                    },
                                    "building_image_link": {
                                        "description": "The link to the image of the building",
                                        "type": "string",
                                    }
                                },
                                "required": ["building_name", "building_image_link"],  # List all required properties here
                                "additionalProperties": False  # Ensures no additional properties are allowed in each item
                            },
                        },
                    },
                    "required": ["buildings_info"],  # List all required properties here
                    "additionalProperties": False,  # Ensures no additional properties are allowed in the root object
                }
            },
        }








    available_function_map = {
        "get_map_buildings": get_map_buildings,
        "get_map_buildings_response_format" : get_map_buildings_response_format
    }


