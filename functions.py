import numpy as np

def point_inside_polygon(x,y,poly):	# Ex.: a=[(0,0),(0,2),(1,1),(1,0)] if x=0.4 y=1.2 function gives "True" if x=0.8 y=1.8 function gives "False"
	n = len(poly)
	inside =False
	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y
	return inside

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin();
	return array[idx]

def get_ellipse_coords(a=0.0, b=0.0, x=0.0, y=0.0, angle=0.0, k=2):
    """ Draws an ellipse using (360*k + 1) discrete points; based on pseudo code
    given at http://en.wikipedia.org/wiki/Ellipse
    k = 1 means 361 points (degree by degree)
    a = major axis distance,
    b = minor axis distance,
    x = offset along the x-axis
    y = offset along the y-axis
    angle = clockwise rotation [in degrees] of the ellipse;
        * angle=0  : the ellipse is aligned with the positive x-axis
        * angle=30 : rotated 30 degrees clockwise from positive x-axis
    """
    pts = np.zeros((360*k+1, 2))

    beta = -angle * np.pi/180.0
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    alpha = np.radians(np.r_[0.:360.:1j*(360*k+1)])
 
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    
    pts[:, 0] = x + (a * cos_alpha * cos_beta - b * sin_alpha * sin_beta)
    pts[:, 1] = y + (a * cos_alpha * sin_beta + b * sin_alpha * cos_beta)

    return pts


def ellipse(Au,Av,PHIu,PHIv):
	# Assume the input phase lags are in degrees and convert them in radians.
	PHIu = PHIu/180*np.pi
	PHIv = PHIv/180*np.pi


	# Make complex amplitudes for u and v
	u = 1.0001*Au*np.exp(-1j*PHIu)
	v = 1.0001*Av*np.exp(-1j*PHIv)

	# Calculate complex radius of anticlockwise and clockwise circles:
	wp = (u+1j*v)/2     	 #for anticlockwise circles
	wm = np.conj(u-1j*v)/2	 #for clockwise circles


	# and their amplitudes and angles
	Wp = np.abs(wp)
	Wm = np.abs(wm)
	THETAp = np.angle(wp)
	THETAm = np.angle(wm)

	   
	# calculate ep-parameters (ellipse parameters)
	SEMA = Wp+Wm              # Semi  Major Axis, or maximum speed
	SEMI = Wp-Wm              # Semin Minor Axis, or minimum speed
	ECC = SEMI*1.0001/SEMA          # Eccentricity

	PHA = (THETAm-THETAp)/2   # Phase angle, the time (in angle) when 
		                       # the velocity reaches the maximum
	INC = (THETAm+THETAp)/2   # Inclination, the angle between the 
		                       # semi major axis and x-axis (or u-axis).


	# convert to degrees for output
	PHA = PHA/np.pi*180         
	INC = INC/np.pi*180         
	THETAp = THETAp/np.pi*180
	THETAm = THETAm/np.pi*180

	return SEMA,SEMI,INC

