

def check_convex_polygon(c):
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
		return False, None
	elif len(c) == pos + zer:
		return True, True
	elif len(c) == neg + zer:
		return True, False
	else:
		return False, None


def cyrus_beck(cutter, p1, p2, clockwise):
	D = get_vec(p1, p2)
	n = len(cutter)
	visible = False
	t_bot = 0
	t_top = 1

	for i in range(n):
		edge_vec = get_vec(cutter[i], cutter[(i + 1) % n])
		n_vec = get_normal_vector(edge_vec, clockwise)

		W = get_vec(cutter[i], p1)
		Dsc = mul_scal(D, n_vec)
		Wsc = mul_scal(W, n_vec)

		if Dsc == 0:
			if Wsc < 0:
				print("1")
				return visible, p1, p2
	
		t = -Wsc / Dsc

		if Dsc > 0:
			if t > 1:
				return visible, p1, p2
			else:
				t_bot = max(t_bot, t)
		if Dsc < 0:
			if t < 0:
				return visible, p1, p2
			else:
				t_top = min(t_top, t)

	if t_bot <= t_top:
		tmp = p(t_bot, p1, p2)
		p2 = p(t_top, p1, p2)
		p1 = tmp
		visible = True

	return visible, p1, p2





def get_normal_vector(vec, clockwise):
	if clockwise:
		return (-vec[1], vec[0])
	else:
		return (vec[1], -vec[0])


def get_vec(p1, p2):
	return (p2[0] - p1[0], p2[1] - p1[1])


def mul_vec(a, b):
	return a[0] * b[1] - a[1] * b[0]


def mul_scal(a, b):
	return a[0] * b[0] + a[1] * b[1]


def p(t, p1, p2):
	return (p1[0] + round((p2[0] - p1[0]) * t), p1[1] + round((p2[1] - p1[1]) * t))