
var app = angular.module('myApp', ['autocomplete', 'angular-loading-bar']);
var pageSize = 10;
var currPage = 1;
var keywords;
var testLocally = true;


app.controller('newsCtrl', function($scope, $http) {
  $scope.noResult = false;
  $scope.comment = 'Top searches: Brexit, Trump, Syria';

  $scope.suggest = function(suggestion) {
    $scope.keywords = suggestion;
    keywords = $scope.keywords;
    $scope.hasSuggestions = false;
    makeRequest(true);
    // makeSuggestion();
  };

  $scope.update = function(typed) {
    var url = 'solr/world_news/suggest?';

    if(testLocally) {
      url = 'http://localhost:8983/solr/world_news/suggest?';
    }
    var component = 'json.wrf=JSON_CALLBACK';

    component += '&spellcheck.q=' + encodeURIComponent(typed);

    $http.jsonp(url + component).success(function(data) {
        console.log(url+component)
      var items = [];

      for(var i = 0;i < data.spellcheck.collations.length;i++) {
        if(i % 2 == 0) {
          continue;
        }
        items.push(data.spellcheck.collations[i]);
      }
      $scope.items = items;
    });

  };





  $scope.endDate = new Date();
  $scope.startDate = new Date($scope.endDate.getTime() - 1 * 365 * 24 * 60 * 60 * 1000);

  $scope.currPage = 0;
  $scope.pageCount = 0;

  $scope.showDateFilter = false;
  $scope.showSourceFilter = false;
  $scope.enableMonthFilter = false;
  $scope.showSentimentFilter = false;

  $scope.sourceSelection = [];
  $scope.sentimentSelection = [];


  $scope.location = "w";
  $scope.sortby = "rel";

  $scope.toggleSourceSelection = function(source) {

    var idx = $scope.sourceSelection.indexOf(source);

    if (idx > -1) {
      $scope.sourceSelection.splice(idx, 1);
    }else {
      $scope.sourceSelection.push(source);
    }
    makeRequest(false);
  };

  $scope.toggleSentimentSelection = function(sentiment) {

    var idx = $scope.sentimentSelection.indexOf(sentiment);

    if (idx > -1) {
      $scope.sentimentSelection.splice(idx, 1);
    }else {
      $scope.sentimentSelection.push(sentiment);
    }
    makeRequest(false);
  };



  function makeMonthQuery(low,high) {
    var query = '';

    query += 'creation_date:[';
    query += low.toISOString();
    query += ' TO ';
    query += high.toISOString() + ']';

    return query;
  }

  function makeSourceQuery(source) {
    var query = '';

    query += 'author:("';
    query += encodeURIComponent(source);
    query += '")';
    return query;
  }

  function makeSentimentQuery(sentiment) {
    var query = '';

    query += 'label:("';
    query += encodeURIComponent(sentiment);
    query += '")';
    return query;
  }

  function getlocation(){

      if($scope.location === "sg"){return '1.35,103.81';}
      else if($scope.location === "ny"){return '34.05,-118.24';}
      else if($scope.location === "la"){return '40.71,-74.00';}
      else if($scope.location === "nd"){return '28.61,77.20';}
      else if($scope.location === "ln"){return '51.50,-0.12';}
      else{return false;}
  }

  function makeRequest(updateFaceting) {

    var start = (currPage - 1) * pageSize;


    var domain = 'solr/world_news/select?';

    if(testLocally) {
      domain = 'http://localhost:8983/solr/world_news/select?';
    }


    var component = 'json.wrf=JSON_CALLBACK' +
        '&q=' + encodeURIComponent(keywords) +
        '&start=' + start +
        '&rows=' + pageSize +
        '&facet.field=author'+
        '&facet.field=label';

    if(getlocation()){
        component += '&fq={!geofilt}&sfield=location&pt='+getlocation()+'&d=15'
    }
    if($scope.sortby == "fav"){
        component += '&sort='+'fav_count+desc'
    }

    var dateQuery = '(';

      var low = $scope.startDate;

      if (typeof low === 'undefined') {
        alert('Please enter the start date.');
        return;
      }
      var high = $scope.endDate;

      if (typeof high === 'undefined') {
        alert('Please enter the end date.');
        return;
      }

      dateQuery += makeMonthQuery(low,high);
    // }
    dateQuery += ')';

    var sentimentQuery = '(';
    if($scope.sentimentSelection.length != 0){
        sentimentQuery += makeSentimentQuery($scope.sentimentSelection[0]);
        for(var i = 1;i<$scope.sentimentSelection.length;i++){
            sentimentQuery+= ' OR ' + makeSentimentQuery($scope.sentimentSelection[i]);
        }
    }
    sentimentQuery+=')';

    var sourceQuery = '(';

    if($scope.sourceSelection.length != 0) {
      sourceQuery += makeSourceQuery($scope.sourceSelection[0]);

      for(var i = 1;i < $scope.sourceSelection.length;i++) {
        sourceQuery += ' OR ' + makeSourceQuery($scope.sourceSelection[i]);
      }
    }
    sourceQuery += ')';
    component += '&fq=cat:(';
    component += dateQuery;
    if($scope.sourceSelection.length!=0){
        component += 'AND';
        component += sourceQuery;
    }
    if($scope.sentimentSelection.length!=0){
        component += 'AND';
        component += sentimentQuery;
    }
    component += ')';

    var url = domain + component;
    console.log(url);

    $http.jsonp(url).success(function(data) {
        updateFilterCheckboxes = true;

      $scope.currPage = currPage ;
      $scope.pageCount = Math.ceil(data.response.numFound / pageSize) ;
      if ($scope.pageCount > 1) {
        $scope.nextDisabled = false;
      }

      if(data.response.docs.length == 0) {
        $scope.noResult = true;
      }else{
        $scope.noResult = false;
      }
      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.comment = 'The query takes ' + queryTime + ' milliseconds. ';

      if(updateFaceting) {


        var sources = [];
        var author;
        var count = 0;
        var source = {};

        for (i = 0; i < data.facet_counts.facet_fields.author.length; i++) {

          if(i % 2 == 0) {
            author = data.facet_counts.facet_fields.author[i];
            source.name = author;
          }else{
            count = data.facet_counts.facet_fields.author[i];
            source.count = count;
            sources.push(source);
            source = {};
          }
        }
        $scope.showSourceFilter = true;
        $scope.sources = sources;



        var sentiments = [];
        var polarity;
        var s_count = 0;
        var sentiment = {};

        for(i=0; i<data.facet_counts.facet_fields.label.length; i++){
            if(i%2 == 0){
                polarity = data.facet_counts.facet_fields.label[i];
                sentiment.name = polarity;
            }else{
                count = data.facet_counts.facet_fields.label[i];
                sentiment.count = count;
                sentiments.push(sentiment);
                sentiment = {};
            }
        }
        $scope.showSentimentFilter = true;
        $scope.sentiments = sentiments;


      }
    });
  }

  function makeSuggestion() {

    var url = 'solr/world_news/select?';

    if(testLocally) {
      url = 'http://localhost:8983/solr/world_news/select?';
    }
    var comp = 'json.wrf=JSON_CALLBACK' +
    '&spellcheck.q=' + encodeURIComponent(keywords);


    $http.jsonp(url + comp).success(function(data) {
      var suggestions = [];

      for(var i = 0;i < data.spellcheck.collations.length;i++) {
        if(i % 2 == 0) {
          continue;
        }
        suggestions.push(data.spellcheck.collations[i]);
      }

      if(suggestions.length > 0) {
        $scope.hasSuggestions = true;
      }
      $scope.suggestions = suggestions;
    });
  }

  $scope.pre = function() {
    currPage = currPage - 1;
    $scope.currPage = currPage;
    $scope.nextDisabled = false;
    if (currPage == 1) {
      $scope.preDisabled = true;
    }

    makeRequest(false);
  };

  $scope.next = function() {
    currPage = currPage + 1;
    $scope.currPage = currPage;
    $scope.preDisabled = false;
    if (currPage == 1) {
      $scope.nextDisabled = true;
    }

    makeRequest(false);

  };


  $scope.search = function() {
    $scope.preDisabled = true;
    $scope.nextDisabled = true;
    $scope.hasSuggestions = false;

    currPage = 1;

    keywords = $scope.keywords;

    makeRequest(true);
    makeSuggestion();

  };

});
