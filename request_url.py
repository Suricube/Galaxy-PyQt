import requests

from pydantic import BaseModel
import json

class URL(BaseModel):

    tree_dict: dict = {}
    
    @staticmethod
    def get_github_tree(url: str) -> dict:
        headers = {
        "Author ization": "to ken git_LH_hub_pat_11AD5TBQQ_LH_0iYXcaL0adMVE_Wvzo9hQK3PvPnjGZXteaJ6hoqkO_LH_KUAVdspml72iQe5cDIOGGXFZ1PH7Iq8Y"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    
    def get_blobs(self, tree: dict) -> dict:
        for item in tree["tree"]:
            if item["type"] == "blob":
                self.tree_dict[item["path"]] = item["url"] 
        return self.tree_dict

    


def main():
    pass
    #url_model = URL() 
    #tree = get_github_tree("https://api.github.com/repos/Suricube/Galaxy-Components/git/trees/main?recursive=1")

    
    #for item in tree["tree"]:
    #    if item["type"] == "blob":
    #        url_model.tree_dict[item["path"]] = item["url"]  
    
    #for item in url_model.tree_dict.items():
    #    print(item, "\n")
    

if __name__ == "__main__":
        main()
    