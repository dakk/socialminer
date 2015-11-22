socialminer
===

Peer-to-peer search and report for social accounts related to the ISIS. The search is based on a dictionary of suspicious keywords, results are not 
guaranteed to be reliable. The software automatically connect to a peer-to-peer network of social miners: miners exchange account reports for creating 
a distributed database.


You can help the development of this software and the deploy of report servers by donating BTC to: **129k6fDTd66j1LMY5RAdFSQozeBe58nfxE**

Installation
---

First you need to install requirements:

```git clone https://github.com/pythonforfacebook/facebook-sdk.git && cd facebook-sdk && sudo python3 setup.py install```


Then clone the socialminer repository:

```git clone https://github.com/dakk/socialminer```

Install the software:

```cd socialminer && sudo python3 setup.py install```


Configuration
---
Start socialminer for the first time:

``` socialminer ```

Socialminer will create an empty configuration file 'socialminer.json' in your current directory.


Configure Peer-to-peer network
---
Socialminer allows you to customize your p2p port, or insert new seed node in the form "host:port" (by editing 'socialminer.json').


Configure Twitter
---
Go to https://apps.twitter.com/, create a new application.
Go to 'Keys and Access Tokens' tab, press on 'Generate Access Token'; edit 'socialminer.json' and put all the request data in the empty fields.


Configure Facebook
---
Go to https://developers.facebook.com/tools/explorer/ and get a temp access token, or register a new facebook application. Edit 'socialminer.json'
and put the access token in the empty field.


Start socialminer
---
To start the socialminer instance after its configuration, type:

``` socialminer ```

The program will create a file **reports_Facebook.json** and **reports_Twitter.json** with all found accounts and relevant resources. It also
maintein a local database **reports.db**




TODO
---
The software is still work in progress, planned features are:
- A more robust search crtieria
- Integration of other social networks
- Auto report on social network



