'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', function () {
  });

angular.module('frontendApp')
  .controller('Form', ['$scope', 'Upload', function ($scope, Upload) {
    $scope.doUpload = function (event, file) {
        event.preventDefault();
        if (!file)
          return;
        $scope.progress = true; 
        Upload.upload({
            url: '/upload',
            data: {file: file}
        }).then(function (resp) {
            var data = resp.data;
            var className = data.className;
            var hasIntrusion = className !== 'normal';
            console.log('Success:  ' + JSON.stringify(resp.data));
            $scope.progress = false; 
            if (hasIntrusion) {
                alert('Нарушениe контроля доступа!');
            } else {
                alert('Нет нарушения контроля доступа');
            }
        }, function (resp) {
            console.log('Error status: ' + resp.status);
            $scope.progress = false; 
        }, function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            $scope.progressPercent = progressPercentage;
            console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
        });
    }
  }]);
