app = angular.module('genAlg', []);

function AppController($scope) {
    $scope.processors = 3;

    $scope.taskCount = 1;
    $scope.tasks = [
        {id: 1, name: 'Task 1', length: 1, depend: null, timeConstraint: 0}
    ];
    $scope.updateTasks = function () {
        if ($scope.taskCount > $scope.tasks.length) {
            var task = {};
            task['name'] = 'Task ' + $scope.taskCount;
            task['depend'] = null;
            task['id'] = $scope.taskCount;
            task['timeConstraint'] = 0;
            task['length'] = 1;
            $scope.tasks.push(task);
        } else if ($scope.taskCount < $scope.tasks.length) {
            $scope.tasks.pop();
        }
    };
    $scope.setDependency = function (task, depend) {
        task.depend = depend;
    };
    $scope.getDependency = function (task) {
        if (task.depend == null) {
            return {name: 'None'};
        }
        for (var i = 0; i < $scope.tasks.length; i++) {
            if ($scope.tasks[i].id == task.depend) {
                return $scope.tasks[i];
            }
        }
        return null;
    };

    $scope.range = function (n) {
        return new Array(n);
    };

    $scope.taskIDs = [1, 2, 3];

    $scope.schedule = [
        [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ],
        [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ],
        [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ]
    ];

    $scope.getTasks = function (processor) {
        var schedule = {};
        for (var i = 0; i < $scope.processors; i++) {
            schedule[i] = {};
            for (var j = 0; j < 10; j++) {
                schedule[i][j] = {}
            }
        }

        var schedule = {};
        console.log($scope.tasks.length);
        for (var i = 0; i < $scope.tasks.length; i++) {
            var task = $scope.tasks[i];
            console.log(task.processor == processor);
            if (task.processor == processor) {
                var start = task.start;
                var length = task.length;
                for (var j = start; j < start + length; j++) {
                    schedule[j] = 'test';
                }
            }
        }

        console.log(schedule)
        return schedule;
    }
}