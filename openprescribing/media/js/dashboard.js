(function() {

global.jQuery = require('jquery');
global.$ = global.jQuery;
require('bootstrap');
require('Highcharts');
require('mapbox.js');
var _ = require('underscore');
var Handlebars = require('handlebars');
var measures = require('./dashboard-measures');

var utils = require('./src/chart_utils');
var formatters = require('./src/chart_formatters');
var chartOptions = require('./src/highcharts-options');

Highcharts.setOptions({
    global: { useUTC: false }
});

L.mapbox.accessToken = 'pk.eyJ1IjoiYW5uYXBvd2VsbHNtaXRoIiwiYSI6ImNzY1VpYkkifQ.LC_IcHpHfOvWOQCuo5t7Hw';

var dashboard = {
    el: {
        noData: '',
        status: '.status',
        trendsPanel: '#trends',
        mapPanel: 'map-ccg'
    },
    errorMessage: '<p>Sorry, something went wrong.</p>',

    setUp: function() {

        this.setUpShowPractices();

        var _this = this;
        _this.orgId = orgId;
        _this.orgName = orgName;
        _this.orgType = orgType;
        _this.baseUrl = '/api/1.0/';
        _this.spendUrl = _this.baseUrl;
        _this.spendUrl += (_this.orgType === 'CCG') ? 'spending_by_ccg' : 'spending_by_practice';

        this.setUpMap(_this.orgId, _this.orgType);

        var metric_panel_source = $("#metric-panel").html();
        var metric_panel_template = Handlebars.compile(metric_panel_source);
        var metric_explanation_source = $("#metric-explanation").html();
        var metric_explanation_template = Handlebars.compile(metric_explanation_source);

        _.each(measures, function(m) {
            var data = {
                "metric_id": m.chartId,
                "metric_intro": m.chartIntro,
                "metric_name": m.chartName,
                "metric_description": m.chartDescription,
                "org_name": _this.orgName,
                "org_type": _this.orgType
            };
            function getUrl(d) {
                var url = '&numIds=';
                _.each(d.numIds, function(numId, i) {
                    url += numId.id;
                    url += (i < (d.numIds.length-1)) ? ',' : '';
                });
                if (d.denomIds.length) {
                    url += '&denomIds=';
                    _.each(d.denomIds, function(denomId, i) {
                        url += denomId.id;
                        url += (i < (d.denomIds.length-1)) ? ',' : '';
                    });
                } else {
                    url += '&denom=' + d.denom;
                }
                return url;
            }
            if (_this.orgType == 'CCG') {
                data.metric_footer = '<a href="/analyse#';
                data.metric_footer += 'org=CCG&orgIds=' + this.orgId;
                data.metric_footer += getUrl(m);
                data.metric_footer += '">how this CCG compares to all CCGs</a>, or ';
                data.metric_footer += '<a href="/analyse#org=practice&orgIds=' + this.orgId;
                data.metric_footer += getUrl(m);
                data.metric_footer += '">trends for all ';
                data.metric_footer += 'practices in the same CCG</a>';
            } else {
                data.metric_footer = '<a href="/analyse#';
                data.metric_footer += 'org=practice&orgIds=' + this.orgId;
                data.metric_footer +=  getUrl(m);
                data.metric_footer += '">how this practice compares to all ';
                data.metric_footer += 'practices in the same CCG</a>';
            }
            var r = metric_panel_template(data);
            $('#metric-panels').append(r);
            r = metric_explanation_template(data);
            $('#metric-explanations').append(r);
            _this.setUpChart(_this.getChartOptions(m));
        });
    },

    setUpShowPractices: function() {
        $('#showall').on('click', function(e) {
            e.preventDefault();
            $('#practices li.hidden').each(function () {
                this.style.setProperty( 'display', 'list-item', 'important' );
            });
            $(this).hide();
        });
    },

    setUpMap: function(orgId, orgType) {
        var _this = this;
        var map = L.mapbox.map(_this.el.mapPanel, 'mapbox.streets').setView([52.905, -1.79], 6);
        map.scrollWheelZoom.disable();
        var url = '/api/1.0/org_location/?org_type=' + orgType.toLowerCase();
        url += '&q=' + orgId;
        var layer = L.mapbox.featureLayer()
            .loadURL(url)
            .on('ready', function() {
                if (layer.getBounds().isValid()) {
                    map.fitBounds(layer.getBounds(), {maxZoom: 12});
                    layer.setStyle({fillColor: '#ff00ff',
                                    fillOpacity: 0.2,
                                    weight: 0.5,
                                    color: "#333",
                                    radius: 10});
                } else {
                    $('#map-container').html('');
                }
            })
            .addTo(map);
    },

    setUpChart: function(chartOptions) {
        var _this = this;
        $.when(
            $.ajax(chartOptions.numOrgUrl),
            $.ajax(chartOptions.denomOrgUrl),
            $.ajax(chartOptions.numAllNHS),
            $.ajax(chartOptions.denomAllNHS)
            ).done(function(numOrgResponse, denomOrgResponse, numAllResponse, denomAllResponse) {
                var numOrgData = numOrgResponse[0];
                var denomOrgData = denomOrgResponse[0];
                var combinedOrgData = utils.combineXAndYDatasets(denomOrgData, numOrgData, chartOptions.chartValues);
                var numAllData = numAllResponse[0];
                var denomAllData = denomAllResponse[0];
                var combinedAllData = utils.combineXAndYDatasets(denomAllData, numAllData, chartOptions.chartValues);
                var chartOrgData = _this.convertData(combinedOrgData);
                var chartAllData = _this.convertData(combinedAllData);
                $('#' + this.chartId).find(_this.el.status).hide();
                _this.renderGraph(chartOptions, chartOrgData, chartAllData);
            })
            .fail(function(){
                $('#' + this.chartId).find(_this.el.status).html(_this.errorMessage).show();
            });
    },

    getChartOptions: function(d) {
        var _this = this;
        var chartOptions = {
            'activeOption': 'items',
            'org': _this.orgType,
            'orgIds': [{ 'id': _this.orgId, 'name': _this.orgName}],
            'num': 'chemical',
        };
        chartOptions.chartId = d.chartId;
        chartOptions.numIds = d.numIds;
        chartOptions.denom = d.denom || 'chemical';
        chartOptions.denomIds = d.denomIds;
        if (chartOptions.denom !== 'chemical') {
            chartOptions.chartValues = {
                x_val: chartOptions.denom,
                x: chartOptions.denom
            };
        } else {
            chartOptions.chartValues = {
                x_val: 'x_items',
                x: 'items'
            };
        }
        chartOptions.chartValues.y = 'y_items';
        chartOptions.chartValues.ratio = 'ratio_items';

        var numStr = utils.idsToString(chartOptions.numIds);
        chartOptions.numOrgUrl = _this.spendUrl + '/?format=json&code=' + numStr;
        chartOptions.numOrgUrl += '&org=' + _this.orgId;
        chartOptions.numAllNHS = _this.baseUrl + 'spending/?format=json&code=' + numStr;

        var denomStr = utils.idsToString(chartOptions.denomIds);
        if (chartOptions.denom === 'chemical') {
            chartOptions.denomOrgUrl = _this.spendUrl + '/?format=json&code=' + denomStr;
            chartOptions.denomAllNHS = _this.baseUrl + 'spending/?format=json&code=' + denomStr;
        } else {
            chartOptions.denomOrgUrl = _this.baseUrl + 'org_details/?format=json';
            chartOptions.denomOrgUrl += '&org_type=' + _this.orgType.toLowerCase();
            chartOptions.denomAllNHS = _this.baseUrl + 'org_details/?format=json';
        }
        chartOptions.denomOrgUrl += '&org=' + _this.orgId;
        chartOptions.friendly = formatters.getFriendlyNamesForChart(chartOptions);
        return chartOptions;
    },

    renderGraph: function(chartOptions, combined1, combined2) {
        var _this = this;
        if (combined1.length) {
            var hcOptions = _this.getHighchartsOptions(chartOptions);
            hcOptions.series = [{
                'name': 'Ratio across ' + _this.orgName.replace(/&amp;/g, "&"),
                'data': combined1,
                'color': 'red'
            },
            {
                'name': 'Ratio across all GPs in NHS England',
                'data': combined2
            }];
            var chart = new Highcharts.Chart(hcOptions);
        } else {
            $('#' + chartOptions.chartId).find(_this.el.status).html('No data found for this ' + _this.orgType).show();
        }
    },

    convertData: function(data) {
        _.each(data, function(d) {
            var dates = d.date.split('-');
            var date =  Date.UTC(dates[0], dates[1]-1, dates[2]);
            d.x = date;
            d.y = (d.ratio_items !== null) ? parseFloat(d.ratio_items) : null;
        });
        return data;
    },

    getHighchartsOptions: function(graphOptions) {
        var _this = this,
            values = graphOptions.chartValues;
        var options = $.extend(true, {}, chartOptions.dashOptions);
        options.chart.renderTo = graphOptions.chartId;
        options.yAxis.title.text = graphOptions.friendly.yAxisTitle;
        options.tooltip = {
            formatter: function() {
                var str = '<b>' + this.series.name;
                str += ' in ' + Highcharts.dateFormat('%b \'%y',
                                      new Date(this.x));
                str += '</b><br/>';
                str += Highcharts.numberFormat(this.point[values.y], 0);
                str += (graphOptions.denom === 'chemical') ? ' items for ' : ' ';
                str += graphOptions.friendly.friendlyNumerator + '<br/>';

                str += Highcharts.numberFormat(this.point[values.x_val], 0);
                str += (graphOptions.denom === 'chemical') ? ' items for ' : ' ';
                str += graphOptions.friendly.friendlyDenominator + '<br/>';

                str += 'Ratio: ' + Highcharts.numberFormat(this.point[values.ratio], 2);
                str += ' ' + graphOptions.friendly.friendlyNumerator;
                str += ' items<br/>per ' + graphOptions.friendly.fullDenominator;
                return str;
            }
        };
        return options;
    }
};

dashboard.setUp();


})();

