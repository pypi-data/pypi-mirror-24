Instaloader
===========

Installation
------------

.. installation-start

Instaloader requires `Python <https://www.python.org/>`__, at least
version 3.5.  If you have `pip <https://pypi.python.org/pypi/pip>`__
installed, you may install Instaloader using

::

    pip3 install instaloader

Alternatively, to get the most current version of Instaloader from our
`Git repository <https://github.com/Thammus/instaloader>`__:

::

    pip3 install git+https://github.com/Thammus/instaloader

(pass ``--upgrade`` to upgrade if Instaloader is already installed)

Instaloader requires
`requests <http://python-requests.org/>`__, which
will be installed automatically, if it is not already installed.

.. installation-end

How to Automatically Download Pictures from Instagram
-----------------------------------------------------

.. basic-usage-start

To **download all pictures and videos of a profile**, as well as the
**profile picture**, do

::

    instaloader profile [profile ...]

where ``profile`` is the name of a profile you want to download. Instead
of only one profile, you may also specify a list of profiles.

To later **update your local copy** of that profiles, you may run

::

    instaloader --fast-update profile [profile ...]

If ``--fast-update`` is given, Instaloader stops when arriving at the
first already-downloaded picture. When updating profiles, Instaloader
automatically **detects profile name changes** and renames the target
directory accordingly.

Instaloader can also be used to **download private profiles**. To do so,
invoke it with

::

    instaloader --login=your_username profile [profile ...]

When logging in, Instaloader **stores the session cookies** in a file in
your temporary directory, which will be reused later the next time
``--login`` is given.  So you can download private profiles
**non-interactively** when you already have a valid session cookie file.

What to Download
^^^^^^^^^^^^^^^^

Instaloader does not only download media by-profile. More generally, you
may specify the following targets:

- ``profile``: Public profile, or private profile with ``--login``,

- ``"#hashtag"``: Posts with a certain **hashtag** (the quotes are
  usually neccessary),

- ``:stories``: The currently-visible **stories** of your followees
  (requires ``--login``),

- ``:feed``: Your **feed** (requires ``--login``),

- ``@profile``: All profiles that are followed by ``profile``, i.e. the
  *followees* of ``profile`` (requires ``--login``).

Instaloader goes through all media matching the specified targets and
downloads the pictures and videos and their captions. You can specify
``--comments`` to also **download comments** of each post and
``--geotags`` to **download geotags** of each post and save them as
Google Maps link.  For each profile you download, ``--stories``
instructs Instaloader to **download the user's stories**.

Filename Specification
^^^^^^^^^^^^^^^^^^^^^^

For each target, Instaloader creates a directory named after the target,
i.e. ``profile``, ``#hashtag``, ``:feed``, etc. and therein saves the
posts in files named after the post's timestamp.

``--dirname-pattern`` allows to configure the directory name of each
target. The default is ``--dirname-pattern={target}``. In the dirname
pattern, the token ``{target}`` is replaced by the target name, and
``{profile}`` is replaced by the owner of the post which is downloaded.

``--filename-pattern`` configures the path of the post's files relative
to the target directory. The default is ``--filename-pattern={date}``.
The tokens ``{target}`` and ``{profile}`` are replaced like in the
dirname pattern. Further, the tokens ``{date}`` and ``{shortcode}`` are
defined.

For example, encode the poster's profile name in the filenames with:

::

    instaloader --filename-pattern={date}_{profile} "#hashtag"

The pattern string is formatted with Python's string formatter. This
gives additional flexibilty for pattern specification. For example,
`strftime-style formatting options <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>`__
are supported for the post's
timestamp. The default for ``{date}`` is ``{date:%Y-%m-%d_%H-%M-%S}``.

Filter Posts
^^^^^^^^^^^^

The ``--only-if`` option allows to specify criterias that posts have to
meet to be downloaded. If not given, all posts are downloaded. It must
be a boolean Python expression where the variables ``likes``,
``comments``, ``viewer_has_liked``, ``is_video``, and many
more are defined.

A few examples:

To **download the pictures from your feed that you have liked**:

::

    instaloader --login=your_username --only-if=viewer_has_liked :feed

Or you might only want to download **posts that either you liked or were
liked by many others**:

::

    instaloader --login=your_username --only-if="likes>100 or viewer_has_liked" profile

Or you may **skip videos**:

::

    instaloader --only-if="not is_video" target

Or you may filter by hashtags that occur in the Post's caption. For
example, to download posts of kittens that are cute: ::

    instaloader --only-if="'cute' in caption_hashtags" "#kitten"

.. basic-usage-end

(For a more complete description of the ``-only-if`` option, refer to
the `Instaloader Documentation <https://instaloader.readthedocs.io/basic-usage.html#filter-posts>`__)


Advanced Options
----------------

.. cli-options-start

The following flags can be given to Instaloader to specify how profiles should
be downloaded.

To get a list of all flags, their abbreviations and their descriptions, you may
run ``instaloader --help``.

What to Download
^^^^^^^^^^^^^^^^

Specify a list of profiles or #hashtags. For each of these, Instaloader
creates a folder and downloads all posts along with the pictures's
captions and the current **profile picture**. If an already-downloaded profile
has been renamed, Instaloader automatically **finds it by its unique ID** and
renames the folder likewise.

Instead of a *profile* or a *#hashtag*, the special targets
``:feed`` (pictures from your feed) and
``:stories`` (stories of your followees) can be specified.

