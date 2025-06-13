PIDFILE="$PWD/pid"

if [ -f $PIDFILE ]; then
    echo "pid file exists...."
    PID=$(cat $PIDFILE)
    ps -ef | grep $PID | grep -v grep

    if [ $? -ne 0 ]; then
        echo "process provider not exist"
#       echo "process id: $PID"
#        kill -9 $PID
    else
        echo "process id: $PID"
        kill -9 $PID
#       echo "process provider not exist"
    fi
fi