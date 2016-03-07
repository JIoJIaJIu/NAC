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
    $scope.doUpload = function (file) {
        $scope.progress = true; 
        Upload.upload({
            url: '/upload',
            data: {file: file}
        }).then(function (resp) {
            console.log('Success:  ' + resp.data);
            $scope.progress = false; 
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
