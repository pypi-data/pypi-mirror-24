=======
History
=======

0.8.0 (2017-09-01)
------------------

* Move project to gitlab
* Add support for emails with payload encoded in base64
* Improve handling of email with special characters sent from stdin
* Normalize file names before save
* Can use subject in file name
* Can choose not to save the file
* Can extract HTML from the mail
* Add support for ``-t`` option. This is useful if the dots of the mail are escaped before being sent to the script, ie a dot (``.``) at the start of a line is replaced by two dots (``..``).

0.5.0 (2017-07-26)
------------------

* Add an option to print the version
* Don't print traceback when quitting the "readline" version with CTRL-C
* Can use a template for the file


0.4.0 (2017-07-10)
------------------

* Can choose the name of the file in which to save.


0.3.0 (2017-07-06)
------------------

* Don't fail if script receive undefined option. It is important to act as a
  replacement for sendmail. Some program will try to call it with custom options.
* Include LICENSE and HISTORY.rst in release made to pypi.
* Add a single file version so users don't have to install mailsave with pip.


0.2.0 (2017-07-05)
------------------

* Can read mail from SMTP.


0.1.0 (2017-07-05)
------------------

* Can act as a replacement of sendmail.
