app = angular.module('genAlg', []);

function AppController($scope, $http) {
    $scope.constraints = {
        processors: 3,
        total_time: 10,
        generations: 10
    };

    $scope.tasks = [
        {id: 1, name: 'Task 1', length: 1, depend: null, priority: 1}
    ];

    $scope.addTask = function () {
        var task = {};
        task['name'] = 'Task ' + ($scope.tasks.length + 1);
        task['depend'] = null;
        task['id'] = ($scope.tasks.length + 1);
        task['length'] = 1;
        task['priority'] = 1;
        $scope.tasks.push(task);
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

    $scope.schedule = [];

    var initSchedule = function () {
        for (var i = 0; i < $scope.constraints.processors; i++) {
            p = [];
            for (var j = 0; j < $scope.constraints.total_time; j++) {
                p.push({});
            }
            $scope.schedule.push(p);
        }
    };
    initSchedule();

    $scope.updateSchedule = function () {
        if ($scope.constraints.processors > $scope.schedule.length) {
            p = [];
            for (var i = 0; i < $scope.constraints.total_time; i++) {
                p.push({});
            }
            $scope.schedule.push(p);
        } else if ($scope.constraints.processors < $scope.schedule.length) {
            $scope.schedule.pop();
        } else if ($scope.constraints.total_time > $scope.schedule[0].length) {
            for (var i = 0; i < $scope.schedule.length; i++) {
                $scope.schedule[i].push({});
            }
        } else if ($scope.constraints.total_time < $scope.schedule[0].length) {
            for (var i = 0; i < $scope.schedule.length; i++) {
                $scope.schedule[i].pop();
            }
        }
    };

    $scope.generateSchedule = function () {
        var btn = $('#generate-schedule');
        var text = btn.text();
        btn.text('Generating...');

        var data = {
            tasks: $scope.tasks,
            constraints: $scope.constraints
        };

        $http({
            url: '/schedule',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            data: data
        }).success(function (data, status, headers, config) {
                $scope.schedule = data;
                console.log($scope.schedule);
                btn.text(text);
            }).error(function (data, status, headers, config) {
                btn.text(text);
                alert('There was an error processing this schedule.');
            });
    };

    $scope.getColor = function (task) {
        var color = '#ffffff';
        if (task != null) {
            color = task.color;
        }
        return {'background-color': color}
    }
}

AppController.$inject = ['$scope', '$http'];

