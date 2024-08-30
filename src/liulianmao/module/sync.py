import os
from typing import Dict, List

import requests

from .log import logger
from .storage import PROJECT_FOLDER, get_user_folder

default_profile_name = "apikey.liulianmao"
default_apikey = os.path.join(
    get_user_folder(), PROJECT_FOLDER, default_profile_name
)


import os

import opendal

os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""

op = opendal.Operator(
    scheme="s3",
    root="/",
    bucket="laoshubaby",
    region="cn-beijing",
    endpoint="https://laoshubaby.oss-cn-beijing.aliyuncs.com",
    enable_virtual_host_style="True",
)

file_content = op.read("/static/nihongo/nhgbkysms.metadata.json")
print(file_content.decode("utf-8"))


class DriverAWSS3:
    def __init__(
        self,
        endpoint: str,
        accesskey: str,
        access_serect: str,
        region: str,
        bucket: str,
        path="/",
    ):
        logger.debug("[Sync]Driver AWS S3 was created!")
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

    def read(self, method: str = "restful") -> str:
        content = ""
        return content

    def write(self, content: str, method: str = "restful") -> Dict[str, str]:
        response = {}
        return response


class DriverAliyunOSS(DriverAWSS3):
    def __init__(self, method="compatiable"):
        if method == "native":
            # use aliyun sdk method
            import oss2
        elif method == "restful":
            # use http request
            super.read(method="restful")
            pass
        else:
            # compatiable method
            super.read(method="compatiable")
            pass


class DriverTencentCOS(DriverAWSS3):
    def __init__(self):
        pass


class DriverGit:
    def __init__(self):
        logger.debug("[Sync]Driver Git repository was created!")
        pass


class DriverPastebin:
    """
    注意：这里的pastebin不是Ubuntu Pastebin之类的，因为它们是只读的不可反复对同一个地址更新
    是为了统一GitHub、Gitee的Gist和GitLab的Snippets在称呼上的不同。

    文档：
    * GitHub: https://docs.github.com/en/rest/gists
    * GitLab: https://docs.gitlab.com/ee/user/snippets.html
    * Gitee: https://gitee.com/api/v5/swagger#/getV5Gists

    这里如果出现GitLab，特指GitLab official，如果是自部署的请自行传参
    """

    endpoint_collection = {
        "github": "https://gist.github.com/",
        "gitlab": "https://snippet.gitlab.com/",
        "gitee": "做梦呢小可爱？今天必须报这个Exception让你爱死什么叫特供平台",
    }

    def _get_endpoint(self, x: str = "GitHub") -> str:
        available_endpoint_presets = [key for key in self.endpoint_collection]
        if x.lower() in available_endpoint_presets:
            return self.endpoint_collection.get(x.lower())
        else:
            return x

    def __init__(
        self,
        pastebin_token: str,
        pastebin_id: str,
        endpoint: str = _get_endpoint("GitHub"),
        alt_name: str = "",
    ):
        logger.debug("[Sync]Driver Pastebin was created!")

        pass

    def read(self) -> str:
        content = ""
        return content

    def write(self, content: str) -> Dict[str, str]:
        response = {}
        return response


def sync_profiles(
    target_profile_list: List[str] = [default_apikey],
    driver: str = "s3.aws",
    **kwargs
):
    """
    本函数主要用于进行配置文件同步
    以确保在跨设备工作时为不同模型不同endpoint配置的apikey
    均可快速迁移，无需反复配置。

    命名为apikey是因为accesskey要在S3里面用，token在LLM领域有特指含义，访问控制的令牌只能叫apikey了

    此外，这个文件就是重新实现了 https://github.com/mfuentesg/SyncSettings 果然又一次重新发明了轮子
    """
    if driver == "s3.aws":
        driver = DriverAWSS3(
            endpoint="",
            accesskey="114514",
            access_serect="1919810",
            region="",
            bucket="",
            path="/",
        )
    elif driver == "pastebin":
        driver = DriverPastebin(
            pastebin_id="", pastebin_token="", endpoint="GitHub"
        )
