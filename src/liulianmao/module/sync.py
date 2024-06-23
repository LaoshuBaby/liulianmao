import os
from typing import Dict, List

from .log import logger
from .storage import PROJECT_FOLDER, get_user_folder

default_profile_name = "apikey.liulianmao"
default_apikey = os.path.join(
    get_user_folder(), PROJECT_FOLDER, default_profile_name
)


class DriverAWSS3:
    def __init__(
        self,
        endpoint: str,
        accesskey: str,
        access_serect: str,
        region="",
        bucket="",
        path="",
    ):
        pass

    def check_path_style(self) -> str:
        """
        可参考AWS文档
        https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html
        """
        if self.endpoint[0 : len(self.bucket) + 1] == self.bucket + ".":
            return "virtual_hosted_style"
        else:
            return "path_style"

    def read(self) -> str:
        content = ""
        return content

    def write(self, content: str) -> Dict[str, str]:
        response = {}
        return response


class DriverAliyunOSS(DriverAWSS3):
    def __init__(self, method="compatiable"):
        if method == "native":
            pass
            # import aliyun_sdk_python_oss
        pass


class DriverTencentCOS(DriverAWSS3):
    def __init__(self):
        pass


class DriverGitHubGist:
    def __init__(self):
        pass


class DriverGit:
    endpoint_collection = {
        "github": "https://gist.github.com/",
        "gitlab": "https://gist.gitlab.com/",
        "gitlab_official": "",
        "gitee": "做梦呢小可爱？今天必须报这个Exception让你爱死什么叫特供平台",
    }

    def _get_endpoint(self, name: str = "GitHub") -> str:
        return self.endpoint_collection.get(name.lower())

    def __init__(
        self,
        gist_token: str,
        gist_id: str,
        endpoint: str = _get_endpoint("GitHub"),
        alt_name: str = "",
    ):
        pass


def sync_profiles(target_profile_list: List[str] = [default_apikey], driver:str="s3.aws"):
    """
    本函数主要用于进行配置文件同步
    以确保在跨设备工作时为不同模型不同endpoint配置的apikey
    均可快速迁移，无需反复配置。
    """
    if driver=="s3.aws":
        driver=DriverAWSS3(endpoint="",accesskey="114514",access_serect="1919810")
    pass