<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Hogeschool Rotterdam Keuzecursussen</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
        <style>
            h1 {
                line-height: 20px;
            }
            h1 small {
                font-size: 15px;
            }
            table img {
                opacity: 0;
            }
        </style>
    </head>
    <body ng-app="KeuzeCursussen">

        {# Google Tag Manager #}
        <noscript><iframe src="//www.googletagmanager.com/ns.html?id=GTM-TQRD3N"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-TQRD3N');</script>

        {# Content #}
        <div class="container">
            {{ content() }}

            <hr>

            <footer style="margin-bottom: 50px">
                Copyright &copy; 2016 - <a href="https://www.paradoxis.nl/">Luke Paris (Paradoxis)</a><br />
                Website contents are property of the Hogeschool Rotterdam.
            </footer>
        </div>

        {# GitHub fork banner #}
        <a href="https://github.com/Paradoxis/Hogeschool-Rotterdam-Course-Scraper"><img style="position: absolute; top: 0; right: 0; border: 0;" 
src="https://camo.githubusercontent.com/38ef81f8aca64bb9a64448d0d70f1308ef5341ab/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6461726b626c75655f3132313632312e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png"></a>

        {# Scripts #}
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.7/angular.min.js"></script>
        <script>
            angular.module("KeuzeCursussen", []).directive('filterList', function() {
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
