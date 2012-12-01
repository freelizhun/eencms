var menutimer = 0

function cmsmenu(type, ident, element) {
    mn = openCmsmenu(element);
    options = getMenuOptions(type, ident);

    fillMenu(options, mn);

    mn.show();

    return false;
}

function openCmsmenu(element) {
    mn = $('#cmsmenu-overlay');
    mn.hide();

    offset = $(element).offset();
    mn.css('left', (offset.left + $(element).width() + 10) + 'px');
    mn.css('top', (offset.top + $(element).height()/2) + 'px');
    
    mn.hover(
        function () {
            if (menutimer) {
                window.clearTimeout(menutimer);
            }
        },
        function () {
            menutimer = window.setTimeout(closeCmsmenu, 1000);
        }
    )

    return mn
}

function fillMenu(options, menu) {
    list = $('ul', mn);
    list.empty();

    for (var i=0;i<options.length;i++) {
        newhtml = '';
        option = options[i];

        if (option.valid) {
            if (!eval(option.valid)) {
                continue;
            }
        }

        if (option.separate) {
            newhtml = '<li><hr /></li>';
        }
        if (option.confirm) {
            newhtml += '<li><a href="'+ option.url +'" onclick="return '+ option.confirm +'">'+ option.label +'</li>';
        }
        else {
            newhtml += '<li><a href="'+ option.url +'">'+ option.label +'</li>';
        }

        if (newhtml) {
            list.append(newhtml);
        }
    }
}

function closeCmsmenu() {
    $('#cmsmenu-overlay').hide();
}

function valid_display(input) {
    return input;
}