A/C Control App
===============

Django app that implements the A/C Control front-end of the home-control system.

![Mobile UI in Action](../../docs/UI-in-Mobile-Action.png)


App Description
---------------

For detailed description, refer to [my blog post on my A/C Control project](http://itamaro.com/2013/10/04/ac-control-project-bringing-it-together/).

This app implements the A/C control web interface part of the project,
using an [A/C RPC app](https://github.com/itamaro/home-control-RPC/tree/master/HomeControlRPC/AC). 


App Configuration
-----------------

The app uses the Django DB to store configuration,
so the configuration is managed via Django admin interface.

The app allows controlling unlimited amount of A/C's,
each controlled A/C based on its own record in the DB.

The settings:

* `name`: A name for this controlled A/C.
* `power_state`: The current A/C power state (*).
* `mode`: The current A/C mode (*).
* `fan`: The current A/C fan speed (*).
* `temp`: The current A/C temperature (*).
* `rpc_url`: The A/C RPC URL to be used for sending A/C commands.

(*) Disclaimers regarding cached state data:

 - If the controlled A/C is controlled by other methods (e.g. a remote),
   the cached state data will be inconsistent with the actual state.
 - When creating an A/C record, you should initialize the state according to the current state.
 - The cached power state may become inconsistent whenever a feedback-beep is missed by the RPC.
   You should manually fix it in the admin interface if it happens.
