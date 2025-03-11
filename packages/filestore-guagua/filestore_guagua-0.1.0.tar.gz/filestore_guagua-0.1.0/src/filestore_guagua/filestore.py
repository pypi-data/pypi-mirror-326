import os
import json
import pickle


class FileStore:
    def __init__(self, base_dir: str = "env"):
        self.base_dir = f"{self.get_project_root()}/{base_dir}"

    def saveJSON(self, fileName: str, data: dict) -> None:
        """
        保存json文件

        参数：
            fileName (str): 文件的完整路径,不需带后缀。
            data (dict): 字典对象。
        """
        self.ensure_directories(fileName)
        file_path = os.path.join(self.base_dir, f"{fileName}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def readJSON(self, fileName: str) -> dict:
        """
        读取json文件

        参数：
            fileName (str): 文件的完整路径,不需带后缀。
        """
        file_path = os.path.join(self.base_dir, f"{fileName}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def saveData(self, fileName: str, save_data: any) -> None:
        """
        保存文件

        参数：
            fileName (str): 文件的完整路径。
            save_data (any): 对象。
        """
        self.ensure_directories(fileName)
        file_path = os.path.join(self.base_dir, fileName)
        with open(file_path, "wb") as fw:
            pickle.dump(save_data, fw)

    def openData(self, fileName: str) -> any:
        """
        读取文件

        参数：
            fileName (str): 文件的完整路径。
        """
        try:
            file_path = os.path.join(self.base_dir, fileName)
            with open(file_path, "rb") as fr:
                return_Mat = pickle.load(fr)
            return return_Mat
        except:
            return []

    @staticmethod
    def get_project_root() -> str:
        """
        获取项目的执行目录
        """ 
        return os.getcwd()

    def exists_file(self, fileName) -> bool:
        """
        判断文件是否存在

        参数：
            fileName (str): 文件的完整路径。
        """
        file_path = os.path.join(self.base_dir, fileName)
        return os.path.exists(file_path)

    def ensure_directories(self, fileName):
        """
        确保给定文件路径中的所有目录都存在，如果不存在则创建它们。

        参数：
            fileName (str): 文件的完整路径。
        """
        # 获取文件所在的目录路径
        file_path = os.path.join(self.base_dir, fileName)
        directory = os.path.dirname(file_path)
        # 检查目录是否存在
        if not os.path.exists(directory):
            # 如果目录不存在，创建所有中间目录
            os.makedirs(directory)

    def create_json_files(self, fileNameList: list, jsonDataList: list[dict]) -> None:
        """
        批量创建json文件

        参数：
            fileNameList (list): 需创建的json文件列表,不需带后缀。
            jsonDataList (list[dict]): 其中每个元素为一个字典,表示一个json文件的内容。
        """
        if len(fileNameList) != len(jsonDataList):
            raise ValueError("文件名列表和json数据列表长度不一致！")
        for file_index in range(len(fileNameList)):
            self.ensure_directories(f"{fileNameList[file_index]}.json")
            file_path = os.path.join(self.base_dir, f"{fileNameList[file_index]}.json")
            with open(file_path, "w") as fw:
                json.dump(jsonDataList[file_index], fw, indent=4)
