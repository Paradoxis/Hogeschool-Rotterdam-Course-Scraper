<div ng-app="KeuzeCursussen">
    <div class="page-header">
        <h1>HR Keuzecursussen <small>Omdat OSIRIS onoverzichtelijk als de tering is</small></h1>
    </div>

    <div class="row">
        <div class="col-xs-12">
            <div class="form-group">
                <input type="text" class="form-control" placeholder="Zoek op naam.." ng-model="search">
            </div>
        </div>
    </div>

    <div class="row" ng-controller="Finder">
        <div class="col-xs-12">
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead>
                        <tr>
                            <th>
                                <a href="#" ng-click="sortType = 'korteNaamCursus'; sortReverse = !sortReverse">
                                    Naam
                                    <span ng-show="sortType == 'korteNaamCursus' && !sortReverse" class="fa fa-caret-down"></span>
                                    <span ng-show="sortType == 'korteNaamCursus' && sortReverse" class="fa fa-caret-up"></span>
                                </a>
                            </th>
                            <th>
                                <a href="#" ng-click="sortType = 'cursuscode'; sortReverse = !sortReverse">
                                    Code
                                    <span ng-show="sortType == 'cursuscode' && !sortReverse" class="fa fa-caret-down"></span>
                                    <span ng-show="sortType == 'cursuscode' && sortReverse" class="fa fa-caret-up"></span>
                                </a>
                            </th>
                            <th>
                                <a href="#" ng-click="sortType = 'aanvangsblok'; sortReverse = !sortReverse">
                                    Aanvangsblok
                                    <span ng-show="sortType == 'aanvangsblok' && !sortReverse" class="fa fa-caret-down"></span>
                                    <span ng-show="sortType == 'aanvangsblok' && sortReverse" class="fa fa-caret-up"></span>
                                </a>
                            </th>
                            <th>
                                <a href="#" ng-click="sortType = 'studiePunten'; sortReverse = !sortReverse">
                                    Studiepunten
                                    <span ng-show="sortType == 'studiePunten' && !sortReverse" class="fa fa-caret-down"></span>
                                    <span ng-show="sortType == 'studiePunten' && sortReverse" class="fa fa-caret-up"></span>
                                </a>
                            </th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr ng-repeat="row in courses | filter:search | orderBy:sortType:sortReverse" data-filter-list="search">
                            <td>
                                <a href="/course/view/{{ ng("row.cursuscode") }}">{{ ng("row.korteNaamCursus") }}</a>
                            </td>
                            <td>{{ ng("row.cursuscode") }}</td>
                            <td>{{ ng("row.aanvangsblok") }}</td>
                            <td>{{ ng("row.studiePunten") }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.7/angular.min.js"></script>
<script>
    angular.module("KeuzeCursussen", []).controller("Finder", function ($scope) {

        $scope.courses = {{ courses | json_encode }};
        $scope.sortType = 'korteNaamCursus';
        $scope.sortReverse = false;
    });
</script>