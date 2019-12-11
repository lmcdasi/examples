(function () {
    'use strict';

    angular.module('YOURAPP')
        .factory('httpInterceptor', ['$injector', function($injector) {
            var service = {
                request: function(config) {
                    var authBearer = $injector.get('YOURAUTHSERVICE').getBearer();
                    if (typeof authBearer !== 'undefined' && authBearer != null) {
                        config.headers.Authorization = authBearer;
                    }
                    return config;
                }
            };
            return service;
    }]);
}());

