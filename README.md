# time-manager

A simple command line working-time logger.

## Installation

Clone the repo

```bash
$ git clone https://github.com/n-bigler/time-manager.git
```

In your `.bashrc` add

```bash
$ alias tm='python ~/path/to/time-manager/tm --path ~/path/to/logfile'
```

## Usage

To check in when you arrive at work, do

```bash
$ tm
Logged check-in at 20170612/08-00-00
```

Then, at the end of the day, simply

```bash
$ tm
Logged check-out at 20170612/18-00-00
Total working time today: 09:15 
You did 00:45 of overtime
```

You can also add modifiers if you work during a holiday or during a
half-day with the flags `--holiday` or `--half-day`. The script will reduce
the expected worktime accordingly.

## Configuration

By default, the script considers an expected worktime of 8 hours and 30 minutes
per day and a lunch break of 45 minutes. You can tweak this by modifying the
constants LUNCH_DURATION and WORKING_HOURS at the beginning of the code. 
