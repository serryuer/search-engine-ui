export FLASK_APP=run.py
log=`date +%Y-%m-%d-%H-%M-%S`.log
nohup python run.py 2>&1 $log &
