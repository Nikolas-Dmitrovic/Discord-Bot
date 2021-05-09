
def find_roots(a, b, c):
    rootspos = (-b+(((b**2)-(4*a*c))**(1/2)))/(2*a)
    rootsneg = (-b-(((b**2)-(4*a*c))**(1/2)))/(2*a)
    roots = (rootspos,rootsneg)
    return roots
print(find_roots(2, 10, 8))