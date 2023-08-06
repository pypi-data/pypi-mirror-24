Changelog
=========

0.4.0-drred (2017-08-13)
------------------------

- Replace urllib with Python Requests
- Add debugging output for running tests
- Add `url` attribute to FakeRequest class, to fix failing test
- Refactoring: Rename the test unit files to have test_ prefix
- Refactoring: Change set_debug_string_append to accept dictionary instead
- Refactoring: Replace md5 with more secure way to generate random string



0.3.1-drred (2017-08-08)
----------------
- Variable tracking support
- Custom dimensions support
- Events support
- Site Search support
- Content tracking support
- User ID tracking support

0.3 (2013-02-20)
----------------
- Python 3.2 support
- Switch to hashlib
- Test 'builds' on travis

0.2.2 (2013-01-20)
------------------
- Don't require anonymous view access for unit tests to pass
- Test against Piwik 1.10
- Fix readthedocs build

0.2.1 (2012-10-25)
------------------
- A few small improvements

0.2 (2012-04-15)
----------------
First release as piwikapi on pypi.

- Ecommerce tracking support
- Custom variables tracking support
- Action tracking support
- Goal tracking support
- Added unit tests
- Code refactoring
- Got rid of the Django dependency

0.1 (2012-04-03)
----------------
First release as django-piwik-tracker

- Written in a few hours for a client's project that had just gone live
- Very basic implementation

TODO
----
- Implement and test all the cookie stuff
- Refactor the tracking API code, it's not very pythonic
- Verify all unit tests through the analytics API
- Create sites etc. automatically if necessary for the tests
- TODO: SitesManager plugin
- TODO: ImageGraph plugin
- TODO: UserCountry plugin
- TODO: VisitsSummary plugin
- Fix Failing tests

- test_missing_api_url
- Just a basic test to see if we can get an image
- Test add_ecommerce_item() together with do_track_ecommerce_cart_update(). 
 Also make sure that an abandoned cart was logged.
- test_ecommerce_view
- TODO We could test that each product was added, not only the sums
- Make sure goal conversions are logged
- test_set_debug_string_append
- test_default_action_title_is_correct
- test_default_action_url_is_correct
- This test can't fail, we use IPs from testing networks
- test_default_repeat_visits_recognized
- test_set_visitor_id
- test_setting_ip_works_for_authed_user_only
- test_token_auth_succeeds
- Test download action
- Test out action
- Piwik doesn't save the UA string but processes it.
- test_set_visitor_feature_plugins
- test_set_visitor_feature_resolution
- test_set_visitor_feature_single_plugin