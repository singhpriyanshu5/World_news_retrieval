var app = angular.module('crawlApp', ['angular-loading-bar']);
app.controller('crawlCtrl', function($scope, $http) {
    $scope.handles = [{"text":'BBCWorld', "display":"BBC News (World)"},
                        {"text":'cnnbrk', "display":"CNN Breaking News"},
                        {"text":'FoxNews', "display":"Fox news"},
                        {"text":'STcom', "display":"The Straits Times"},
                        {"text":'timesofindia', "display":"Times of India"}];
    $scope.selected = {}
    $scope.crawlSelected=function(){
        console.log($scope.selected);
        var handles_lst = [];
        for(var key in $scope.selected){
            if($scope.selected[key] === true){
                handles_lst.push(key)
            }
        }
        handles_str = handles_lst.join(",");
        console.log(handles_str);
        var url = 'http://localhost:8000/incremental_crawler/recrawl?callback=JSON_CALLBACK&handles='+handles_str;
        $http.jsonp(url).success(function(data) {
            console.log(JSON.stringify(data));
            console.log('recrawling!!');
          alert('The latest tweets have been crawled!!');
        });

    };

});
