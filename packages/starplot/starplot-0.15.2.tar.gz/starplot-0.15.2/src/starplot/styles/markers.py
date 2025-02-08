from functools import cache

from matplotlib import transforms
from matplotlib.path import Path

import numpy as np


def ellipse_points(
    center_x, center_y, semi_major_axis, semi_minor_axis, num_points=100
):
    """Generates points on an ellipse.

    Args:
        center_x: X coordinate of the center.
        center_y: Y coordinate of the center.
        semi_major_axis: Length of the semi-major axis.
        semi_minor_axis: Length of the semi-minor axis.
        num_points: Number of points to generate.

    Returns:
        A list of (x, y) coordinates of the ellipse points.
    """

    theta = np.linspace(0, 2 * np.pi, num_points)
    x = center_x + semi_major_axis * np.cos(theta)
    y = center_y + semi_minor_axis * np.sin(theta)

    return list(zip(x, y))


@cache
def ellipse():
    verts = ellipse_points(0, 0, 1, 0.5)

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])
    p = Path(verts, codes).transformed(transforms.Affine2D().rotate_deg(15))

    return p


@cache
def circle_cross():
    verts = ellipse_points(0, 0, 1, 1)

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])

    verts.extend(
        [
            (-1, 0),
            (1, 0),
            (0, 1),
            (0, -1),
        ]
    )
    codes.extend(
        [
            Path.MOVETO,
            Path.LINETO,
            Path.MOVETO,
            Path.LINETO,
        ]
    )

    return Path(verts, codes)


@cache
def circle_crosshair():
    verts = ellipse_points(0, 0, 1, 1)

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])

    verts.extend(
        [
            (-1, 0),
            (-1.7, 0),
            (0, 1),
            (0, 1.7),
            (1, 0),
            (1.7, 0),
            (0, -1),
            (0, -1.7),
        ]
    )
    codes.extend(
        [
            Path.MOVETO,
            Path.LINETO,
            Path.MOVETO,
            Path.LINETO,
            Path.MOVETO,
            Path.LINETO,
            Path.MOVETO,
            Path.LINETO,
        ]
    )

    return Path(verts, codes)


@cache
def circle_dot():
    verts = ellipse_points(0, 0, 1, 1)

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])

    verts.extend(ellipse_points(0, 0, 0.6, 0.6))

    codes.extend([Path.MOVETO])
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])

    return Path(verts, codes)


@cache
def circle_dotted_rings(num_rings=2):
    verts = ellipse_points(0, 0, 1, 1)

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])

    step = 2
    for n in range(num_rings):
        radius = 1.4 + n * 0.3
        ring_verts = ellipse_points(0, 0, radius, radius)

        for k in range(step, 100, step):
            if k % (step * 2):
                verts.extend(ring_verts[k : k + step])
                codes.extend([Path.MOVETO])
                codes.extend([Path.LINETO] * (step - 1))

    return Path(verts, codes)


