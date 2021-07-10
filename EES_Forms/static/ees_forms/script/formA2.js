// Get Required Input Fields


function updateCalcs(){

    // Push Side

    const pushSide_startTime_value  = document.getElementById('pushSide_startTime').value;
    const pushSide_endTime_value = document.getElementById('pushSide_endTime').value;
    const pushSide_tempBlocked_min_value = document.getElementById('pushSide_tempBlocked_min').value;
    const pushSide_tempBlocked_max_value = document.getElementById('pushSide_tempBlocked_max').value;
    const pushSide_traverseTime_value_min = document.getElementById('pushSide_traverseTime_min').value;
    const pushSide_traverseTime_value_second = document.getElementById('pushSide_traverseTime_second').value;
    
    pushSide_startTime_array = getTimeArray(pushSide_startTime_value);
    pushSide_endTime_array = getTimeArray(pushSide_endTime_value);

    pushSide_timeDelta = timeDelta(pushSide_startTime_array, pushSide_endTime_array);
    
    
    document.getElementById('pushSide_traverseTime_min').value = pushSide_timeDelta[1];
    document.getElementById('pushSide_traverseTime_second').value = pushSide_timeDelta[2];

    // coke Side

    const cokeSide_startTime_value  = document.getElementById('cokeSide_startTime').value;
    const cokeSide_endTime_value = document.getElementById('cokeSide_endTime').value;
    //const cokeSide_tempBlocked_min_value = document.getElementById('cokeSide_tempBlocked_min').value;
    //const cokeSide_tempBlocked_max_value = document.getElementById('cokeSide_tempBlocked_max').value;
    const cokeSide_traverseTime_value_min = document.getElementById('cokeSide_traverseTime_min').value;
    const cokeSide_traverseTime_value_second = document.getElementById('cokeSide_traverseTime_second').value;
    
    cokeSide_startTime_array = getTimeArray(cokeSide_startTime_value);
    cokeSide_endTime_array = getTimeArray(cokeSide_endTime_value);

    cokeSide_timeDelta = timeDelta(cokeSide_startTime_array, cokeSide_endTime_array);
    
    
    document.getElementById('cokeSide_traverseTime_min').value = cokeSide_timeDelta[1];
    document.getElementById('cokeSide_traverseTime_second').value = cokeSide_timeDelta[2];
    
    //Total Traverse Time
    traverseTime_total = 60*(pushSide_timeDelta[1]+cokeSide_timeDelta[1])+pushSide_timeDelta[2]+cokeSide_timeDelta[2];
    document.getElementById('total_traverseTime').value = traverseTime_total;
}


// takes a time string 'hh:mm:ss' and returns a int array [hh, mm, ss]
const getTimeArray = (timeString) => {
    let timeArray = timeString.split(":");
    let intTimeArray = [parseInt(timeArray[0]),parseInt(timeArray[1]),parseInt(timeArray[2])];
    return intTimeArray;
}

// takes a 2 int arrays (mil time) [hh, mm, ss] and returns the time difference in a int array [hh, mm, sss]
const timeDelta = (startTimeArray,endTimeArray) => {
    let hourDelta = endTimeArray[0] - startTimeArray[0];
    let minuteDelta = endTimeArray[1] - startTimeArray[1];
    let secondDelta = endTimeArray[2] - startTimeArray[2];
    
    if (secondDelta < 0){
        minuteDelta--;
        secondDelta = 60-Math.abs(secondDelta);
    }
    
    if (minuteDelta < 0){
        hourDelta--;
        minuteDelta = 60-Math.abs(minuteDelta);
    }

    if(hourDelta < 0){
        prevDayTimeDelta = 24 - startTimeArray[0];
        currentDayTimeDelta = endTimeArray[0];
        hourDelta = prevDayTimeDelta + currentDayTimeDelta;
        // 3 - 16 = -13
    }

    
    
    

    

    deltaArray = [hourDelta, minuteDelta, secondDelta];
    return deltaArray;    
    
}




