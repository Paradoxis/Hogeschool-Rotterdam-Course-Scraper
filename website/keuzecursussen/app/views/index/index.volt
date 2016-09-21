
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

<div class="row">
    <div class="col-xs-12">
        <div class="table-responsive">
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Naam</th>
                    <th>Code</th>
                    <th>Aanvangsblok</th>
                    <th>Studiepunten</th>
                </tr>


                {% for row in courses %}
                    <tr data-filter-list="search">
                        {% autoescape true %}
                            <td>
                                <a href="/course/view/{{ row.cursuscode }}">{{ row.korteNaamCursus }}</a>
                            </td>
                            <td>{{ row.cursuscode }}</td>
                            <td>{{ row.aanvangsblok }}</td>
                            <td>{{ row.studiePunten }}</td>
                        {% endautoescape %}
                    </tr>
                {% else %}
                    <tr>
                        <td><p>No courses found :(</p></td>
                    </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</div>

