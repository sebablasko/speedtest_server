jQuery(document).ready(function() {
	
    // Fullscreen background
    $.backstretch("assets/img/backgrounds/1.jpg");
    $('#top-navbar-1').on('shown.bs.collapse', function(){
    	$.backstretch("resize");
    });
    $('#top-navbar-1').on('hidden.bs.collapse', function(){
    	$.backstretch("resize");
    });
    
    // Form
    $('.registration-form fieldset:first-child').fadeIn('slow');
    
    // next step
    $('.registration-form .btn-next').on('click', function() {
    	forwardDialog();
    });

    $("input[type=hidden]").bind("change", function() {
        // la idea en cada case es hacer cosas, y llamar de callback a forwardDialog()
        switch(parseInt($(this).val())){
            case 1:
                heimdal.init(geolocation);
                break;
            case 2:
                speedTestNational();
                break;
            case 3:
                speedTestInternational();
                break;
            case 4:
                TOP_CL.forEach(addPingSite);
                pingTest();
                break;
            case 5:
                reportJSON();
                break;
            default:
                location.reload();
                break;
       }
    });
    
});

/* General Controls */

var stepClassNames = ["one", "two", "three", "four", "five"];

function getCurrentStep(){
    return $('#step_counter')[0].value;
}

function stepIn(){
    $('#step_counter').val(parseInt(getCurrentStep()) + 1).triggerHandler('change');
    updateGeneralProgressBar()
}

function stepOff(){
    $('#step_counter').val(parseInt(getCurrentStep()) - 1).triggerHandler('change');
    updateGeneralProgressBar()
}

function updateGeneralProgressBar(){
    var currentState = $('#step_counter')[0].value;
    // update general test progress bar
    $('#general-test-progress-bar')[0].style.width = String(parseInt(currentState)*20)+"%";
    // color stage's points
    for (var i = 0; i < stepClassNames.length; i++) {
        var stage = $(String("."+stepClassNames[i]))[0];
        if (i < currentState) {
            if(stage.classList.contains("no-color")){
                stage.classList.remove("no-color");
                stage.classList.add("primary-color");
                var tick = $('<i class="fa fa-check"></i>');
                $(stage).append(tick);
            };
        }else{
            if(stage.classList.contains("primary-color")){
                stage.classList.remove("primary-color");
                stage.classList.add("no-color");
                $(stage).children().remove();
            }  
        };
    };
}

function forwardDialog(){
    var fieldsets = $('fieldset');
    var currentFieldset = fieldsets[getCurrentStep()];

    // validate
    var next_step = $('[name="user_conn_type"]').is(':checked');
    
    if( next_step ) {
        $('#alert-box').fadeOut(400);
        $(currentFieldset).fadeOut(400, function() {
            $(currentFieldset).next().fadeIn();
        });
        stepIn();
    }else{
        $('#alert-box').removeClass('hide');
    };
}

function addPingSite(value, index, ar){
    var row = $('<tr></tr>');
    $('<td></td>').text(index+1).appendTo(row);
    $('<td></td>').text(value).appendTo(row);

    var tableBody = $('#ping_list_sites')[0];
    row.appendTo(tableBody);
}


/* step 2 functions */
function map(lat,lon){
    latlon = new google.maps.LatLng(lat, lon)
    mapholder = document.getElementById('mapholder')
    mapholder.style.height = '250px';
    mapholder.style.width = '500px';
    var myOptions = {
        center:latlon,zoom:12,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        mapTypeControl:false,
        navigationControlOptions:{
            style:google.maps.NavigationControlStyle.SMALL
        }
    }
    var map = new google.maps.Map(document.getElementById("mapholder"), myOptions);
    var marker = new google.maps.Marker({position:latlon,map:map,title:"Su localización"});
}

function geolocation(){
    var nijs = heimdal.getNetworkInfo();
    var success = nijs.isSuccessful();
    var sysLog = ""
    var proxy = "Falso";
    if(nijs.useProxy()){
        proxy = "Verdadero";
    }
    if(success){
        sysLog += "AS:" + nijs.getAS() + "\n";
        sysLog += "Sistema Operativo:" + nijs.getOS() + "\n";
        sysLog += "Proxy:" + proxy + "\n";
        sysLog += "País:" + nijs.getCountry() + "\n";
        sysLog += "Region:" + nijs.getRegionName() + "\n";
        sysLog += "Ciudad:" + nijs.getCity() + "\n";
        sysLog += "ISP:" + nijs.getIsp() + "\n";
        sysLog += "IP:" + nijs.getIp() + "\n";
        sysLog += "Zona horaria:" + nijs.getTimezone() + "\n";
    }else{
        sysLog += "Estado conexión: Fallida \n";
    }
    console.log(sysLog);
    var coords = nijs.getCoordinates();
    map(coords[0], coords[1]);

    // next step
    setTimeout(function(){
        forwardDialog();
    }, 1500);
}

