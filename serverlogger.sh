#below command for adding it to crontab
#* * * * * sh /home/<path to >/sh_files/serverlogger.sh


cd /home/<path to directory>
Process1=$(pgrep -f -x "python serverlogger.py")
if [ ! -z "$Process1" -a "$Process1" != " " ]; then
        echo "Process Running"
else
        echo "Process is not running"
	python serverlogger.py
fi

