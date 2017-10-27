XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
C
C  Cylindrical foil with a material couple
C
0000000000000000000000000000000000000000000000000000000000000000
SURFACE (   1)   Plane Z=0
INDICES=( 0, 0, 0, 1, 0)
Z-SHIFT=( 1.000000000000000E-10,   0)
0000000000000000000000000000000000000000000000000000000000000000
SURFACE (   2)   Plane Z=-0.1
INDICES=( 0, 0, 0, 1, 0)
Z-SHIFT=(-1.000000000000000E-01,   0)
0000000000000000000000000000000000000000000000000000000000000000
SURFACE (   3)   Cylinder, 1 cm radius
INDICES=( 1, 1, 0, 0,-1)
X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)
Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)
0000000000000000000000000000000000000000000000000000000000000000
SURFACE (   4)   Plane X=0
INDICES=( 0, 0, 0, 0, 0)
     AX=(+1.000000000000000E+00,   0)              (DEFAULT=0.0)
     A0=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)
0000000000000000000000000000000000000000000000000000000000000000
MODULE  (   1)   Right half of the sample
MATERIAL(   1)
SURFACE (   1), SIDE POINTER=(-1)
SURFACE (   2), SIDE POINTER=( 1)
SURFACE (   3), SIDE POINTER=(-1)
SURFACE (   4), SIDE POINTER=( 1)
0000000000000000000000000000000000000000000000000000000000000000
MODULE  (   2)   Left half of the sample
MATERIAL(   2)
SURFACE (   1), SIDE POINTER=(-1)
SURFACE (   2), SIDE POINTER=( 1)
SURFACE (   3), SIDE POINTER=(-1)
MODULE  (   1)
0000000000000000000000000000000000000000000000000000000000000000
END      0000000000000000000000000000000000000000000000000000000