/* step 3 and 4 functions */
function speedTestNational(){
    var divProgressBarID = 'local_test_progress_bar';
    var onprogress = function aux(evt){
        if (evt.lengthComputable){
            var percentComplete = (evt.loaded / evt.total)*100;
            updateLoadingBar(percentComplete, divProgressBarID);
            if(percentComplete >= 100){
                setTimeout(function(){
                    logSpeedTestSummary(divProgressBarID.split("_")[0]+" "+divProgressBarID.split("_")[1]);

                    // next step
                    forwardDialog();
                }, 500);
            }
        }
    }
    heimdal.runTest(onprogress,file_national);
}

function speedTestInternational(){
    var divProgressBarID = 'international_test_progress_bar';
    var onprogress = function aux(evt){
        if (evt.lengthComputable){
            var percentComplete = (evt.loaded / evt.total)*100;
            updateLoadingBar(percentComplete, divProgressBarID);
            if(percentComplete >= 100){
                setTimeout(function(){
                    logSpeedTestSummary(divProgressBarID.split("_")[0]+" "+divProgressBarID.split("_")[1]);

                    // next step
                    forwardDialog();
                }, 500);
            }
        }
    }
    heimdal.runTest(onprogress,file_international);
}

function updateLoadingBar(currentPercent, progressBarID){
    var percentValue = String(Math.floor(currentPercent)+'%');
    // update Bar
    var progressBar = $($('#'+progressBarID).children()[0]);
    progressBar.css('width', percentValue);
    progressBar.text(percentValue);
}

function logSpeedTestSummary(testTitle){
    var arr = heimdal.getSpeedTests();
    var nijs = arr[arr.length - 1];
    var logMsg = testTitle + '\n';
    logMsg += "El proceso demoró " + nijs.getTestTime() + " dando así una velocidad de bajada de " + nijs.getDownloadSpeed() + " Mbps" + "\n";
    logMsg +=  "Latencia : " + nijs.getLatency() + "\n";
    logMsg += "La latencia es equivalente a una conexión del tipo: " + nijs.getLatencyType() + "\n";
    logMsg += "Throughput : " + nijs.getThroughput() + "\n";
    logMsg += "ThroughPut equivalente a una conexión del tipo : " + nijs.getThroughputType() + "\n";
    console.log(logMsg);
}


/* step 5 functions */
function pingTest(){
    var nu = heimdal.getUtilities();
    function _callback(){
        var pings = nu.getPings();
        var logMsg = "Página\tTiempo (ms)\tEstado\n";
        for(x in pings){
            var p = pings[x];
            if(p.status === "SUCCESS"){
                logMsg += "\t"+p.url+"\t"+p.time+"\tAccesible\n";
                $( "tr:contains("+p.url+")" ).attr("class", "info");
            }else{
                logMsg += "\t"+p.url+"\t-\tInaccesible\n";
            }
        }
        console.log(logMsg);

        // next step
        forwardDialog();
    }
    function earlycall(pingRecord){
        //console.log(pingRecord.url);
        $( "tr:contains("+pingRecord.url+")" ).attr("class", "info");
    }
    //heimdal.pingTest(_callback);
    heimdal.pingTestConcurrentVersion(_callback, earlycall);
    /*
    En el calculo de pings, se debería llamar la siguiente linea cuando una url esté terminada
    $( "tr:contains(url)" ).attr("class", "info");
    */
}

/* step 6 functions */
function reportJSON(){
    var fieldsets = $('fieldset');
    var currentFieldset = fieldsets[getCurrentStep()];
    $('.form-main', currentFieldset).html("<pre>"+JSON.stringify(heimdal, null, 4)+"</pre>");
    var resultsDiv = $(fieldsets.parents()[1]);
    resultsDiv.attr("class", resultsDiv.attr("class").replace("6","8").replace("3","2"));
    console.log(JSON.stringify(heimdal, null, 4));
}