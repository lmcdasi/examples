(function () {
    'use strict';

    var app = angular.module('YOURAPP', ['ngRoute']);
    app.constant('_', window._)
        .config(['$controllerProvider', '$compileProvider', '$filterProvider', '$injector', '$provide', '$routeProvider', '$locationProvider', '$httpProvider', 'LAZYLOAD', 'lazyLoadServiceProvider',
            function ($controllerProvider, $compileProvider, $filterProvider, $injector, $provide, $routeProvider, $locationProvider, $httpProvider, LAZYLOAD, lazyLoadServiceProvider) {
                $routeProvider = $routeProvider
                    .when( ..... })
                    })
                    .when('YOUR_ROUTE', {
                        templateUrl: LAZYLOAD.MODULE.CTRL.TEMPLATE,
                        controller: LAZYLOAD.MODULE.CTRL.NAME,
                        resolve: {
                            load: function($http, $q) {
                                try {
                                      return lazyLoadServiceProvider.load(LAZYLOAD.MODULE.CTRL.FILES, $http, $q);
                                } catch(ex) {console.error(ex);}
                            }
                        },
                        secure: true
                    })
                    .otherwise({
                        redirectTo: ...
                    });

                if ({{YOUR_OAUTH_IS_ENABLED}}) {
                    $httpProvider.interceptors.push('httpInterceptor');
                }

                ..................................
                lazyLoadServiceProvider.init(LAZYLOAD, app, $compileProvider, $controllerProvider, $filterProvider, $provide);
            }])

        // Inject the constant module into the rootScope so CONSTANT can be injected in HTML as other scope variable injection.
        .run(function ($rootScope, $location, $route, $templateCache) {
            ................
        });

        // manual bootstrap - to support lazyload
        document.addEventListener("DOMContentLoaded", function() {
           console.log("DOMContentLoaded event received");
           angular.bootstrap(document, ['YOURAPP']);
        });
}());
