'''
Description: 对于bbox的处理
version: 1.0
Author: ShuaiLei
Date: 2024-11-18 19:14:07
LastEditors: ShuaiLei
LastEditTime: 2024-11-19 10:23:33
'''

def triangle_area(p1, p2, p3):
    """
    计算三个点围成的三角形面积
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def is_point_in_polygon_area(point, polygon):
    """
    判断点是否在四边形内部，通过面积法
    """
    total_area = triangle_area(polygon[0], polygon[1], polygon[2]) + triangle_area(polygon[2], polygon[3], polygon[0])
    
    sum_area = 0
    for i in range(4):
        sum_area += triangle_area(point, polygon[i], polygon[(i + 1) % 4])
    
    return abs(total_area - sum_area) < 1e-6  # 允许浮点误差
