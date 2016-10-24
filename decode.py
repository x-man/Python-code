import string
n = string.digits
import hashlib

def sha512(x):
    m = hashlib.sha512()
    m.update(x)
    return m.hexdigest()

for i1 in n:
	for i2 in n:
		for i3 in n:
			for i4 in n:
				for i5 in n:
					for i6 in n:
						for i7 in n:
							for i8 in n:
								s = 'TSCTF{lifeisliar_'+str(i1)+str(i2)+str(i3)+str(i4)+str(i5)+str(i6)+str(i7)+str(i8)+'}'
								tmp = sha512(s)
								if tmp == '3ee56ca06fc611f93e5bb5af155a5674f7da2eb6116f338a519bbab313a0ccc0f6158b99814e0f5e62970af3d4b32ae187c8a7c8e920bdd550ca19f94b45662a':
									print s
