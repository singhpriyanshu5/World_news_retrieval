var app = angular.module('crawlApp', ['angular-loading-bar']);
app.controller('crawlCtrl', function($scope, $http) {
    $scope.handles = [{"text":'TechCrunch', "display":"TechCrunch"},
                        {"text":'mashabletech', "display":"Mashable Tech"},
                        {"text":'WIRED', "display":"WIRED"},
                        {"text":'e27co', "display":"e27 Asia Tech News"},
                        {"text":'pogue', "display":"David Pogue"}];
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
