MastodonInstances
=================

Introduction
############

`instances.social <https://instances.social>`_ is the main Mastodon
instances list out there. It is maintained by
`thekinrar <https://mastodon.xyz/@TheKinrar>`_ who, recently, added
a better API (before, it was just about getting :code:`/instances.json`).
This Python 3.x module eases the use of this API.

How to use
##########

Hello world
************

First, install this module using :code:`pip3 install MastodonInstances`.

In order to be able to contact API users, a token system has been set up,
and is mandatory in order to use the API and therefore, this module.
This API token only requires an application name and your email address;
[you can get one here][tk].

Once this is done, you can start using this module! Here is a Hello World
that gets the user count of the :code:`mastodon.social` instance:

.. code-block:: python

	from MastodonInstances import Instances
	
	instances = Instances("<token>")
	instance = instances.get('mastodon.social')
	
	print("mastodon.social has {} users!".format(instance.users))

Listing instances
*****************

There are three types of instances listing served by the API:

- :code:`instances.sample()`: get a random sample of instances;
- :code:`instances.list()`:   list instances in order of their added date;
- :code:`instances.search()`: search through instances using a query.

:code:`instances.sample()` takes a :code:`count` parameter (from 1 to 100) and
an :code:`include_dead` boolean parameter, which is whether we should get
dead instances or not (dead instances are the ones that have been down for
two weeks in a row). By default, we don't want to get dead instances.

:code:`instances.list()` lists instances in the same manner that GETting
:code:`/instances.json` did. :code:`count` can be the maximum number of
instances to get, or :code:`0`, :code:`None` or :code:`"all"` to get all
of the instances (by default, 20 instances will be gathered). You can
also use the :code:`start` parameter to gather the list page by page -- for
example, setting :code:`start` to 20 and :code:`count` to 10 means you are
gathering the third page of 10 elements.
It also takes the :code:`include_dead` parameter.

:code:`instances.search()` searchs through instances with a query (as a
positional argument). It will look for the query in the names, topics and
descriptions. If you only want to look in the names, set :code:`only_names`
to :code:`True`. This method also takes the `count` parameter, with the same
values interpretation as for :code:`instances.list()`.

Here are some examples of these three:

.. code-block:: python

	# Get a random sample of 5 instances that can be dead.
	lst = instances.sample(5, include_dead=True)
	
	# Get two pages of the list (with two different styles of setting count).
	first  = instances.list(10)
	second = instances.list(count=10, start=10)
	
	# Search for instances around retrocomputing.
	retro  = instances.query("retrocomputing")

Accessing instance data
***********************

An instance is an object in this module. There are plenty of properties you
can access:

- :code:`id`: the ID of the instance in the instances.social database (string);
- :code:`name`: the name of the instance (string);
- :code:`version`: the Mastodon software version of the instance (string);
- :code:`open`: whether the registrations are open or not (bool);
- :code:`shortdesc`: a short description of the instance (string, None if
  not set);
- :code:`fulldesc`: a long description of the instance (string, None if
  not set);
- :code:`topic`: the instance topic (string, None if not set);
- :code:`lang`: the list of languages you can write in on this instance (list);
- :code:`otherlang`: whether you can write in other languages on this
  instance (bool);
- :code:`federates_with`: either "all" if the instance federates with all
  instances, or "some" if it doesn't federate with at least one;
- :code:`prohibited`: the prohibited object (see below);
- :code:`added`: the date when the instance was registered in the database
  (datetime, None if not set);
- :code:`updated`: the date when the instance was last updated in the database
  (datetime, None if not set);
- :code:`checked`: the date the instance was last checked (datetime, None if
  not set);
- :code:`uptime`: the uptime proportion (float, 0 to 1 included);
- :code:`up`: whether the instance is currently up or not (bool);
- :code:`dead`: whether the instance is dead or not (bool);
- :code:`ipv6`: whether the instance is accessible through IPv6 or not (bool);
- :code:`https`: the HTTPS rank (see below);
- :code:`obs`: the OBS rank (see below);
- :code:`users`: the user count (int);
- :code:`statuses`: the statuses count (int);
- :code:`connections`: the connections count (int).

The HTTPS and OBS ranks are simple objects that contain the :code:`score` (int,
0 to 100 included) and the :code:`rank` (string). The ranks in the instance
data can also be :code:`None` if not set.

The Prohibited object is an object with a range of booleans indicating
whether the element is prohibited (True) or not (False):

- :code:`nudity_cw`: Nudity with Content Warning;
- :code:`nudity_nocw`: Nudity without Content Warning;
- :code:`porn_cw`: Porn with Content Warning;
- :code:`porn_nocw`: Porn without Content Warning;
- :code:`sexism`: Sexism;
- :code:`racism`: Racism;
- :code:`illegal`: Links to Illegal Content;
- :code:`spam`: Spam;
- :code:`ads`: Advertising;
- :code:`hate`: Hate speeches;
- :code:`harassment`: Harassment;
- :code:`spoilers_nocw`: Spoilers without Content Warning.
