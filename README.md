#scan-server#


##Requirement##
I have a old machine which I want to use it for scanning purpose. It is not attached to Monitor, Keyboard or Mouse. But runs continuously. So created this small python http server which would intialize the scanning process.


##Getting started##
The application is linux based. Hopefully you have all the necessary drivers to run command scanimage. If not there are links available to install scanimage on the linux box.

Download the git source and run 
```
python scanserver.py
```

You can use any browser to initiate the scan process. What I do is point my Android Chrome browser to http://ipaddress:9098/scan and it starts the scan process. When I am done I point my browser to http://ipaddress:9098/scanstop. All the files are scanned to priv folder in the same folder where you run the python process. Make sure the ipaddress is the on which you are running scanserver and has scanner attached.

##TODO##
Add the code to sync priv folder with google drive or dropbox. 


##Info##
The code is covered under Mozilla Public License, version 2.0.





