let channel_counter = 0; //when creating a channel an id is given to it

document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('username'))
        alert('Please sumbit your name');
    else
        document.querySelector('#user').innerHTML = localStorage.getItem('username');

    //By default, submit button is disabled
    document.querySelector('#submit-username').disabled = true;
    //Enable button only if there is text in the input field
    document.querySelector('#username').onkeyup = () => {
        if (document.querySelector('#username').value.length > 0)
            document.querySelector('#submit-username').disabled = false;
        else
            document.querySelector('#submit-username').disabled = true;
    };

    document.querySelector('#submit-username').onclick = () => {
        username = document.querySelector('#username').value;
        localStorage.setItem('username', username);
        document.querySelector('#username').value = '';
        document.querySelector('#submit-username').disable = true;
        document.querySelector('#user').innerHTML = localStorage.getItem('username');
        return false;
    };

    //ckeck if previous user was in a channel and load it
    if (localStorage.getItem('channel_id') != null)
        load_channel(localStorage.getItem('channel_id'));

    //check if there are already some channels and display them
    //initialize new request
    const request = new XMLHttpRequest();
    request.open('POST', '/getchannels');
    //Callback function for when request completes
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        data.channels.forEach( item => {
            const a = document.createElement('a');
            a.setAttribute('href', '');
            a.setAttribute('class', 'nav-link');
            channel_counter++;
            a.setAttribute('data-channel_id', channel_counter);
            a.innerHTML = `${item} </br>`;
            /*When I create element dynamically reqular query for some class
            to add to it an event handler in general is not ok.
            The following is not ok (it would be ok with staticaly created elements)

            document.querySelectorAll('.nav-link').forEach(link => {
                link.onclick = () => {
                    load_channel(link.dataset.channel_id);
                    return false;
                };
            });

            I have to add an addEventListener in every new element I create, like below.
             */
            a.addEventListener( 'click', () => {
                load_channel(a.dataset.channel_id);
                window.event.returnValue = false;
            });
            //add the new item to the channel list
            document.querySelector('#channels').append(a);
        });
    }
    //send request
    request.send(null);

    document.querySelector('#submit-message').disabled = true;
    document.querySelector('#message').onkeyup = () => {
        if (localStorage.getItem('channel_id') != null)
            if (document.querySelector('#message').value.length > 0)
                document.querySelector('#submit-message').disabled = false;
            else
                document.querySelector('#submit-message').disabled = true;
    };

    document.querySelector('#submit-channel').disabled = true;
    document.querySelector('#channel').onkeyup = () => {
        if (document.querySelector('#channel').value.length > 0)
            document.querySelector('#submit-channel').disabled = false;
        else
            document.querySelector('#submit-channel').disabled = true;
    };

    //SOCKET FOR CHANNELS
    //connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //when connected
    socket.on('connect', () => {
        document.querySelector('#submit-channel').onclick = () => {
            const new_channel_name = document.querySelector('#channel').value;
            socket.emit('submit_new_channel', {'new_channel_name': new_channel_name});
            //clear input field and disable button again
            document.querySelector('#channel').value = '';
            document.querySelector('#submit-channel').disable = true;
            //stop form from submitting
            return false;
        };
    });

    socket.on('announce_new_channel', data => {
        //create new item for the list
        const a = document.createElement('a');
        a.setAttribute('href', '');
        a.setAttribute('class', 'nav-link');
        channel_counter++;
        a.setAttribute('data-channel_id', channel_counter);
        a.innerHTML = `${data.new_channel_name} </br>`;
        a.addEventListener( 'click', () => {
            load_channel(a.dataset.channel_id);
            window.event.returnValue = false;
        });
        //add the new item to the channel list
        document.querySelector('#channels').append(a);
    });

    //SOCKET FOR MESSAGING
    //connect to the websocket
    var socket_msg = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket_msg.on('connect', () => {
        document.querySelector('#submit-message').onclick = () => {
            const new_message_text = document.querySelector('#message').value;
            socket_msg.emit('submit_new_message', {'new_message_text': new_message_text,
                                                    'channel_id': Number(localStorage.getItem('channel_id'))
                                                    ,'username': localStorage.getItem('username')});
            //clear input field and disable button again
            document.querySelector('#message').value = '';
            document.querySelector('#submit-message').disable = true;
            //stop form from submitting
            return false;
        };
    });

    socket_msg.on('announce_new_message', data => {
        //create new item for the list
        const msg = document.createElement('p');
        msg.innerHTML = `${data.new_message[0]}, ${data.new_message[1]} ${data.new_message[2]} </br>`;

        //add the new message in the screen if I am in the same channel as in that in which
        //maybe another user submitted a message
        if (Number(localStorage.getItem('channel_id')) === data.channel_id)
            document.querySelector('#messages').append(msg);
    });
});

//this function loads a channel according to its channel_id
function load_channel(channel_id){
    localStorage.setItem('channel_id', channel_id);

    const request = new XMLHttpRequest();
    request.open('POST', '/getmessages');

    request.onload = () => {
        document.querySelector('#messages').innerHTML = ''; //empty the previous channel's messages
            const data = JSON.parse(request.responseText);

        data.forEach(message => {
            const msg = document.createElement('p');
            msg.innerHTML = `${message[0]}, ${message[1]} ${message[2]} </br>`;
            document.querySelector('#messages').append(msg);
        });

        //Push state to URL.
        document.title = channel_id;
        history.pushState({'text': document.querySelector('#messages').innerHTML}, channel_id, channel_id);
    }

    const data = new FormData();
    data.append('channel_id', channel_id);
    request.send(data);
};

//this is to pop states when going backwards and forward
window.onpopstate = e => {
    const data = e.state;
    document.title = data.title;
    document.querySelector('#messages').innerHTML = data.text;
};

//when logging out clean the localStorage meaning: username and channel_id
function clean_localStorage() {
    localStorage.clear();
    alert('You are logged out');
};
