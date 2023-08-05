$(function() {
    $('.django-autocomplete-widget').each(function(_, widget) {
        $('input.django-autocomplete-value', widget).keyup(function(event) {
            var input = this;

            if (event.keyCode == 38 || event.keyCode == 40) {
                var selected_index = -1;
                var active = $('li.active', widget);
                active.each(function (index, element) {
                    if ($(element).hasClass('selected'))
                        selected_index = index;
                });
                active.removeClass('selected');
                if (event.keyCode == 38) {
                    $(active[Math.max(selected_index - 1, 0)]).addClass('selected');
                } else {
                    $(active[Math.min(selected_index + 1, active.length - 1)]).addClass('selected');
                }
                return;
            }

            if (event.keyCode == 13) {
                var selected = $('li.active.selected', widget).first();
                $('input.django-autocomplete-key', widget).val(selected.data('key'));
                $(input).val(selected.data('value'));
                $('li.active', widget).first().addClass('selected');
                $(widget).addClass('none');
                return;
            }
            var value = $(input).val().toLowerCase();

            if (value.length == 0) {
                $('li', widget).removeClass('active').removeClass('selected');
                $(widget).addClass('none');
                return;
            }

            $('li', widget).each(function(_, item) {
                if ($(item).data('value').toLowerCase().indexOf(value) >= 0)
                    $(item).addClass('active');
                else
                    $(item).removeClass('active');
            });

            if ($('li.active.selected', widget).length == 0) {
                $('li', widget).removeClass('selected');
                $('li.active', widget).first().addClass('selected');
            }

            if ($('li.active', widget).length > 0)
                $(widget).removeClass('none');
            else
                $(widget).addClass('none');
        });
    });
});