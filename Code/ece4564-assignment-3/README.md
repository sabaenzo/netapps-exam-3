# ece4564-assignment-3

### List of libraries
- Flask
  - Used for creating a flask server to handle HTTP requests
- Regex
  - Used for regular expression matching
- Requests
  - Used for making HTTP requests
- Socket
  - Used for making socket connections
- Zeroconf
  - Used for zeroconf connection
- Pymongo
  - Used for communication with a MongoDB instance


### Quickstart

To download a Canvas file:

`curl -u <user>:<pass> 'http://0.0.0.0:<port>/Canvas?file=<file_id>&operation=download'`

To upload a Canvas file

`curl -X POST -u <user>:<pass> 'http://0.0.0.0:<port>/Canvas?file=<file_path>&operation=upload'`

To get current LED status:

`curl -u <user>:<pass> 'http://0.0.0.0:<port>/LED'`

To change current LED status:

`curl -X POST -u <user>:<pass> 'http://0.0.0.0:<port>/LED?command=on-red-100'`      <------- example of turning red led on at 100 intensity
