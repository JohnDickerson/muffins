from fractions import *
from math import *
from bounds_old import *

def ret_info(ub, msg="Unknown"):
        return {
                'upper_bound': ub,
                'bound_type': msg,
        }


def upper_bound(m, s):

	#Reduce m/s
	if gcd(m,s) != 1:
		return ret_info( bounds_old(int(float(m)/gcd(m,s)),int(float(s)/gcd(m,s))) )
		
	#Dual theorem
	if(s > m):
		return ret_info( bounds_old(s,m)*Fraction(m,s), "Dual" )
		
	if(min(m,s) < 6):
		return ret_info( bounds_old(m,s) )
		
	if(m == s+1):
		if(s%3 == 0):
			return ret_info( Fraction(1,3) )
		if(s%3 == 1):
			return ret_info( Fraction(2*s+1,6*s) )
		if(s%3==2):
			return ret_info( Fraction(s+1,3*s) )
		
	#The list of all [ (upper_bounds, "type_of_bound") ]
	b = []

	#Floor ceiling theorem
	b.append( (
                max(Fraction(1,3),min(Fraction(m,int(s*ceil(2*float(m)/float(s)))),1-Fraction(m,s*int(floor(2*float(m)/float(s)))))),
                  "Floor-Ceiling"
                ) )
                  
	
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
		m11 = Fraction(int(floor(V*float(sv)/float(sv1)))+(V-1-int(floor(V*float(sv)/float(sv1))))*(V-Fraction(m,s)-1)-Fraction(m,s),int(floor(V*float(sv)/float(sv1)))+(V-2)*(V-1-int(floor(V*float(sv)/float(sv1)))))
		m12 = Fraction(Fraction(m,s)-(V-1-int(ceil(V*float(sv)/float(sv1))))*(Fraction(m,s)-V+2)-int(ceil(V*float(sv)/float(sv1)))*(1-Fraction(m,s)),int(ceil(V*float(sv)/float(sv1)))*(V-1)+(V-1-int(ceil(V*float(sv)/float(sv1))))*(V-2))
		
		Q1v = min(m11,m12) if min(m11,m12) < Fraction(Fraction(1,2)-Fraction(m,s)+V-2,V-2) else 1
		#Compute Q2v
		
		#Compute MINTWO
                m21_num = Fraction(m,s) - (V-int(floor(((V-1)*float(sv1))/float(sv)))) * (1-Fraction(m,s))
                m21_denom = int(floor(((V-1)*float(sv1))/float(sv))) + (V-int(floor(((V-1)*float(sv1))/float(sv)))) * (V-1)
                if m21_denom != 0:
                        m21 = Fraction(m21_num,m21_denom)
                else:
                        m21 = Fraction(1,1)   # Loosest upper bound = 1.0

                m22_num = int(ceil((V-1)*float(sv1)/float(sv)))*(V-Fraction(m,s)-1)+(V-int(ceil((V-1)*float(sv1)/float(sv))))*Fraction(m,s)-Fraction(m,s)
                m22_denom = int(ceil((V-1)*float(sv1)/float(sv)))*(V-2) + (V-int(ceil((V-1)*float(sv1)/float(sv))))*(V-1)
                if m22_denom != 0:
                        m22 = Fraction(m22_num,m22_denom)
		else:
                        m22 = Fraction(1,1)   # Loosest upper bound = 1.0

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
		b.append( (
                        min(al),
                        "Interval-Theorem",
                        ))

        # Return the tuple with the lowest upper bound
	return ret_info( *min(b, key = lambda x: x[0]) )
