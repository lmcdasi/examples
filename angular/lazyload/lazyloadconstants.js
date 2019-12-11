(function () {
    'use strict';

    // other files types support can be added
    angular.module('YOURAPP')
        .constant('LAZYLOAD', {
            'ENABLED': true,
            'MODULE': {
                'CTRL': {
                    'NAME': 'ControllerName',
                    'FILES': ['ARRAYS OF JS FILES']
                    ],
                    'TEMPLATE': 'YOURTEMPLATE'
                },
                ....................
            }
        });
}());
