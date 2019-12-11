Sample of angularjs lazyload.

According to the definition of $routeProvider:

https://docs.angularjs.org/api/ngRoute/provider/$routeProvider

'
resolve - {Object.<string, Function>=} - An optional map of dependencies which should be injected into the controller. If any of these dependencies are promises, the router will wait for them all to be resolved or one to be rejected before the controller is instantiated. If all the promises are resolved successfully, the values of the resolved promises are injected and $routeChangeSuccess event is fired. If any of the promises are rejected the $routeChangeError event is fired. For easier access to the resolved dependencies from the template, the resolve map will be available on the scope of the route, under $resolve (by default) or a custom name specified by the resolveAs property (see below). This can be particularly useful, when working with components as route templates.
'

Which implies that the controller will be instantiated ONLY after the $http requests are completed.
This allows to download any type of file and configure the page before the controller is instantiated.

The manual bootstral allows the instantiated controller to register AFTER the page has been loaded.
