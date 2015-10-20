#!/usr/bin/env bash

# Makes sure we exit if flock fails.
set -e
set -x

(
    # wait rfor lock for 30 sec
    flock -x -w 30 200 || exit 1

    USER="logstash"    
    DAY=$(date +"%d")
    MONTH=$(date +"%m")
    YEAR=$(date +"%Y")
    WORKDIR="/var/lib/logstash/auctions"

    FILES=$(find /var/lib/logstash/auctions -name "*[a-z0-9]-auction.log" -exec grep -il "Scheduler has been shut down" {} \;)
    echo "$FILES"
    
    for AUCTION_FILE in $FILES
    do
        echo "$AUCTION_FILE"
        aws s3 sync $WORKDIR "s3://logstash-logs-sandbox/auction/$YEAR/$MONTH/$DAY" --exclude "*" --include "$AUCTION_FILE"
        echo "$?"
        if [ "$?" -eq "0" ]; then
#            echo "deleting ${AUCTION_FILE} "|systemd-cat -t $0
            echo "deleting ${AUCTION_FILE} "|logger -t $0
            echo "deleting ${AUCTION_FILE} "
              rm -fr $AUCTION_FILE && \
            echo "successfully deleting ${AUCTION_FILE}"
            #echo "successfully deleting ${AUCTION_FILE}"|logger -t $0
        fi

        if [ "$?" -gt "0" ]; then
#            logger "can't upload $AUCTION_FILE to S3"
#            echo "can't upload $AUCTION_FILE to S3"|systemd-cat -t $0
            echo "can't upload $AUCTION_FILE to S3"|logger -t $0
            echo "can't upload $AUCTION_FILE to S3"
        fi
    done && \

	echo "Finished"

) 200>/tmp/s3_auction_upload.lock
