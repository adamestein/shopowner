"""Create the JavaScript needed to use AJAX
"""

class ajax(object):
    def __init__(self):
        self.params = {}

    def add(self, name, submit_button="submit_button"):
        """ Add AJAX component """

        def_init = "alert('TBD Default Init');"

        self.params[name] = {
            "init":             def_init,
            "name":             name,
            "submit_button_id": submit_button,
            "success":          "",
        }

    def generate_js(self):
        """ Generate the AJAX JavaScript """

        script = """
<script type="text/javascript">
    $.extend({
        namespace: function(arg) {
            return "namespace." + arg
        }
    });

    jQuery.namespace("_ajax");

    jQuery._ajax = function() {
        return {
            remove_errors: function() {
                // Remove any error messages being displayed
                alert("Fill in remove_errors");
            }
        }
    };
</script>
        """
        
        for name in self.params.keys():
            params = self.params[name]

            script += """
<script type="text/javascript">
    jQuery._ajax.%(name)s = function() {
        var ajax;
        var user_callback;
        
        return {
            init: function() {
                ajax = jQuery._ajax.%(name)s;

                $.ajaxSetup({traditional: true});

                %(init)s
            },

            send_request: function(url, callback, data) {
                def_callback = ajax.callback;

                // Only save if callback is different than default
                if (callback && callback != def_callback) {
                    user_callback = callback;
                }

                $.getJSON(url, data, function(data) {
                    if (data.errors) {
                        display_errors(data.errors);
                    } else {
                        %(success)s

                        if (user_callback) {
                            if (user_callback.success) {
                                user_callback.success(data);
                            } else {
                                user_callback(data);
                            }
                        }
                    }
                }, "json").error(function(jqXHR, textStatus, errorThrown) {
                    if (user_callback && user_callback.error) {
                        user_callback.error(jqXHR, textStatus, errorThrown);
                    } else {
                        error_page(jqXHR, textStatus, errorThrown);
                    }
                });
            }
        };
    }();

    // Run init when web page finishes loading
    $(document).ready(function() {
        $.ajaxSetup({traditional: true});
        $._ajax.%(name)s.init();
    });
</script>
            """ % params

        return script

    def init_function(self, name, script):
        """ JavaScript function to run when AJAX script is initializing """

        self.params[name]["init"] = script

    def success_function(self, name, script):
        """ JavaScript function to run when AJAX call is successful """

        self.params[name]["success"] = script