--profile-pic-only         Only download profile picture.
--no-videos                Do not download videos.
--geotags                  **Download geotags** when available. Geotags are stored as
                           a text file with the location's name and a Google Maps
                           link. This requires an additional request to the
                           Instagram server for each picture, which is why it is
                           disabled by default.
--no-geotags               Do not store geotags, even if they can be obtained
                           without any additional request.
--comments                 Download and update comments for each post. This
                           requires an additional request to the Instagram server
                           for each post, which is why it is disabled by default.
--no-captions              Do not store media captions, although no additional
                           request is needed to obtain them.
--stories                  Also **download stories** of each profile that is
                           downloaded. Requires ``--login``.
--stories-only             Rather than downloading regular posts of each
                           specified profile, only download stories.
                           Requires ``--login``.
--only-if filter           Expression that, if given, must evaluate to True for each post to
                           be downloaded. Must be a syntactically valid python
                           expression. Variables are evaluated to
                           ``instaloader.Post`` attributes.
                           Example: ``--only-if=viewer_has_liked``.


When to Stop Downloading
^^^^^^^^^^^^^^^^^^^^^^^^

If none of these options are given, Instaloader goes through all pictures
matching the specified targets.

--fast-update              For each target, stop when encountering the first
                           already-downloaded picture. This flag is recommended
                           when you use Instaloader to update your personal
                           Instagram archive.
--count COUNT              Do not attempt to download more than COUNT posts.
                           Applies only to ``#hashtag``, ``:feed-all`` and ``:feed-liked``.


Login (Download Private Profiles)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Instaloader can **login to Instagram**. This allows downloading private
profiles. To login, pass the ``--login`` option. Your session cookie (not your
password!) will be saved to a local file to be reused next time you want
Instaloader to login.

--login YOUR-USERNAME      Login name (profile name) for your Instagram account.
--sessionfile SESSIONFILE  Path for loading and storing session key file.
                           Defaults to a path
                           within your temporary directory, encoding your local
                           username and your Instagram profile name.
--password YOUR-PASSWORD   Password for your Instagram account. Without this
                           option, you'll be prompted for your password
                           interactively if there is not yet a valid session
                           file.

How to Download
^^^^^^^^^^^^^^^

--dirname-pattern DIRNAME_PATTERN
                           Name of directory where to store posts. ``{profile}``
                           is replaced by the profile name, ``{target}`` is replaced
                           by the target you specified, i.e. either ``:feed``,
                           ``#hashtag`` or the profile name. Defaults to ``{target}``.
--filename-pattern FILENAME_PATTERN
                           Prefix of filenames. Posts are stored in the
                           directory whose pattern is given with ``--dirname-pattern``.
                           ``{profile}`` is replaced by the profile name,
                           ``{target}`` is replaced by the target you specified, i.e.
                           either ``:feed``, ``#hashtag`` or the profile name. Also, the
                           fields ``{date}`` and ``{shortcode}`` can be specified.
                           Defaults to ``{date:%Y-%m-%d_%H-%M-%S}``.
--user-agent USER_AGENT    User Agent to use for HTTP requests. Per default,
                           Instaloader pretends being Chrome/51.

Miscellaneous Options
^^^^^^^^^^^^^^^^^^^^^

--quiet                    Disable user interaction, i.e. do not print messages
                           (except errors) and fail if login credentials are
                           needed but not given. This makes Instaloader
                           **suitable as a cron job**.

.. cli-options-end

Usage as Python module
----------------------

.. as-module-intro-start

You may also use parts of Instaloader as library to do other interesting
things.

For example, to get a list of all followees and a list of all followers of a profile, do

.. code:: python

    import instaloader

    # Get instance
    loader = instaloader.Instaloader()

    # Login
    loader.interactive_login(USERNAME)

    # Print followees
    print(PROFILE + " follows these profiles:")
    for f in loader.get_followees(PROFILE):
        print("\t%s\t%s" % (f['username'], f['full_name']))

    # Print followers
    print("Followers of " + PROFILE + ":")
    for f in loader.get_followers(PROFILE):
        print("\t%s\t%s" % (f['username'], f['full_name']))

Then, you may download all pictures of all followees with

.. code:: python

    for f in loader.get_followees(PROFILE):
        loader.download_profile(f['username'])

You could also download your last 20 liked pics with

.. code:: python

    loader.download_feed_posts(max_count=20, fast_update=True,
                               filter_func=lambda post: post.viewer_has_liked)

To download the last 20 pictures with hashtag #cat, do

.. code:: python

    loader.download_hashtag('cat', max_count=20)

Generally, Instaloader provides methods to iterate over the Posts from
a certain source.

.. code:: python

    for post in loader.get_hashtag_posts('cat'):
        # post is an instance of instaloader.Post
        loader.download_post(post, target='#cat')

Each Instagram profile has its own unique ID which stays unmodified even
if a user changes his/her username. To get said ID, given the profile's
name, you may call

.. code:: python

    loader.get_id_by_username(PROFILE_NAME)

.. as-module-intro-end

Refer to the
`Instaloader Documentation <https://instaloader.readthedocs.io/as-module.html>`__ for
more information.

Disclaimer
----------

.. disclaimer-start

Instaloader is in no way affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or
subsidiaries. This is an independent and unofficial project. Use at your own risk.

.. disclaimer-end

Instaloader is licensed under an MIT license. Refer to ``LICENSE`` file for more information.
