/***
 Target: Cisco Spark specific integration
 Version: 0.1
 Date: 2017/01/18
 Author: Guillain (guillain@gmail.com)
***/

/* Duty alert function */
  $(function() {
    $('a#dutyAlertSub').bind('click', function() {
        $.ajax({
            url: 'dutyAlert',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

