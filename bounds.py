from fractions import *
from math import *
from bounds_old import *

def upper_bound(m, s):

	#Reduce m/s
	if gcd(m,s) != 1:
		return bounds_old(int(m/gcd(m,s)),int(s/gcd(m,s)))
		
	#Dual theorem
	if(s > m):
		return bounds_old(s,m)*Fraction(m,s)
		
	if(min(m,s) < 6):
		return bounds_old(m,s)
		
	if(m == s+1):
		if(s%3 == 0):
			return Fraction(1,3)
		if(s%3 == 1):
			return Fraction(2*s+1,6*s)
		if(s%3==2):
			return Fraction(s+1,3*s)
		
	#The list of all bounds
	b = []

	#Floor ceiling theorem
	b.append(max(Fraction(1,3),min(Fraction(m,int(s*ceil(2*m/s))),1-Fraction(m,s*int(floor(2*m/s))))))
	
	#List of all ANSv for all V
	al = []
	flag = False;
	for V in range(3,m+1):
		
		#Compute Sv and Sv-1
		sv = 2*m-V*s+s
		sv1 = V*s-2*m
		
		#Easy case
		if sv <= -1 or sv1 <= -1 or Fraction(V-2,2*V-3) >= min(Fraction(m,sv),Fraction(V-1-Fraction(m,s),V-1)):
			al.append(max(Fraction(1,3), Fraction(m,s*(V+1)), 1-Fraction(m,s*(V-2))))
			continue
		
		#Hard case
	
		#Compute Q1v
		
		#Compute MINONE
		m11 = Fraction(int(floor(V*sv/sv1))+(V-1-int(floor(V*sv/sv1)))*(V-Fraction(m,s)-1)-Fraction(m,s),int(floor(V*sv/sv1))+(V-2)*(V-1-int(floor(V*sv/sv1))))
		m12 = Fraction(Fraction(m,s)-(V-1-int(ceil(V*sv/sv1)))*(Fraction(m,s)-V+2)-int(ceil(V*sv/sv1))*(1-Fraction(m,s)),int(ceil(V*sv/sv1))*(V-1)+(V-1-int(ceil(V*sv/sv1)))*(V-2))
		
		Q1v = min(m11,m12) if min(m11,m12) < Fraction(Fraction(1,2)-Fraction(m,s)+V-2,V-2) else 1
		#Compute Q2v
		
		#Compute MINTWO
		m21 = Fraction(Fraction(m,s)-(V-int(floor(((V-1)*sv1)/sv)))*(1-Fraction(m,s)),int(floor(((V-1)*sv1)/sv))+(V-int(floor(((V-1)*sv1)/sv)))*(V-1))
		m22 = Fraction(int(ceil((V-1)*sv1/sv))*(V-Fraction(m,s)-1)+(V-int(ceil((V-1)*sv1/sv)))*Fraction(m,s)-Fraction(m,s),int(ceil((V-1)*sv1/sv))*(V-2)+(V-int(ceil((V-1)*sv1/sv)))*(V-1))
		
		Q2v = min(m21,m22) if min(m21,m22) < Fraction(Fraction(m,s)-Fraction(1,2),V-1) else 1
		#Compute Q3v
		Q3v = Fraction(V-Fraction(m,s)-Fraction(3,2),V-2) if V*sv != (V-1)*sv1 else 1
		
		#Compute Q4v
		Q4v = Fraction(Fraction(m,s)-Fraction(1,2),V-1) if V*sv != (V-1)*sv1 else 1

		#Compute Qv
		Qc = [Q1v, Q2v, Q3v, Q4v]
		
		Qc.sort()
		Qv = 1
		for i in range(4):
			TempQv = Qc[i]
			if Fraction(V-2,2*V-3) < TempQv and TempQv < min(Fraction(m,sv),Fraction(V-1-Fraction(m,s),V-1)):
				Qv = TempQv
				flag = True
				break
		
		#Compute ANSv
		al.append(max(Fraction(1,3),Fraction(m,s*(V+1)),1-Fraction(m,s*(V-2)),Qv))

	if flag:
		b.append(min(al))

	return min(b)
