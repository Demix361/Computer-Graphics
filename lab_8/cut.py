

def check_convex_polygon(self):
    c = self.cutter.coords
    neg = 0
    pos = 0
    zer = 0

    for i in range(len(c)):
    	c1 = c[i - 1]
    	c2 = c[i]
    	c3 = c[(i + 1) % len(c)]

    	vec1 = (c2[0] - c1[0], c2[1] - c1[1])
    	vec2 = (c3[0] - c2[0], c3[1] - c2[1])
    	
    	res = vec1[0] * vec2[1] - vec1[1] * vec2[0]

    	if res > 0:
    		pos += 1
    	elif res < 0:
    		neg += 1
    	else:
    		zer += 1

    if len(c) == zer:
    	return False
    elif len(c) == pos + zer:
    	return True
    elif len(c) == neg + zer:
    	return True
    else:
    	return False

    	