@cache
def circle_line():
    # verts = list(ellipse_points(0, 0, 1, 1))
    # size = len(verts)
    # top = verts[2 : int(size / 2 - 2)]
    # bottom = verts[int(size / 2 + 2) : size - 2]
    # y = top[-1][1]
    # top = [[2, 0], [2, y]] + top + [[-2, top[-1][1]], [-2, 0]]
    # bottom = [[-2, 0], [-2, -1 * y]] + bottom + [[2, -1 * y], [2, 0], [2, 0]]

    points = [
        [2, 0],
        [2, 0.18925124436040974],
        (0.9819286972627067, 0.18925124436041021),
        (0.9679487013963562, 0.2511479871810792),
        (0.9500711177409454, 0.3120334456984871),
        (0.9283679330160726, 0.3716624556603276),
        (0.9029265382866212, 0.42979491208917164),
        (0.8738493770697849, 0.4861967361004687),
        (0.8412535328311812, 0.5406408174555976),
        (0.8052702575310586, 0.5929079290546404),
        (0.766044443118978, 0.6427876096865393),
        (0.7237340381050701, 0.690079011482112),
        (0.6785094115571322, 0.7345917086575333),
        (0.6305526670845225, 0.7761464642917568),
        (0.5800569095711982, 0.8145759520503357),
        (0.5272254676105024, 0.8497254299495144),
        (0.4722710747726827, 0.8814533634475821),
        (0.41541501300188644, 0.9096319953545183),
        (0.3568862215918719, 0.9341478602651067),
        (0.2969203753282749, 0.9549022414440739),
        (0.23575893550942728, 0.9718115683235417),
        (0.17364817766693041, 0.984807753012208),
        (0.1108381999010111, 0.9938384644612541),
        (0.04758191582374218, 0.998867339183008),
        (-0.01586596383480803, 0.9998741276738751),
        (-0.07924995685678854, 0.9968547759519424),
        (-0.14231483827328523, 0.9898214418809327),
        (-0.20480666806519074, 0.9788024462147787),
        (-0.26647381369003503, 0.963842158559942),
        (-0.32706796331742166, 0.9450008187146685),
        (-0.3863451256931287, 0.9223542941045814),
        (-0.4440666126057741, 0.8959937742913359),
        (-0.5000000000000002, 0.8660254037844385),
        (-0.5539200638661103, 0.8325698546347714),
        (-0.6056096871376668, 0.795761840530832),
        (-0.654860733945285, 0.7557495743542583),
        (-0.7014748877063214, 0.7126941713788627),
        (-0.7452644496757547, 0.6667690005162917),
        (-0.7860530947427875, 0.6181589862206051),
        (-0.8236765814298327, 0.5670598638627709),
        (-0.8579834132349771, 0.5136773915734063),
        (-0.8888354486549234, 0.4582265217274105),
        (-0.9161084574320696, 0.4009305354066136),
        (-0.9396926207859083, 0.3420201433256689),
        (-0.9594929736144974, 0.28173255684142967),
        (-0.975429786885407, 0.2511479871810792),
        (-0.9874388886763943, 0.18925124436040974),
        [-2, 0.18925124436040974],
        [-2, 0],
        [-2, 0],
        [-2, -0.18925124436040974],
        (-0.9874388886763943, -0.18925124436040974),
        (-0.975429786885407, -0.2511479871810792),
        (-0.9594929736144974, -0.28173255684142984),
        (-0.9396926207859084, -0.34202014332566866),
        (-0.9161084574320696, -0.4009305354066138),
        (-0.8888354486549235, -0.4582265217274103),
        (-0.857983413234977, -0.5136773915734064),
        (-0.8236765814298328, -0.5670598638627706),
        (-0.7860530947427874, -0.6181589862206053),
        (-0.7452644496757548, -0.6667690005162915),
        (-0.7014748877063213, -0.7126941713788629),
        (-0.6548607339452852, -0.7557495743542582),
        (-0.6056096871376666, -0.7957618405308321),
        (-0.5539200638661105, -0.8325698546347713),
        (-0.4999999999999996, -0.8660254037844388),
        (-0.44406661260577396, -0.895993774291336),
        (-0.3863451256931287, -0.9223542941045814),
        (-0.3270679633174219, -0.9450008187146683),
        (-0.26647381369003464, -0.9638421585599422),
        (-0.20480666806519054, -0.9788024462147787),
        (-0.14231483827328523, -0.9898214418809327),
        (-0.07924995685678879, -0.9968547759519423),
        (-0.01586596383480761, -0.9998741276738751),
        (0.04758191582374238, -0.998867339183008),
        (0.11083819990101086, -0.9938384644612541),
        (0.17364817766692997, -0.9848077530122081),
        (0.23575893550942748, -0.9718115683235417),
        (0.2969203753282749, -0.9549022414440739),
        (0.35688622159187167, -0.9341478602651068),
        (0.4154150130018868, -0.9096319953545182),
        (0.4722710747726829, -0.881453363447582),
        (0.5272254676105024, -0.8497254299495144),
        (0.5800569095711979, -0.8145759520503358),
        (0.6305526670845228, -0.7761464642917566),
        (0.6785094115571323, -0.7345917086575332),
        (0.7237340381050701, -0.690079011482112),
        (0.7660444431189778, -0.6427876096865396),
        (0.8052702575310587, -0.5929079290546402),
        (0.8412535328311812, -0.5406408174555974),
        (0.8738493770697849, -0.4861967361004688),
        (0.9029265382866211, -0.4297949120891719),
        (0.9283679330160727, -0.37166245566032724),
        (0.9500711177409454, -0.31203344569848707),
        (0.9679487013963562, -0.2511479871810794),
        (0.9819286972627068, -0.18925124436040974),
        [2, -0.18925124436040974],
        [2, 0],
        [2, 0],
    ]

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * (len(points) - 2))
    codes.extend([Path.CLOSEPOLY])

    return Path(points, codes)


def circle_line_deprecated():
    verts = ellipse_points(0, 0, 1, 1)

    codes = [
        Path.MOVETO,
    ]
    codes.extend([Path.LINETO] * 98)
    codes.extend([Path.CLOSEPOLY])

    verts.extend(
        [
            (-2, 0),
            (2, 0),
            (-2, 0.04),
            (2, 0.04),
            (-2, -0.04),
            (2, -0.04),
        ]
    )
    codes.extend(
        [
            Path.MOVETO,
            Path.LINETO,
            Path.MOVETO,
            Path.LINETO,
            Path.MOVETO,
            Path.LINETO,
        ]
    )

    return Path(verts, codes)
