


from __future__ import division

#ces données correspondent à l'exemple dans l'article de Knuth
n=36

beta=[0]+[1,6,9,77,5,95,12,50,16,77,2,35,1,1,34,37,2,5,8,5,5,16,29,2,13,9,0,0,5,5,34,1,8,34,8,16]
alpha=[33,5,0,26,37,12,54,0,23,0,15,0,36,0,57,7,142,0,113,2,0,30,38,0,0,0,0,23,11,0,99,2,4,5,4,0,111]
words= [0]+ ['abs', 'and', 'array', 'begin', 'case', 'comment', 'div', 'do', 'else', 'end', 'false', 'for', 'go', 'goto', 'if', 'integer', 'logical', 'long', 'null', 'of', 'or', 'procedure', 'real		', 'record', 'reference', 'rem', 'result', 'short', 'step', 'string', 'then', 'to', 'true', 'until', 'value', 'while']

w=[[0 for e in range(n+1)] for e in range(n+1)]
p=[[0 for e in range(n+1)] for e in range(n+1)]
r=[[0 for e in range(n+1)] for e in range(n+1)]

d={}  #Dictionnaire qui contient les 'Rij': (noeud, fils gauche, fils droit) des sous problèmes


for i in range(n+1):
    w[i][i]=alpha[i]
    p[i][i]=alpha[i]
    r[i][i]=0
compteur=0

for length in range(1,n+1):
    for i in range(0,n-length+1):
        j=i+length
        w[i][j]=w[i][j-1]+beta[j]+alpha[j]
        if length==1: m=j
        else:
            for x in range(r[i][j-1],r[i+1][j]+1):
                compteur+=1
                if p[i][x-1]+p[x][j]==min(p[i][k-1]+p[k][j] for k in range(r[i][j-1],r[i+1][j]+1)): m=x
        p[i][j]=w[i][j]+p[i][m-1]+p[m][j]
        r[i][j]=m
        d["r"+str(i)+","+str(j)]=(m,r[i][m-1],r[m][j])
z=d
for i in range(1,37):
    for j in range(1,37):
        if 'r'+str(i)+','+str(j) not in d.keys(): d['r'+str(i)+','+str(j)]=(0,0,0)


d_words=dict()
for e in d.keys(): d_words[e]=(words[d[e][0]],words[d[e][1]],words[d[e][2]])

print("Compteur de complexite")
print(compteur)
print("")
print("Sachant que "+str(n)+"^2="+str(n**2)+": l'algorithme est on O(n2)")


def create_tree(i,j):
    dictionnaire_parents=dict()
    if d['r'+str(i)+','+str(j)][1]==0 and d['r'+str(i)+','+str(j)][2]==0: return d['r'+str(i)+','+str(j)][0];
    elif d['r'+str(i)+','+str(j)][1] == 0: return [d['r'+str(i)+','+str(j)][0],d['r'+str(i)+','+str(j)][2]];
    elif d['r' + str(i) + ',' + str(j)][2] == 0: return [d['r' + str(i) + ',' + str(j)][0], d['r' + str(i) + ',' + str(j)][1]]
    else:
        r=d['r' + str(i) + ',' + str(j)][0]
        return [r, create_tree(i,r-1),create_tree(r,j)]


def tableau_parents(l):
    tableau = dict()
    tableau[l[0]]=l[0]
    def procedure(l):
        if type(l)==type(list()) and set(type(e) for e in l)==set(type(e) for e in [1]):
            if len(l)==2: tableau[l[1]]=l[0]
            if len(l)==3: tableau[l[2]]=l[0];tableau[l[1]]=l[0]
            return d
        elif type(l)==type(list()):
            if len(l)==2:
                try: tableau[l[1][0]]=l[0]
                except: tableau[l[1]]=l[0]
            if len(l)==3:
                try :tableau[l[2][0]]=l[0]
                except: tableau[l[2]]=l[0]
                try: tableau[l[1][0]]=l[0]
                except: tableau[l[1]]=l[0]
            for i in range(1,len(l)):
                procedure(l[i])
    procedure(l)
    return tableau

print("")
print("Arbre résultant")
print(create_tree(1,n))
print("")
print("Tableau sous forme de dictionnaire  qui contient pour chaque indice i l’indice du parent ")
l=create_tree(1,n)
print(tableau_parents(l))

pr=[]
for e in words:
    if words.index(e) not in tableau_parents(l).keys(): pr.append(e)
