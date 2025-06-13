PIDFILE="$PWD/pid"

if [ -f $PIDFILE ]; then
    echo "pid file exists...."
    PID=$(cat $PIDFILE)
    ps -ef | grep $PID | grep -v grep

    if [ $? -ne 0 ]; then
        echo "process provider not exist"
    else
        echo "kill process group: $PID"
        kill -9 -$PID
    fi
fi