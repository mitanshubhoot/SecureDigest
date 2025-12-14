import json
from pathlib import Path
from typing import List, Dict, Optional

class ToolsDirectoryService:
    """Service for managing security tools directory"""
    
    def __init__(self):
        self.data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        self.tools_file = self.data_dir / "tools.json"
        
    def get_all_tools(self) -> List[Dict]:
        """Get all tools from the dataset"""
        if not self.tools_file.exists():
            return []
            
        try:
            with open(self.tools_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading tools: {e}")
            return []
            
    def get_tool_by_id(self, tool_id: str) -> Optional[Dict]:
        """Get a specific tool by ID"""
        tools = self.get_all_tools()
        for tool in tools:
            if tool["id"] == tool_id:
                return tool
        return None
        
    def get_categories(self) -> List[str]:
        """Get list of unique tool categories"""
        tools = self.get_all_tools()
        categories = set(tool["category"] for tool in tools)
        return sorted(list(categories))
        
    def filter_tools(self, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict]:
        """Filter tools by category and search term"""
        tools = self.get_all_tools()
        
        if category and category != "All":
            tools = [t for t in tools if t["category"] == category]
            
        if search:
            search_lower = search.lower()
            tools = [
                t for t in tools 
                if search_lower in t["name"].lower() 
                or search_lower in t["description"].lower()
                or any(search_lower in tag.lower() for tag in t.get("tags", []))
            ]
            
        return tools
