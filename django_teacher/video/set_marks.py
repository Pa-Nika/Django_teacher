from .upload import constants


def get_list_name_columns() -> list:
    name_columns = []
    for i in constants.ARRAY_OF_POINTS:
        name_columns.append(str(i) + '_x')
        name_columns.append(str(i) + '_y')
    name_columns.append('square')
    name_columns.append('width')
    name_columns.append('height')
    name_columns.append('eye_mark')
    name_columns.append('duration')
    return name_columns


def square_mark(row) -> int:
    if row['eye_mark'] == 0:
        return 0
    elif row['eye_mark'] == -1:
        return -1

    square = row['height'] * row['width']
    limit_5_up, limit_5_bottom = square * 0.09, square * 0.14
    limit_4_up, limit_4_bottom = square * 0.08, square * 0.15
    limit_3_up, limit_3_bottom = square * 0.06, square * 0.16
    if (row['square'] > limit_5_up) & (row['square'] < limit_5_bottom):
        return 5
    elif (row['square'] > limit_4_up) & (row['square'] < limit_4_bottom):
        return 4
    elif (row['square'] > limit_3_up) & (row['square'] < limit_3_bottom):
        return 3
    else:
        return 2


def ver_mark(row) -> int:
    if row['eye_mark'] == 0:
        return 0
    elif row['eye_mark'] == -1:
        return -1

    up = row['height']
    limit_5_up, limit_5_bottom = up * 0.3, up * 0.33
    limit_4_up, limit_4_bottom = up * 0.28, up * 0.33
    limit_3_up, limit_3_bottom = up * 0.19, up * 0.34
    if (row['28_y'] > limit_5_up) & (row['28_y'] < limit_5_bottom):
        return 5
    elif (row['28_y'] > limit_4_up) & (row['28_y'] < limit_4_bottom):
        return 4
    elif (row['28_y'] > limit_3_up) & (row['28_y'] < limit_3_bottom):
        return 3
    else:
        return 2


def hor_mark(row) -> int:
    if row['eye_mark'] == 0:
        return 0
    elif row['eye_mark'] == -1:
        return -1

    center = round(row['width'] / 2)
    limit_5, limit_4, limit_3 = center * 0.03, center * 0.05, center * 0.08
    if (row['28_x'] > center - limit_5) & (row['28_x'] < center + limit_5):
        return 5
    elif (row['28_x'] > center - limit_4) & (row['28_x'] < center + limit_4):
        return 4
    elif (row['28_x'] > center - limit_3) & (row['28_x'] < center + limit_3):
        return 3
    else:
        return 2
