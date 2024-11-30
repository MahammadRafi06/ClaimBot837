import os
import pathlib
# print(pathlib.Path(__file__).parent.parent)
# print(f"{pathlib.Path(__file__).parent.parent}\data")

print(os.listdir(f"{pathlib.Path(__file__).parent.parent}/data")[0])