


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

### Quadratic equation

$a = (u \cdot u) = \|u\|^2$ <br>
$b = 2[u \cdot (o-c)]$ <br>
$c = (o-c) \cdot (o-c) - r^2 = \|o-c\|^2 - r^2$ <br>

***

$d=\frac{-b \pm \sqrt{b^2-4ac}}{2a}$

$d=\frac{-2[u \cdot (o-c)] \pm \sqrt{(2[u \cdot (o-c)])^2-4\|u\|^2s[(o-c) \cdot (o-c) - r^2]}}{2\|u\|^2}$

*Since $u$ is a unit vector (Vec3 of length 1), $u \cdot u$ returns $1$.*

$d=\frac{-2[u \cdot (o-c)] \pm \sqrt{(2[u \cdot (o-c)])^2-4(\|o-c\|^2 - r^2)}}{2}$

***

Written with the help of Wikipedia:

Wikipedia contributors. (2026, January 1). Line–sphere intersection. In Wikipedia, The Free Encyclopedia. Retrieved 08:55, November 16, 2026, from https://en.wikipedia.org/w/index.php?title=Line%E2%80%93sphere_intersection&oldid=1330580641