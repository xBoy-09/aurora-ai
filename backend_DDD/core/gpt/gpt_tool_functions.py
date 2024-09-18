class GptToolFunctions:
    
    def get_map_building(building_name: str) -> str:
        return f"Here is the map of the {building_name} building", True
    
    def get_map_instructions(building_name: str) -> str:
        return 'Give only list of buildings', False
    
    available_function_map = {
        "get_map_building": get_map_building,
        "get_map_instructions" : get_map_instructions,
    }
    

