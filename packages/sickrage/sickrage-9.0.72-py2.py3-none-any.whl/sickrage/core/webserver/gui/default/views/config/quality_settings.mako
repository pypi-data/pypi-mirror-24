<%inherit file="../layouts/main.mako"/>
<%!
    import sickrage
    from sickrage.core.common import Quality
    from sickrage.core.helpers import anon_url
%>
<%block name="content">
    <div id="config">
        <form id="configForm" action="saveQualities" method="post">
            <ul class="nav nav-tabs">
                <li class="active"><a data-toggle="tab" href="#core-tab-pane1">Quality Sizes</a></li>
            </ul>

            <div class="tab-content">
                <div id="core-tab-pane1" class="tab-pane fade in active">

                    <div class="tab-pane-desc">
                        <h3>Quality Sizes</h3>
                        <p>Use default qualitiy sizes or specify custom ones per quality definition.</p>

                        <div>
                            <p class="note"> Settings repersent maximum size allowed per episode video file.</p>
                        </div>
                    </div>

                    <fieldset class="tab-pane-list">
                        <table>
                            % for qtype, qsize in sickrage.srCore.srConfig.QUALITY_SIZES.items():
                                % if not qsize == 0:
                                    <tr>
                                        <td>
                                            <label for="${qtype}"
                                                   style="vertical-align:middle;">${Quality.qualityStrings[qtype]}</label>
                                        </td>
                                        <td>
                                            <input type="number" value="${qsize}" name="${qtype}" id="${qtype}"
                                                   min="1"> MB
                                        </td>
                                    </tr>
                                % endif
                            % endfor
                        </table>
                        <br><input type="submit" class="btn config_submitter" value="Save Changes"/><br>
                    </fieldset>
                </div><!-- /tab-pane1 //-->
            </div><!-- /ui-components //-->
            <br><input type="submit" class="btn config_submitter_refresh" value="Save Changes"/><br>
        </form>
    </div>
</%block>
