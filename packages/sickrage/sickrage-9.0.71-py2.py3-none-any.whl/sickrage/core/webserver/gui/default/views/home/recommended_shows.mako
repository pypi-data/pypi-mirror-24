<%inherit file="../layouts/main.mako"/>
<%!
    import sickrage
%>

<%block name="content">
    <div id="tabs">
        <ul>
            <li><a href="#tabs-1">Manage Directories</a></li>
            <li><a href="#tabs-2">Customize Options</a></li>
        </ul>
        <div id="tabs-1" class="existingtabs">
                <%include file="../includes/root_dirs.mako"/>
        </div>
        <div id="tabs-2" class="existingtabs">
            <%include file="../includes/add_show_options.mako"/>
        </div>
        <br>

        <span>Sort By:</span>
        <select id="showsort" class="form-control form-control-inline input-sm">
            <option value="name">Name</option>
            <option value="original" selected="selected">Original</option>
            <option value="votes">Votes</option>
            <option value="rating">% Rating</option>
            <option value="rating_votes">% Rating > Votes</option>
        </select>

        <span style="margin-left:12px">Sort Order:</span>
        <select id="showsortdirection" class="form-control form-control-inline input-sm">
            <option value="asc" selected="selected">Asc</option>
            <option value="desc">Desc</option>
        </select>
    </div>

    <br>
    <div id="recommendedShows"></div>
    <br>
</%block>
