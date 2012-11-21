
// usage: log('inside coolFunc',this,arguments);
// http://paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};

var serverErrorFlag = 0;
function serverErrorHandler(errorType, readyState, status) {
    alert("readyState is " + readyState + " and status is " + status);
    throw new Error("readyState is " + readyState + " and status is " + status);
    if (errorType == 'response') {
        status = xmlHttp.status;
        xmlHttp.abort();
        alert('The server encountered a problem (response status: ' + status + ')');
    }
    else if (errorType == 'timeout') {
        alert("The server did not respond within the timeout period");
    }
    serverErrorFlag = 1;
}

function alertTest() {
    doc = httpGet("overlay.json");
    jsonDoc = jQuery.parseJSON(doc);
    alert(jsonDoc['1']['user_first_name']);
}

function ongoingUpdateDisplay(jsonUrl) {
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
                if (serverErrorFlag == 0) {
                    serverErrorHandler('response', 0, 0);
                }
            }
        }
    }
    if (serverErrorFlag == 0) {
        // set timeout for request
        var xhrTimeout = setTimeout(function(){serverErrorHandler('timeout');}, 4600);
        // set min time between requests sent
        var minRequestTime = setTimeout(function(){xmlHttp.send(null);}, 600);
    }
}

function processResponse(xmlHttp, jsonUrl) {
    jsonDoc = jQuery.parseJSON(xmlHttp.responseText);
//    nameClasses = document.getElementsByClassName('name');
    nameClasses = jQuery('.name');
    x=0
    for(y=0; y<12; y+=1) {
        while(x<7*(y+1)) {
//            log(jsonDoc[y]['user_first_name'] + ' ' + jsonDoc[y]['user_last_name'] + ' ' + jsonDoc[y]['user_status']);
            if(jsonDoc[y]['user_status'] == 'logged_in') {
                nameClasses[x].style.visibility='';
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

window.onload=function(){ongoingUpdateDisplay('overlay.json');};
