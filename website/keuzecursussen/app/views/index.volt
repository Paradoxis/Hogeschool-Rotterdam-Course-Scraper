<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <title>Hogeschool Rotterdam Keuzecursussen</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

        <style>
            h1 {
                line-height: 20px;
            }
            h1 small {
                font-size: 15px;
            }
        </style>
    </head>
    <body ng-app="KeuzeCursussen">

        <!-- Google Tag Manager -->
        <noscript><iframe src="//www.googletagmanager.com/ns.html?id=GTM-TQRD3N"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-TQRD3N');</script>
        <!-- End Google Tag Manager -->

        <div class="container">
            {{ content() }}

            <hr>

            <footer style="margin-bottom: 50px">
                Copyright &copy; 2016 - <a href="https://www.paradoxis.nl/">Luke Paris (Paradoxis)</a><br />
                Website contents are property of the Hogeschool Rotterdam.
            </footer>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.7/angular.min.js"></script>
        <script>
            $("img").css("opacity", "0");

            angular.module("KeuzeCursussen", []);

            angular.module("KeuzeCursussen").directive('filterList', function($timeout) {
                return {
                    link: function(scope, element, attrs) {

                        function filterBy(value) {
                            element[0].className = element.children()[0].innerText.toLowerCase().indexOf(value.toLowerCase()) !== -1 ? '' : 'ng-hide';
                        }

                        scope.$watch(attrs.filterList, function(newVal, oldVal) {
                            if (newVal !== oldVal) {
                                filterBy(newVal);
                            }
                        });
                    }
                };
            });
        </script>
    </body>
</html>
