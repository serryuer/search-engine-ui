export FLASK_APP=run.py
log=`date +%Y-%m-%d-%H-%M-%S`.log
nohup /root/anaconda3/envs/ir/bin/python run.py 2>&1 $log &
