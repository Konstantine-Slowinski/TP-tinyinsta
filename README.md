# TP-tinyinsta

Benchmark Results Report
Task 1: Concurrency Benchmark
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



Conclusion : Cela démontre l’élasticité de GCP. 
Le système a subi un impact initial, mais a réussi à monter jusqu’à 20 instances pour ramener la latence à un niveau raisonnable.

Ceci dit, meme si le nombre d'instances augmente, le temps d'attente augmente aussi, qui nous indique que le systeme envisagé ne permettera pas la géstion de millions de users, avec des centaines+ followees/followers.
