# Description
This is a simple python script to list and sort your EC2 instances. 

# Prerequisites
Make sure you have python and pip installed on the server. For ubuntu run 
```
apt-get install -y python2.7 python-pip
```

On Mac you should install homebrew and then run
```
sudo brew install python && sudo easy_install pip
```

# Installation and Setup

Once you have python installed, clone the respository to your local machine and update the `setup.sh` file by replacing 'YOURKEY' and 'YOURSECRET' with your AWS access id and secret key respectively. 
```
export AWS_ACCESS_KEY_ID='YOURKEY'
export AWS_ACCESS_SECRET_KEY='YOURSECRET'
```

Now simply run `source ./setup.sh` and the script will install and setup a virtualenv and download the script requirements. 

# Usage
The script options can be viewed using `./instances.py -h`

```
usage: instances.py [-h] [--region REGION] [--order-by ORDER_BY]
                    [--fields FIELDS]
                    command

positional arguments:
  command              Commands {list}

optional arguments:
  -h, --help           show this help message and exit
  --region REGION      Set the region to get instances from
  --order-by ORDER_BY  Which field should be used to order results, must be in
                       the list of fields
  --fields FIELDS      Specify fields to return in a comma seperated list.
```

The only command currently available is the `list` command. To run it simply run `./instances.py list`

```
Checking region us-west-2
+---------------------+---------+---------------------------+--------------+
| InstanceId          | Owner   | LaunchTime                | InstanceType |
+---------------------+---------+---------------------------+--------------+
| i-00007089efb1c5551 | Jim     | 2016-06-22 01:02:28+00:00 | t2.nano      |
| i-0bfc55c0abba070bd | Mark    | 2016-06-22 01:02:28+00:00 | t2.nano      |
| i-0815cf4ac3811ef04 | Unknown | 2016-06-22 01:02:28+00:00 | t2.nano      |
| i-0cb0e38cdd63d9692 | Unknown | 2016-06-22 01:02:28+00:00 | t2.nano      |
+---------------------+---------+---------------------------+--------------+
```

By default the script sorts by the "Owner" tag if it is present. You may include other tags/fields using the `--field` option and change the order using `--order-by`. For instance:

```
(env) $ ./instances.py list --fields=Name --order-by=Name

Checking region us-west-2
+---------------------+---------+---------------------------+--------------+---------------+
| InstanceId          | Owner   | LaunchTime                | InstanceType | Name          |
+---------------------+---------+---------------------------+--------------+---------------+
| i-0bfc55c0abba070bd | Mark    | 2016-06-22 01:02:28+00:00 | t2.nano      | web-db        |
| i-0815cf4ac3811ef04 | Unknown | 2016-06-22 01:02:28+00:00 | t2.nano      | web-jobrunner |
| i-0cb0e38cdd63d9692 | Unknown | 2016-06-22 01:02:28+00:00 | t2.nano      | web-memcache  |
| i-00007089efb1c5551 | Jim     | 2016-06-22 01:02:28+00:00 | t2.nano      | web-server    |
+---------------------+---------+---------------------------+--------------+---------------+
```