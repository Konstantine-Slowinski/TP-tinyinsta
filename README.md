# TP-tinyinsta

Benchmark Results Report
### Task 1: Concurrency Benchmark
| PARAM | AVG_TIME | RUN | FAILED | NB instances |
| ---   | ---      | --- | ---    | ---          |
| 1     | 81ms     | 1   | 0      | 2            |
| 1     | 71ms     | 2   | 0      | 1            |
| 1     | 66ms     | 3   | 0      | 1            |
| 10    | 74ms     | 1   | 0      | 1            |
| 10    | 72ms     | 2   | 0      | 1            |
| 10    | 70ms     | 3   | 0      | 1            |
| 20    | 80ms     | 1   | 0      | 1            |
| 20    | 76ms     | 2   | 0      | 1            |
| 20    | 76ms     | 3   | 0      | 1            |
| 50    | 154ms    | 1   | 1      | 2            |
| 50    | 130ms    | 2   | 1      | 2            |
| 50    | 137ms    | 3   | 1      | 2            |
| 100   | 271ms    | 1   | 1      | 3            |
| 100   | 164ms    | 2   | 1      | 4            |
| 100   | 246ms    | 3   | 1      | 4            |
| 1000  | 1452ms   | 1   | 1      | 20           |
| 1000  | 302ms    | 2   | 1      | 20           |
| 1000  | 344ms    | 3   | 1      | 20           |

![App Screenshot](/TEST1.jpg)

Conclusion : Cela démontre l’élasticité de GCP.
Le système subit un impact initial, mais parvient à monter jusqu’à 20 instances afin de ramener la latence à un niveau raisonnable.
Cela dit, même si le nombre d’instances augmente, le temps d’attente augmente également, ce qui indique que le système envisagé ne permettra pas de gérer des millions d’utilisateurs avec des centaines+ de followees/followers.


### Task 2: Fanout Benchmark
| PARAM | AVG_TIME | RUN | FAILED | Nb instances |
| --- | --- | --- | --- | --- |
| 20 | 170ms | 1 | 1 | 2 |
| 20 | 149ms | 2 | 1 | 2 |
| 20 | 136ms | 3 | 1 | 2 |
| 40 | 5653ms | 1 | 1 | 7 |
| 40 | 5276ms | 2 | 1 | 7 |
| 40 | 1262ms | 3 | 1 | 13 |
| 60 | 2513ms | 1 | 1 | 20 |
| 60 | 1456ms | 2 | 1 | 20 |
| 60 | 1371ms | 3 | 1 | 20 |

![App Screenshot](/TEST2.jpg)

L’augmentation du nombre de followees affecte directement et très fortement le temps de réponse des requêtes.
On observe que le nombre d’instances augmente pour gérer une charge qui, elle aussi, croît de manière exponentielle.

On peut donc penser que cette architecture, étant élastique et flexible, est capable de gérer un flux important de requêtes.
Cependant, les temps de réponse restent trop élevés et ne sont pas adaptés aux besoins d’une application comme Instagram.
