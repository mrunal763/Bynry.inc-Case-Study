

class followUpStateSwitcher {

    constructor(id){
        this.DOMId = id;
        this.application_id_ref = null;
    }

    startedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('start', id_ref, function(e) {
            console.log(e.originalEvent.detail[1].id);
        });
    }

    stoppedDrag() {
        $(document).on('stopped', '#'+this.DOMId, function(e) {
            console.log('STOPPED'+this.DOMId);
            console.log(e);
        });
    }

    movedDrag() {
        $(document).on('#'+this.DOMId, 'moved', function(e) {
            // console.log(e.detail[1].id)
            console.log('MOVED'+this.DOMId);
            console.log(e);
        });
    }

    addedDrag() {
        var id_ref = '#'+this.DOMId;
        console.log(id_ref)
        $(document).on('added', id_ref, function(e) {

            const cookieValue = document.cookie
            .split("; ")
            .find((row) => row.startsWith("csrftoken="))
            ?.split("=")[1];

            console.log('CSRF=', cookieValue);
            
            let followup_id = null;
            followup_id = e.originalEvent.detail[1].id.split('_')[1];

            console.log("SR tracking ID: ", followup_id);
            console.log("SR status updated to: ", e.currentTarget.id);

            $.ajax({
                url: 'http://localhost:8000/csr/csr_sr_state_toggler',
                type: 'PUT',
                data: {
                    csrfmiddlewaretoken: cookieValue,
                    'id': followup_id,
                    'status': e.currentTarget.id
                },
                success: function(data){

                    console.log(data);

                    // if(data.status == 200){
                    //     console.log('chk3');
                    //     window.location.reload();
                    // }else{
                    //     console.log('chk_fail');
                    //     console.log(data);
                    // }
                    // window.location.reload();
                },
                error: function(jqXHR, exception){
                    console.log('chk_500');
                    console.log(jqXHR, ' | ', exception);
                    // alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
                },
            });

        });
    }

    removedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('removed', id_ref, function(e) {
            console.log('chk_removed');
            console.log(e.originalEvent.detail[1].id);
        });
    }
}


