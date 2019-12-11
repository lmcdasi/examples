(function () {
    'use strict';

    angular.module('YOURAPP')
        .provider('lazyLoadService', function LazyLoadProvider() {
            var self = this;
            self.enabled = false;

            self.init = function(config, app, compileProvider, controllerProvider, filterProvider, provide) {
                self.enabled = config.ENABLED;

                if (self.enabled) {
                    app._constant   = app.constant;
                    app._controller = app.controller;
                    app._directive  = app.directive;
                    app._decorator  = app.decorator;
                    app._factory    = app.factory;
                    app._filter     = app.filter;
                    app._service    = app.service;
                    app._value      = app.value;

                    app.controller = function(name, constructor) {
                        controllerProvider.register(name, constructor);
                        return this;
                    };
                    app.service = function(name, constructor) {
                        provide.service(name, constructor);
                        return this;
                    };
                    app.factory = function(name,factory) {
                        provide.factory(name, factory);
                        return this;
                    };
                    app.constant = function(name, value) {
                        provide.constant(name, value);
                        return this;
                    };
                    app.value = function(name, value) {
                        provide.value(name, value);
                        return this;
                    };
                    app.decorator = function(name, decorator) {
                        provide.decorator(name, decorator);
                        return this;
                    };
                    app.directive = function(name, directive) {
                        compileProvider.directive(name, directive);
                        return this;
                    };
                    app.filter = function(name, filter) {
                        filterProvider.register(name, filter);
                        return this;
                    };
                    console.info('LAZYLoad enabled.');
                }
            };

            self.load = function(files, $http, $q) {
                if (self.enabled) {
                    return $q.all(files.map(function(file) {
                        var req = {
                            method: 'GET',
                            url: file,
                        };
                        // 1. if an http interceptor is added then the access_token
                        // can be fed into the http req authorization header.
                        // 2. support for other file types can be added.
                        return $http(req).then(function(response) {
                            var id = response.config.url.replace(/^.*[\\\/]/, '').split('.')[0];
                            var head  = document.getElementsByTagName('head')[0];
                            var prevScript = document.getElementById(id);
                            var script = document.createElement('script');
                            script.id = id;
                            script.type = 'text/javascript';
                            if (typeof prevScript !== 'undefined' && prevScript != null) {
                                head.replaceChild(script, prevScript);
                            } else {
                                head.appendChild(script);
                            }
                            script.innerHTML = response.data + '//# sourceURL=' + response.config.url;
                            return '';
                        });
                    }));
                }
            };

            self.$get = angular.noop;
        });
}());

