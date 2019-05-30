export FLASK_APP=run.py
log=`date +%Y-%m-%d-%H-%M-%S`.log
PYTHONIOENCODING=utf-8 nohup /root/anaconda3/envs/ir/bin/python run.py 2>&1 $log &
