# Broker Packager

Package Manager based on broker messages

## Install

    pip install brokerpackager

## Usage

    broker-packager monitor -e 'localhost' -p 61613 -s "Email = 'email@email.com'" -d '/topic/test' -p 'raw.request.body.python' -r 'raw.request.body.r'

Or 

    broker-packager install -l python -n notebook