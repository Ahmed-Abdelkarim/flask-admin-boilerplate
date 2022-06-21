function list_dicts_to_dict_list(L) {
    let D = {};
    Object.keys(L[0]).forEach(k => {
        D[k] = L.map(o => o[k]);
    });
    return D
}

function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}



const sum_reducer = (accumulator, curr) => accumulator + curr;

fetch("/getSessions", {
    method: "GET",
}).then(response => response.json()).then(res => {
    // Initialization for the data
    var listening_stats_dicts = [];
    var speaking_stats_dicts = [];
    var time_line = [];
    var days_times = [];
    var times_sum;
    var listen_char_acc_time = {};
    var speak_char_acc_time = {};
    // loop over the time stamps
    for (const [key, value] of Object.entries(res)) {
        // 1.general session data collection
        time_line.push(key);
        // session times in minutes
        times_sum = value['time'].reduce(sum_reducer) / (60);
        days_times.push(times_sum);


        // charachters stats

        //collect characters data
        var chars_data = value['characters'];
        var listening = chars_data['listening'];
        var speaking = chars_data['speaking'];
        listening_stats_dicts.push(listening)
        speaking_stats_dicts.push(speaking)


        // chars accuracies with time
        for (const [char, value] of Object.entries(listening)) {
            var r = listening[char]['rightanswers'].reduce(sum_reducer)
            var w = listening[char]['wronganswers'].reduce(sum_reducer)
            var acc = 100 * r / (r + w)
            if (!listen_char_acc_time.hasOwnProperty(char))
                listen_char_acc_time[char] = []
            listen_char_acc_time[char].push(acc)
        }

        for (const [char, value] of Object.entries(speaking)) {
            var r = speaking[char]['rightanswers'].reduce(sum_reducer)
            var w = speaking[char]['wronganswers'].reduce(sum_reducer)
            var acc = 100 * r / (r + w)
            if (!speak_char_acc_time.hasOwnProperty(char))
                speak_char_acc_time[char] = []
            speak_char_acc_time[char].push(acc)

        }

    }

    var listening_stats = list_dicts_to_dict_list(listening_stats_dicts)
    var speaking_stats = list_dicts_to_dict_list(speaking_stats_dicts)
    // collect characters names
    l_keys = Object.keys(listening_stats)
    s_keys = Object.keys(speaking_stats)
    all_keys = l_keys.concat(s_keys)
    var all_unique_chars = all_keys.filter(onlyUnique);
    // apply a fix for the listening and speaking stats
    all_unique_chars.forEach((key, i) => {
        if (!speaking_stats.hasOwnProperty(key))
            speaking_stats[key] = {
                'wronganswers': [0],
                'rightanswers': [0]
            }
        if (!listening_stats.hasOwnProperty(key))
            listening_stats[key] = {
                'wronganswers': [0],
                'rightanswers': [0]
            }
    })


    // Draw the KPIs

    // days vs play time
    var ctx = document.getElementById("dailyPlayTime");
    var label = 'minutes';
    draw_line(time_line, days_times, ctx, label);
    // Characters and number of trials
    var ctx = document.getElementById("skillsNumberOfTrials");
    // extract the pie chart data
    var listening_n_trials = 0
    var speaking_n_trials = 0
    var chars_n_trials = []
    for (const [key, value] of Object.entries(listening_stats)) {
        var curr_l_trials = 0
        var curr_s_trials = 0
        listening_stats[key].forEach((val, i) => {
            curr_l_trials += val['wronganswers'].reduce(sum_reducer)
            curr_l_trials += val['rightanswers'].reduce(sum_reducer)
        })
        speaking_stats[key].forEach((val, i) => {
            curr_s_trials += val['wronganswers'].reduce(sum_reducer)
            curr_s_trials += val['rightanswers'].reduce(sum_reducer)
        })
        listening_n_trials += curr_l_trials
        speaking_n_trials += curr_s_trials
        chars_n_trials.push(curr_l_trials + curr_s_trials)
    }
    labels = ['Listening', 'Speaking']
    data = [listening_n_trials, speaking_n_trials]

    draw_pie(labels, data, ctx);
    // charachters and number of trials
    var ctx = document.getElementById("charNumberOfTrials");
    label = "trials"
    draw_bar(all_unique_chars, chars_n_trials, ctx, label)
    // a
    var ctx = document.getElementById("charNumberOfTrials");
    label = "trials"
    draw_bar(all_unique_chars, chars_n_trials, ctx, label)

    var ctx = document.getElementById("charactersTimeAccuracyListening");
    label = "accuracy"
    console.log(listen_char_acc_time['0'])

    // extract the accuracies for the characters for the line plots
    listen_char_acc_time_list = []
    for (const [key, value] of Object.entries(listen_char_acc_time)) {
        listen_char_acc_time_list.push(listen_char_acc_time[key])
    }
    speak_char_acc_time_list = []
    for (const [key, value] of Object.entries(speak_char_acc_time)) {
        speak_char_acc_time_list.push(speak_char_acc_time[key])
    }
    var listening_chart = draw_line(time_line, listen_char_acc_time_list[all_unique_chars[0]], ctx, label)

    var ctx = document.getElementById("charactersTimeAccuracySpeaking");
    var speaking_chart = draw_line(time_line, speak_char_acc_time_list[all_unique_chars[0]], ctx, label)

    // add the call backs
    var drop_down_listen = document.getElementById('listening_drop_down');
    var drop_down_speak = document.getElementById('speaking_drop_down');
    console.log(all_unique_chars)
    addDropDown(all_unique_chars, drop_down_speak, 'speaking_', speaking_chart, speak_char_acc_time_list)
    addDropDown(all_unique_chars, drop_down_listen, 'listening_', listening_chart, listen_char_acc_time_list)


})
fetch("/getLevels", {
    method: "GET",
}).then(response => response.json()).then(res => {
    var data = {}
    var all_lives = []
    for (const [key, value] of Object.entries(res)) {
        best_lives = value['Best_Lives']
        if (!data.hasOwnProperty(best_lives))
            data[best_lives] = 0
        data[best_lives] += value['Best_Time']
        all_lives.push(best_lives)
    }
    all_lives = all_lives.filter(onlyUnique);
    all_times = []
    all_lives.forEach((live, i) => {
        all_times.push(data[live])
    })
    console.log(all_lives)
    console.log(all_times)
    sorted_arrs = sortTwoArrays(all_lives, all_times)
    all_lives = sorted_arrs[0]
    all_times = sorted_arrs[1]
    var ctx = document.getElementById("heartsTrials");
    label = "trials"
    draw_bar(all_lives, all_times, ctx, label)

})

function sortTwoArrays(arr1, arr2) {
    const indices = Array.from(arr1.keys())
    indices.sort((a, b) => a.itemIndex - b.itemIndex)

    const sortedArr1 = indices.map(i => arr1[i])
    const sortedArr2 = indices.map(i => arr2[i])
    return [sortedArr1, sortedArr2]
}

function addDropDown(vals, parent_element, id_pref, chart, data) {
    vals.forEach((val, i) => {
        const e = document.createElement('a');
        e.className = 'dropdown-item'
        e.id = id_pref + val
        e.innerHTML = val
        parent_element.appendChild(e);
        e.addEventListener("click", () => {
            removeData(chart)
            setData(chart, data[val])
        })
    })
}