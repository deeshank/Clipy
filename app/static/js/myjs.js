$(document).ready(function () {


    var BASE_URL = "http://localhost:5000";

    $.ajax({
        dataType: "json",
        url: BASE_URL + '/get' + window.location.pathname,
        success: function (data) {
            if (data.status != "ERR") {
                alert(data.data);
                $("#content").html(data.data);
            }
        },
        contentType: "application/json"
    });

    $("#content").bind("keyup", function () {
        //alert($("#content").html());

        $.ajax({
            type: 'POST',
            url: BASE_URL + '/paste',
            data: JSON.stringify({uid: window.location.pathname, data: $("#content").html()}),
            success: function (data) {
                //alert('data: ' + data);
            },
            contentType: "application/json",
            dataType: 'json'
        });

    });


    $("#content").on("paste", function (e) {

        e.preventDefault();
        var pastedData = e.originalEvent.clipboardData.getData('text');

        var clipbd = (e.clipboardData || e.originalEvent.clipboardData).items;
        console.log("Length => " + clipbd.length);
        console.log("Contents => " + clipbd);
        var img = new Image();
        for (var i = 0; i < clipbd.length; i++) {
            console.log("Type => " + clipbd[i].type);
            var blob = clipbd[i].getAsFile();
            var reader = new FileReader();
            reader.onload = function (event) {
                var data = event.target.result;
                console.log("Data => " + event.target.result)
                // $.post("http://127.0.0.1:5000/paste/",
                //     {'data': data},
                //     function (data, status) {
                //         alert(data);
                //     });
                img.src = event.target.result;
            }; // data url
            if (clipbd[i].type == "image/png") {
                reader.readAsDataURL(blob);
                console.log(blob);
            }
            var url = window.URL || window.webkitURL;
            var src = url.createObjectURL(blob);
            console.log(src);
            //img.src = src;
            console.log(img);
            $('#content').append(img);
        }

        setTimeout(function () {
            /*alert('count:'+items);

             for (var i = 0; i < items.length; i++) {
             var item =items[i];
             alert('data:'+item);
             }*/

            if (pastedData.length != 0)
                alert(pastedData);
            /*$.get('http://127.0.0.1:5000/test/'+pastedData, function(data) {
             $('#content').append('<div>'+data+'</div>');
             });*/
            $('#content').append('<div>' + pastedData + '</div>');
        }, 1);
    });


});