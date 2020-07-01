
key_predic = "ysnn??????ltu_idr_aoug_iy_fptd"

for key_len in range(10, 60):
	if key_len % 2 == 0:
		continue
	key = [" " for c in range(60)]
	for i in range(0, len(key_predic)):
		tmp = key_predic[i % key_len]
		key[((8 * i) + 7) % key_len] = tmp
	print("".join(key))

# EOF
