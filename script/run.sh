cd ../fm
make
cd ../gbdt
make
cd ../script

pypy addc.py
pypy fcount.py
pypy rare.py
pypy id_day.py
pypy prep.py
pypy id_stat.py
pypy gbdt_dense.py
pypy index1.py
pypy index2.py
../gbdt/gbdt -d 5 -t 19 ../test_dense ../train_dense ../test_gbdt_out ../train_gbdt_out

# fm model 1
pypy append_gbdt.py
../fm/fm -k 8 -t 5 -l 0.00003 ../fm_test_2 ../fm_train_2

# fm model 2
pypy append_gbdt_1.py
../fm/fm -k 8 -t 4 -l 0.00004 ../fm_test_2_1 ../fm_train_2_1
../fm/fm -k 8 -t 10 -l 0.00005 ../fm_test_2_2 ../fm_train_2_2
pypy split.py ../fm_test_2_split ../fm_test_2_1.out ../fm_test_2_2.out

# ftrl model prepare
pypy prep_1.py
pypy append.py
pypy genDict.py
pypy genM.py
python lsa.py

# ftrl model 1
pypy ftrl_1.py

# ftrl model 2
pypy ftrl_2.py

# ensemble
pypy ensemble.py