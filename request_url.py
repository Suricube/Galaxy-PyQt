import requests

from pydantic import BaseModel
import json

class URL(BaseModel):
    token: str = ""
    tree_dict: dict = {}
    
    def get_github_tree(self, url: str) -> dict:
        headers = {
        "Authorization": self.token
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    
    def get_blobs(self, tree: dict) -> dict:
        for item in tree["tree"]:
            if item["type"] == "blob":
                self.tree_dict[item["path"]] = item["url"] 
        return self.tree_dict

    def set_token(self):
        f = open("assets/token.json")
        data = f.read()
        f.close()
        self.token = json.loads(data).get("Authorization")




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
    