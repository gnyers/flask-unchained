config files
------------
* need a good way for bundle configs to get access to the current app config during initialization (probably somehow need to LocalProxy to it... challenge is app ctx)
* probably would be nice to have some kind of command to view the current config
    - maybe filter by bundle


api bundle
----------
* finish integrating OpenAPI/APISpec


security bundle
---------------
* implement support for JWT tokens (and maybe PASETO tokens too?)
* implement support for OAuth 2.0


logging
-------
* integrate Flask-LogConfig (or Logbook, need to investigate)


documentation
-------------
* document usage of admin, babel, and webpack bundles
* document creating extendable bundles
* finish tutorial


dependency injection
--------------------
* would be way less typing to allow setting services-to-be-injected as class attributes instead of as arguments to the constructor
* should services be lazily instantiated on an as-needed basis?


tests
-----
* add more tests for the di subsystem, eg register services hook needs tests
* register commands hook


lower priority
--------------
* verify it's possible to override hooks (certainly bundles should be able to override hooks from parent bundles, but should it also be possible to override unchained's hooks too?)
* webpack support could use some improvement
   - maybe default configs for common setups?
   - hot reloading would be nice
* admin bundle could also use some improvement
   - honestly i haven't spent much time looking too deeply into flask-admin, and am kind of leaning towards researching SPA-based admin interfaces
* should commands have dependency injection set up automatically on them?
* it should probably be possible to define multiple modules a hook should load from


bucket list
-----------
* websockets support
* out-of-the-box support for production deployment
   - docker
   - AWS
   - GCP
   - ansible? it works but it's got some pain points
* frontend app templates
   - react
   - angular
   - vue
