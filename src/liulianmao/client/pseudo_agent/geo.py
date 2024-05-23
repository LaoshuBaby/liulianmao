from pyproj import Geod

def calculate_distance(point1_lon, point1_lat, point2_lon, point2_lat, crs:Union[str,int]='epsg:4326'):
    if isinstance(crs,int):
        crs="epsg:"+str(crs)
    elif isinstance(crs,str):
        try:
            if crs[0:5]="epsg:" and isinstance(int(crs[5:]),int):
                pass
            elif isinstance(int(crs),int):
                crs="epsg:"+crs
            else:
                return None
        except Exception as e:
            logger.error(e)
            return None
    else:
        return None

    geod = Geod(crs='epsg:4326')

    point1 = (float(point1_lon), float(point1_lat))
    point2 = (float(point2_lon), float(point2_lat))

    distance = geod.inv(point1[0], point1[1], point2[0], point2[1])[2]

    return distance

