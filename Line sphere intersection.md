


## Equation for a circle:

$||{x-c}||^2=r^2$

$x$ : points on a sphere : *Vec3* <br>
$c$ : center point : *Vec3* <br>
$r$ : radius of sphere : *float* <br>

## Equation for a ray:

$x=o+du$

$x$ : points on ray : *Vec3* <br>
$o$ : ray origin : *Vec3* <br>
$d$ : distance from ray origin : *float* <br>
$u$ : direction of ray : *Vec3* <br>

***

### Equations combined

$||o+du-c||^2=r^2 \iff (o+du-c)\cdot(o+du-c)=r^2$

### Expanded

$[du+(o-c)]\cdot[du+(o-c)]=r^2$

$\downarrow$ *First quadratic theorem applied to* $[du+(o-c)] \cdot [du+(o-c)]$

$(du)^2+2 \cdot du \cdot (o-c)+(o-c)^2=r^2$

$\downarrow$ *Rearranged to have the form of a quadratic formula*

$d^2(u \cdot u) + d \cdot 2[u \cdot (o-c)] + (o-c) \cdot (o-c) - r^2=0$

***

$\|v\|$ means length of $v$.

$v \cdot v$ gives $\|v\|^2$

### Quadratic equation

$a = (u \cdot u) = \|u\|^2$ <br>
$b = 2[u \cdot (o-c)]$ <br>
$c = (o-c) \cdot (o-c) - r^2 = \|o-c\|^2 - r^2$ <br>

***

$d=\frac{-b \pm \sqrt{b^2-4ac}}{2a}$

$d=\frac{-2[u \cdot (o-c)] \pm \sqrt{(2[u \cdot (o-c)])^2-4\|u\|^2[(o-c) \cdot (o-c) - r^2]}}{2\|u\|^2}$

*Since $u$ is a unit vector (Vec3 of length 1), $\|u\|^2$ returns $1$. We can cancel that out.*

$d=\frac{-2[u \cdot (o-c)] \pm \sqrt{(2[u \cdot (o-c)])^2-4(\|o-c\|^2 - r^2)}}{2}$


$d=\frac{-2[u \cdot (o-c)] \pm \sqrt{4[u \cdot (o-c)]^2-4(\|o-c\|^2 - r^2)}}{2}$

*We can write $u$ as $û$, as $u$ is a unit vector.*

$\Delta = 4([û \cdot (o-c)]^2-\|o-c\|^2 + r^2)$

$d = \frac{-2[û \cdot (o-c)] \pm \sqrt{\Delta}}{2}$

*We can simplify more, by removing the denominator and halving the numerator.*

*Dividing by $4$ inside a square root is the same as dividing by $2$ outside it:*

$\nabla = (û \cdot (o-c))^2-\|o-c\|^2 + r^2$

$d = -[û \cdot (o-c)] \pm \sqrt{\nabla}$

***

Now we can find the amount of intersections based on the three cases:

- $\nabla < 0$ : No solutions $\iff$ No intersections
- $\nabla = 0$ : No solution $\iff$ One intersection
- $\nabla > 0$ : Two solutions $\iff$ Two intersections

***

Written in code:

```
nabla = (Vec3.dot(u,o-c))**2 - (o-c).lengthSquared() + r**2
if nabla == 0:
	d = -Vec3.dot(u,o-c)
elif nabla > 0:
	d = -Vec3.dot(u,o-c) - sqrt(nabla)
	dFurthest = -Vec3.dot(u,o-c) + sqrt(nabla)
```
***

Written with the help of Wikipedia:

Wikipedia contributors. (2026, January 1). Line–sphere intersection. In Wikipedia, The Free Encyclopedia. Retrieved 08:55, November 16, 2026, from https://en.wikipedia.org/w/index.php?title=Line%E2%80%93sphere_intersection&oldid=1330580641