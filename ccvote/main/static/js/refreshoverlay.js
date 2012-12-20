
// usage: log('inside coolFunc',this,arguments);
// http://paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};

var serverCommunicationsStopped = 0;
function serverErrorHandler(errorType, status, waitUntilTimeout) {
    if (serverCommunicationsStopped == 0) {
//        alert("readyState is " + readyState + " and status is " + status);
//        throw new Error("readyState is " + readyState + " and status is " + status);
        if (errorType == 'response') {
            serverCommunicationsStopped = 1;
            if (status == 0) {
                alert('Communication with the server has stopped. (status: ' + status + ')');
            }
            else {
                alert('The server encountered a problem (response status: ' + status + ').');
            }
        }
        else {
            alert("The server did not respond within the past " + waitUntilTimeout/1000 + " seconds.");
        }
    }
}

function alertTest() {
    doc = httpGet("overlay.json");
    jsonDoc = jQuery.parseJSON(doc);
    alert(jsonDoc['1']['user_first_name']);
}

//alert(window.location.search);

function ongoingUpdateDisplay(jsonUrl) {
    waitUntilTimeout = 4600;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", jsonUrl, true);
    xmlHttp.onreadystatechange = function() {
//        alert('readyState is '+xmlHttp.readyState+' and status is '+xmlHttp.status);
        if (xmlHttp.readyState === 4) {
            if (xmlHttp.status === 200) {
                clearTimeout(xhrTimeout);
                processResponse(xmlHttp, jsonUrl);
            }
            else {
                    serverErrorHandler('response', xmlHttp.status);
                    xmlHttp.abort();
            }
        }
    }
    if (serverCommunicationsStopped == 0) {
        // set timeout for request if communications with server up
        var xhrTimeout = setTimeout(function(){serverErrorHandler('timeout', null, waitUntilTimeout);}, waitUntilTimeout);
    }
    // set min time between requests sent
    var minRequestTime = setTimeout(function(){xmlHttp.send(null);}, 400);
}

function processResponse(xmlHttp, jsonUrl) {
//    alert(getData);
    jsonDoc = jQuery.parseJSON(xmlHttp.responseText);
//    alert(jsonDoc[7]['vote'])
//    alert(jsonDoc[11]['user_status']);
//    nameClasses = document.getElementsByClassName('name');
    nameClasses = jQuery('.name');
    x=0
    for(y=0; y<12; y+=1) {
        while(x<7*(y+1)) {
//            log(jsonDoc[y]['user_first_name'] + ' ' + jsonDoc[y]['user_last_name'] + ' ' + jsonDoc[y]['user_status']);
            if(jsonDoc[y]['user_status'] == 'logged_in') {
                if(jsonDoc[y]['show'] == 'logged-in' || jsonDoc[y]['vote'] != '') {
                    nameClasses[x].style.visibility='';
                }
                else {
                    nameClasses[x].style.visibility='hidden';                
                }
            }
            else {
                nameClasses[x].style.visibility='hidden';
            }
            x+=1;
        }
    }    
    var yesVoteCount = 0;
    var noVoteCount = 0;
    for(x=0, y=0; y<12; x+=7, y+=1) {
//        alert(jsonDoc[y]['vote']);
        if(jsonDoc[y]['vote'] == 'pro') {
            nameClasses[x].className = 'name yesVote';
            yesVoteCount += 1;            
        }
        else if(jsonDoc[y]['vote'] == 'con') {
            nameClasses[x].className = 'name noVote';
            noVoteCount += 1;
        }
        else {
            nameClasses[x].className = 'name lackingVote';

        }
    }
    yesTotalVoteCountDivs = jQuery('.yesTotalNumber');
    noTotalVoteCountDivs = jQuery('.noTotalNumber');
    if(yesVoteCount > 9) {
        document.getElementById('yesLegendTextCont').className = 'yesDoubleDigit';
    }
    else {
        document.getElementById('yesLegendTextCont').className = '';
    }
    if(noVoteCount > 9) {
        document.getElementById('noLegendTextCont').className = 'noDoubleDigit';
    }
    else {
        document.getElementById('noLegendTextCont').className = '';
    }
    for(x=0; x<yesTotalVoteCountDivs.length; x+=1) {
        yesTotalVoteCountDivs[x].innerHTML = yesVoteCount;
    }
    for(x=0; x<noTotalVoteCountDivs.length; x+=1) {
        noTotalVoteCountDivs[x].innerHTML = noVoteCount;
    }
    if(yesVoteCount + noVoteCount > 0) {
        document.getElementById('legendCont').style.visibility='';
    }
    else {
        document.getElementById('legendCont').style.visibility='hidden';
    }
    ongoingUpdateDisplay(jsonUrl);
}

jsonUrl = 'overlay.json' + document.location.search

window.onload=function(){ongoingUpdateDisplay(jsonUrl);};
