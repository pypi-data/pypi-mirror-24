numina-cli
=========

*A numina command line program to explore your data.*

Installing
==========

pip install numina-cli


Usage
-----

After installation run numina -h to see a list of available commands

numina

Usage:
  numina authenticate <token>
  numina counts <feeds> [--starttime=<starttime> --endtime=<endtime> --bins=<bins>]
  numina movements <feeds> [--starttime=<starttime>|--endtime=<endtime>]
  numina devices
  numina -h | --help

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --starttime=<starttime>           A RFC-3339 timestamp of query starttime, defaults to 7 days before the current time
  --endtime=<endtime>               A RFC-3339 timestamp of query endtime, defaults to the current utc time
  --bins=<bins>                     A time duration literal representing groupings of time - available bins (uµsmhdw), defaults to 1 hour

Examples:

  numina authenticate 2n3kkd3_234kn.adf&20$9u3.casdf

  numina counts dkkd20994739 --starttime=2017-06-01T15:00:00Z

  numina devices

