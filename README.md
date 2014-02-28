django-format
=============

Django template helper, allows you to use format in template, with translation support.

Features
========

Syntax is really simple: `{% format "format base" args ... %}`,

    {% format "Hello! {user}" user=jackyyf %}

quote argument with ' or " if key or value contains spaces,

    {% format "Hello! {user}" "user=jack yyf" %}

use a variable in context,

    {% format "Hi! {user}" user=$username %}

which do the same job of "Hi! {{ username }}".  
And more, you may access attribute of a class,

    {% format "Hi! {user}" user=$request.user %}

or get an item from a dict,

    {% format "Hi! {user}" user=$request.session$username %}

of course with an int index/key,

    {% format "The second book is {bookname}." bookname=$books#1 %}

and combine them,

	{% format "The third book is {bookname}." bookname=$request.session$books#2 %}

function or callable objects also works,

    {% format "Return value of foo() is {result}" result=$foo %}

fallback to function or callable objects if function raises an exception,

    {% format "Function instance for bar(has_arg) is {instance}" instance=$bar %}

and multiple calls,

    {% format "Your email is {email}" email=$request.getUser.getEmail %}

i18n are also welcomed, just add an entry in your .po file,

    {% transformat "Good morning! {user}" user=$request.user %}

or let django add entries for you with `python manage.py makemessages` ([Patch required.](#django-patch)).

Usage
=====

Copy whole django-format directory to your project root, add django-format 
to your `INSTALLED_APPS` and `{% load format %}` to the top of your 
template, and everything should work.

Django patch
============

Since `transformat` is not standard tag, `makemessage` with django-admin.py 
or manage.py does not automaticly add entries to your .po file. You may 
use trans\_real.patch to make it so. Patch is based on django 1.6.2 and
not tested with other django release.

Donations
=========

If you find this tiny project helpful, please report bugs and feature requests, 
with issue tracker and/or pull request, or buy me a beer :)   
[![Buy me a beer!](https://www.paypal.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WV3FHKUWKBESJ)
[![请我喝一杯饮料~](https://cdn.jackyyf.me/images/alipay.png)](https://me.alipay.com/jackyyf)
