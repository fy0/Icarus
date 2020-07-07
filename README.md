# Icarus

![](misc/screenshot.png)

> A opensource forum project write with python3 and vue.js

[More screenshots (old version)] (SCREENSHOT.md)

[During the 2.0 branch development, see the roadmap here] (https://t.myrpg.cn/topic/2827)

### NOTE

The current master branch has merged parts of 2.0, which is actually equivalent to the SSR version of 1.3.

This branch will temporarily not add new features, only for BUG maintenance. Function development will be carried out in the 2.0 branch.

This version will not be released separately, please report back in time if you have any bugs, thank you.


## How to deploy

More content, see [deployment document](misc/how-to-deploy.md)


## Open source agreement

[ZLIB](LICENSE)

Free and business friendly, this agreement is basically the same as MIT.


## Features

* Global

    * File upload (Qiniu Cloud)

    * Ultra widescreen support

    * Simple mobile support

    * Real-time online number

    * Markdown posts and comments

    * Full-text search with topics, comments, encyclopedia content (based on Elasticsearch)

* User system

    * register log in

    * Mail activation

    * Retrieve password by email

    * edit personal information

    * Upload avatar (Seven Cow Cloud)

    * Daily check-in

    * Personal reminder

* Forum

    * Flat content display

    * Create and manage sections

    * Plate theme color

    * Post and edit topics

    * The article page automatically generates quick navigation

    * @Features

* Encyclopedia

    * Customize sidebar and homepage

    * Article creation and editing

    * List of all articles

    * Article history

    * Random pages

* Management background

    * Provide management of sections, topics, users and comments

    * Management log

* Security Mechanism

    * The front-end password is encrypted, and the back-end does not obtain the user's initial password, which minimizes the harm of man-in-the-middle attacks and database leaks

    * Secondary back-end encryption, sha512 plus salt iterates 100,000 times to store user password

    * Password-related APIs are all explosion-proof, and IP request interval and account request interval can be set to increase the difficulty of batch database collision and single-point blasting, respectively

    * Privacy data, such as IP addresses can be stored in the database after desensitization

## Upgrade Guide

First stop the service and update the source code.

Then please look for the corresponding upgrade file in the `backend/misc/upgrade` directory, for example 1.2 upgrade 1.3 use `u12-u13.py`.

It can be deleted after executing in the `backend` directory.

Note that if pipenv or other virtual environment is used, this operation should be done in the environment corresponding to the project.

Then upgrade the project dependencies of the front-end project (root directory) and back-end project (backend directory) respectively.

If there is no special upgrade instructions for this version, just restart the service at this time.



## Planning

Due to limited free time, and the development of the entire project alone.

The current version still has some imperfections and missing features that are too late to complete. Let me plan as follows:

Recently:

* Collection, thanks, likes

* Personal Center

* Enhance mobile experience

* Support users to delete and edit comments

Follow-up:

* Multi-terminal simultaneous login support

* Support third-party login

* Build an independent project site

* RSS support

* Improve tests


## Donate

In the process of developing this project, I paid a lot of time and energy. Hope this project can help everyone, or you can like this project.

This is already a good affirmation for me, please be sure to order a star to let me know.

I also welcome donations to support my development:

<img src="http://wx3.sinaimg.cn/large/007474KTgy1fxcni97ntdj30u00u00x2.jpg" width=350 />

WeChat

