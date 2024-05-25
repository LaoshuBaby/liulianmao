import os
import sys
from typing import Union

from pyproj import CRS, Geod

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))

# from module.log import logger


def calculate_distance(
    point_a_lon,
    point_a_lat,
    point_b_lon,
    point_b_lat,
    crs: Union[str, int] = "epsg:4326",
):
    # 解析CRS
    crs_obj = CRS.from_user_input(crs)
    # 获取必要的参数
    a = crs_obj.ellipsoid.semi_major_metre
    b = crs_obj.ellipsoid.semi_minor_metre
    # 创建Geod对象
    geod = Geod(a, b)

    point1 = (float(point_a_lon), float(point_a_lat))
    point2 = (float(point_b_lon), float(point_b_lat))

    distance = geod.inv(point1[0], point1[1], point2[0], point2[1])[2]

    answer = distance
    logger.trace(
        f"[calculate_distance().point_a]: (lat={point_a_lat}, lon={point_a_lon})"
    )
    logger.trace(
        f"[calculate_distance().point_b]: (lat={point_b_lat}, lon={point_b_lon})"
    )
    logger.trace(f"[calculate_distance().answer]: {answer}")
    return answer


if __name__ == "__main__":
    distance = calculate_distance(116.4074, 39.9042, 121.4737, 31.2304, 4326)
    print(distance)
