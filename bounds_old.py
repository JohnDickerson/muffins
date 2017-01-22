from fractions import *
from math import *

# This code was initially written by Naveen D
# https://github.com/ndurvasula
# Thanks to him!

#Currently assuming m, s are natural numbers
def bounds_old(m, s):
    global fl

    s=int(s); m=int(m)

    msg = ""
    lb = 0
    #Easy cases (Theorem 0.1)
    if m%s == 0:
        #return "f("+str(m)+", "+str(s)+") = 1 (Easy)\n"
        return 1.
    if int(float(s)/float(m)) == float(s)/float(m):
        #return "f("+str(m)+", "+str(s)+") = "+str(Fraction(m,s))+" (Easy)\n"
        return float(m)/float(s)
    if s%(2.0*m) == 0 and int(float(m)/float(s)) != float(m)/float(s):
        #return "f("+str(m)+", "+str(s)+") = 1/2 (Easy)\n"
        return 0.5
    if m == 1 or (s%2 == 1 and m == 2):
        #return "f("+str(m)+", "+str(s)+") = 1/"+str(s)+" (Easy)\n"
        return 1.0/float(s)
    if (s%2 == 0) and float(m)/(float(s)/2.0)%2 == 1:
        #return "f("+str(m)+", "+str(s)+") = 1/2 (Easy)\n"
        return 0.5

    #Not an easy case - find UBs then see if they match the LBs

    #Assume f(m,s) > 1/3 and find floor ceiling UB
    fl = []
    pl = []
    
    #Check if floor ceiling method can be applied
    if floor(2.0*float(m)/float(s)) != 0 and \
       min([Fraction(m,s*int(ceil(2.0*float(m)/float(s)))),1-Fraction(m,s*int(floor(2.0*float(m)/float(s))))]) > Fraction(1,3):
        fl.append(min([Fraction(m,s*int(ceil(2.0*float(m)/float(s)))),1-Fraction(m,s*int(floor(2.0*float(m)/float(s))))]))
    else:
        fl.append(1)
    pl.append("")
    #Check if share theorem can be applied
    if floor(2*m/s) != 0 and \
       min([Fraction(1,int(ceil(2.0*float(m)/float(s)))),1-Fraction(1,int(floor(2.0*float(m)/float(s))))]) > Fraction(m,3*s):
        fl.append(min([Fraction(1,int(ceil(2.0*float(m)/float(s)))),1-Fraction(1,int(floor(2.0*float(m)/float(s))))]))
    else:
        fl.append(1)
    pl.append("")
    #Moderate Half
    rl = []
    vhl = []
    for V in range(3,m+1):
        for h in range(V):
            if V==3:
                q11 = 0
                q12 = 0
            else:
                q11 = min(Fraction(m,(V-2)*s),1-Fraction(m,s*V-2))
                q12 = 1-Fraction(m,s*(V-3))

            sv = 2*m-V*s+s
            sv1 = V*s - 2*m
            q2 = min(Fraction(Fraction(m,s)-Fraction(Fraction(m,s)-Fraction(h,2),V-h+1),V-2),1-Fraction(Fraction(m,s)-Fraction(h,s),V-h+1))
            q3 = min(Fraction(m,s)-(1-Fraction(Fraction(m,s)-Fraction(h,2),V-h)),Fraction(Fraction(m,s)-(1-Fraction(Fraction(m,s)-Fraction(h,2),Fraction(V-h))),V-2))
            
            if sv <= -1 or sv1 <= -1:
                rl.append(max(Fraction(1,3),Fraction(m,(V+1)*s),q11,q12))
                vhl.append([V,h,sv,sv1])

            if sv1 >= 0 and sv >=0 and m < sv1*(V-h):
                rl.append(max(Fraction(1,3),Fraction(m,(V+1)*s),q11,q12,q2))
                vhl.append([V,h,sv,sv1])

            if sv1 >= 0 and sv >=0 and m < sv*(V-h+1):
                rl.append(max(Fraction(1,3),Fraction(m,(V+1)*s),q11,q12,q3))
                vhl.append([V,h,sv,sv1])
            
            
    #Moderate UB theorems
    al = []
    intl = []
    vl = []
    for V in range(3,m+1):
        if V == 3:
            q11 = 0
            q12 = 0
        else:
            q11 = min([Fraction(m,(V-2)*s),1-Fraction(m,s*(V-2))])
            q12 = 1-Fraction(m,s*(V-3))
        a = 2*m-V*s+s
        b = V*s-2*m
        if (a<= -1 or b <=-1) or \
           (a == 0 and b*(V-1) != 2*m) or \
           (b == 0 and a*V != 2*m):
            al.append(max([Fraction(1,3), \
                           Fraction(m,(V+1)*s), \
                                    q11, \
                                    q12]))
        elif (a == 0 and b*(V-1) == 2*m) or \
           (b == 0 and a*V == 2*m):
            return str(V)+" BLUEFLAG"
        else:
            qst = max([Fraction(Fraction(2*m,s)-1,2*(V-1)), \
                       Fraction(Fraction(Fraction(m,s),int(ceil(float(a)*float(V)/float(b))))-1+Fraction(m,s),V-1)])
            if a >= 1 and b >= 1:
                intl.append(max([Fraction(1,3), \
                                 Fraction(m,(V+1)*s), \
                                 q11, \
                                 q12, \
                                 qst]))
                vl.append([V,a,b])
            q2 = min([Fraction(Fraction(m,s)-Fraction(Fraction(m,s)-Fraction(1,2),V-2),V-2), \
                      1-Fraction(Fraction(m,s)-Fraction(1,2),V-2)])
            q3 = min([Fraction(m,s)-(1-Fraction(Fraction(m,s)-Fraction(1,2),V-2)), \
                      Fraction(Fraction(m,s)-(1-Fraction(Fraction(m,s)-Fraction(1,2),V-2)),V-1)])
            if m < b*(V-1) and m < a*V:
                return str(V) + " REDFLAG"
            elif m < b*(V-1):
                al.append(max([Fraction(1,3), \
                               Fraction(m,(V+1)*s), \
                               q11, \
                               q12, \
                               q2]))
            elif m < a*V:
                al.append(max([Fraction(1,3), \
                               Fraction(m,(V+1)*s), \
                               q11, \
                               q12, \
                               q3]))
    if m/s > 1:
        fl.append(min(rl))
        fl.append(min(intl))
        pl.append("V = "+str(vhl[rl.index(min(rl))][0])+", h = "+str(vhl[rl.index(min(rl))][1])+", sv = "+str(vhl[rl.index(min(rl))][2])+", s(v-1) = "+str(vhl[rl.index(min(rl))][3]))
        pl.append("V = "+str(vl[intl.index(min(intl))][0])+", a = "+str(vl[intl.index(min(intl))][1])+", b = "+str(vl[intl.index(min(intl))][2]))
    else:
        fl.append(1)
        fl.append(1)
        pl.append("")
        pl.append("")
    

    #Small theorems UB
    s1 = []
    s2 = []
    ps1 = []
    ps2 = []
    
    for U in range(2,s+1):

        #Get Q
        ql = []
        for j in range(2,U):
            ql.append(min([Fraction(1,j), \
                            Fraction(m,s)-Fraction(1,j)]))

        #Check if length > 0
        if len(ql) == 0:
            q = 0
        else:
            q = max(ql)

        #Small NOT theorem
        if 2*s != U*m:
            s1.append(max([Fraction(1,U+1), \
                           q, \
                           Fraction(m,3*s)]))
            ps1.append(U)

        #Small ABBA theorem

        if U >= 3:

            #Get Q

            #Check if length > 0
            if len(ql) < 2:
                q = 0
            else:
                q = max(ql[:-1])

            #Get a and b
            a = 2*s + m - m*U
            b = m*U - 2*s

            #Case 1
            if a <= -1 or b <= -1:
                s2.append(max([Fraction(1,U+1), \
                               q, \
                               Fraction(m,3*s)]))
                ps2.append([U,a,b])


            #Case 2
            if a >= 0 and b >= 0 and a*U <= b*(U-1) - 2:
                 s2.append(max([Fraction(1,U+1), \
                                q, \
                                Fraction(m, 3*s), \
                                Fraction(m,s) - Fraction(1-Fraction(m,2*s),U-2)]))
                 ps2.append([U,a,b])


            #Case 3
            if a >= 0 and b >= 0 and b*(U-1) <= a*U - 2:
                s2.append(max([Fraction(1,U+1), \
                               q, \
                               Fraction(m,3*s), \
                               Fraction(1-Fraction(m,2*s),U-1)]))
                ps2.append([U,a,b])


    #Check if length > 0
    if len(s1) > 0:
        fl.append(min(s1))
    else:
        fl.append(1)
    pl.append("U = "+str(ps1[s1.index(min(s1))]))
    fl.append(min(s2))
    pl.append("U = "+str(ps2[s2.index(min(s2))][0])+", a = "+str(ps2[s2.index(min(s2))][1])+", b = "+str(ps2[s2.index(min(s2))][2]))
    #Small U=3 theorem A UB

    a = 2*s - 2*m
    b = 3*m - 2*s

    #Solution set of the d,e,f system
    S = []
    for d in range(a+1):
        for e in range(a+1):
            for f in range(a+1):
                if d+e+f == a and 2*d+e == 2*b:
                    S.append((d,e,f))

    #Case 0
    if a <= -1 or b <= -1:
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s)))
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)

    #Case 1
    elif a < Fraction(2*b,3):
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      Fraction(3*m,2*s)-1))
        fl.append(1)
        fl.append(1)
        fl.append(1)

    #Case 2
    elif a < b or len(S) == 0:
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      Fraction(3*m,2*s)-1, \
                      Fraction(2*m,s) - Fraction(4,3)))
        fl.append(1)
        fl.append(1)

    #Case 3
    elif len(list(filter(lambda x: x[0] > 2*x[1] + 3*x[2], S))) == len(S):
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      Fraction(3*m,2*s)-1, \
                      Fraction(2*m,s)-Fraction(4,3), \
                      Fraction(9*m,4*s)-Fraction(3,2)))
        fl.append(1)

    #Case 4
    elif 2*b == 3*a - 4:
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      Fraction(3*m,2*s)-1, \
                      Fraction(9*m,4*s)-Fraction(3,2), \
                      1-Fraction(m,s)))

    else:
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)

    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))

    #Small U=3 theorem B
    a = 2*s - 2*m
    b = 3*m - 2*s

    #Case 0
    if a <= -1 or b <= -1:
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s)))
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)

    #Case 1
    elif b < Fraction(3*a,2):
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      min(Fraction(m,2*s),\
                          Fraction(1-Fraction(m,2*s),2))))
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)

    #Case 2
    elif b < 3*a:
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      min(Fraction(m,2*s), \
                          Fraction(1-Fraction(m,2*s),2)),\
                      Fraction(3,4)-Fraction(m,2*s)))
        fl.append(1)
        fl.append(1)
        fl.append(1)

    #Case 3
    elif b == 3*a+1:
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      min(Fraction(m,2*s), \
                          Fraction(1-Fraction(m,2*s),2)),\
                      Fraction(3,4)-Fraction(m,2*s), \
                      min(Fraction(5,4)-Fraction(m,s),\
                          Fraction(2*m,s)-Fraction(3,2))))
        fl.append(1)
        fl.append(1)

    #Case 4
    elif b < Fraction(9*a,2):
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      min(Fraction(m,2*s), \
                          Fraction(1-Fraction(m,2*s),2)),\
                      Fraction(3,4)-Fraction(m,2*s), \
                      min(1-Fraction(3*m,4*s),\
                          Fraction(3*m,2*s)-1)))
        fl.append(1)

    #Case 5
    elif b< 6*a:
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(max(Fraction(1,4), \
                      Fraction(m,3*s), \
                      min(Fraction(m,2*s), \
                          Fraction(1-Fraction(m,2*s),2)),\
                      Fraction(3,4)-Fraction(m,2*s), \
                      min(1-Fraction(3*m,4*s),\
                          Fraction(3*m,2*s)-1),\
                      min(Fraction(5,4)-Fraction(m,s),\
                          Fraction(2*m,s)-Fraction(3,2))))

    else:
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)
        fl.append(1)

    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
    pl.append("a = "+str(a)+", b = "+str(b))
        

    thml = ["Floor Ceiling",\
            "Share",\
            "Moderate Half", \
            "Moderate Interval",\
            "Small NOT",\
            "Small ABBA",\
            "Small U3 0a",\
            "Small U3 1a",\
            "Small U3 2a",\
            "Small U3 3a",\
            "Small U3 4a",\
            "Small U3 0b",\
            "Small U3 1b",\
            "Small U3 2b",\
            "Small U3 3b",\
            "Small U3 4b",\
            "Small U3 5b"]
        
    
    #Make sure we use the tightest UB
    f = min(fl)
    p = pl[fl.index(f)]

    return f
    

    
    
    
