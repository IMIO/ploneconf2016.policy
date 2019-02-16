=======================================================
Plone Conference Policy Product
=======================================================

Introduction
============

This policy product was originally created for Plone Conference 2016 in Boston but has been used for subsequent
conferences (2017 and 2018) as of this writing.

It pulls in other Plone add-ons and contains content types for persons, keynote speakers, presentations, and training
classes.

Content Types
-------------

The content types defined in this policy product are as follows:

- Person: contains fields for a person's name, summary, biography, profile picture, contact information (Twitter, GitHub
  ID, email address), and a related items field used to connect the person to the presentations or training classes they
  are giving. The email address field is visible only to those who can edit the Person object (typically site
  administrators only, as we have not given out edit access to the individual).

- Keynoter: a person giving a keynote. Contains the same fields as the Person content type. TODO: make Keynoter a
  subclass of Person

- Presentation: contains fields for a presentation or talk: title, summary, full description, name and link to
  presenter(s), length or duration (long, short, demo), target level (beginner, intermediate, expert), audience (user,
  integrator, designer, developer), URL and embed codes for presentation slides and recorded video, start and end
  datetimes, location or room. Also contains a URL to the presentation's Mosaic tile in the schedule page and fields
  for a related slider (more on this later).

- Training Class: contains fields for a training class: title, summary, full description, name and link to
  instructor(s), duration of the class (half day, full day, two day), target audience level (beginner, intermediate,
  expert), target audience type (user, integrator, designer, developer), start and end datetimes, location or room.
  Also contains fields for a related slider (more on this later).

Required Add-ons
----------------

The following add-ons are pulled in by this policy product:

- Products.PloneFormGen
- Products.RedirectionTool
- collective.addthis
- plone.app.mosaic
- Products.QuickImporter
- plone.api
- collective.fbshare
- collective.relatedslider

URL of Schedule Tile
--------------------

The conference sites contain three schedule Mosaic pages, one for each day of the conference. These schedule pages
contain Mosaic tiles arranged in three columns (one for each track). The tiles are mostly Presentation tiles which are
references to the Presentation object they represent (the other tiles are rich text tiles for coffee breaks, lunch
breaks, open spaces, meetings, and so on).

In the Presentation content type, the `schedule_url` field, if set, lets a visitor click through to the presentation's
tile in the schedule page.

Related Slider
--------------

The related slider fields in Presentation and Training Class content types are not currently used on any of the live
conference sites (2016, 2017, 2018), but they are intended to show links to other related site content defined manually
or via collection criteria.


Deployment
==========


The production server currently runs Plone 5.0.7.


Add-ons
-------

The following add-ons are in the `buildout.cfg` on the Linode server:

  - "ploneconf2016.policy = git https://github.com/plone/ploneconf2016.policy.git"
  - "ploneconf2017.theme = git https://github.com/sneridagh/ploneconf2017.theme.git"
  - "collective.fbshare = git https://github.com/alecpm/collective.fbshare.git rev=86056e4ef74f536375bf8c7d538f1612d7a163d2"
  - "collective.relatedslider = git https://github.com/collective/collective.relatedslider.git"
  - uwosh.pfg.d2c
  - collective.recaptcha
  - Products.PloneHotfix20171128

Sites Served
------------

The Linode currently serves the following sites:

- 2015.ploneconf.org (served statically by `nginx`, exported from Plone via `wget`)
- 2016.ploneconf.org (will be exported statically soon)
- 2017.ploneconf.org (will be exported statically soon)
- 2018.ploneconf.org (will be exported statically ~February 2019)
- 2019.ploneconf.org (new clone)



How to Create a New Conference Site
===================================

At the end of each annual conference, we invite the next conference organizers to use this website setup. With their
agreement, we use the Management Interface on the Linode to clone the just-ended conference site, and we grant the new
organizers Manager role on their new site.

The main things the new organizers must do with their new site are as follows:

- create a new theme (January or February)
- create new content for these pages:
  - homepage (early)
  - about (early)
  - logistics and instructions for attendees (1-2 weeks before the conference starts)
- update content for these pages:
  - training, including schedule (2-3 months before the conference starts)
- sprints
- sponsors
- venue
- party
- schedule

The following content can likely stay unchanged:

- terms


Forms
-----
The contact form needs updating of the recipients, usually at least `conf@plone.org`.

The talk submission form does not usually need changes. TODO: use d2c

The training signup form fields do not usually need changes, but its JavaScript needs to be updated to reflect the
training class schedule. This JavaScript helps users by preventing them from choosing overlapping or conflicting
classes.


Areas of Improvement
====================

Based on our experience using this policy product for three conference sites, we are aware of the following possible
improvements:

- There needs to be some way to create Presentation items automatically from talk proposal submissions. A complication
  is that we have separate Person or Keynoter content items, so some of the field values in the talk proposal form
  submission would need to be split into two content items (a Presentation and a Person item), and often one person
  gives more than one presentation or training class.

- The schedule for each day of the conference should be automatically generated. This could be via collections or just
  regular folders containing Presentation items. That would also remove the need for updating presentation times or
  locations in two places (the Presentation item and the schedule Mosaic page).

- The creation and display of the training classes and schedule should be automated. Currently, the training class
  schedule is manually generated by exporting the HTML of a Google Sheet (yes!, or rather, Noooooo!). Ideally, the same
  process would be used to manage and display the training classes and schedule as the presentations and talk schedule.
