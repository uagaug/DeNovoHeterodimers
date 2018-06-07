#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 1920 -dspfvs 20 -grpdly 67.9841918945312  \
  -xN           1536  -yN           6560  -zN              1  -aN              1  \
  -xT            768  -yT             80  -zT             80  -aT            200  \
  -xMODE         DQD  -yMODE     Complex  -zMODE        Real  -aMODE        Real  \
  -xSW     10416.667  -ySW      1600.000  -zSW      8000.000  -aSW     10000.000  \
  -xOBS      800.204  -yOBS       81.093  -zOBS      201.218  -aOBS      800.204  \
  -xCAR        4.677  -yCAR      118.485  -zCAR       42.640  -aCAR        4.677  \
  -xLAB           HN  -yLAB          15N  -zLAB          13C  -aLAB           1H  \
  -ndim            4  -nusDim          4  -aq2D      Complex                      \
| nmrPipe  -fn POLY -time                             \
| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5    \
| nmrPipe  -fn ZF -zf 1 -auto                         \
| nmrPipe  -fn FT                                     \
| nmrPipe  -fn POLY -auto -ord 2 -x1 11ppm -xn 6ppm   \
| nmrPipe  -fn EXT -x1 9.5ppm -xn 6.5ppm -sw -round 2 \
| nmrPipe  -fn PS -p0 22 -p1 0 -di                    \
| nusExpand.tcl -in stdin -out stdout -aqORD 0        \
              -sample nuslist -sampleCount 820       \
              -off 0 -1 0                             \
| pipe2xyz -out ft1/test%03d.ft1 -a

date

xyz2pipe -in ft1/test%03d.ft1 -x                      \
| nmrPipe  -fn SMILE -nDim 4 -nThread 32 -maxMem 480  \
           -sample nuslist -sampleCount 820 -report 2 \
           -xT 80 -yT 80 -zT 200 -thresh 0.80         \
           -off 0 -1 0 -xzf 2 -yzf 2 -zzf 1           \
| pipe2xyz -out ft1.smile/test%03d.ft1 -x

date

xyz2pipe -in ft1.smile/test%03d.ft1 -x                \
#| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 1 -c 0.5   \
| nmrPipe  -fn ZF -zf 1 -auto                         \
| nmrPipe  -fn FT                                     \
| nmrPipe  -fn PS -p0 0 -p1 0 -di                     \
| nmrPipe  -fn TP                                     \
#| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 1 -c 0.5   \
| nmrPipe  -fn ZF -zf 1 -auto                         \
| nmrPipe  -fn FT                                     \
| nmrPipe  -fn PS -p0 0 -p1 0 -di                     \
| nmrPipe  -fn TP                                     \
| nmrPipe  -fn ZTP                                    \
#| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 1 -c 0.5   \
| nmrPipe  -fn ZF -zf 1 -auto                         \
| nmrPipe  -fn FT                                     \
| nmrPipe  -fn PS -p0 0 -p1 0 -di                     \
#| nmrPipe  -fn ATP                                    \
#| nmrPipe  -fn POLY -auto -ord 2                      \
#| nmrPipe  -fn EXT -x1 9.1ppm -xn 7.2ppm -sw -round 2 \
#| nmrPipe  -fn ATP                                    \
| pipe2xyz -out ft.tmp/test%03d.ft4 -x

xyz2pipe -in ft.tmp/test%03d.ft4 -a                   \
| nmrPipe  -fn POLY -auto -ord 2                      \
| nmrPipe  -fn EXT -x1 9.1ppm -xn 7.2ppm -sw -round 2 \
| pipe2xyz -out ft/test%03d.ft4 -a

proj4D.tcl -in ft/test%03d.ft4
