/***
 Target: Cisco Spark specific integration
 Version: 0.1
 Date: 2017/01/18
 Author: Guillain (guillain@gmail.com)
***/

/* Auth */
  $(function() {
    $('a#authSub').bind('click', function() {
        $.ajax({
            url: '/auth',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                window.location = data;
                //$("#result").html(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* Save Access token */
  $(function() {
    $('a#saveATSub').bind('click', function() {
        $.ajax({
            url: '/saveAT',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text("Access token saved. Thanks to logout & login to load it");
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

  $(function() {
    $('a#resetATSub').bind('click', function() {
        $.ajax({
            url: '/resetAT',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text("Access token reseted. Thanks to logout & login to unload it and redo the access token request process");
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

