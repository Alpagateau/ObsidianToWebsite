#algebra
Une application $f$ est dite linéaire ssi $f(\lambda u + v) = \lambda f(u) + f(v)$.
L'[[Ensembles|ensemble]] des applications linéaire de $E$ vers $F$ se note $\mathcal{L}(E, F)$.
Si $f$ est définie de $E$ vers $E$ , on l'appel un **endomorphisme**. L'ensemble des endomorphismes est noté $\mathcal{L}(E)$ 
Si $f$ est bijective, on l'appel un **isomorphisme**.
Un **automorphisme** est a la fois un endomorphisme et un isomorphisme.

>L'[[Ensembles|ensemble]]  de tous les automorphismes dans $E$  est noté  $GL(E)$ ![[Preuve GL est un groupe|preuve]]

## Operations
Soient $f$ et $g$ deux applications linéaires, alors $(\alpha f + g)$ est une application linéaire.
De plus $f \circ g$ est une application linéaire. 
Si $f$ est un isomorphisme, on note $f^{-1}$ son isomorphisme réciproque. 

## Image et noyau
L'**image** d'une application linéaire par un ensemble est l'ensemble de toutes les valeurs atteinte par l'application depuis cet ensemble. En language mathématique on écrit :
$$
Im(f) = \{f(u), u \in E \} = f(E)
$$
Le **noyau** est l'ensemble des valeurs qui, donné a une application, retourne l'élément neutre.
$$
Ker(f) = \{u, u \in E, f(u) = 0\} = f^{-1} (\{0_F \})
$$

On a que $Im(f)$ est un [[Espace vectoriel#^48cd3c|SEV]] de $F$ et $Ker(f)$ est un SEV de $E$. 

> 1. $f$ est injective ssi $Ker(f) = \{0_E\}$
> 2. $f$ est surjective ssi $Im(f) = F$
> 3. $f$ est un isomorphisme ssi $Ker(f) = \{0_E\}$ et $Im(f) = F$

## Applications Linéaires Particulières

- Une **homothétie** est une multiplication par un scalaire.
- Une **projection** envoies les éléments de deux SEV complémentaires sur un seul. 
- Une **symétrie** est une symétrie par rapport a l'un de deux SEV complémentaires.

On a qu'une **projection** est idempotent. Tout endomorphisme idempotent est une projection. 
Si $p$ est une projection de $E$, alors $E = Ker(p) \oplus Im(p)$  

Une **symétrie** est une involution ($s \circ s = Id_E$). On a aussi $s^{-1} = s$. 

## Théorème du rang
$$
dim(E) = dim(Ker(f)) + rg(f)
$$

## Représentation matricielle
Il est commun de représenter les applications linéaires par des [[Matrices|matrices]]. En effet, la multiplication matricielle de représenter les applications linéaires. De plus, si la matrice associé a une application est inversible, alors cette application est bijective. 

## Multi-linéarité
Soit une application $f$ de $E$ dans $F$, avec $E$ une ensemble de n-uplets. On dit que $f$ est multilinéaire ssi :
$$
f(\mu x_1, \lambda x_2 ... x_n) = \mu \lambda f(x_1, x_2,..., x_n)
$$