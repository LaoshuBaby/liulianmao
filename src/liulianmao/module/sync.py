from typing import List
import os


from .log import logger
from .storage import PROJECT_FOLDER, get_user_folder


default_profile_name="apikey.liulianmao"
default_apikey=os.path.join(get_user_folder(), PROJECT_FOLDER, default_profile_name)

def driver_aws_s3(accesskey=""):
    pass

def driver_aliyun_oss(accesskey=""):
    """
    S3 alternative
    """
    pass

def driver_tencent_cos(accesskey=""):
    """
    S3 alternative
    """
    pass

def driver_github_gist():
    pass
    

def sync_profiles(target_profile_list:List[str]=[default_apikey]):
    """
    本函数主要用于进行配置文件同步
    以确保在跨设备工作时为不同模型不同endpoint配置的apikey
    均可快速迁移，无需反复配置。
    """
    pass