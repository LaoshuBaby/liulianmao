from typing import List
import os


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


class DriverAliyunOSS(DriverAWSS3):
    def __init__(self):
        pass


class DriverTencentCOS(DriverAWSS3):
    def __init__(self):
        pass


class DriverGitHubGist:
    def __init__(self):
        pass


class DriverGit:
    def __init__(self):
        pass


def sync_profiles(target_profile_list: List[str] = [default_apikey]):
    """
    本函数主要用于进行配置文件同步
    以确保在跨设备工作时为不同模型不同endpoint配置的apikey
    均可快速迁移，无需反复配置。
    """
    pass
