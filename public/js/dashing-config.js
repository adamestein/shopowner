let dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock', {
    col: 2,
    getData: function () {
        let today = new Date();

        $.extend(this.scope, {
            date: today.toDateString(),
            time: today.toLocaleTimeString(
                [],
                {hour: '2-digit', hour12: true, minute: '2-digit', second: '2-digit'}
            )
        });
    }
});

dashboard.addWidget('quick_summary_widget', 'List', {
    getData: function () {
        let self = this;

        Dashing.utils.get('quick_summary_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    row: 1
});
