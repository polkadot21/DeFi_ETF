import os
import json
assets = os.getenv("assets")


if __name__=="__main__":
    env_list = json.loads(assets)
    print(env_list)
    print(type(env_list))
