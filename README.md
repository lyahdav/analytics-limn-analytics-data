# Usage
```
 ./phab-stats --config ./phab-stats-config.json  2015-09-01 2016-01-01
```
# To install 

We have seen issues with phabricator 0.0.5 in linux
and phabricator 0.0.4 in mac. Currently we require version 0.0.4
but please see below of Mac OS X instructions.


## Mac OS X
## Install python libs

```
    sudo pip  install -r ./requirements.txt
```
If lxml gives trouble, uninstall and install again.

Please see issue: https://github.com/disqus/python-phabricator/issues/22
You need phabricator 0.0.5 to workarround it

## Install archanist

See guide here: https://gist.github.com/potench/68d48757d0d56842946a

## Install Certificates

Installing certificates should bring up a prompt for you to enter a token:
```
>arc install-certificate https://phabricator.wikimedia.org

CONNECT  Connecting to "https://phabricator.wikimedia.org/api/"...
LOGIN TO PHABRICATOR
Open this page in your browser and login to Phabricator if necessary:

https://phabricator.wikimedia.org/conduit/login/

Then paste the API Token on that page below.

    Paste API Token from that page: cli-blah
Writing ~/.arcrc...
 SUCCESS!  API Token installed.
```
DONE! You should be able to run the script
