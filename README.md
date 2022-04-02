# ECE 474 - Project 1

Python Tomasulo algorithm sim

## How to run

```
./main.py inputFile.txt
```

## Sim Output:
```
Running simulation w/ input file: input.txt

               Busy           OP             Vj             Vk             Qj             Qk             Disp/Cycle
RS1            1, 1           0, 0           3, N           9, 9           N, 4           N, N           0, 6
RS2            1              0              N              9              4              N              2
RS3            1              0              N              9              5              N              4
RS4            1, 1           2, 2           21, 21         4, 4           N, N           N, N           1, 5
RS5            1              2              21             4              N              N              3

        RF              RAT
0:      3
1:      4
2:      12              RS1
3:      21
4:      3               RS4
5:      4
6:      9
7:      0

Instruction Queue:
Add, R2, R4, R6
Mul, R4, R3, R5

```

## Credit

Created by Andrew Voss
